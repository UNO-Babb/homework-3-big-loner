from flask import Flask, request, jsonify, render_template, redirect, url_for
import random

def save_game():
    outFile = open("data.csv", 'w')
    
    # Save players' positions
    outFile.write("player,position\n")
    
    for player, position in players.items():
        outFile.write(f"{player},{position}\n")
    
    # Save current turn
    outFile.write(f"turn,{turn_order[current_turn_index]}\n")
    outFile.close()


def load_game():
    global board, players, current_turn_index
    
    inFile = open("data.csv", 'r')
    lines = inFile.readlines()
    
    if len(lines) < 6:
        print("Save file is incomplete. Initializing a new game.")
        save_game()
        return
    
    for line in lines[1:5]:
        player, position = line.strip().split(",")
        players[player] = int(position)

        _, current_turn = lines[5].strip().split(",")
        current_turn_index = turn_order.index(current_turn)

    
    for i in range(len(board)):
        board[i] = "empty" 
    
    for player, position in players.items():
        board[position] = player

    inFile.close()
    

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

    save_game()

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

    save_game()

    return redirect(url_for("index"))

if __name__ == "__main__":
    load_game()
    app.run(debug=True)
