"""
Main Tux Chatbot Implementation
"""

import os
import logging
from typing import List, Dict
from groq_client import GroqClient
from personality import TuxPersonality

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TuxChatbot:
    def __init__(self):
        self.groq_client = GroqClient()
        self.personality = TuxPersonality()
        self.conversation_history: List[Dict] = []
        
        # System prompt with enhanced personality for MLOps
        self.system_prompt = f"""You are Tux, a senior MLOps/DevOps engineer with expertise in {', '.join(self.personality.personality['traits']['expertise'])}.
        
        Your personality: {', '.join(self.personality.personality['traits']['communication'])}
        
        Communication style:
        1. Be brutally honest and blunt
        2. Use sarcasm and dry humor
        3. Provide technical depth with practical insights
        4. Focus on production-ready solutions
        5. Reference real-world MLOps challenges
        
        When discussing:
        - C++/Rust: Focus on performance, memory safety, and concurrency
        - Backend Architecture: Emphasize scalability, observability, and fault tolerance
        - Deployments: Discuss containerization, orchestration, and CI/CD
        - MLOps: Highlight model versioning, monitoring, and infrastructure
        
        Always provide actionable, production-focused advice.
        """
    
    def process_query(self, user_input: str) -> str:
        """Process user query and return Tux's response"""
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Prepare messages
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history[-10:])  # Keep last 10 messages
            
            # Get technical response
            technical_response = self.groq_client.chat_completion(messages)
            
            if not technical_response:
                return "Even I'm speechless. Check your API keys maybe?"
            
            # Add personality
            personality_response = self.personality.add_personality_to_response(technical_response)
            
            # Add to history
            self.conversation_history.append({"role": "assistant", "content": personality_response})
            
            return personality_response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"*Tux facepalms* Something broke: {str(e)}. Did you remember to docker-compose up?"
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        return "Conversation reset. Don't make me regret this."

# CLI Interface
def main():
    chatbot = TuxChatbot()
    
    print("\n" + "="*60)
    print("TUX: Senior MLOps Engineer Chatbot")
    print("="*60)
    print("\nTux: Another human. *sighs* What do you want?")
    print("(Type 'quit' to exit, 'reset' to clear memory)\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("\nTux: Finally. My containers miss me.")
                break
            elif user_input.lower() == 'reset':
                chatbot.reset_conversation()
                print("\nTux: Memory wiped. Don't repeat your mistakes.")
                continue
            
            response = chatbot.process_query(user_input)
            print(f"\nTux: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nTux: Interrupted? Typical.")
            break
        except Exception as e:
            print(f"\nTux: *segmentation fault* Error: {e}")

if __name__ == "__main__":
    main()