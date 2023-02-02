import argparse
from word_generation import easy_words
import random
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
import speech_recognition as sr
import sounddevice as sd


margin_length = 20  # Exterior pixels outside of the 9x9 cells
side_length = 50  # Side length of every cell
board_width = margin_length * 2 + side_length * 9 + 300  # Total width of the sudoku board
board_height = margin_length * 2 + side_length * 9  # Height of the sudoku board


class SudokuBoardUI(Frame):
    """
    Delveloping the UI for the Sudoku board using the Tkinter library
    """
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.__initUI()


    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=board_width,
                             height=board_height)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self,
                              text="Clear answers",
                              command=self.__clear_cells)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_sudoku_grid()
        self.__draw_sudoku_puzzle()

        self.canvas.bind("<Button-1>", self.__clicked_cell)
        self.canvas.bind("<Key>", self.__pressed_key)


    def __draw_sudoku_grid(self):
        """
        Drawing grids
        """
        for i in range(10):
            if i%3 == 0:
            	color='blue'
            else:
            	color='gray'
            x_prev = margin_length + i * side_length
            y_prev = margin_length
            x_next = margin_length + i * side_length
            y_next = board_height - margin_length
            self.canvas.create_line(x_prev, y_prev, x_next, y_next, fill=color)

            x_prev = margin_length
            y_prev = margin_length + i * side_length
            x_next = board_width - margin_length
            y_next = margin_length + i * side_length
            self.canvas.create_line(x_prev, y_prev, x_next, y_next, fill=color)


    def __draw_sudoku_puzzle(self):
    	"""
    	This function draws the exterior of the sudoku puzzle
    	"""
    	self.canvas.delete("numbers")
    	for i in range(9):
    		for j in range(10):
    			answer = self.game.puzzle[i][j]
    			if answer != 0:
    				x = margin_length + j * side_length + side_length // 2
    				y = margin_length + i * side_length + side_length // 2
    				original = self.game.start_puzzle[i][j]
    				if answer == original:
    					color = 'black'
    				else:
    					color = 'sea green'
    				self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color)





    def __draw_sudoku_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x_prev = margin_length + self.col * side_length + 1
            y_prev = margin_length + self.row * side_length + 1
            x_next = margin_length + (self.col + 1) * side_length - 1
            y_next = margin_length + (self.row + 1) * side_length - 1
            self.canvas.create_rectangle(
                x_prev, y_prev, x_next, y_next,
                outline="red", tags="cursor"
            )


    def __draw_sudoku_victory(self):
        """ 
        To demonstrate the victory stage of the puzzle
        """
        x_prev = y_prev = margin_length + side_length * 2
        x_next = y_next = margin_length + side_length * 7
        self.canvas.create_oval(
            x_prev, y_prev, x_next, y_next,
            tags="victory", fill="dark orange", outline="orange"
        )
   
        x = y = margin_length + 4 * side_length + side_length / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="victory",
            fill="white", font=("Arial", 32)
        )


    def __clicked_cell(self, event):
        """
        This function is invoked whenever the user clicks a cell
        """
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if (margin_length < x < board_width - margin_length and margin_length < y < board_height - margin_length):
            self.canvas.focus_set()

            # To get the row and column value where the input needs to inserted
            row, col = (y - margin_length) // side_length, (x - margin_length) // side_length

            # If a cell is already highlighted, this deselects it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1
        # self.game.puzzle[WIDTH-100][HEIGHT-100] = "abc"
        self.__draw_sudoku_cursor()
        number_word_pair=self.__input_words()
        # input_word=self.__voice_input()

    def __validate_match(self,number_word_pair,input_word):
        """
        This function checks if the user voice input matches with the words displayed on the screen
        """
        flag=0
        for key,value in number_word_pair.items():
            if input_word == value:
                flag=1
                self.game.puzzle[self.row][self.col]= int(key)
                break
        if flag==0:
            self.game.puzzle[self.row][self.col]= 0
        self.__draw_sudoku_puzzle()


    def __voice_input(self):
        """
        This function is used to take voice input from the user through a microphone
        """
        r= sr.Recognizer()
	# r.pause_threshold = 0.8
        r.operation_timeout=5
        my_mic=sr.Microphone(device_index=1)
        with my_mic as source:
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source)
                voice_input=r.recognize_google(audio)
		# print(voice_input)
            except Exception as e:
                return(0)
        return voice_input


    def __input_words(self):
    	"""
    	This function creates the list of voice therapy words to be displayed on screen
    	"""
    	random.shuffle(easy_words)
    	number_word_pair={}
    	for i in range(9):
    		number_word_pair[i]=easy_words[i]
    		self.game.puzzle[i][9]="  " +str(i+1) + " --- " + number_word_pair[i]
    	self.__draw_sudoku_puzzle()
    	return number_word_pair


    def __pressed_key(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "0123456789":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_sudoku_puzzle()
            self.__draw_sudoku_cursor()
            if self.game.validate_win():
                self.__draw_sudoku_victory()


    def __clear_cells(self):
        """
        This function is used to clear all cells whenever required by user
        """
        self.game.start()
        self.canvas.delete("victory")
        self.__draw_sudoku_puzzle()


class SudokuBoardCreation(object):
    """
    This class creates a representation of the sudoku board
    """
    def __init__(self, board_file):
        self.board = self.__draw_sudoku_board(board_file)

    def __draw_sudoku_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip()
            board.append([])

            for c in line:
                board[-1].append(int(c))
        return board


class Game(object):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """
    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = SudokuBoardCreation(board_file).board

    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])
        for i in range(9):
        	self.puzzle[i].append(" ")

    def validate_win(self):
        for row in range(9):
            if not self.__row_check(row):
                return False
        for column in range(9):
            if not self.__col_check(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__square_check(row, column):
                    return False
        self.game_over = True
        return True

    def __cell_check(self, block):
        return set(block) == set(range(1, 10))

    def __row_check(self, row):
        return self.__cell_check(self.puzzle[row])

    def __col_check(self, column):
        return self.__cell_check(
            [self.puzzle[row][column] for row in range(9)]
        )

    def __square_check(self, row, column):
        return self.__cell_check(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )


if __name__ == '__main__':
    with open("l33t.sudoku", 'r') as boards_file:
        game = Game(boards_file)
        game.start()

        root = Tk()
        SudokuBoardUI(root, game)
        root.geometry("%dx%d" % (board_width, board_height + 40))
        root.mainloop()
