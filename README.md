```markdown
# Tux - Senior MLOps Engineer Chatbot 🤖

![TUX Character](uu.webp)
*TUX: "Let me be blunt: I'm Tux, a Senior MLOps Engineer with a passion for building scalable production systems."*

A production-ready chatbot with personality, designed for MLOps/DevOps mentoring. Features multi-API fallback, Docker deployment, CI/CD, and comprehensive monitoring.

> **Note:** No API keys are included in this repository. Create your own `.env` file to run locally.

---

## 🚀 Features

### Production Architecture
* Multi-API key fallback system with automatic rotation
* Model fallback: Llama 3.3 → Mixtral
* Conversation state management
* Error handling & retry logic

### MLOps Best Practices
* Containerized deployment with Docker
* Health checks, logging, and metrics collection
* CI/CD pipelines with automated testing
* Environment configuration management via `.env`

### Technical Showcase
* Async/await patterns for scalability
* Type hints & documentation
* Unit and integration tests
* Code quality tools: `flake8`, `black`, `mypy`
* Performance monitoring & metrics collection

### Personality System
* Configurable personality traits
* Context-aware, technical responses with humor
* MLOps-focused insights
* Conversation history management

---

## 📁 Project Structure

```
Tux-AI/
├── src/
│   ├── chatbot.py
│   ├── groq_client.py
│   ├── personality.py
│   └── utils.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── setup.py
└── run.sh
```

---

## 🛠️ Setup (Safe for GitHub)

1. **Copy environment example**
```bash
cp .env.example .env
# Edit .env and add your own Groq API keys
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the chatbot**
```bash
# GUI version
python simple_tux.py

# CLI version
python tux_bot_simple.py
```

4. **Optional: Docker**
```bash
docker-compose up --build
# or
docker build -t tux-mlops-chatbot .
docker run -p 8000:8000 --env-file .env tux-mlops-chatbot
```

> ⚠️ **Important:** The `.env` file must contain your API keys. This repository contains no keys.

---

## 📸 Demo

![Terminal Demo](cli.webp)
*Example terminal session showing the chatbot in action*

### Running the Application
The screenshot above demonstrates:
- Safe error handling with `KeyboardInterrupt`
- Project file structure visibility
- Multi-environment support (Anaconda, Zorin Linux)
- Clean process management

---

## 💡 Quick Tips for Recruiters

* The bot demonstrates **multi-API fallback, error handling, and MLOps best practices**
* Easily testable locally without any secrets (canned responses optional)
* Showcases both GUI and CLI interfaces for real-world application
* Includes comprehensive error handling as shown in the terminal screenshot

### Key Technical Highlights:
1. **Production-Ready Architecture**: Built with scalability and reliability in mind
2. **Safety First**: No exposed secrets - uses `.env.example` pattern
3. **Real-World Scenarios**: Includes proper interrupt handling and error recovery
4. **MLOps Focus**: Containerization, CI/CD, and monitoring baked in

---

## 🎯 What This Project Demonstrates

This project showcases my ability to:
- Build production-grade AI/ML applications
- Implement proper security practices (no exposed keys)
- Create both GUI and CLI interfaces
- Handle real-world deployment scenarios
- Apply MLOps best practices throughout the development lifecycle

---

## 📝 License & Attribution

MADE BY AYMAN SHAIKH

---
```
