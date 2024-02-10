import math
import tkinter as tk
from tkinter import messagebox
from enum import Enum

CANVAS_WIDTH, CANVAS_HEIGHT = 800, 600
BOARD_WIDTH = 560
BOARD_HEIGHT = 480
FIELD_WIDTH = BOARD_WIDTH / 7
FIELD_HEIGHT = math.ceil(BOARD_HEIGHT / 6)
START_FIELD_X = (CANVAS_WIDTH - BOARD_WIDTH) // 2
START_FIELD_Y = CANVAS_HEIGHT - BOARD_HEIGHT
PENDING_PIECE_START_Y = START_FIELD_Y - 1.2 * FIELD_HEIGHT
HOLE_PADDING = 8
BACKGROUND = "#fab696"
BOARD_COLOR = "#3333ff"
BAR_THICKNESS = 4
BAR_COLOR = "#0000dd"
FONT = ("Helvetica", 48, "bold")
DROP_DELAY = 10


class Color(Enum):
    NONE = 0
    RED = 1
    YELLOW = 2


COLOR = {
    Color.RED: "red",
    Color.YELLOW: "yellow"
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connect four")
        self.geometry("800x700")
        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH,
                                height=CANVAS_HEIGHT, background=BACKGROUND)
        self.canvas.pack()

        self.buttonFrame = tk.Frame(self)
        self.newGameButton = tk.Button(
            self.buttonFrame, text="New Game", command=self.on_newGame)
        self.newGameButton.grid(row=0, column=0, ipadx=10, ipady=10)
        self.quitButton = tk.Button(
            self.buttonFrame, text="Quit", command=self.on_quit)
        self.quitButton.grid(row=0, column=1, ipadx=10, ipady=10)
        self.buttonFrame.pack(expand=True)

        self.initialize_game()

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.bind("<s>", lambda e: self.simulation_modus())

    def on_mouse_move(self, event):
        if self.moving_piece or self.winner:
            return

        if event.x > START_FIELD_X + FIELD_WIDTH * 6:
            column_index = 6
        elif event.x < START_FIELD_X:
            column_index = 0
        else:
            column_index = (event.x - START_FIELD_X) // FIELD_WIDTH

        if column_index == self.pending_piece_column:
            # No change
            return

        self.pending_piece_column = column_index
        new_x = START_FIELD_X + FIELD_WIDTH * column_index
        self.canvas.coords(self.pending_piece,
                           new_x,
                           PENDING_PIECE_START_Y, new_x + FIELD_WIDTH,
                           PENDING_PIECE_START_Y + FIELD_HEIGHT)

    def initialize_game(self):
        self.reset_fields()
        self.canvas.delete("all")
        self.winner = {}
        self.current_player = Color.RED
        self.pending_piece_column = 3
        self.pending_piece = self.generate_next_piece()
        self.moving_piece = None
        self.render_initial_state()

    def generate_next_piece(self):
        init_x = START_FIELD_X + self.pending_piece_column * FIELD_WIDTH
        oval = self.canvas.create_oval(init_x, PENDING_PIECE_START_Y, init_x + FIELD_WIDTH,
                                       PENDING_PIECE_START_Y + FIELD_HEIGHT, fill=COLOR[self.current_player])
        self.canvas.tag_lower(oval)
        return oval

    def reset_fields(self):
        self.fields = [[0] * 7, [0] * 7,
                       [0] * 7, [0] * 7,
                       [0] * 7, [0] * 7]

    def on_canvas_click(self, event):
        if self.moving_piece or self.winner:
            return

        x = event.x - START_FIELD_X
        if x < 0 or x > BOARD_WIDTH:
            return

        column_index = int(x // FIELD_WIDTH)
        self.execute_move(column_index)

    def execute_move(self, column_index):
        pieces_in_column = self.find_pieces_in_column(column_index)
        if pieces_in_column == 6:
            # Column already filled
            return

        adjusted_x = START_FIELD_X + FIELD_WIDTH * column_index
        self.canvas.coords(self.pending_piece, adjusted_x, PENDING_PIECE_START_Y,
                           adjusted_x + FIELD_WIDTH, PENDING_PIECE_START_Y + FIELD_HEIGHT)
        destination_y = START_FIELD_Y + \
            (6 - pieces_in_column - 1) * FIELD_HEIGHT
        self.moving_piece = {
            "ref": self.pending_piece,
            "destination_y": destination_y,
            "coords": (5 - pieces_in_column, column_index)
        }
        self.drop_piece()

    def drop_piece(self):
        if not self.moving_piece:
            return

        ref = self.moving_piece["ref"]
        self.canvas.move(ref, 0, 50)
        self.after(DROP_DELAY, self.drop_piece)
        if self.canvas.coords(ref)[1] > self.moving_piece["destination_y"]:
            dest_x, dest_y = self.canvas.coords(
                ref)[0], self.moving_piece["destination_y"]
            final_coords = dest_x, dest_y, dest_x + FIELD_WIDTH, dest_y + FIELD_HEIGHT
            self.canvas.coords(ref, *final_coords)
            self.finalize_move()

    def finalize_move(self):
        row, col = self.moving_piece["coords"]
        self.fields[row][col] = self.current_player
        self.moving_piece = {}
        self.current_player = Color.RED if self.current_player == Color.YELLOW else Color.YELLOW
        self.winner = self.check_winner()
        if self.winner:
            self.visualize_winner()
        elif self.board_full():
            self.draw()
        else:
            self.pending_piece = self.generate_next_piece()

    def find_pieces_in_column(self, column_index):
        return sum(bool(row[column_index]) for row in self.fields)

    def check_winner(self):
        for row_idx in range(6):
            for col_idx in range(7):
                if col_idx <= 3:
                    horiz_coords = [(row_idx, col_idx+i) for i in range(4)]
                    if self.is_same_color(self.get_fields(horiz_coords)):
                        return horiz_coords

                    diag_direction = 1 if row_idx <= 2 else -1
                    diag_coords = [(row_idx + i * diag_direction, col_idx + i)
                                   for i in range(4)]
                    if self.is_same_color(self.get_fields(diag_coords)):
                        return diag_coords

                if row_idx <= 2:
                    vert_coords = [(row_idx+i, col_idx) for i in range(4)]
                    if self.is_same_color(self.get_fields(vert_coords)):
                        return vert_coords

    def get_fields(self, coords):
        return [self.fields[y][x] for y, x in coords]

    def visualize_winner(self):
        start, end = self.winner[0], self.winner[3]
        start_x = START_FIELD_X + (start[1] + .5) * FIELD_WIDTH
        start_y = START_FIELD_Y + (start[0] + .5) * FIELD_HEIGHT
        end_x = START_FIELD_X + (end[1] + .5) * FIELD_WIDTH
        end_y = START_FIELD_Y + (end[0] + .5) * FIELD_HEIGHT

        winner_color = COLOR[self.fields[self.winner[0][0]][self.winner[0][1]]]
        self.canvas.create_line(start_x, start_y, end_x,
                                end_y, width=30, fill=winner_color)

        text = winner_color.upper() + " WINS"
        self.canvas.create_text(CANVAS_WIDTH / 2, 50, text=text,
                                font=FONT, fill=winner_color, anchor="center")

    def moves_made(self):
        for row in self.fields:
            if any(x for x in row):
                return True
        return False

    def board_full(self):
        for row in self.fields:
            if not all(x for x in row):
                return False
        return True

    def draw(self):
        self.winner = "draw"
        self.canvas.create_text(CANVAS_WIDTH / 2, 50, text="DRAW",
                                font=FONT, fill="gray", anchor="center")

    def is_same_color(self, fields):
        first = fields[0]
        if first == 0:
            return False
        for f in fields[1:]:
            if f != first:
                return False
        return True

    def on_quit(self):
        result = messagebox.askyesno("Confirmation", "Really quit?")
        if not result:
            return
        self.destroy()

    def on_newGame(self):
        if self.moves_made() and not self.winner:
            result = messagebox.askyesno(
                "Confirmation", "Abort the current game?")
            if not result:
                return

        self.initialize_game()

    def simulate_seq(self, sequence):
        if not sequence:
            return
        self.execute_move(sequence[0])
        self.after(300, lambda: self.simulate_seq(sequence[1:]))

    def simulate(self, sequence):
        self.initialize_game()
        self.simulate_seq(sequence)

    def simulation_modus(self):
        self.bind("<r>", lambda e: self.simulate([0, 0, 1, 1, 2, 2, 3]))
        self.bind("<c>", lambda e: self.simulate([0, 1, 0, 1, 0, 1, 0]))
        self.bind("<d>", lambda e: self.simulate(
            [0, 1, 2, 3, 0, 0, 0, 1, 0, 1, 1, 2, 2, 4, 3]))
        self.bind("<f>", lambda e: self.simulate(
            [3, 3, 3, 2, 3, 2, 2, 1, 1, 4, 0]))
        self.bind("<q>", lambda e: self.draw())

    def render_initial_state(self):
        self.canvas.create_rectangle(START_FIELD_X,
                                     START_FIELD_Y,
                                     START_FIELD_X + BOARD_WIDTH,
                                     START_FIELD_Y + BOARD_HEIGHT,
                                     outline=BOARD_COLOR,
                                     width=10)

        for y in range(6):
            for x in range(7):
                x_start = int(START_FIELD_X + FIELD_WIDTH * x)
                y_start = int(START_FIELD_Y + FIELD_HEIGHT * y)
                self.canvas.create_oval(x_start,
                                        y_start,
                                        x_start + FIELD_WIDTH,
                                        y_start + FIELD_HEIGHT,
                                        outline=BOARD_COLOR, width=10)

        for i in range(1, 7):
            x_start = int(START_FIELD_X + FIELD_WIDTH * i) - BAR_THICKNESS
            r = self.canvas.create_rectangle(x_start,
                                             START_FIELD_Y,
                                             x_start + BAR_THICKNESS * 2,
                                             START_FIELD_Y + BOARD_HEIGHT,
                                             fill=BAR_COLOR)
            self.canvas.tag_lower(r)

        for i in range(1, 6):
            y_start = int(START_FIELD_Y + FIELD_HEIGHT * i) - BAR_THICKNESS
            r = self.canvas.create_rectangle(START_FIELD_X,
                                             y_start,
                                             START_FIELD_X + BOARD_WIDTH,
                                             y_start + BAR_THICKNESS * 2,
                                             fill=BAR_COLOR)
            self.canvas.tag_lower(r)


app = App()
app.mainloop()
