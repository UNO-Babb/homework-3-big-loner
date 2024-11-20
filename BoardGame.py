from flask import Flask, request, jsonify, render_template, redirect, url_for
import random

app = Flask(__name__)

# Initialize game state
board = ["empty"] * 50  # 50 spots on the board
players = {"red": 0, "blue": 0, "green": 0, "yellow": 0}  # Start positions
turn_order = ["red", "blue", "green", "yellow"]  # Player turn sequence
current_turn_index = 0

# Function to roll dice
def roll_dice():
    return random.randint(1, 6)

# Function to move a player
def move_player(player_color, steps):
    global board
    current_position = players[player_color]
    board[current_position] = "empty"  # Clear current position

    new_position = min(current_position + steps, len(board) - 1)  # Avoid going off the board
    players[player_color] = new_position
    board[new_position] = player_color  # Mark new position
    return new_position

@app.route("/")
def index():
    return render_template("index.html", board=board, players=players, current_turn=turn_order[current_turn_index])

@app.route("/roll_dice", methods=["POST"])
def roll_dice_endpoint():
    global current_turn_index
    current_player = turn_order[current_turn_index]
    dice_roll = roll_dice()
    new_position = move_player(current_player, dice_roll)

    # Check if the player won
    game_over = new_position == len(board) - 1

    # Update turn
    current_turn_index = (current_turn_index + 1) % len(turn_order)

    return render_template(
        "index.html",
        board=board,
        players=players,
        current_turn=turn_order[current_turn_index],
        last_roll=dice_roll,
        game_over=game_over,
        last_player=current_player
    )

@app.route("/reset_game", methods=["POST"])
def reset_game():
    global board, players, current_turn_index
    board = ["empty"] * 50
    players = {"red": 0, "blue": 0, "green": 0, "yellow": 0}
    current_turn_index = 0
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
