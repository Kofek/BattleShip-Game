from tkinter import Button, Label
import settings
import inscriptions
from game_state import Game_State
import time


class Cell:
    all = []
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

    @staticmethod
    def build_player_grid(name, location):
        cell_list = []
        if name == "player1":
            cell_list = Cell.player1_cells
        elif name == "player2":
            cell_list = Cell.player2_cells

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

    def is_click_valid(self):
        return (
                self not in Cell.player1_GuessedShips and
                self not in Cell.player2_GuessedShips and
                self not in Cell.player1_MarkedCells and
                self not in Cell.player2_MarkedCells
        )

    def left_click_actions(self, event):
        if not self.is_click_valid():
            return
        if Game_State.setup_phase:
            self.handle_setup_phase()
        else:
            self.handle_game_phase()

    def handle_setup_phase(self):
        self.is_ship = True
        self.cell_btn_object.unbind('<Button-1>')

        color = "green" if Game_State.player1_time else "blue"
        self.cell_btn_object.configure(bg=color)

        ship_list = Cell.player1_Ships if Game_State.player1_time else Cell.player2_Ships
        ship_list.append(self)

        if len(ship_list) == 5:
            Game_State.player_block(Cell.player1_cells if Game_State.player1_time else Cell.player2_cells)
            if Game_State.player1_time:
                Game_State.player1_time = False
                Game_State.switch_to_player2()
                Game_State.remove_buttons(Cell.player1_cells)
            else:
                Game_State.player1_time = True
                Game_State.setup_phase = False
                Game_State.player_block(Cell.player1_cells)
                Game_State.player_block(Cell.player2_cells)
                Game_State.player_reset(Cell.player1_cells, Cell.player1_MarkedCells,Cell.player1_GuessedShips)
                Game_State.player_reset(Cell.player2_cells, Cell.player2_MarkedCells,Cell.player2_GuessedShips)
                Game_State.remove_buttons(Cell.player1_cells)
            inscriptions.update_message_label()

    def handle_game_phase(self):
        if Game_State.player1_time:
            if self in Cell.player2_cells:
                if self.is_ship:
                    self.show_ship()
                else:
                    self.mark_cell()
                Game_State.player_block(Cell.player2_cells)
                self.cell_btn_object.after(1500,lambda:Game_State.finish_turn(Cell.player1_cells,Cell.player2_cells,Cell.player1_MarkedCells,Cell.player1_GuessedShips,False))
        else:
            if self in Cell.player1_cells:
                if self.is_ship:
                    self.show_ship()
                else:
                    self.mark_cell()
                Game_State.player_block(Cell.player1_cells)
                self.cell_btn_object.after(1500,lambda:Game_State.finish_turn(Cell.player2_cells,Cell.player1_cells,Cell.player2_MarkedCells,Cell.player2_GuessedShips,True))

    def show_ship(self):
        self.cell_btn_object.configure(bg='red')

        if self in Cell.player1_Ships:
            self.register_hit(Cell.player1_GuessedShips)
            winner = "Player 2"
        else:
            self.register_hit(Cell.player2_GuessedShips)
            winner = "Player 1"

        inscriptions.update_ship_labels()

        if len(Cell.player1_GuessedShips) == 5 or len(Cell.player2_GuessedShips) == 5:
            Game_State.end_game(winner)

    def register_hit(self, guessed_ships):
        guessed_ships.append(self)

    def mark_cell(self):
        self.cell_btn_object.configure(bg='yellow')
        self.cell_btn_object.unbind('<Button-1>')
        marked_cells = Cell.player1_MarkedCells if Game_State.player1_time else Cell.player2_MarkedCells
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