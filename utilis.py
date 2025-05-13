# --- utils.py ---
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from config import PLAYER_COLORS

def draw_board(board, player_labels, score_overlay=False, scores=None):
    grid_size = board.shape[0]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    dx = 3 ** 0.5

    for r in range(grid_size):
        for c in range(grid_size):
            x = dx * (c + 0.5 * (r % 2))
            y = 1.5 * r
            pid = board[r, c]
            color = PLAYER_COLORS.get(pid, "#d3d3d3")
            hex = patches.RegularPolygon((x, y), 6, radius=0.95, orientation=0.52,
                                          facecolor=color, edgecolor='black')
            ax.add_patch(hex)

            # Label player or show coordinates
            label = player_labels.get(pid, f"{r},{c}") if pid else f"{r},{c}"
            ax.text(x, y, label, ha='center', va='center', fontsize=7, color='black')

    ax.set_xlim(-1, dx * grid_size)
    ax.set_ylim(-1, 1.5 * grid_size)
    ax.axis('off')
    return fig
