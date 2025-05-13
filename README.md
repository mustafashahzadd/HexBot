
# 🤖 HexBots – AI Grid Conquest

HexBots is a strategic, turn-based hexagonal grid domination game developed using **Streamlit**, featuring interactive gameplay modes like:
- Manual multiplayer
- User vs AI (1 human + AI bots)
- AI vs AI (automated simulation)

Players take turns to claim hexagonal cells on a grid, and AI players make intelligent decisions based on the board state using LLM prompts or model logic.

## 📁 Project Structure

```
.
├── .devcontainer/           # VSCode dev container config (optional)
├── .github/                 # GitHub Actions/workflow files
├── AI Demo Video/           # Demo recordings for presentation/showcase
├── config.py                # Configuration (model list, settings)
├── logic.py                 # Core game logic (board, move validation, scoring)
├── models.py                # AI move generation & decision strategy (LLM or random)
├── streamlit_app.py         # Entry-point to launch app via Streamlit
├── Ui.py                    # Streamlit UI logic (game modes, grid, rendering)
├── utils.py                 # Helper functions (draw_board, board formatting)
├── requirements.txt         # Python dependencies
├── README.md                # You're here!
```

##  Features

###  Game Modes
- **Manual** – Play locally with 2–4 players manually clicking hexes.
- **User vs AI** – Human vs selected AI models.
- **AI vs AI** – Fully autonomous simulation with time-delayed animations.

### 🤖 AI Decision Logic
- Supports multiple AI models (e.g., LLaMA, Mistral, DeepSeek)
- Configurable via `MODEL_NAMES` in `config.py`
- AI responds using smart prompts, optionally influenced by human "hints"
- Decisions generated using `generate_ai_move(...)` from `models.py`

###  Visual Features
- Color-coded territory zones with live score updates
- In-turn animations: AI moves shown with 2–3 sec delays and natural explanations
- Responsive on-screen grid input (clickable buttons)

##  Installation

1. Clone the repository:

```bash
git clone https://github.com/mustafashahzadd/HexBot.git
cd HexBot
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # on Unix/macOS
.venv\Scripts\activate   # on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run streamlit_app.py
```

##  AI Prompting (LLM Logic)

Located in `models.py`, the AI uses a context-aware prompt that includes:
- Objective + Rules
- Model name + board ID
- Current board state (formatted)
- Legal move options
- Optional human hint (`user_hint`)
- Returns move as `(row, col)` tuple

##  Example AI Response

>  **Mistral** says: “I’m choosing (4, 2) to gain territory near the corner.”

This message appears before each AI move to simulate thoughtful reasoning.

## 📹 Demo And Report

A walkthrough video is included in the `/AI Demo Video` folder. You may also run a full match using “Play to End” to visualize AI turns.
A walkthrough of report included in the `/AI Project Report` folder.

Want a direct access to the demo and report follow the drive link below
https://drive.google.com/drive/u/0/folders/1itRf7YRnVr3xjzMS7DeE3_uMGKxmddAm

## 🔧 Future Enhancements
- Real-time multiplayer over sockets (WebSockets)
- Leaderboard + scoring history
- AI training mode with RAG-enhanced suggestions
- Sound/turn alert system
- Skin/theme customizer

##  License

This project is licensed under the [Apache 2.0 License](LICENSE).

---
