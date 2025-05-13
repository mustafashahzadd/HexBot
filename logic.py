import numpy as np
from config import GRID_SIZES, PLAYER_IDS

class HexBotsGame:
    def __init__(self, mode_type, player_count, model_players=None):
        self.grid_size = GRID_SIZES[player_count]
        self.board = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.turn = 1
        self.current_player = 1
        self.player_count = player_count
        self.mode_type = mode_type
        self.ai_players = model_players or []  # <-- This line is required
        self.score_log = {pid: 0 for pid in PLAYER_IDS[:player_count]}

    def is_valid_move(self, r, c):
        return 0 <= r < self.grid_size and 0 <= c < self.grid_size and self.board[r, c] == 0

    def apply_move(self, r, c, player_id):
        if self.is_valid_move(r, c):
            self.board[r, c] = player_id
            self.score_log[player_id] += 5  # Example scoring
            return True
        return False

    def get_legal_moves(self):
        return [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if self.board[r, c] == 0]

    def next_player(self):
        self.current_player = self.current_player % self.player_count + 1
        self.turn += 1

    def game_over(self):
        return not any(self.board[r, c] == 0 for r in range(self.grid_size) for c in range(self.grid_size))

    def get_scores(self):
        return self.score_log