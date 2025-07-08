from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell:
    all = []
    setup_phase = True;
    player1_time = True;
    player1_Ships = []
    player2_Ships = []
    cell_count_label_object = None
    ships_count_label_object = None

    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.is_ship = False
        self.cell_btn_object = None
        Cell.all.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def create_btn_object(self, location, height, width, text=" "):
        btn = Button(
            location,
            height = height,
            width = width,
            text = text
        )
        btn.bind('<Button-1>', self.left_click_actions) # left click
        self.cell_btn_object = btn


    def left_click_actions(self, event):
        if Cell.setup_phase:
            self.is_ship = True
            self.cell_btn_object.configure(bg='blue')
            if Cell.player1_time:
                Cell.player1_Ships.append(self)
                if len(Cell.player1_Ships) == 5:
                    Cell.player1_time = False
            else:
                Cell.player2_Ships.append(self)
                if len(Cell.player2_Ships) == 5:
                    Cell.setup_phase = False
        else:
            if self.is_ship:
                self.show_ship()
            else:
                self.mark_cell()
            self.cell_btn_object.unbind('<Button-1>')
    def show_ship(self):
        self.cell_btn_object.configure(bg='red')
        if self in self.player1_Ships:
            self.player1_Ships.remove(self)
        else:
            self.player2_Ships.remove(self)
        if len(self.player1_Ships) == 0:
            ctypes.windll.user32.MessageBoxW(0, "Congratulations, player 2 wins!", "Player 2 wins.", 0)
            sys.exit()
        if len(self.player2_Ships) == 0:
            ctypes.windll.user32.MessageBoxW(0, "Congratulations, player 1 wins!", "Player 1 wins.", 0)
            sys.exit()
        Cell.ships_count_label_object.configure(text=f"Player1 ships left: {Cell.player1_Ships.__len__()}")
        Cell.ships_count_label_object.configure(text=f"Player2 ships left: {Cell.player2_Ships.__len__()}")

    def mark_cell(self):
        color = self.cell_btn_object.cget('bg')
        if color == "orange":
            self.cell_btn_object.config(bg="SystemButtonFace")
        self.is_opened = True
        number_of_surrounding_ships = 0
        x = self.x,y = self.y
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (x + a) < 0 or (x + a) > (settings.button_rows - 1) or (y + b) < 0 or (y + b) > (settings.button_columns - 1):
                    continue
                if (self.get_cell_by_axis(x + a, y + b)).is_ship:
                    number_of_surrounding_ships += 1
        self.cell_btn_object.configure(text=number_of_surrounding_ships)
        if number_of_surrounding_ships == 0:
            self.automatic_0_check()

    def show_cell2(self):
        color = self.cell_btn_object.cget('bg')
        if color == "orange":
            self.cell_btn_object.config(bg="SystemButtonFace")
        if self.is_opened == False:
            Cell.cell_count -= 1
        self.is_opened = True
        Cell.cell_count_label_object.configure(text=f"Cells left: {Cell.cell_count}")
        number_of_surrounding_bombs = 0
        x = self.x
        y = self.y
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (x + a) < 0 or (x + a) > (settings.button_rows - 1) or (y + b) < 0 or (y + b) > (
                        settings.button_columns - 1):
                    continue
                if (self.get_cell_by_axis(x + a, y + b)).is_mine:
                    number_of_surrounding_bombs += 1
        self.cell_btn_object.configure(text=number_of_surrounding_bombs)

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    def list_of_surroundings(self):
        list_of_surroundings = []
        x = self.x
        y = self.y
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (x + a) < 0 or (x + a) > (settings.button_rows - 1) or (y + b) < 0 or (y + b) > (settings.button_columns - 1):
                    continue
                elif a == 0 and b == 0:
                    continue
                else:
                    list_of_surroundings.append(self.get_cell_by_axis(x + a, y + b))
        return list_of_surroundings

    def list_of_surroundings_lenght(self):
        list = self.list_of_surroundings()
        return len(list)

    def automatic_0_check(self):
        list = self.list_of_surroundings()










    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg = "black",
            fg = "white",
            width = 10,
            height = 2,
            text = (f"Cells left: {Cell.cell_count}"),
            font = ("", 21)
        )
        Cell.cell_count_label_object = lbl
    def create_mines_count_label(location):
        lbl = Label(
            location,
            bg = "black",
            fg = "white",
            width = 10,
            height = 2,
            text = (f"Mines left: {Cell.mines_count}"),
            font = ("", 21)
        )
        Cell.ships_count_label_object = lbl



# btn = Button(
#     center_frame, # tutaj decyzja w jakim oknie bedzie przycisk
#     bg = "blue", # kolor
#     text = "First button" # tekst
# )