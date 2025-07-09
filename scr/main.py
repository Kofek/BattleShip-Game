from tkinter import *
from cell import Cell
from game_state import Game_State
import inscriptions
import settings
import utilities
# podstawowe ustawienia okna
root = Tk()
root.configure(bg="black")
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title('BattleShip Game')
root.resizable(False, False)

top_frame = Frame(
    root,
    bg='black',
    width=utilities.width_percentage(100),
    height=utilities.height_percentage(20)
)
top_frame.place(x=0, y=0)

game_title = Label(
    top_frame,
    bg = "black",
    fg = "white",
    text = ("BattleShip"),
    font = ("", 48)
)
game_title.place(relx=0.5, rely=0.5, anchor='center')

left_frame = Frame(
    root,
    bg='yellow',
    width=utilities.width_percentage(20),
    height=utilities.height_percentage(80)
)
left_frame.place(x=0, y=utilities.height_percentage(20))

middle_frame = Frame(
    root,
    bg='purple',
    width=utilities.width_percentage(80),
    height=utilities.height_percentage(20)
)
middle_frame.place(x=utilities.width_percentage(20), y=utilities.height_percentage(20))

player1 = Frame(
    root,
    bg='green',
    width=utilities.width_percentage(30),
    height=utilities.height_percentage(60)
)
player1.place(x=utilities.width_percentage(30), y=utilities.height_percentage(40))

between_players = Frame(
    root,
    bg='red',
    width=utilities.width_percentage(20),
    height=utilities.height_percentage(30)
)
between_players.place(x=utilities.width_percentage(50), y=utilities.height_percentage(40))

player2 = Frame(
    root,
    bg='blue',
    width=utilities.width_percentage(30),
    height=utilities.height_percentage(60)
)
player2.place(x=utilities.width_percentage(70), y=utilities.height_percentage(40))

def switch_to_player2():
    Cell.build_player_grid("player2", player2)

Game_State.switch_to_player2 = switch_to_player2

inscriptions.creating_labels(left_frame, left_frame, middle_frame,between_players)

Cell.build_player_grid("player1", player1)

# uruchomienie okna
root.mainloop()
