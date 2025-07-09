from tkinter import Button, Label
from game_state import Game_State

def create_player1_ship_count(location):
    from cell import Cell
    lbl = Label(
        location,
        bg="black",
        fg="white",
        width=20,
        height=2,
        text=("Player1 ships left: 5"),
        font=("", 21)
    )
    Cell.player1_ships_count_label_object = lbl

def create_player2_ship_count(location):
    from cell import Cell
    lbl = Label(
        location,
        bg="black",
        fg="white",
        width=20,
        height=2,
        text=("Player2 ships left: 5"),
        font=("", 21)
    )
    Cell.player2_ships_count_label_object = lbl

def create_message_label(location):
    from cell import Cell
    lbl = Label(
        location,
        bg="black",
        fg="white",
        width=50,
        height=2,
        text=("Player1 chooses ships."),
        font=("", 21)
    )
    Cell.message_label_object = lbl

def creating_labels(player1_location, player2_location, message_location):
    from cell import Cell
    create_player1_ship_count(player1_location)
    Cell.player1_ships_count_label_object.place(x=0, y=0)
    create_player2_ship_count(player2_location)
    Cell.player2_ships_count_label_object.place(x=0, y=50)
    create_message_label(message_location)
    Cell.message_label_object.place(x=0, y=0)

def update_ship_labels():
    from cell import Cell
    p1_remaining = len(Cell.player1_Ships) - len(Cell.player1_GuessedShips)
    p2_remaining = len(Cell.player2_Ships) - len(Cell.player2_GuessedShips)

    Cell.player1_ships_count_label_object.configure(text=f"Player1 ships left: {p1_remaining}")
    Cell.player2_ships_count_label_object.configure(text=f"Player2 ships left: {p2_remaining}")

def update_message_label():
    from cell import Cell
    if Game_State.setup_phase:
        if not Game_State.player1_time:
            Cell.message_label_object.configure(text=f"Player2 chooses ships.")
        else:
            Cell.message_label_object.configure(text=f"Player1 turn.")
    else:
        if Game_State.player1_time:
            Cell.message_label_object.configure(text=f"Player1 turn.")
        else:
            Cell.message_label_object.configure(text=f"Player2 turn.")


