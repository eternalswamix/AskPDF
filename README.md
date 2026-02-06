# AskPDF • Intelligent Document Assistant

![AskPDF Banner](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css)

**AskPDF** is a powerful, AI-driven web application that allows users to upload PDF documents and interact with them using natural language. Built with a modern, dark-themed UI and powered by Google's Gemini AI, it transforms static documents into dynamic knowledge bases.

---

## 🚀 Features

-   **📄 PDF Analysis**: Drag-and-drop upload with instant text extraction and vectorization.
-   **🤖 AI Chat**: Ask questions, request summaries, and get citations using Google Gemini 1.5.
-   **🔐 Secure Vault**: Enterprise-grade document storage powered by Supabase.
-   **🎨 Modern Dark UI**: A sleek, responsive interface built with TailwindCSS and Glassmorphism.
-   **🔑 Google Auth**: Seamless sign-in and account management.
-   **⚡ Real-time Stream**: Fast, streaming AI responses.

---

## 🛠️ Tech Stack

-   **Backend**: Flask (Python), Supabase (PostgreSQL + pgvector).
-   **Frontend**: HTML5, TailwindCSS, Vanilla JS (No heavy framework overhead).
-   **AI Engine**: Google Gemini API (Embeddings & Generation).
-   **Authentication**: OAuth 2.0 (Google) via Authlib.
-   **Deployment**: Vercel Ready.

---

## ⚡ Quick Start

### Prerequisites
-   Python 3.10+
-   Supabase Account
-   Google Cloud Project (for OAuth & Gemini API)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/eternalswamix/AskPDF.git
    cd AskPDF
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```ini
    # App Secret
    FLASK_SECRET=your_super_secret_key

    # Supabase (Database & Auth)
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_anon_key
    SUPABASE_SERVICE_KEY=your_service_role_key

    # Google Gemini AI
    GEMINI_API_KEY=your_gemini_api_key

    # Google OAuth
    GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret
    
    # App URL (for redirects)
    BASE_URL=http://localhost:5000 
    ```

4.  **Run the Application**
    ```bash
    python run.py
    ```
    Access the app at `http://127.0.0.1:5000`.

---

## 📂 Project Structure

```
AskPDF/
├── api/                # Vercel Serverless Entry
├── app/
│   ├── core/           # Config, Errors, Logging
│   ├── routes/         # Blueprints (Auth, Chat, PDF)
│   ├── services/       # Business Logic (Gemini, Vector Store)
│   ├── static/         # CSS, Images, JS
│   └── templates/      # Jinja2 HTML Templates
├── requirements.txt    # Dependencies
├── run.py              # Local Development Entry
├── schema.sql          # Database Schema
└── vercel.json         # Deployment Config
```

---

## 🤝 Connect with Me

Developed by **Madhav Swami (EternalSwamiX)**.

-   [![GitHub](https://img.shields.io/badge/GitHub-eternalswamix-181717?style=flat&logo=github)](https://github.com/eternalswamix)
-   [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/madhavswami)
-   [![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2?style=flat&logo=twitter)](https://twitter.com/eternalswamix)
-   [![Website](https://img.shields.io/badge/Website-Portfolio-FF5722?style=flat&logo=firefox)](https://eternalswamix.github.io)

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
