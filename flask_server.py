from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import urllib.parse
import json
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import speech_recognition as sr
import time

app = Flask(__name__)
CORS(app)  


model_id = 'MLP-KTLim/llama-3-Korean-Bllossom-8B'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    offload_folder="offload"
)
model.eval()

max_length = model.config.max_position_embeddings
print(f"Model's max input length: {max_length}")

def summarize_text(text):
    try:
        text = text[:max_length]

        prompt = f"입력된 텍스트를 요약해 주세요: {text}\n요약:"
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs.input_ids.to(model.device)
        attention_mask = inputs.attention_mask.to(model.device)
        with torch.no_grad():
            outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=max_length, max_new_tokens=150, num_beams=5, early_stopping=True)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        summary_start = summary.find("요약:") + len("요약:")
        summary_clean = summary[summary_start:].strip()
        
        return summary_clean
    except Exception as e:
        print(f"Error in summarize_text: {e}")
        return str(e)

def extract_keywords(summary):
    try:
        prompt = f"다음 텍스트에서 주요 키워드를 추출해 주세요: {summary}\n키워드:"
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs.input_ids.to(model.device)
        attention_mask = inputs.attention_mask.to(model.device)
        with torch.no_grad():
            outputs = model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=50, num_beams=5, early_stopping=True)
        
        keywords_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if "키워드:" in keywords_text:
            keywords_text = keywords_text.split("키워드:")[1].strip()
        
        keywords = keywords_text.split(', ')
        keywords = [keyword.strip() for keyword in keywords]

        return keywords
    except Exception as e:
        print(f"Error in extract_keywords_from_summary: {e}")
        return [str(e)]

def split_audio(file_path, chunk_length_ms):
    sound = AudioSegment.from_file(file_path)
    return make_chunks(sound, chunk_length_ms)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audioFile' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    audio_file = request.files['audioFile']
    audio_path = "uploads/" + audio_file.filename
    audio_file.save(audio_path)

    chunk_length_ms = 60000  # 1분 단위로 분할
    chunks = split_audio(audio_path, chunk_length_ms)

    recognizer = sr.Recognizer()
    audio_text = ""

    for i, chunk in enumerate(chunks):
        chunk_path = f"chunk{i}.wav"
        chunk.export(chunk_path, format="wav")

        try:
            with sr.AudioFile(chunk_path) as source:
                audio_data = recognizer.record(source)
                audio_text += recognizer.recognize_google(audio_data, language="ko-KR") + " "
        except Exception as e:
            print(f"Error recognizing chunk {i}: {e}")
        finally:
            if os.path.exists(chunk_path):
                os.remove(chunk_path)

    if os.path.exists(audio_path):
        os.remove(audio_path)

    print(f"Extracted text: {audio_text}")

    def split_text_into_chunks(text, max_length):
        return [text[i:i + max_length] for i in range(0, len(text), max_length)]

    text_chunks = split_text_into_chunks(audio_text, 8192)

    summaries = []
    full_keywords = []

    for chunk in text_chunks:
        
        chunk_summary = summarize_text(chunk).replace("다음 텍스트를 요약해 주세요:", "").strip()
        summaries.append(chunk_summary)
        chunk_keywords = extract_keywords(chunk_summary)
        full_keywords.extend(chunk_keywords)

    full_summary = " ".join(summaries)
    full_keywords = list(set(full_keywords))

    return jsonify({
        "text": audio_text,
        "summary": full_summary.strip(),
        "keywords": full_keywords
    })



NAVER_CLIENT_ID = "H5NGHy71uGcG3akjx2MZ"
NAVER_CLIENT_SECRET = "H5NGHy71uGcG3akjx2MZ"
KAKAO_API_KEY = "9bef84ab6ebcbc98466f6370d9bb5b14"
GOOGLE_SEARCH_ENGINE_ID = "d3703fe5755b54933"
GOOGLE_API_KEY = "AIzaSyBmQvly6xmSJyzq95EtobXDHYLGeEPZ-l4"
TRASH_LINK = ["kin", "news", "dcinside", "fmkorea", "ruliweb", "theqoo", "clien", "mlbpark", "instiz", "todayhumor"]

