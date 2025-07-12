from root import Root
from cell import Cell
from game_state import Game_State
import inscriptions
import settings
import app_contex

app_contex.root = Root()

inscriptions.adding_labels_and_buttons_to_root(
    app_contex.root,
    settings.player1_ship_count_coordinates,
    settings.player2_ship_count_coordinates,
    settings.message_label_object_coordinates,
    settings.direction_btn_object_coordinates
)

def switch_to_player2():
    Cell.build_player_grid("player2", app_contex.root.player2)

Game_State.switch_to_player2 = switch_to_player2

Cell.build_player_grid("player1", app_contex.root.player1)

app_contex.root.running_root()
