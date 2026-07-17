import tkinter as tk
from tkinter import messagebox

from ai import choose_move
from game import TicTacToeGame
from settings import (
    APP_TITLE,
    DARK_THEME,
    LIGHT_THEME,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from sounds import play_click, play_draw, play_win
from storage import load_data, save_data


class TicTacToeApp:
    def __init__(self, window):
        self.window = window
        self.window.title(APP_TITLE)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(False, False)

        self.game = TicTacToeGame()
        self.saved_data = load_data()

        self.theme_name = self.saved_data.get("theme", "Dark")
        self.theme = DARK_THEME if self.theme_name == "Dark" else LIGHT_THEME
        self.sound_enabled = self.saved_data.get("sound", True)

        self.mode = "1 Player"
        self.difficulty = "Easy"
        self.player_x_name = "Player X"
        self.player_o_name = "Computer"
        self.human_symbol = "X"
        self.computer_symbol = "O"
        self.target_score = 3

        self.x_score = 0
        self.o_score = 0
        self.draw_score = 0
        self.round_number = 1
        self.match_history = []

        self.game_started = False
        self.game_over = False
        self.computer_job = None
        self.countdown_job = None
        self.next_round_job = None

        self.board_buttons = []

        self.container = tk.Frame(self.window)
        self.container.pack(fill="both", expand=True)

        self.menu_frame = tk.Frame(self.container)
        self.game_frame = tk.Frame(self.container)

        self.build_menu_screen()
        self.build_game_screen()
        self.apply_theme()
        self.show_menu_screen()

        self.window.bind("<Key>", self.handle_keyboard)
        self.window.protocol("WM_DELETE_WINDOW", self.close_application)

    # =====================================================
    # SCREEN CREATION
    # =====================================================

    def build_menu_screen(self):
        self.menu_title = tk.Label(
            self.menu_frame,
            text="ULTIMATE TIC-TAC-TOE",
            font=("Arial", 30, "bold"),
        )
        self.menu_title.pack(pady=(35, 4))

        self.menu_subtitle = tk.Label(
            self.menu_frame,
            text="Choose your game settings",
            font=("Arial", 13, "bold"),
        )
        self.menu_subtitle.pack(pady=(0, 18))

        self.settings_panel = tk.Frame(self.menu_frame, padx=25, pady=20)
        self.settings_panel.pack()

        self.mode_variable = tk.StringVar(value="1 Player")
        self.difficulty_variable = tk.StringVar(value="Easy")
        self.symbol_variable = tk.StringVar(value="X")
        self.target_variable = tk.StringVar(value="3")

        tk.Label(
            self.settings_panel,
            text="Game mode",
            font=("Arial", 13, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.mode_menu = tk.OptionMenu(
            self.settings_panel,
            self.mode_variable,
            "1 Player",
            "2 Players",
            command=self.update_menu_fields,
        )
        self.mode_menu.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        self.player_one_label = tk.Label(
            self.settings_panel,
            text="Player 1 name",
            font=("Arial", 11, "bold"),
        )
        self.player_one_label.grid(row=2, column=0, sticky="w")

        self.player_one_entry = tk.Entry(
            self.settings_panel,
            width=28,
            font=("Arial", 12),
        )
        self.player_one_entry.insert(0, "Player 1")
        self.player_one_entry.grid(row=3, column=0, sticky="ew", pady=(3, 12))

        self.player_two_label = tk.Label(
            self.settings_panel,
            text="Player 2 name",
            font=("Arial", 11, "bold"),
        )
        self.player_two_label.grid(row=4, column=0, sticky="w")

        self.player_two_entry = tk.Entry(
            self.settings_panel,
            width=28,
            font=("Arial", 12),
        )
        self.player_two_entry.insert(0, "Player 2")
        self.player_two_entry.grid(row=5, column=0, sticky="ew", pady=(3, 12))

        tk.Label(
            self.settings_panel,
            text="Computer difficulty",
            font=("Arial", 11, "bold"),
        ).grid(row=6, column=0, sticky="w")

        self.difficulty_menu = tk.OptionMenu(
            self.settings_panel,
            self.difficulty_variable,
            "Easy",
            "Medium",
            "Hard",
        )
        self.difficulty_menu.grid(row=7, column=0, sticky="ew", pady=(3, 12))

        tk.Label(
            self.settings_panel,
            text="Choose your symbol",
            font=("Arial", 11, "bold"),
        ).grid(row=8, column=0, sticky="w")

        self.symbol_menu = tk.OptionMenu(
            self.settings_panel,
            self.symbol_variable,
            "X",
            "O",
        )
        self.symbol_menu.grid(row=9, column=0, sticky="ew", pady=(3, 12))

        tk.Label(
            self.settings_panel,
            text="Match target",
            font=("Arial", 11, "bold"),
        ).grid(row=10, column=0, sticky="w")

        self.target_menu = tk.OptionMenu(
            self.settings_panel,
            self.target_variable,
            "3",
            "5",
            "10",
        )
        self.target_menu.grid(row=11, column=0, sticky="ew", pady=(3, 5))

        menu_buttons = tk.Frame(self.menu_frame)
        menu_buttons.pack(pady=18)

        self.continue_button = tk.Button(
            menu_buttons,
            text="START MATCH",
            font=("Arial", 12, "bold"),
            padx=24,
            pady=10,
            relief="flat",
            command=self.start_session,
        )
        self.continue_button.grid(row=0, column=0, padx=5)

        self.about_button = tk.Button(
            menu_buttons,
            text="ABOUT",
            font=("Arial", 12, "bold"),
            padx=18,
            pady=10,
            relief="flat",
            command=self.show_about,
        )
        self.about_button.grid(row=0, column=1, padx=5)

        self.theme_button_menu = tk.Button(
            menu_buttons,
            text="THEME",
            font=("Arial", 12, "bold"),
            padx=18,
            pady=10,
            relief="flat",
            command=self.toggle_theme,
        )
        self.theme_button_menu.grid(row=0, column=2, padx=5)

        self.sound_button_menu = tk.Button(
            self.menu_frame,
            text="Sound: On",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.toggle_sound,
        )
        self.sound_button_menu.pack()

        self.update_menu_fields()

    def build_game_screen(self):
        top_bar = tk.Frame(self.game_frame)
        top_bar.pack(fill="x", padx=20, pady=(15, 5))

        self.game_heading = tk.Label(
            top_bar,
            text="TIC-TAC-TOE",
            font=("Arial", 24, "bold"),
        )
        self.game_heading.pack(side="left")

        self.sound_button_game = tk.Button(
            top_bar,
            text="Sound: On",
            font=("Arial", 9, "bold"),
            relief="flat",
            command=self.toggle_sound,
        )
        self.sound_button_game.pack(side="right", padx=3)

        self.theme_button_game = tk.Button(
            top_bar,
            text="Theme",
            font=("Arial", 9, "bold"),
            relief="flat",
            command=self.toggle_theme,
        )
        self.theme_button_game.pack(side="right", padx=3)

        self.mode_label = tk.Label(
            self.game_frame,
            text="",
            font=("Arial", 11, "bold"),
        )
        self.mode_label.pack(pady=(0, 8))

        self.score_panel = tk.Frame(self.game_frame, padx=15, pady=8)
        self.score_panel.pack(pady=(0, 8))

        self.x_name_label = tk.Label(
            self.score_panel,
            text="PLAYER X",
            font=("Arial", 10, "bold"),
            width=14,
        )
        self.x_name_label.grid(row=0, column=0)

        self.draw_name_label = tk.Label(
            self.score_panel,
            text="DRAWS",
            font=("Arial", 10, "bold"),
            width=10,
        )
        self.draw_name_label.grid(row=0, column=1)

        self.o_name_label = tk.Label(
            self.score_panel,
            text="PLAYER O",
            font=("Arial", 10, "bold"),
            width=14,
        )
        self.o_name_label.grid(row=0, column=2)

        self.x_score_label = tk.Label(
            self.score_panel,
            text="0",
            font=("Arial", 20, "bold"),
        )
        self.x_score_label.grid(row=1, column=0)

        self.draw_score_label = tk.Label(
            self.score_panel,
            text="0",
            font=("Arial", 20, "bold"),
        )
        self.draw_score_label.grid(row=1, column=1)

        self.o_score_label = tk.Label(
            self.score_panel,
            text="0",
            font=("Arial", 20, "bold"),
        )
        self.o_score_label.grid(row=1, column=2)

        self.target_label = tk.Label(
            self.game_frame,
            text="",
            font=("Arial", 10, "bold"),
        )
        self.target_label.pack()

        self.status_label = tk.Label(
            self.game_frame,
            text="Press Start Game",
            font=("Arial", 16, "bold"),
        )
        self.status_label.pack(pady=(8, 4))

        self.action_frame = tk.Frame(self.game_frame)
        self.action_frame.pack(pady=4)

        self.start_round_button = tk.Button(
            self.action_frame,
            text="START GAME",
            font=("Arial", 10, "bold"),
            padx=14,
            pady=7,
            relief="flat",
            command=self.start_round,
        )
        self.start_round_button.grid(row=0, column=0, padx=4)

        self.change_level_button = tk.Button(
            self.action_frame,
            text="CHANGE LEVEL",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=7,
            relief="flat",
            command=self.return_to_settings,
        )
        self.change_level_button.grid(row=0, column=1, padx=4)

        self.board_frame = tk.Frame(self.game_frame)
        self.board_frame.pack(pady=(4, 6))

        for position in range(9):
            button = tk.Button(
                self.board_frame,
                text="",
                font=("Arial", 28, "bold"),
                width=4,
                height=2,
                relief="flat",
                state="disabled",
                command=lambda index=position: self.handle_square_click(index),
            )
            button.grid(
                row=position // 3,
                column=position % 3,
                padx=4,
                pady=4,
            )
            self.board_buttons.append(button)

        bottom_buttons = tk.Frame(self.game_frame)
        bottom_buttons.pack(pady=(3, 7))

        self.undo_button = tk.Button(
            bottom_buttons,
            text="UNDO",
            font=("Arial", 9, "bold"),
            padx=14,
            pady=7,
            relief="flat",
            command=self.undo_move,
        )
        self.undo_button.grid(row=0, column=0, padx=3)

        self.reset_match_button = tk.Button(
            bottom_buttons,
            text="RESET MATCH",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=7,
            relief="flat",
            command=self.reset_match,
        )
        self.reset_match_button.grid(row=0, column=1, padx=3)

        self.main_menu_button = tk.Button(
            bottom_buttons,
            text="MAIN MENU",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=7,
            relief="flat",
            command=self.return_to_settings,
        )
        self.main_menu_button.grid(row=0, column=2, padx=3)

        self.history_title = tk.Label(
            self.game_frame,
            text="MATCH HISTORY",
            font=("Arial", 10, "bold"),
        )
        self.history_title.pack(pady=(7, 2))

        self.history_list = tk.Listbox(
            self.game_frame,
            height=4,
            width=50,
            font=("Arial", 10),
            activestyle="none",
        )
        self.history_list.pack()

        self.result_panel = tk.Frame(self.game_frame, padx=12, pady=8)

        self.result_label = tk.Label(
            self.result_panel,
            text="",
            font=("Arial", 14, "bold"),
        )
        self.result_label.pack(pady=(0, 6))

        result_buttons = tk.Frame(self.result_panel)
        result_buttons.pack()

        self.play_again_button = tk.Button(
            result_buttons,
            text="PLAY AGAIN",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=6,
            relief="flat",
            command=self.prepare_next_round,
        )
        self.play_again_button.grid(row=0, column=0, padx=3)

        self.result_change_button = tk.Button(
            result_buttons,
            text="CHANGE LEVEL",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=6,
            relief="flat",
            command=self.return_to_settings,
        )
        self.result_change_button.grid(row=0, column=1, padx=3)

        self.result_menu_button = tk.Button(
            result_buttons,
            text="MAIN MENU",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=6,
            relief="flat",
            command=self.return_to_settings,
        )
        self.result_menu_button.grid(row=0, column=2, padx=3)

    # =====================================================
    # MENU AND SESSION
    # =====================================================

    def update_menu_fields(self, *_):
        one_player = self.mode_variable.get() == "1 Player"

        self.player_two_entry.config(state="disabled" if one_player else "normal")
        self.difficulty_menu.config(state="normal" if one_player else "disabled")
        self.symbol_menu.config(state="normal" if one_player else "disabled")

    def show_menu_screen(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)

    def show_game_screen(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    def start_session(self):
        self.mode = self.mode_variable.get()
        self.difficulty = self.difficulty_variable.get()
        self.target_score = int(self.target_variable.get())

        player_one = self.player_one_entry.get().strip() or "Player 1"
        player_two = self.player_two_entry.get().strip() or "Player 2"

        if self.mode == "1 Player":
            self.human_symbol = self.symbol_variable.get()
            self.computer_symbol = "O" if self.human_symbol == "X" else "X"

            if self.human_symbol == "X":
                self.player_x_name = player_one
                self.player_o_name = "Computer"
            else:
                self.player_x_name = "Computer"
                self.player_o_name = player_one
        else:
            self.human_symbol = "X"
            self.computer_symbol = "O"
            self.player_x_name = player_one
            self.player_o_name = player_two

        self.x_score = 0
        self.o_score = 0
        self.draw_score = 0
        self.round_number = 1
        self.match_history = []
        self.history_list.delete(0, tk.END)

        self.mode_label.config(
            text=(
                f"{self.mode} • {self.difficulty}"
                if self.mode == "1 Player"
                else "Two Players"
            )
        )
        self.target_label.config(text=f"First to {self.target_score} wins")
        self.x_name_label.config(text=f"{self.player_x_name} (X)")
        self.o_name_label.config(text=f"{self.player_o_name} (O)")

        self.update_scoreboard()
        self.prepare_next_round()
        self.show_game_screen()

    # =====================================================
    # ROUND CONTROL
    # =====================================================

    def prepare_next_round(self):
        self.cancel_jobs()
        self.game.reset()
        self.game_started = False
        self.game_over = False
        self.result_panel.pack_forget()

        for button in self.board_buttons:
            button.config(
                text="",
                state="disabled",
                bg=self.theme["board"],
                activebackground=self.theme["hover"],
                disabledforeground=self.theme["text"],
            )

        self.status_label.config(
            text="Press START GAME",
            fg=self.theme["text"],
        )
        self.start_round_button.config(state="normal")
        self.change_level_button.config(state="normal")
        self.undo_button.config(state="disabled")

    def automatically_start_next_round(self):
        """
        Clears the completed board and automatically starts the next round
        without resetting the current match scores.
        """
        self.next_round_job = None
        self.prepare_next_round()

        self.status_label.config(
            text=f"Round {self.round_number} starting...",
            fg=self.theme["text"],
        )

        self.window.after(500, self.start_round)

    def start_round(self):
        if self.game_started:
            return

        self.game_started = True
        self.game_over = False
        self.start_round_button.config(state="disabled")
        self.change_level_button.config(state="disabled")
        self.countdown(3)

    def countdown(self, number):
        if number > 0:
            self.status_label.config(
                text=f"Starting in {number}...",
                fg=self.theme["text"],
            )
            self.countdown_job = self.window.after(
                400,
                lambda: self.countdown(number - 1),
            )
            return

        self.countdown_job = None
        self.change_level_button.config(state="normal")

        if self.mode == "1 Player" and self.computer_symbol == "X":
            self.game.current_player = "X"
            self.status_label.config(
                text="Computer starts",
                fg=self.theme["x"],
            )
            self.disable_board()
            self.computer_job = self.window.after(150, self.computer_move)
        else:
            self.game.current_player = "X"
            self.update_turn_message()
            self.enable_board()

    # =====================================================
    # GAMEPLAY
    # =====================================================

    def handle_square_click(self, position):
        if not self.game_started or self.game_over:
            return

        if self.mode == "1 Player" and self.game.current_player == self.computer_symbol:
            return

        if not self.game.make_move(position, self.game.current_player):
            return

        play_click(self.sound_enabled)
        self.draw_symbol(position, self.game.current_player)

        if self.finish_if_needed(self.game.current_player):
            return

        self.game.switch_player()
        self.update_turn_message()

        if self.mode == "1 Player" and self.game.current_player == self.computer_symbol:
            self.disable_board()
            self.computer_job = self.window.after(150, self.computer_move)
        else:
            self.enable_board()

    def computer_move(self):
        self.computer_job = None

        if self.game_over or not self.game_started:
            return

        position = choose_move(
            self.game,
            self.difficulty,
            self.computer_symbol,
        )

        if position is None:
            return

        self.game.make_move(position, self.computer_symbol)
        self.draw_symbol(position, self.computer_symbol)

        if self.finish_if_needed(self.computer_symbol):
            return

        self.game.switch_player()
        self.update_turn_message()
        self.enable_board()

    def draw_symbol(self, position, symbol):
        colour = self.theme["x"] if symbol == "X" else self.theme["o"]

        self.board_buttons[position].config(
            text=symbol,
            fg=colour,
            disabledforeground=colour,
            state="disabled",
        )

    def finish_if_needed(self, symbol):
        winning_line = self.game.check_winner(symbol)

        if winning_line:
            self.finish_round(symbol, winning_line)
            return True

        if self.game.is_draw():
            self.finish_draw()
            return True

        return False

    def finish_round(self, symbol, winning_line):
        self.game_over = True
        self.game_started = False
        self.disable_board()

        for position in winning_line:
            self.board_buttons[position].config(bg=self.theme["win"])

        if symbol == "X":
            self.x_score += 1
            winner_name = self.player_x_name
        else:
            self.o_score += 1
            winner_name = self.player_o_name

        self.saved_data["lifetime_scores"][symbol] += 1
        save_data(self.saved_data)

        play_win(self.sound_enabled)
        self.update_scoreboard()
        self.add_history(f"Round {self.round_number}: {winner_name} won")
        self.round_number += 1

        self.status_label.config(
            text=f"{winner_name} wins this round!",
            fg=self.theme["win"],
        )

        if self.x_score >= self.target_score or self.o_score >= self.target_score:
            self.show_match_champion(winner_name)
        else:
            self.result_panel.pack_forget()
            self.status_label.config(
                text=f"{winner_name} wins this round! Next round starting...",
                fg=self.theme["win"],
            )
            self.next_round_job = self.window.after(
                2000,
                self.automatically_start_next_round,
            )

    def finish_draw(self):
        self.game_over = True
        self.game_started = False
        self.draw_score += 1
        self.saved_data["lifetime_scores"]["Draws"] += 1
        save_data(self.saved_data)

        self.disable_board()
        play_draw(self.sound_enabled)
        self.update_scoreboard()
        self.add_history(f"Round {self.round_number}: Draw")
        self.round_number += 1

        self.result_panel.pack_forget()
        self.status_label.config(
            text="Draw! Next round starting...",
            fg=self.theme["o"],
        )
        self.next_round_job = self.window.after(
            2000,
            self.automatically_start_next_round,
        )

    def show_result_panel(self, message):
        self.result_label.config(text=message)
        self.result_panel.pack(pady=8)

    def show_match_champion(self, winner_name):
        self.result_label.config(
            text=f"{winner_name} is the match champion!"
        )
        self.result_panel.pack(pady=8)

    def update_turn_message(self):
        symbol = self.game.current_player
        name = self.player_x_name if symbol == "X" else self.player_o_name
        colour = self.theme["x"] if symbol == "X" else self.theme["o"]

        self.status_label.config(
            text=f"{name}'s turn",
            fg=colour,
        )

    # =====================================================
    # BOARD HELPERS
    # =====================================================

    def enable_board(self):
        if self.game_over or not self.game_started:
            return

        for index, button in enumerate(self.board_buttons):
            button.config(
                state="normal" if self.game.board[index] == "" else "disabled"
            )

        self.undo_button.config(
            state="normal" if self.mode == "2 Players" and self.game.move_history else "disabled"
        )

    def disable_board(self):
        for button in self.board_buttons:
            button.config(state="disabled")

    def undo_move(self):
        if self.mode != "2 Players" or self.game_over:
            return

        undone = self.game.undo_last_move()
        if undone is None:
            return

        position, _ = undone
        self.board_buttons[position].config(
            text="",
            bg=self.theme["board"],
            state="normal",
        )
        self.update_turn_message()
        self.enable_board()

    # =====================================================
    # SCORE, HISTORY, AND SETTINGS
    # =====================================================

    def update_scoreboard(self):
        self.x_score_label.config(text=str(self.x_score))
        self.o_score_label.config(text=str(self.o_score))
        self.draw_score_label.config(text=str(self.draw_score))

    def add_history(self, message):
        self.match_history.append(message)
        self.match_history = self.match_history[-5:]

        self.history_list.delete(0, tk.END)
        for item in self.match_history:
            self.history_list.insert(tk.END, item)

    def reset_match(self):
        confirmed = messagebox.askyesno(
            "Reset Match",
            "Reset the current scores and match history?",
        )

        if not confirmed:
            return

        self.x_score = 0
        self.o_score = 0
        self.draw_score = 0
        self.round_number = 1
        self.match_history = []
        self.history_list.delete(0, tk.END)
        self.update_scoreboard()
        self.prepare_next_round()

    def return_to_settings(self):
        self.cancel_jobs()
        self.prepare_next_round()
        self.show_menu_screen()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.saved_data["sound"] = self.sound_enabled
        save_data(self.saved_data)
        self.update_sound_buttons()

    def update_sound_buttons(self):
        text = "Sound: On" if self.sound_enabled else "Sound: Off"
        self.sound_button_menu.config(text=text)
        self.sound_button_game.config(text=text)

    def toggle_theme(self):
        self.theme_name = "Light" if self.theme_name == "Dark" else "Dark"
        self.theme = DARK_THEME if self.theme_name == "Dark" else LIGHT_THEME
        self.saved_data["theme"] = self.theme_name
        save_data(self.saved_data)
        self.apply_theme()

    def apply_theme(self):
        theme = self.theme
        self.window.configure(bg=theme["background"])
        self.container.configure(bg=theme["background"])
        self.menu_frame.configure(bg=theme["background"])
        self.game_frame.configure(bg=theme["background"])

        widgets = [
            self.menu_title,
            self.menu_subtitle,
            self.mode_label,
            self.game_heading,
            self.target_label,
            self.status_label,
            self.history_title,
        ]

        for widget in widgets:
            widget.config(
                bg=theme["background"],
                fg=theme["text"],
            )

        self.menu_subtitle.config(fg=theme["x"])
        self.mode_label.config(fg=theme["muted"])
        self.target_label.config(fg=theme["muted"])

        self.settings_panel.config(bg=theme["panel"])
        self.score_panel.config(bg=theme["panel"])
        self.action_frame.config(bg=theme["background"])
        self.board_frame.config(bg=theme["background"])
        self.result_panel.config(bg=theme["panel"])

        for child in self.settings_panel.winfo_children():
            try:
                child.config(
                    bg=theme["panel"],
                    fg=theme["text"],
                    activebackground=theme["hover"],
                    activeforeground=theme["text"],
                )
            except tk.TclError:
                pass

        self.player_one_entry.config(
            bg=theme["board"],
            fg=theme["text"],
            insertbackground=theme["text"],
        )
        self.player_two_entry.config(
            bg=theme["board"],
            fg=theme["text"],
            insertbackground=theme["text"],
        )

        for menu in (
            self.mode_menu,
            self.difficulty_menu,
            self.symbol_menu,
            self.target_menu,
        ):
            menu.config(
                bg=theme["board"],
                fg=theme["text"],
                activebackground=theme["hover"],
                activeforeground=theme["text"],
            )
            menu["menu"].config(
                bg=theme["board"],
                fg=theme["text"],
            )

        score_widgets = [
            self.x_name_label,
            self.draw_name_label,
            self.o_name_label,
            self.x_score_label,
            self.draw_score_label,
            self.o_score_label,
        ]

        for widget in score_widgets:
            widget.config(bg=theme["panel"], fg=theme["text"])

        self.x_name_label.config(fg=theme["x"])
        self.o_name_label.config(fg=theme["o"])
        self.draw_name_label.config(fg=theme["muted"])

        self.history_list.config(
            bg=theme["panel"],
            fg=theme["text"],
            selectbackground=theme["hover"],
        )

        self.result_label.config(
            bg=theme["panel"],
            fg=theme["text"],
        )

        for button in self.board_buttons:
            button.config(
                bg=theme["board"],
                activebackground=theme["hover"],
                fg=theme["text"],
                disabledforeground=theme["text"],
            )

        primary_buttons = [
            self.continue_button,
            self.start_round_button,
            self.play_again_button,
        ]

        for button in primary_buttons:
            button.config(
                bg=theme["win"],
                fg="#ffffff",
                activebackground=theme["win"],
            )

        secondary_buttons = [
            self.about_button,
            self.theme_button_menu,
            self.sound_button_menu,
            self.sound_button_game,
            self.theme_button_game,
            self.change_level_button,
            self.undo_button,
            self.reset_match_button,
            self.main_menu_button,
            self.result_change_button,
            self.result_menu_button,
        ]

        for button in secondary_buttons:
            button.config(
                bg=theme["board"],
                fg=theme["text"],
                activebackground=theme["hover"],
                activeforeground=theme["text"],
            )

        self.update_sound_buttons()

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Ultimate Tic-Tac-Toe Deluxe\n\n"
            "Built with Python and Tkinter.\n"
            "Features one-player and two-player modes,\n"
            "three computer difficulty levels, themes,\n"
            "sound, match history, keyboard controls,\n"
            "saved lifetime scores, and more.",
        )

    # =====================================================
    # KEYBOARD AND CLOSING
    # =====================================================

    def handle_keyboard(self, event):
        if event.char in "123456789" and self.game_started and not self.game_over:
            position = int(event.char) - 1
            self.handle_square_click(position)

        if event.keysym == "Escape":
            self.return_to_settings()

    def cancel_jobs(self):
        for job_name in (
            "computer_job",
            "countdown_job",
            "next_round_job",
        ):
            job = getattr(self, job_name)

            if job is not None:
                try:
                    self.window.after_cancel(job)
                except tk.TclError:
                    pass

                setattr(self, job_name, None)

    def close_application(self):
        self.saved_data["theme"] = self.theme_name
        self.saved_data["sound"] = self.sound_enabled
        save_data(self.saved_data)
        self.window.destroy()
