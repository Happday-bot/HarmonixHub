# 🎵 HarmonixHub

**HarmonixHub** is a full-stack music management platform where users can **upload**, **store**, and **stream their personal music files** securely from anywhere. Built with FastAPI and MongoDB, it supports user authentication, audio compression, metadata updates, and seamless file handling.

---
![login page](/static/assets/login.jpg)
---
![dashboard](/static/assets/dashboard.jpg)
---

## 🚀 Features

* 🔐 User **Sign Up**, **Login**, and **Delete Account**
* 📤 **Bulk Upload** of MP3 songs with artist and title metadata
* 📥 Compressed MP3 storage using `zlib`
* 🎧 Streamable song data (Base64 encoded)
* 🗑️ Delete and update uploaded songs
* ⚙️ RESTful API design with FastAPI
* 🌐 Static frontend support via `/static`

---

## 🛠️ Tech Stack

* **Backend**: FastAPI
* **Database**: MongoDB Atlas
* **Compression**: `zlib`
* **Environment Management**: `python-dotenv`
* **Frontend**: Static HTML/CSS/JS (served via FastAPI)

---

## 📁 Folder Structure

```
/AK_SC
│
├── static/                 # Frontend files
├── .env                   # Secrets (Mongo URI, etc.)
├── .gitignore             # Ignored files
├── db.py (if applicable)  # Optional DB logic
└── main.py                # FastAPI app
```

---

## 🔧 Environment Variables

Create a `.env` file with the following:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
MONGO_DB_NAME=akshaya
```

> ⚠️ **NEVER commit your `.env` to GitHub.**

---

## 🚦 Running Locally

1. **Install dependencies:**

   ```bash
   pip install fastapi pymongo uvicorn python-dotenv
   ```

2. **Run the server:**

   ```bash
   python main.py
   ```

3. Open: `http://localhost:8000/static/auth.html`

---

## 📬 API Endpoints

| Method | Endpoint               | Description           |
| ------ | ---------------------- | --------------------- |
| POST   | `/signup`              | Register user         |
| POST   | `/login`               | Authenticate user     |
| POST   | `/upload`              | Upload multiple songs |
| GET    | `/get_songs/{email}`   | Retrieve user songs   |
| PUT    | `/update_song/{id}`    | Update song metadata  |
| DELETE | `/delete_user/{email}` | Delete user and songs |
| DELETE | `/delete_songs`        | Bulk delete songs     |

---

## 📄 License

This project is licensed under the **Apache License**.

---
