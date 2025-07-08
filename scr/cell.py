from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell:
    all = []
    cell_count_label_object = None
    mines_count_label_object = None

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.x=x
        self.y=y
        self.is_opened = False
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
        btn.bind('<Button-3>', self.right_click_actions) # right click
        self.cell_btn_object = btn
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.show_cell()
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')
        if self.cell_count == 0:
            ctypes.windll.user32.MessageBoxW(0, "Congratulations, you won", "You Won", 0)
            sys.exit()

    def right_click_actions(self, event):
        color = self.cell_btn_object.cget('bg')
        if color == "SystemButtonFace":
            self.cell_btn_object.configure(bg="orange")
        if color == "orange":
            self.cell_btn_object.config(bg="SystemButtonFace")
    def list_of_surroundings(self):
        list_of_surroundings = []
        x = self.x
        y = self.y
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (x + a) < 0 or (x + a) > (settings.button_rows - 1) or (y + b) < 0 or (y + b) > (
                        settings.button_columns - 1):
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
        for cell in list:
            cell.show_cell2()

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
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
        Cell.mines_count_label_object = lbl
    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        if self.is_opened == False:
            Cell.mines_count -= 1
        self.is_opened = True
        Cell.mines_count_label_object.configure(text=f"Mines left: {Cell.mines_count}")
        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine", "Game Over", 0)
        sys.exit()

    def show_cell(self):
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
        for a in range(-1,2):
            for b in range(-1,2):
                if (x+a)<0 or (x+a)>(settings.button_rows-1) or (y+b)<0 or (y+b)>(settings.button_columns-1):
                    continue
                if (self.get_cell_by_axis(x+a, y+b)).is_mine:
                    number_of_surrounding_bombs += 1
        self.cell_btn_object.configure(text=number_of_surrounding_bombs)
        if number_of_surrounding_bombs == 0:
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
        for a in range(-1,2):
            for b in range(-1,2):
                if (x+a)<0 or (x+a)>(settings.button_rows-1) or (y+b)<0 or (y+b)>(settings.button_columns-1):
                    continue
                if (self.get_cell_by_axis(x+a, y+b)).is_mine:
                    number_of_surrounding_bombs += 1
        self.cell_btn_object.configure(text=number_of_surrounding_bombs)


# btn = Button(
#     center_frame, # tutaj decyzja w jakim oknie bedzie przycisk
#     bg = "blue", # kolor
#     text = "First button" # tekst
# )