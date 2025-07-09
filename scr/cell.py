from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell:
    all = []
    setup_phase = True
    player1_time = True
    player1_cells = []
    player2_cells = []
    player1_Ships = []
    player2_Ships = []
    player1_GuessedShips = []
    player2_GuessedShips = []
    player1_MarkedCells = []
    player2_MarkedCells = []
    player1_ships_count_label_object = None
    player2_ships_count_label_object = None
    message_label_object = None

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

    def create_player1_ship_count(location):
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

    @staticmethod
    def player_block(cell_List):
        for cell in cell_List:
            cell.cell_btn_object.unbind('<Button-1>')

    @staticmethod
    def player_reset(cell_list,marked_list,guessed_list):
        for cell in cell_list:
            if cell not in marked_list and cell not in guessed_list:
                cell.cell_btn_object.bind('<Button-1>', cell.left_click_actions)

    @staticmethod
    def bulid_player_grid(name,location):
        if name == "player1":
            cell_list = Cell.player1_cells
        elif name == "player2":
            cell_list =Cell.player2_cells

        for x in range(settings.button_rows):
            for y in range(settings.button_columns):
                button = Cell(x, y)
                button.create_btn_object(
                    location,
                    height=settings.button_height,
                    width=settings.button_width
                )
                button.cell_btn_object.grid(column=x, row=y)
                cell_list.append(button)

    @staticmethod
    def end_game(winner):
        ctypes.windll.user32.MessageBoxW(0, f"Congratulations, {winner} wins!", f"{winner} wins.", 0)
        sys.exit()

    @staticmethod
    def update_ship_labels():
        p1_remaining = len(Cell.player1_Ships) - len(Cell.player1_GuessedShips)
        p2_remaining = len(Cell.player2_Ships) - len(Cell.player2_GuessedShips)

        Cell.player1_ships_count_label_object.configure(text=f"Player1 ships left: {p1_remaining}")
        Cell.player2_ships_count_label_object.configure(text=f"Player2 ships left: {p2_remaining}")

    @staticmethod
    def update_message_label():
        if Cell.setup_phase:
            if not Cell.player1_time:
                Cell.message_label_object.configure(text=f"Player2 chooses ships.")
            else:
                Cell.message_label_object.configure(text=f"Player1 turn.")
        else:
            if Cell.player1_time:
                Cell.message_label_object.configure(text=f"Player1 turn.")
            else:
                Cell.message_label_object.configure(text=f"Player2 turn.")

    @staticmethod
    def creating_labels(player1_location,player2_location,message_location):
        Cell.create_player1_ship_count(player1_location)
        Cell.player1_ships_count_label_object.place(x=0, y=0)
        Cell.create_player2_ship_count(player2_location)
        Cell.player2_ships_count_label_object.place(x=0, y=50)
        Cell.create_message_label(message_location)
        Cell.message_label_object.place(x=0, y=0)

    def left_click_actions(self, event):
        if not self.is_click_valid():
            return
        if Cell.setup_phase:
            self.handle_setup_phase()
        else:
            self.handle_game_phase()

    def is_click_valid(self):
        return (
                self not in Cell.player1_GuessedShips and
                self not in Cell.player2_GuessedShips and
                self not in Cell.player1_MarkedCells and
                self not in Cell.player2_MarkedCells
        )

    def handle_setup_phase(self):
        self.is_ship = True
        self.cell_btn_object.unbind('<Button-1>')

        color = "green" if Cell.player1_time else "blue"
        self.cell_btn_object.configure(bg=color)

        ship_list = Cell.player1_Ships if Cell.player1_time else Cell.player2_Ships
        ship_list.append(self)

        if len(ship_list) == 5:
            Cell.player_block(Cell.player1_cells if Cell.player1_time else Cell.player2_cells)
            if Cell.player1_time:
                Cell.player1_time = False
                Cell.switch_to_player2()
            else:
                Cell.player1_time = True
                Cell.setup_phase = False
                Cell.player_block(Cell.player1_cells)
                Cell.player_block(Cell.player2_cells)
                Cell.player_reset(Cell.player1_cells, Cell.player1_MarkedCells, Cell.player1_GuessedShips)
                Cell.player_reset(Cell.player2_cells, Cell.player2_MarkedCells, Cell.player2_GuessedShips)
            Cell.update_message_label()

    def handle_game_phase(self):
        if Cell.player1_time:
            if self in Cell.player2_cells:
                if self.is_ship:
                    self.show_ship()
                else:
                    self.mark_cell()
                Cell.player_block(Cell.player2_cells)
                Cell.player1_time = False
                Cell.player_reset(Cell.player1_cells, Cell.player1_MarkedCells, Cell.player1_GuessedShips)
                Cell.update_message_label()
        else:
            if self in Cell.player1_cells:
                if self.is_ship:
                    self.show_ship()
                else:
                    self.mark_cell()
                Cell.player_block(Cell.player1_cells)
                Cell.player1_time = True
                Cell.player_reset(Cell.player2_cells, Cell.player2_MarkedCells, Cell.player2_GuessedShips)
                Cell.update_message_label()

    def register_hit(self, guessed_ships):
        guessed_ships.append(self)

    def show_ship(self):
        self.cell_btn_object.configure(bg='red')

        if self in Cell.player1_Ships:
            self.register_hit(Cell.player1_GuessedShips)
            winner = "Player 2"
        else:
            self.register_hit(Cell.player2_GuessedShips)
            winner = "Player 1"

        Cell.update_ship_labels()

        if len(Cell.player1_GuessedShips) == 5 or len(Cell.player2_GuessedShips) == 5:
            Cell.end_game(winner)

    def mark_cell(self):
        self.cell_btn_object.configure(bg='yellow')
        self.cell_btn_object.unbind('<Button-1>')
        marked_cells = Cell.player1_MarkedCells if Cell.player1_time else Cell.player2_MarkedCells
        marked_cells.append(self)



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