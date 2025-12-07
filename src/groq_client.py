"""
Groq API Client with Fallback Mechanism
"""

import os
import random
from typing import List, Optional
from groq import Groq
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        self.clients = self._initialize_clients()
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.backup_model = os.getenv("GROQ_MODEL_BACKUP", "mixtral-8x7b-32768")
    
    def _load_api_keys(self) -> List[str]:
        """Load all API keys from environment"""
        keys = []
        for i in range(1, 10):  # Support up to 9 keys
            key = os.getenv(f"GROQ_API_KEY_{i}")
            if key:
                keys.append(key)
        
        if not keys:
            raise ValueError("No GROQ API keys found in environment variables")
        
        logger.info(f"Loaded {len(keys)} API keys")
        return keys
    
    def _initialize_clients(self) -> List[Groq]:
        """Initialize Groq clients for all keys"""
        clients = []
        for key in self.api_keys:
            try:
                client = Groq(api_key=key)
                clients.append(client)
            except Exception as e:
                logger.warning(f"Failed to initialize client for key: {e}")
        return clients
    
    def _rotate_key(self):
        """Rotate to next API key"""
        self.current_key_index = (self.current_key_index + 1) % len(self.clients)
        logger.info(f"Rotated to API key {self.current_key_index + 1}")
    
    def chat_completion(self, messages: List[dict], max_retries: int = 3) -> Optional[str]:
        """Get chat completion with fallback mechanism"""
        for attempt in range(max_retries):
            try:
                client = self.clients[self.current_key_index]
                
                # Try primary model first
                try:
                    response = client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=float(os.getenv("TEMPERATURE", 0.7)),
                        max_tokens=int(os.getenv("MAX_TOKENS", 4096))
                    )
                except Exception:
                    # Fallback to backup model
                    logger.warning(f"Primary model failed, trying backup: {self.backup_model}")
                    response = client.chat.completions.create(
                        model=self.backup_model,
                        messages=messages,
                        temperature=float(os.getenv("TEMPERATURE", 0.7)),
                        max_tokens=int(os.getenv("MAX_TOKENS", 4096))
                    )
                
                return response.choices[0].message.content
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                
                if "rate limit" in str(e).lower() or "quota" in str(e).lower():
                    self._rotate_key()
                    continue
                
                if attempt < max_retries - 1:
                    self._rotate_key()
                    continue
                else:
                    raise Exception(f"All retries failed. Last error: {e}")
        
        return None