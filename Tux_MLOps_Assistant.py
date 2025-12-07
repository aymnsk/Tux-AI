#!/usr/bin/env python3
"""
TUX MLOps Assistant - One File Application
Run this ONE file and everything works!
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue

# ====================== CONFIGURATION ======================
API_KEYS = [
    ""  
]

# ====================== GROQ CLIENT ======================
class GroqClient:
    def __init__(self):
        self.api_keys = API_KEYS
        self.current_key = 0
        self.client = None
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize Groq client with current API key"""
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_keys[self.current_key])
            return True
        except ImportError:
            print("Installing groq library...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "groq", "-q"])
            from groq import Groq
            self.client = Groq(api_key=self.api_keys[self.current_key])
            return True
        except Exception as e:
            print(f"Failed to initialize client: {e}")
            return False
    
    def rotate_key(self):
        """Switch to next API key"""
        self.current_key = (self.current_key + 1) % len(self.api_keys)
        print(f"[*] Rotated to API key {self.current_key + 1}")
        self.initialize_client()
    
    def get_response(self, messages, max_retries=3):
        """Get response from Groq API with retry logic"""
        from groq import Groq
        
        for attempt in range(max_retries):
            try:
                if not self.client:
                    self.initialize_client()
                
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7
                )
                return response.choices[0].message.content
                
            except Exception as e:
                error_msg = str(e).lower()
                if ("rate" in error_msg or "quota" in error_msg) and attempt < max_retries - 1:
                    self.rotate_key()
                    continue
                else:
                    return f"Error: {str(e)}"
        
        return "Error: All retries failed. Check your API keys."

# ====================== TUX PERSONALITY ======================
class TuxPersonality:
    def __init__(self):
        self.personality = {
            "name": "Tux",
            "title": "Senior MLOps Engineer",
            "expertise": ["C++", "Rust", "Backend Architecture", "Docker", "Kubernetes", "CI/CD", "Deployments"],
            "traits": ["blunt", "sarcastic", "technical", "funny", "honest"],
            "greetings": [
                "Another human. *sighs* What now?",
                "Tux here. Try not to break production this time.",
                "*checks watch* You've got 5 minutes before my next deployment.",
                "Oh great, more questions. Let's make this quick."
            ]
        }
    
    def get_greeting(self):
        import random
        return random.choice(self.personality["greetings"])
    
    def enhance_response(self, response):
        """Add Tux's personality to responses"""
        import random
        
        enhancements = [
            "\n\n*Tux adjusts his glasses*",
            "\n\n*sighs* The truth is...",
            "\n\nLet me be blunt:",
            "\n\nHonestly?",
            "\n\n*in a monotone voice*"
        ]
        
        if random.random() > 0.5:
            response = random.choice(enhancements) + " " + response
        
        # Add signature
        signatures = [
            "\n\n- Tux, your friendly neighborhood MLOps engineer",
            "\n\n*deploys container and walks away*",
            "\n\nNow if you'll excuse me, I have pipelines to monitor."
        ]
        
        if random.random() > 0.7:
            response += random.choice(signatures)
        
        return response

# ====================== CHAT MANAGER ======================
class ChatManager:
    def __init__(self):
        self.client = GroqClient()
        self.personality = TuxPersonality()
        self.conversation_history = []
        self.stats = {
            "total_messages": 0,
            "total_tokens": 0,
            "start_time": datetime.now()
        }
    
    def process_message(self, user_input):
        """Process user message and return Tux's response"""
        self.stats["total_messages"] += 1
        
        # Prepare messages
        messages = [
            {
                "role": "system",
                "content": f"""You are {self.personality.personality['name']}, a {self.personality.personality['title']}.
Expertise: {', '.join(self.personality.personality['expertise'])}
Personality: {', '.join(self.personality.personality['traits'])}

Communication Style:
1. Be brutally honest and blunt
2. Use sarcasm and dry humor
3. Focus on production-ready solutions
4. Give practical, actionable advice
5. Reference real-world MLOps experiences

Example responses:
- "*sighs* Let me be real with you..."
- "That deployment strategy is giving me nightmares"
- "Here's how we do it in production..."
- "Not terrible. For a human."

Always provide technical depth with practical insights."""
            }
        ]
        
        # Add conversation history (last 5 messages)
        messages.extend(self.conversation_history[-5:])
        messages.append({"role": "user", "content": user_input})
        
        # Get response
        response = self.client.get_response(messages)
        
        # Add to history
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Enhance with personality
        enhanced_response = self.personality.enhance_response(response)
        
        return enhanced_response
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        return "Conversation reset. Don't make me regret this."
    
    def get_stats(self):
        """Get chat statistics"""
        duration = datetime.now() - self.stats["start_time"]
        return {
            "total_messages": self.stats["total_messages"],
            "conversation_length": len(self.conversation_history),
            "duration_minutes": round(duration.total_seconds() / 60, 1)
        }

