#!/usr/bin/env python3
import os
import sys
from groq import Groq

# Your API keys
API_KEYS = [
    GROQ-KEY-HERE
]

class TuxChatbot:
    def __init__(self):
        self.current_key = 0
        self.client = Groq(api_key=API_KEYS[self.current_key])
        self.history = []
    
    def rotate_key(self):
        self.current_key = (self.current_key + 1) % len(API_KEYS)
        self.client = Groq(api_key=API_KEYS[self.current_key])
        print(f"[*] Switched to key {self.current_key + 1}")
    
    def ask(self, question):
        messages = [
            {"role": "system", "content": """You are Tux, a senior MLOps engineer.
Be blunt, sarcastic, and technical. Focus on C++, Rust, backend, deployments.
Example style: "*sighs* Let me be real with you..."""},
        ]
        messages.extend(self.history[-3:])
        messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            self.history.append({"role": "user", "content": question})
            self.history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            if "rate" in str(e).lower():
                self.rotate_key()
                return self.ask(question)
            return f"Error: {e}"

def main():
    bot = TuxChatbot()
    
    print("\n" + "="*50)
    print("TUX: Senior MLOps Engineer Chatbot")
    print("="*50)
    print("\nTux: Another developer. *sighs* What now?\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("\nTux: Finally. I have containers to orchestrate.")
                break
            
            print("\nTux: Thinking...")
            response = bot.ask(user_input)
            print(f"\nTux: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nTux: Interrupted? Typical.")
            break

if __name__ == "__main__":
    main()
