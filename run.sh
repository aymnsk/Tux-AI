#!/bin/bash

cd "$(dirname "$0")"

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Creating from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Created .env file. Please edit it with your API keys."
        echo "Opening editor..."
        nano .env
        
    else
        echo "Creating new .env file..."
        cat > .env << 'ENVEOF'
# Groq API Keys (fallback system)
GROQ_API_KEY_1=your_key_here_1
GROQ_API_KEY_2=your_key_here_2
GROQ_API_KEY_3=your_key_here_3
GROQ_API_KEY_4=your_key_here_4
GROQ_API_KEY_5=your_key_here_5

# Model Configuration
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_MODEL_BACKUP=mixtral-8x7b-32768

# Chatbot Configuration
MAX_TOKENS=4096
TEMPERATURE=0.7
ENVEOF
        echo "Created .env file. Please edit it with your API keys."
        echo "Opening editor..."
        nano .env
    fi
    exit 1
fi

# Add current directory to Python path
export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/src"

# Check Python version
python -c "
import sys
if sys.version_info < (3, 8):
    print('ERROR: Python 3.8+ required')
    sys.exit(1)
"

# Install dotenv if missing
python -c "import dotenv" 2>/dev/null || pip install python-dotenv -q

# Run the chatbot
echo "Starting Tux Chatbot..."
echo "=============================="

python -c "
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Check for API keys
api_keys = []
for i in range(1, 6):
    key = os.getenv(f'GROQ_API_KEY_{i}')
    if key and key != f'your_key_here_{i}':
        api_keys.append(key)

if not api_keys:
    print('ERROR: No valid API keys found in .env file!')
    print('Please add your Groq API keys to .env')
    sys.exit(1)

print(f'Found {len(api_keys)} API keys')
print('==============================')
print('TUX: Senior MLOps Engineer Chatbot')
print('==============================')

try:
    from groq import Groq
except ImportError:
    print('Installing groq...')
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'groq'])
    from groq import Groq

class SimpleTux:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.current_key = 0
        self.client = Groq(api_key=self.api_keys[self.current_key])
        self.conversation = []
    
    def rotate_key(self):
        self.current_key = (self.current_key + 1) % len(self.api_keys)
        self.client = Groq(api_key=self.api_keys[self.current_key])
        print(f'[*] Rotated to API key {self.current_key + 1}')
    
    def chat(self, message):
        # Prepare messages
        messages = [
            {
                'role': 'system', 
                'content': '''You are Tux, a senior MLOps/DevOps engineer with expertise in C++, Rust, backend architecture, and deployments.

Your personality:
- Blunt, honest, sarcastic, and funny
- Technical and production-focused
- No-nonsense attitude
- Loves container orchestration
- Hates bad deployment practices

Example responses:
- "Let me be blunt..."
- "*sighs in binary*"
- "That deployment strategy is giving me segmentation faults."
- "Not terrible. For a human."

Focus on practical, production-ready advice.'''
            }
        ]
        messages.extend(self.conversation[-4:])  # Keep last 4 messages for context
        messages.append({'role': 'user', 'content': message})
        
        try:
            response = self.client.chat.completions.create(
                model=os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile'),
                messages=messages,
                max_tokens=int(os.getenv('MAX_TOKENS', 500)),
                temperature=float(os.getenv('TEMPERATURE', 0.7))
            )
            
            reply = response.choices[0].message.content
            self.conversation.append({'role': 'user', 'content': message})
            self.conversation.append({'role': 'assistant', 'content': reply})
            
            # Keep conversation manageable
            if len(self.conversation) > 10:
                self.conversation = self.conversation[-10:]
            
            return reply
            
        except Exception as e:
            error_msg = str(e).lower()
            if 'rate' in error_msg or 'quota' in error_msg:
                self.rotate_key()
                return self.chat(message)  # Retry with new key
            else:
                return f"*Tux facepalms* Error: {e}"

def main():
    tux = SimpleTux(api_keys)
    
    print('\\nTux: *checks watch* You\'ve got 5 minutes. Make it quick.')
    print('Type "quit" to exit, "reset" to clear memory\\n')
    
    while True:
        try:
            user_input = input('You: ').strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'quit':
                print('\\nTux: Finally. My containers miss me.')
                break
            elif user_input.lower() == 'reset':
                tux.conversation = []
                print('\\nTux: Memory wiped. Try not to repeat your mistakes.')
                continue
            
            print('\\nTux: Thinking...')
            response = tux.chat(user_input)
            print(f'\\nTux: {response}\\n')
            
        except KeyboardInterrupt:
            print('\\n\\nTux: SIGINT? Amateur.')
            break
        except EOFError:
            print('\\n\\nTux: EOF? Typical.')
            break
        except Exception as e:
            print(f'\\nTux: *kernel panic* {e}')

if __name__ == '__main__':
    main()
"
