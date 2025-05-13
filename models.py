# --- models.py ---
import random
import os
import re
from dotenv import load_dotenv
from groq import Groq

# Load API Key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Model backend IDs
MODEL_MAP = {
    "LLaMA": "meta-llama/llama-4-scout-17b-16e-instruct",
    "Mistral": "mistral-saba-24b",
    "DeepSeek": "deepseek-r1-distill-llama-70b"
}

def format_board_as_text(board):
    return "\n".join([" ".join([str(cell) for cell in row]) for row in board])

def extract_tuple(text):
    match = re.search(r"\((\d+),\s*(\d+)\)", text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None

def generate_ai_move(board, model_name, legal_moves, user_hint=""):
    model_id = MODEL_MAP.get(model_name)
    if not model_id:
        return random.choice(legal_moves) if legal_moves else None

    readable_board = format_board_as_text(board)
    prompt = f"""
You are an intelligent AI agent playing a 6x6 **Hexagonal Grid Territory Game**.

🎯 **Objective**: Dominate the grid by choosing and conquering empty cells (0). Your goal is to expand your territory and outperform other players.

🎮 **Game Details**:
- The board is a 6x6 grid of hexagonal tiles.
- Each tile contains a number:
    - 0 → unoccupied
    - 1-4 → tiles owned by Player 1 to Player 4
- You are playing as **{model_name}**, identified as **Player {model_name}**
- Your legal move options are: {legal_moves}
- {f'💬 The user suggests: {user_hint}' if user_hint else ''}
- Choose one move from this list to expand your territory.

🧠 **What to Do**:
1. Think aloud or express thoughts ("Hmm... looks like (2,3) is a smart move!")
2. Then return your move **as a single Python tuple only**, like: (row, col)

📋 **Current Board**:
{readable_board}

Return your final move below, formatted like: (row, col)
"""

    try:
        completion = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=60,
            stream=False
        )
        raw_output = completion.choices[0].message.content.strip()
        print(f"[{model_name}] Groq Raw Output:", raw_output)

        move = extract_tuple(raw_output)
        if move and move in legal_moves:
            return move

    except Exception as e:
        print(f"[{model_name}] Groq API failed: {e}")

    return random.choice(legal_moves) if legal_moves else None

def model_decision(board, model_name, legal_moves, user_hint=""):
    if not legal_moves:
        return None  # Prevents NoneType unpacking errors
    return generate_ai_move(board, model_name, legal_moves, user_hint)

