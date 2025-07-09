import ctypes
import sys
import time


class Game_State:
    setup_phase = True
    player1_time = True
    switch_to_player2 = None
    current_ship_direction = 'horizontal'

    ships_to_place = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    current_ship_index = 0
    current_ship_cells = []

    @staticmethod
    def player_block(cell_list):
            for cell in cell_list:
                cell.cell_btn_object.unbind('<Button-1>')

    @staticmethod
    def player_reset(cell_list,marked_list,guessed_list):
        for cell in cell_list:
            if cell not in marked_list and cell not in guessed_list:
                cell.cell_btn_object.bind('<Button-1>', cell.left_click_actions)

    @staticmethod
    def remove_buttons(cell_list):
        for cell in cell_list:
            if cell.cell_btn_object:
                cell.cell_btn_object.grid_forget()

    @staticmethod
    def restore_buttons(cell_list):
        for cell in cell_list:
            if cell.cell_btn_object:
                cell.cell_btn_object.grid(column=cell.x, row=cell.y)

    @staticmethod
    def end_game(winner):
        ctypes.windll.user32.MessageBoxW(0, f"Congratulations, {winner} wins!", f"{winner} wins.", 0)
        sys.exit()

    @staticmethod
    def white_buttons(cell_list):
        for cell in cell_list:
            cell.cell_btn_object.configure(bg = 'white')

    @staticmethod
    def white_all_buttons():
        from cell import Cell
        Game_State.white_buttons(Cell.player1_cells)
        Game_State.white_buttons(Cell.player2_cells)

    @staticmethod
    def finish_turn(own_cells, opponent_cells, marked, guessed, player1_time):
        import inscriptions
        Game_State.player_reset(own_cells, marked, guessed)
        Game_State.restore_buttons(own_cells)
        Game_State.player_block(opponent_cells)
        Game_State.remove_buttons(opponent_cells)
        Game_State.player1_time = player1_time
        inscriptions.update_message_label()



