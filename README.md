# 📄 PDF-CHAT-ASSISTENT — AI Chat With Your PDFs

PDF-CHAT-ASSISTENT is an AI-powered web application that allows users to upload PDFs and chat with them using natural language.  
The assistant answers **strictly based on the uploaded PDF content** and rejects any out-of-context questions.

Built using **Flask, Google Gemini, Supabase (Auth + Storage + pgvector)** with a premium dark glass UI.

---

## 🚀 Features

- 📄 Upload PDF and start chatting instantly
- 🧠 AI-powered answers using Google Gemini
- 🔍 Semantic search using Supabase pgvector
- 🚫 No hallucinations — PDF-only answers
- 🗄️ Persistent chat history
- 🔐 Authentication
  - Email & Password
  - Google OAuth
  - Profile completion flow
- 🌙 Premium dark glass UI (Tailwind CSS)
- 🧾 Smart commands like `summary`, `summarize`
- ☁️ Deployable on Vercel (Free Tier)

---

## 🧠 How the Project Works (High-Level Flow)

1. User logs in using Email/Password or Google  
2. User uploads a PDF  
3. PDF is stored in Supabase Storage  
4. Text is extracted from the PDF  
5. Text is split into adaptive chunks  
6. Each chunk is embedded using Gemini Embeddings  
7. Embeddings are stored in Supabase pgvector  
8. User asks a question → semantic search → Gemini answer  
9. Chat history is saved and shown in sidebar  

---

## 🛠️ Tech Stack

**Backend:** Flask (Python)  
**AI:** Google Gemini (LLM + Embeddings)  
**Database:** Supabase PostgreSQL + pgvector  
**Storage:** Supabase Storage  
**Frontend:** Jinja + Tailwind CSS  
**Deployment:** Vercel (Free Tier)

---

## 🗄️ Supabase SQL Schema

```sql
create extension if not exists vector;

create table users (
  id uuid primary key,
  email text unique,
  username text unique,
  first_name text,
  last_name text,
  phone_no text,
  created_at timestamp default now()
);

create table pdf_files (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id),
  filename text,
  original_filename text,
  storage_path text,
  created_at timestamp default now()
);

create table pdf_chunks (
  id bigserial primary key,
  pdf_id uuid,
  user_id uuid,
  content text,
  embedding vector(768)
);

create table chat_history (
  id bigserial primary key,
  pdf_id uuid,
  user_id uuid,
  question text,
  answer text,
  created_at timestamp default now()
);
```

---

## ⚙️ Environment Variables

```env
FLASK_SECRET=supersecretkey
GEMINI_API_KEY=AIzaSyXXXXXXXX
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOi...
SUPABASE_KEY=sb_publishable...

MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=abcdabcdabcdabcd
MAIL_FROM=your@gmail.com
```

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
python run.py
```

---

## 📄 License

MIT License
