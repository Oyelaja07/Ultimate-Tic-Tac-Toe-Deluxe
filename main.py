import tkinter as tk

from gui import TicTacToeApp


def main():
    window = tk.Tk()
    TicTacToeApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()
