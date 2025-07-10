from tkinter import *
import utilities
import settings

class Root:
    def __init__(self):
        self.root = Tk()
        self.root.configure(bg="black")
        self.root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
        self.root.title('BattleShip Game')
        self.root.resizable(False, False)

        self.top_frame = Frame(
            self.root,
            bg='black',
            width=utilities.width_percentage(100),
            height=utilities.height_percentage(20)
        )
        self.top_frame.place(x=0, y=0)

        self.left_frame = Frame(
            self.root,
            bg='yellow',
            width=utilities.width_percentage(20),
            height=utilities.height_percentage(80)
        )
        self.left_frame.place(x=0, y=utilities.height_percentage(20))

        self.middle_frame = Frame(
            self.root,
            bg='purple',
            width=utilities.width_percentage(80),
            height=utilities.height_percentage(20)
        )
        self.middle_frame.place(x=utilities.width_percentage(20), y=utilities.height_percentage(20))

        self.player1 = Frame(
            self.root,
            bg='green',
            width=utilities.width_percentage(30),
            height=utilities.height_percentage(60)
        )
        self.player1.place(x=utilities.width_percentage(30), y=utilities.height_percentage(40))

        self.between_players = Frame(
            self.root,
            bg='red',
            width=utilities.width_percentage(20),
            height=utilities.height_percentage(30)
        )
        self.between_players.place(x=utilities.width_percentage(50), y=utilities.height_percentage(40))

        self.player2 = Frame(
            self.root,
            bg='blue',
            width=utilities.width_percentage(30),
            height=utilities.height_percentage(60)
        )
        self.player2.place(x=utilities.width_percentage(70), y=utilities.height_percentage(40))

        self.game_title = Label(
            self.top_frame,
            bg="black",
            fg="white",
            text="BattleShip",
            font=("", 48)
        )
        self.game_title.place(relx=0.5, rely=0.5, anchor='center')

        self.player1_ship_count_location = self.left_frame
        self.player2_ship_count_location = self.left_frame
        self.message_label_object_location = self.middle_frame
        self.direction_btn_object_location = self.between_players

    def running_root(self):
        self.root.mainloop()

