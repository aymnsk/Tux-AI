# Tux - Senior MLOps Engineer Chatbot 🤖

A production-ready chatbot with personality, designed for MLOps/DevOps mentoring. Features API fallback, Docker deployment, CI/CD, and comprehensive monitoring.

## 🚀 Features for MLOps Portfolio

### 1. **Production Architecture**

- Multi-API key fallback system with automatic rotation
- Load balancing across 5+ API keys
- Model fallback (Llama 3.3 → Mixtral)
- Conversation state management
- Error handling and retry logic

### 2. **MLOps Best Practices**

- Containerized deployment with Docker
- Health checks and monitoring
- Logging and metrics collection
- CI/CD pipeline with automated testing
- Environment configuration management

### 3. **Technical Showcase**

- Async/await patterns for scalability
- Type hints and documentation
- Unit and integration tests
- Code quality tools (flake8, black, mypy)
- Performance monitoring

### 4. **Personality System**

- Configurable personality traits
- Context-aware responses
- Technical depth with humor
- MLOps-focused insights
- Conversation history management

## 📁 Project Structure

chatbot-mlops/
├── src/
│ ├── chatbot.py
│ ├── groq_client.py
│ ├── personality.py
│ └── utils.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── setup.py
└── .github/
└── workflows/
└── ci-cd.yml

## 🛠️ Setup & Deployment

1. **Environment Setup:**

````bash
cp .env.example .env
# Add your Groq API keys

pip install -r requirements.txt
python -m src.chatbot


docker-compose up --build


docker build -t tux-mlops-chatbot .
docker run -p 8000:8000 --env-file .env tux-mlops-chatbot


## 8. Quick Start Script

### `run.sh`
```bash
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Tux MLOps Chatbot${NC}"

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found. Copying from example...${NC}"
    cp .env.example .env
    echo -e "${RED}Please edit .env file with your API keys!${NC}"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo -e "${RED}Python 3.10 or higher required. Found $python_version${NC}"
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Run chatbot
echo -e "${GREEN}Starting Tux...${NC}"
python -m src.chatbot
````