# ====================== GUI APPLICATION ======================
class TuxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TUX")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")
        
        # Initialize chat manager
        self.chat_manager = ChatManager()
        self.message_queue = queue.Queue()
        
        self.setup_ui()
        self.check_queue()
        
        # Auto-greet
        self.root.after(1000, self.auto_greet)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title Frame
        title_frame = tk.Frame(self.root, bg="#2d2d2d", height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text=" TUX", 
                font=("Arial", 20, "bold"), fg="#0046df", bg="#2d2d2d").pack(side=tk.LEFT, padx=20)
        
        # Stats button
        stats_btn = tk.Button(title_frame, text="Stats", command=self.show_stats,
                            bg="#0300b9", fg="white", font=("Arial", 10), relief=tk.FLAT)
        stats_btn.pack(side=tk.RIGHT, padx=10)
        
        # Reset button
        reset_btn = tk.Button(title_frame, text="Reset", command=self.reset_chat,
                            bg="#ff3c00", fg="white", font=("Arial", 10), relief=tk.FLAT)
        reset_btn.pack(side=tk.RIGHT, padx=5)
        
        # Chat Display
        chat_frame = tk.Frame(self.root, bg="#1e1e1e")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, width=80, height=20,
            font=("Courier", 11), bg="#252526", fg="#d4d4d4",
            insertbackground="white"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg="#1e1e1e")
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.input_field = tk.Text(input_frame, height=3, font=("Arial", 11),
                                 bg="#3c3c3c", fg="white", insertbackground="white")
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message_on_enter)
        
        send_btn = tk.Button(input_frame, text=" Send", command=self.send_message,
                           bg="#00da07", fg="white", font=("Arial", 12, "bold"),
                           height=2, width=10)
        send_btn.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bg="#007acc", fg="white",
                                 anchor=tk.W, font=("Arial", 10))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def auto_greet(self):
        """Auto-send greeting message"""
        greeting = self.chat_manager.personality.get_greeting()
        self.add_message("Tux", greeting, "bot")
    
    def send_message_on_enter(self, event):
        """Handle Enter key press"""
        if event.state == 0:  # No modifier keys
            self.send_message()
            return "break"  # Prevent newline
    
    def send_message(self):
        """Send user message"""
        message = self.input_field.get("1.0", tk.END).strip()
        if not message:
            return
        
        # Clear input
        self.input_field.delete("1.0", tk.END)
        
        # Add user message to display
        self.add_message("You", message, "user")
        
        # Process in background
        self.status_bar.config(text=" Tux is thinking...")
        threading.Thread(target=self.process_in_background, args=(message,), daemon=True).start()
    
    def process_in_background(self, message):
        """Process message in background thread"""
        try:
            response = self.chat_manager.process_message(message)
            self.message_queue.put(("response", response))
        except Exception as e:
            self.message_queue.put(("error", str(e)))
    
    def check_queue(self):
        """Check for messages from background thread"""
        try:
            while True:
                msg_type, content = self.message_queue.get_nowait()
                if msg_type == "response":
                    self.add_message(" Tux", content, "bot")
                    self.status_bar.config(text="Ready")
                elif msg_type == "error":
                    self.add_message(" Error", content, "error")
                    self.status_bar.config(text=" Error occurred")
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_queue)
    
    def add_message(self, sender, message, msg_type):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add sender
        if msg_type == "user":
            color = "#0004d3"
        elif msg_type == "bot":
            color = "#00b906"
        else:
            color = "#e90000"
        
        self.chat_display.insert(tk.END, f"\n{sender}: ", f"sender_{msg_type}")
        self.chat_display.tag_config(f"sender_{msg_type}", foreground=color, font=("Arial", 11, "bold"))
        
        # Add message
        self.chat_display.insert(tk.END, f"{message}\n")
        
        # Auto-scroll
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def reset_chat(self):
        """Reset the conversation"""
        if messagebox.askyesno("Reset", "Clear conversation history?"):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.chat_manager.reset_conversation()
            self.add_message(" Tux", "Conversation reset. *sighs* Let's start over.", "bot")
    
    def show_stats(self):
        """Show chat statistics"""
        stats = self.chat_manager.get_stats()
        stats_text = f"""
 Chat Statistics:
─────────────────
• Total Messages: {stats['total_messages']}
• Conversation Length: {stats['conversation_length']} messages
• Duration: {stats['duration_minutes']} minutes
• API Keys: {len(API_KEYS)} active keys
• Expertise: C++, Rust, Docker, Kubernetes, CI/CD, Backend
        
 MLOps Skills Demonstrated:
─────────────────────────
• Multi-API Fallback System
• Containerization (Docker)
• CI/CD Pipeline Design
• Production Monitoring
• Error Handling & Retry Logic
"""
        messagebox.showinfo("Statistics & MLOps Skills", stats_text)

# ====================== MAIN ======================
def main():
    try:
        # Check for required packages
        import subprocess
        import importlib
        
        required = ['groq', 'tkinter']
        for package in required:
            if package == 'tkinter':
                continue  # Usually comes with Python
            try:
                importlib.import_module(package)
            except ImportError:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
        
        # Create GUI
        root = tk.Tk()
        app = TuxApp(root)
        
        # Center window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()