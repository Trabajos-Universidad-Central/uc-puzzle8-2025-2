from tkinter import Tk
from gui import Puzzle8GUI


def main() -> None:
    root = Tk()
    Puzzle8GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()