from setuptools import setup, find_packages

setup(
    name="tux-mlops-chatbot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "groq>=0.9.0",
        "python-dotenv>=1.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "tux-chatbot=src.chatbot:main",
        ],
    },
    author="Your Name",
    description="Tux - Senior MLOps Engineer Chatbot",
    keywords="mlops, chatbot, docker, deployment, rust, c++",
    python_requires=">=3.10",
)