create table if not exists users (
	id varchar(100) primary key,
    password varchar(100) not null
);

CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(100),
    title VARCHAR(255),
    memo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(100) DEFAULT NULL,
    title VARCHAR(255) DEFAULT NULL,
    memo TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    audio_text LONGTEXT DEFAULT NULL,
    summary TEXT DEFAULT NULL,
    keywords TEXT DEFAULT NULL
);