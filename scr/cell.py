from tkinter import Button, Label
import settings
import inscriptions
from game_state import Game_State
import app_contex
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
        current_ship_length = Game_State.ships_to_place[Game_State.current_ship_index]
        direction = Game_State.current_ship_direction
        start_x,start_y = self.x, self.y
        positions = []
        for i in range(current_ship_length):
            x = start_x + i if direction == "horizontal" else start_x
            y = start_y if direction == "horizontal" else start_y + i

            if x >= settings.button_rows or y >= settings.button_columns:
                return
            if Game_State.player1_time:
                cell = self.get_cell_by_axis(x, y,"player1")
            else:
                cell = self.get_cell_by_axis(x, y,"player2")
            if cell is None or cell.is_ship:
                return

            positions.append(cell)

        for cell in positions:
            cell.is_ship = True
            cell.cell_btn_object.configure(bg="green" if Game_State.player1_time else "blue")
            cell.cell_btn_object.unbind('<Button-1>')
            Game_State.current_ship_cells.append(cell)

        ship_list = Cell.player1_Ships if Game_State.player1_time else Cell.player2_Ships
        ship_list.append(Game_State.current_ship_cells.copy())

        Game_State.current_ship_cells.clear()
        Game_State.current_ship_index += 1

        if Game_State.current_ship_index >= len(Game_State.ships_to_place):
            if Game_State.player1_time:
                Game_State.block_player_cells(Cell.player1_cells)
                Game_State.player1_time = False
                Game_State.current_ship_index = 0
                Game_State.current_ship_cells.clear()
                Game_State.switch_to_player2()
                Game_State.forget_player_buttons(Cell.player1_cells)
            else:
                Game_State.player1_time = True
                Game_State.setup_phase = False
                Game_State.block_player_cells(Cell.player1_cells)
                Game_State.block_player_cells(Cell.player2_cells)
                Game_State.reset_player_cells(Cell.player1_cells, Cell.player1_MarkedCells, Cell.player1_GuessedShips)
                Game_State.reset_player_cells(Cell.player2_cells, Cell.player2_MarkedCells, Cell.player2_GuessedShips)
                Game_State.forget_player_buttons(Cell.player1_cells)
                Game_State.set_all_buttons_color_to_white()
            inscriptions.update_message_label(app_contex.root)
    def handle_game_phase(self):
        if Game_State.player1_time:
            if self in Cell.player2_cells:
                if self.is_ship:
                    self.show_ship()
                else:
                    self.mark_cell()
                Game_State.block_player_cells(Cell.player2_cells)
                self.cell_btn_object.after(1500,lambda:Game_State.finish_turn(Cell.player1_cells,Cell.player2_cells,Cell.player1_MarkedCells,Cell.player1_GuessedShips,False))
        else:
            if self in Cell.player1_cells:
                if self.is_ship:
                    self.show_ship()
                else:
                    self.mark_cell()
                Game_State.block_player_cells(Cell.player1_cells)
                self.cell_btn_object.after(1500,lambda:Game_State.finish_turn(Cell.player2_cells,Cell.player1_cells,Cell.player2_MarkedCells,Cell.player2_GuessedShips,True))

    def show_ship(self):
        self.cell_btn_object.configure(bg='red')

        if self in Cell.player1_Ships:
            self.register_hit(Cell.player1_GuessedShips)
            winner = "Player 2"
        else:
            self.register_hit(Cell.player2_GuessedShips)
            winner = "Player 1"

        inscriptions.update_ship_labels(app_contex.root)

        if len(Cell.player1_GuessedShips) == 5 or len(Cell.player2_GuessedShips) == 5:
            Game_State.end_game(winner)

    def register_hit(self, guessed_ships):
        guessed_ships.append(self)

    def mark_cell(self):
        self.cell_btn_object.configure(bg='yellow')
        self.cell_btn_object.unbind('<Button-1>')
        marked_cells = Cell.player1_MarkedCells if Game_State.player1_time else Cell.player2_MarkedCells
        marked_cells.append(self)


    def get_cell_by_axis(self, x, y,player):
        cell_list = []
        if player == "player1":
            cell_list = Cell.player1_cells
        elif player == "player2":
            cell_list = Cell.player2_cells
        for cell in cell_list:
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