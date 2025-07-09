from tkinter import *
from cell import Cell
import settings
import utilities
import ctypes
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
game_title.place(x = utilities.width_percentage(45),y = 0)

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
    width=utilities.width_percentage(40),
    height=utilities.height_percentage(60)
)
player1.place(x=utilities.width_percentage(30), y=utilities.height_percentage(40))

player2 = Frame(
    root,
    bg='blue',
    width=utilities.width_percentage(30),
    height=utilities.height_percentage(60)
)
player2.place(x=utilities.width_percentage(70), y=utilities.height_percentage(40))

Cell.switch_to_player2 = Cell.bulid_player_grid("player2",player2)

Cell.creating_labels(left_frame,left_frame,middle_frame)

Cell.bulid_player_grid("player1",player1)

# uruchomienie okna
root.mainloop()
