const express = require('express');
const mysql = require('mysql');
const path = require('path');
const serveStatic = require('serve-static');
const dbconfig = require('./config/databaseconfig.json');
const multer = require('multer');
const FormData = require('form-data');
const fs = require('fs');
const { fetch } = require('undici');
const axios = require('axios');


const db = mysql.createConnection({
    host: dbconfig.host,
    user: dbconfig.user,
    password: dbconfig.password,
    database: dbconfig.database,
    debug: false
});

const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true, limit: '1000mb' }));
app.use(express.json({ limit: '1000mb' }));
app.use('/frontend', serveStatic(path.join(__dirname, 'frontend')));


const upload = multer({
    dest: 'uploads/',
    limits: { fileSize: 1000 * 1024 * 1024 }
});
db.connect((err) => {
    if (err) {
        console.error('데이터베이스 연결 실패:', err.stack);
        return;
    }
    console.log('데이터베이스 연결 성공. 연결 ID:', db.threadId);
});

app.post('/process/join', (req, res) => {
    console.log('/process/join 호출됨', req.body);

    const paramId = req.body.id;
    const paramPassword = req.body.password;

    if (!paramId || !paramPassword) {
        return res.status(400).send('ID와 비밀번호는 필수 항목입니다');
    }

    const query = 'INSERT INTO users (id, password) VALUES (?, ?)';
    db.query(query, [paramId, paramPassword], (err, result) => {
        if (err) {
            console.error('Error inserting user:', err.stack);
            return res.status(500).send('사용자 등록 중 오류 발생');
        }
        res.redirect('/frontend/complete.html');
    });
});

app.post('/process/login', (req, res) => {
    console.log('/process/login 호출됨', req.body);

    const paramId = req.body.id;
    const paramPassword = req.body.password;

    if (!paramId || !paramPassword) {
        return res.status(400).send('ID와 비밀번호는 필수 항목입니다');
    }

    const query = 'SELECT * FROM users WHERE id = ? AND password = ?';
    db.query(query, [paramId, paramPassword], (err, results) => {
        if (err) {
            console.error('Error querying user:', err.stack);
            return res.status(500).send('로그인 중 오류 발생');
        }

        if (results.length > 0) {
            res.redirect(`/frontend/space.html?id=${paramId}`);
        } else {
            res.status(400).send('ID 또는 비밀번호가 일치하지 않습니다');
        }
    });
});

app.post('/api/notes', (req, res) => {
    const userId = req.body.user_id;
    const title = req.body.title;
    const memo = req.body.memo;
    const audioText = req.body.audio_text;
    const summary = req.body.summary;
    const keywords = req.body.keywords;

    const query = 'INSERT INTO notes (user_id, title, memo, audio_text, summary, keywords) VALUES (?, ?, ?, ?, ?, ?)';
    db.query(query, [userId, title, memo, audioText, summary, keywords], (err, result) => {
        if (err) {
            return res.status(500).send('노트 저장 중 오류 발생');
        }
        res.json({ id: result.insertId, message: '노트 저장 성공' });
    });
});

app.get('/api/notes/:user_id', (req, res) => {
    const userId = req.params.user_id;

    const query = 'SELECT * FROM notes WHERE user_id = ?';
    db.query(query, [userId], (err, results) => {
        if (err) {
            return res.status(500).send('노트 조회 중 오류 발생');
        }
        res.json(results);
    });
});

app.delete('/api/notes/:id', (req, res) => {
    const noteId = req.params.id;
    const query = 'DELETE FROM notes WHERE id = ?';
    db.query(query, [noteId], (err, result) => {
        if (err) {
            return res.status(500).send('노트 삭제 중 오류 발생');
        }
        res.send('노트 삭제 성공');
    });
});




app.post('/upload_audio', upload.single('audioFile'), async (req, res) => {
    const audioPath = req.file.path;
    const formData = new FormData();
    formData.append('audioFile', fs.createReadStream(audioPath));

    try {
        const response = await axios.post('http://localhost:5000/process_audio', formData, {
            headers: {
                ...formData.getHeaders()
            }
        });
        res.json(response.data);
    } catch (error) {
        console.error('Error processing audio file:', error);
        res.status(500).send('음성 파일 처리 중 오류 발생');
    } finally {
        fs.unlink(audioPath, (err) => {
            if (err) console.error('Error deleting uploaded file:', err);
        });
    }
});



app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});