def Google_API(query, wanted_row):
    query = query.replace("|", "OR")
    query += "-filetype:pdf"
    start_pages = []

    df_google = pd.DataFrame(columns=['Title', 'Link', 'Description'])

    row_count = 0

    for i in range(1, wanted_row + 1000, 10):
        start_pages.append(i)

    for start_page in start_pages:
        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_SEARCH_ENGINE_ID}&q={query}&start={start_page}"
        data = requests.get(url).json()
        search_items = data.get("items")

        try:
            for i, search_item in enumerate(search_items, start=1):
                link = search_item.get("link")
                if any(trash in link for trash in TRASH_LINK):
                    pass
                else:
                    title = search_item.get("title")
                    description = search_item.get("snippet")
                    df_google.loc[start_page + i] = [title, link, description]
                    row_count += 1
                    if (row_count >= wanted_row) or (row_count == 300):
                        return df_google
        except Exception as e:
            print(f"Error in Google_API: {e}")
            return df_google

    return df_google

def Naver_API(query, wanted_row):
    query = urllib.parse.quote(query)
    display = 100
    start = 1
    end = wanted_row + 10000
    idx = 0
    sort = 'sim'

    df = pd.DataFrame(columns=['Title', 'Link', 'Description'])
    row_count = 0

    for start_index in range(start, end, display):
        url = "https://openapi.naver.com/v1/search/webkr?query=" + query +\
              "&display=" + str(display) + \
              "&start=" + str(start_index) + \
              "&sort=" + sort
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
        request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)
        try:
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                items = json.loads(response_body.decode('utf-8'))['items']
                remove_tag = re.compile('<.*?>')
                for item_index in range(0, len(items)):
                    link = items[item_index]['link']
                    if any(trash in link for trash in TRASH_LINK):
                        idx += 1
                        pass
                    else:
                        title = re.sub(remove_tag, '', items[item_index]['title'])
                        description = re.sub(remove_tag, '', items[item_index]['description'])
                        df.loc[idx] = [title, link, description]
                        idx += 1
                        row_count += 1
                        if (row_count >= wanted_row) or (row_count == 300):
                            return df
        except Exception as e:
            print(f"Error in Naver_API: {e}")
            return df

    return df

def Daum_API(query, wanted_row):
    pages = wanted_row // 10

    method = "GET"
    url = "https://dapi.kakao.com/v2/search/web"
    header = {'authorization': f'KakaoAK {KAKAO_API_KEY}'}

    df = pd.DataFrame(columns=['Title', 'Link', 'Description'])

    row_count = 0

    for page in range(1, pages + 10):
        params = {'query': query, 'page': page}
        request = requests.get(url, params=params, headers=header)
        for i, item in enumerate(request.json()["documents"], start=1):
            link = item['url']
            try:
                written_year = int(item['datetime'][:4])
            except:
                written_year = 2023

            if (any(trash in link for trash in TRASH_LINK) or (written_year < 2020)):
                pass
            else:
                title = item["title"]
                description = item["contents"]
                df.loc[10 * page + i] = [title, link, description]
                row_count += 1
                if (row_count >= wanted_row) or (row_count == 300):
                    remove_tag = re.compile('<.*?>')
                    df['Title'] = df['Title'].apply(lambda x: re.sub(remove_tag, '', x))
                    df['Description'] = df['Description'].apply(lambda x: re.sub(remove_tag, '', x))

                    return df

    remove_tag = re.compile('<.*?>')
    df['Title'] = df['Title'].apply(lambda x: re.sub(remove_tag, '', x))
    df['Description'] = df['Description'].apply(lambda x: re.sub(remove_tag, '', x))

    return df

def final(query, wanted_row=100):
    df_google = Google_API(query, wanted_row)
    df_google['search_engine'] = 'Google'
    df_naver = Naver_API(query, wanted_row)
    df_naver['search_engine'] = 'Naver'
    df_daum = Daum_API(query, wanted_row)
    df_daum['search_engine'] = 'Daum'
    df_final = pd.concat([df_google, df_naver, df_daum])
    df_final.reset_index(inplace=True, drop=True)

    return df_final

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query')
    wanted_row = int(request.args.get('wanted_row', 100))
    try:
        df_final = final(query, wanted_row)
        results = df_final.to_dict(orient='records')
        return jsonify(results)
    except Exception as e:
        print(f"Error in search endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
