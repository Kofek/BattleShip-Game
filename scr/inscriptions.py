from tkinter import Button, Label
from game_state import Game_State
import utilities

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
        width=int(utilities.width_percentage(1.5)),
        height=int(utilities.width_percentage(0.14)),
        text=(f"Player1, choose your {Game_State.ships_to_place[Game_State.current_ship_index]} ship location"),
        font=("", 21)
    )
    Cell.message_label_object = lbl

def create_direction_btn(location):
    from cell import Cell
    direction_btn = Button(
        location,
        text="Direction: Horizontal",
        command=toggle_direction_btn,
        width=50,
        height=3,
        bg='grey',
        fg='white'
    )
    Cell.direction_btn_object = direction_btn

def creating_labels(player1_location, player2_location, message_location, direction_btn_location):
    from cell import Cell
    create_player1_ship_count(player1_location)
    Cell.player1_ships_count_label_object.place(x=0, y=0)
    create_player2_ship_count(player2_location)
    Cell.player2_ships_count_label_object.place(x=0, y=50)
    create_message_label(message_location)
    Cell.message_label_object.place(relx=0.5, rely=0.5, anchor='center')
    create_direction_btn(direction_btn_location)
    Cell.direction_btn_object.place(relx=0.5, rely=0.5, anchor='center')

def toggle_direction_btn():
    from cell import Cell
    if Game_State.current_ship_direction == 'horizontal':
        Game_State.current_ship_direction = 'vertical'
        Cell.direction_btn_object.config(text="Direction: Vertical")
    else:
        Game_State.current_ship_direction = 'horizontal'
        Cell.direction_btn_object.config(text="Direction: Horizontal")

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
            Cell.message_label_object.configure(text=f"Player2, choose your {Game_State.ships_to_place[Game_State.current_ship_index]} ship location")
        else:
            Cell.message_label_object.configure(text=f"Player1, choose your {Game_State.ships_to_place[Game_State.current_ship_index]} ship location")
    else:
        if Game_State.player1_time:
            Cell.message_label_object.configure(text=f"Player1 turn.")
        else:
            Cell.message_label_object.configure(text=f"Player2 turn.")



