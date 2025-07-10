from tkinter import Button, Label
from game_state import Game_State
import utilities
import app_contex

def create_player1_ship_count(root,location):
    from cell import Cell
    lbl = Label(
        location,
        bg="black",
        fg="white",
        width=20,
        height=2,
        text=f"Player1 ships left: {len(Game_State.ships_to_place)}",
        font=("", 21)
    )
    root.player1_ships_count_label_object = lbl

def create_player2_ship_count(root, location):
    from cell import Cell
    lbl = Label(
        location,
        bg="black",
        fg="white",
        width=20,
        height=2,
        text=f"Player2 ships left: {len(Game_State.ships_to_place)}",
        font=("", 21)
    )
    root.player2_ships_count_label_object = lbl

def create_message_label(root, location):
    lbl = Label(
        location,
        bg="black",
        fg="white",
        width=int(utilities.width_percentage(2.5)),
        height=int(utilities.width_percentage(0.14)),
        text=f"Player 1, place your {Game_State.ships_to_place[Game_State.current_ship_index]}-cell ship by selecting the starting cell.",
        font=("", 21)
    )
    root.message_label_object = lbl

def create_direction_btn(root, location):
    from cell import Cell
    direction_btn = Button(
        location,
        text="Direction: Horizontal",
        command=lambda: toggle_direction_btn(root),
        width=50,
        height=3,
        bg='grey',
        fg='white'
    )
    root.direction_btn_object = direction_btn

def adding_labels_and_buttons_to_root(root, coordinates1, coordinates2, coordinates3, coordinates4):
    create_player1_ship_count(root, root.player1_ship_count_location)
    root.player1_ships_count_label_object.place(x=coordinates1[0], y=coordinates1[1])

    create_player2_ship_count(root, root.player2_ship_count_location)
    root.player2_ships_count_label_object.place(x=coordinates2[0], y=coordinates2[1])

    create_message_label(root, root.message_label_object_location)
    root.message_label_object.place(relx=coordinates3[0], rely=coordinates3[1], anchor=coordinates3[2])

    create_direction_btn(root, root.direction_btn_object_location)
    root.direction_btn_object.place(relx=coordinates4[0], rely=coordinates4[1], anchor=coordinates4[2])

def toggle_direction_btn(root):
    if Game_State.current_ship_direction == 'horizontal':
        Game_State.current_ship_direction = 'vertical'
        root.direction_btn_object.config(text="Direction: Vertical")
    else:
        Game_State.current_ship_direction = 'horizontal'
        root.direction_btn_object.config(text="Direction: Horizontal")

def update_ship_labels(root):
    from cell import Cell
    p1_remaining = len(Cell.player1_Ships) - len(Cell.player1_GuessedShips)
    p2_remaining = len(Cell.player2_Ships) - len(Cell.player2_GuessedShips)

    root.player1_ships_count_label_object.configure(text=f"Player1 ships left: {p1_remaining}")
    root.player2_ships_count_label_object.configure(text=f"Player2 ships left: {p2_remaining}")

def update_message_label(root):
    if Game_State.setup_phase:
        if not Game_State.player1_time:
            root.message_label_object.configure(text=f"Player 1, place your {Game_State.ships_to_place[Game_State.current_ship_index]}-cell ship by selecting the starting cell.")
        else:
            root.message_label_object.configure(text=f"Player 2, place your {Game_State.ships_to_place[Game_State.current_ship_index]}-cell ship by selecting the starting cell.")
    else:
        if Game_State.player1_time:
            root.message_label_object.configure(text=f"Player1 turn.")
        else:
            root.message_label_object.configure(text=f"Player2 turn.")



