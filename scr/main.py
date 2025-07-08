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

player1 = Frame(
    root,
    bg='green',
    width=utilities.width_percentage(80),
    height=utilities.height_percentage(80)
)
player1.place(x=utilities.width_percentage(20), y=utilities.height_percentage(20))

player2 = Frame(
    root,
    bg='blue',
    width=utilities.width_percentage(80),
    height=utilities.height_percentage(80)
)
player2.place(x=utilities.width_percentage(60), y=utilities.height_percentage(20))

for x in range(settings.button_rows):
    for y in range(settings.button_columns):
        button = Cell(x,y)
        button.create_btn_object(
            player1,
            height = settings.button_height,
            width = settings.button_width
            )
        button.cell_btn_object.grid(column=x, row=y)


# uruchomienie okna
root.mainloop()