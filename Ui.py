import streamlit as st
import time
from logic import HexBotsGame
from models import model_decision
from utilis import draw_board
from config import MODEL_NAMES

def run_game_ui():
    st.title("🤖 HexBots – AI Grid Conquest")

    # --- Game Setup ---
    st.sidebar.header("🎮 Game Configuration")
    mode_type = st.sidebar.selectbox("Game Mode", ["Manual", "User vs AI", "AI vs AI"])
    player_count = st.sidebar.selectbox("Player Count", [2, 3] if mode_type == "AI vs AI" else [2, 3, 4])

    ai_players = []
    if "AI" in mode_type:
        ai_players = st.sidebar.multiselect("Select AI Models", MODEL_NAMES, default=MODEL_NAMES[:player_count - 1])

    # --- Game Init ---
    if "game" not in st.session_state or st.sidebar.button("🔁 New Game"):
        if mode_type == "AI vs AI":
            if len(ai_players) < player_count:
                ai_players = (ai_players * player_count)[:player_count]
            if len(ai_players) < player_count:
                st.warning("Please select one AI model per player.")
                st.stop()

        st.session_state.game = HexBotsGame(mode_type, player_count, ai_players)
        st.session_state.ai_explanation = ""
        st.session_state.auto_play = False

    game = st.session_state.game

    # --- Score Display ---
    st.subheader("📊 Scores")
    cols = st.columns(game.player_count)
    player_labels = {}

    for i, pid in enumerate(range(1, game.player_count + 1)):
        if mode_type == "User vs AI":
            label = f"You (P{pid})" if pid == 1 else f"{ai_players[pid - 2] if pid - 2 < len(ai_players) else 'AI'} (P{pid})"
        elif mode_type == "AI vs AI":
            label = f"{ai_players[pid - 1] if pid - 1 < len(ai_players) else 'AI'} (P{pid})"
        else:
            label = f"Player {pid} (P{pid})"
        cols[i].metric(label, f"{game.score_log.get(pid, 0)} pts")
        player_labels[pid] = label

    st.subheader(f"Turn {game.turn} — Player {game.current_player}'s Move")

    # --- Manual Input ---
    if mode_type == "Manual" or (mode_type == "User vs AI" and game.current_player == 1):
        st.markdown("#### 🎯 Enter Move Manually")
        r = st.number_input("Row", min_value=0, max_value=game.grid_size - 1, step=1, key="manual_r")
        c = st.number_input("Col", min_value=0, max_value=game.grid_size - 1, step=1, key="manual_c")
        if st.button("Make Move"):
            if game.apply_move(r, c, game.current_player):
                game.next_player()

    # --- Grid Click ---
    enable_grid_click = st.checkbox("🖱️ Enable On-Screen Cell Selection", value=True)
    if enable_grid_click:
        for r in range(game.grid_size):
            cols = st.columns(game.grid_size + (r % 2))
            for c in range(game.grid_size):
                tile = game.board[r, c]
                label = f"{r},{c}" if tile == 0 else f"P{tile}"
                col_index = c if r % 2 == 0 else c + 1
                if cols[col_index].button(label, key=f"{r},{c}"):
                    if game.is_valid_move(r, c):
                        if mode_type == "Manual" or (mode_type == "User vs AI" and game.current_player == 1):
                            game.apply_move(r, c, game.current_player)
                            game.next_player()

    # --- AI Controls ---
    if mode_type == "AI vs AI":
        col1, col2 = st.columns(2)
        if col1.button("▶️ Next AI Move"):
            st.session_state.auto_play = False
            st.session_state.run_one_step = True
        if col2.button("🎬 Play to End"):
            st.session_state.auto_play = True
            st.session_state.run_one_step = False

    # --- AI vs AI: autoplay ---
    if mode_type == "AI vs AI" and not game.game_over():
        if st.session_state.get("auto_play"):
            current_player = game.current_player
            if current_player < 1 or current_player > game.player_count:
                st.session_state.auto_play = False
                st.rerun()

            ai_index = current_player - 1
            model_name = ai_players[ai_index] if ai_index < len(ai_players) else "AI"
            legal = game.get_legal_moves()
            move = model_decision(game.board, model_name, legal)

            if move is not None:
                game.apply_move(*move, current_player)
                st.session_state.ai_explanation = f"🤖 **{model_name}** says: 'I'm choosing {move} to gain territory.'"
                st.info(st.session_state.ai_explanation)

            game.next_player()
            st.pyplot(draw_board(game.board, player_labels, score_overlay=True, scores=game.get_scores()))
            time.sleep(1)
            st.rerun()

        elif st.session_state.get("run_one_step"):
            st.session_state.run_one_step = False
            if not game.game_over():
                current_player = game.current_player
                ai_index = current_player - 1
                model_name = ai_players[ai_index] if ai_index < len(ai_players) else "AI"
                legal = game.get_legal_moves()
                move = model_decision(game.board, model_name, legal)
                if move is not None:
                    game.apply_move(*move, current_player)
                    st.session_state.ai_explanation = f"🤖 **{model_name}** says: 'I'm choosing {move} to gain territory.'"
                    game.next_player()
            st.rerun()

    # --- User vs AI ---
    elif mode_type == "User vs AI" and game.current_player != 1:
        while game.current_player != 1 and not game.game_over():
            ai_index = game.current_player - 2
            model_name = ai_players[ai_index] if ai_index < len(ai_players) else "AI"
            legal = game.get_legal_moves()
            move = model_decision(game.board, model_name, legal)
            if move is not None:
                game.apply_move(*move, game.current_player)
                st.session_state.ai_explanation = f"🤖 **{model_name}** says: 'I'm choosing {move} to gain territory.'"
                game.next_player()
                time.sleep(1.5)
        st.rerun()

    # --- Explanation ---
    if st.session_state.ai_explanation and not st.session_state.get("auto_play"):
        st.info(st.session_state.ai_explanation)

    # --- Final Board ---
    st.pyplot(draw_board(game.board, player_labels, score_overlay=True, scores=game.get_scores()))

    if game.game_over():
        st.session_state.auto_play = False
        winner = max(game.get_scores(), key=game.get_scores().get)
        st.success(f"🏁 Game Over! Winner: Player {winner}")
