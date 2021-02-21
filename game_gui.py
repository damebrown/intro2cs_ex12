import tkinter as tk
from PIL import Image, ImageTk
import winsound as ws


class GUI:
    DELTA_ROW = 41
    DELTA_COL = 65
    X_MIN_LIMIT = 345
    X_MID_CORD = 375
    X_MAX_LIMIT = 800
    Y_MIN_LIMIT = 90
    Y_MID_CORD = 315
    Y_MAX_LIMIT = 340
    IMAGE_WIDTH = 1127
    IMAGE_HEIGHT = 579
    X_COL_VAR = 400
    Y_COL_VAR = 215

    def __init__(self, master):
        '''
        init function. monitors all of the root's main characteristics.
        '''
        self.root = master
        self.root.geometry("1127x579")
        self.root.resizable(False, False)
        self._col_lst = [None for _ in range(7)]
        self._game_over = False
        #sound initiations:

        self._lose_sound = lambda: ws.PlaySound('disqualified.wav',
                                                ws.SND_FILENAME|ws.SND_ASYNC)
        self._win_sound = lambda: ws.PlaySound('I_like_what_you_got.wav',
                                               ws.SND_FILENAME|ws.SND_ASYNC)
        self._game_sound = lambda: ws.PlaySound('get_schwifty_in_here.wav',
                                                ws.SND_LOOP|ws.SND_ASYNC)
        #all of the UI's image's path's;
        self.path = "tv.png"
        self.your_path = 'your.png'
        self.not_your_path = 'not_your.png'
        morty_path = 'morty.png'
        rick_path = 'rick.png'
        col_path = 'col_marker.png'
        win_path = 'win.png'
        lose_path = "lose.png"

        #initiation of all the images:
        self.win_img = ImageTk.PhotoImage(Image.open(win_path))
        self.lose_img = ImageTk.PhotoImage(Image.open(lose_path))
        self.bg_img = ImageTk.PhotoImage(Image.open(self.path))
        self.rick_img = ImageTk.PhotoImage(Image.open(rick_path))
        self.morty_img = ImageTk.PhotoImage(Image.open(morty_path))
        self.your_img = ImageTk.PhotoImage(Image.open(self.your_path))
        self.not_your_img = ImageTk.PhotoImage(Image.open(self.not_your_path))
        self.col_img = ImageTk.PhotoImage(Image.open(col_path))

        #canvas initiation:
        self._canvased = tk.Canvas(self.root, width=self.IMAGE_WIDTH,
                                   height=self.IMAGE_HEIGHT)
        #background image initiation:
        self._canvased.create_image(self.IMAGE_WIDTH / 2,
                                    self.IMAGE_HEIGHT / 2,
                                    image=self.bg_img)
        #bindings:
        self._canvased.bind('<Button-1>', self.mouse_click)
        self._canvased.bind('<Motion>', self.draw_col)
        self._canvased.pack()

    def get_col(self, event):
        '''
        getter function, returns the column in which the event occurred
        :param event: any event
        :return: the column in which the event occurred
        '''
        col = (event.x - self.X_MIN_LIMIT) // self.DELTA_COL
        return col

    def get_root(self):
        '''
        getter function, returns the tkinter root (GUI class instance).
        :return: a GUI class instance
        '''
        return self.root

    def set_isit_myturn(self, is_it_my_turn):
        '''
        setter function, receives 'is_it_my_turn' function from the main game
        file and makes it a method of the class so we are able to use it here.
        :param is_it_my_turn: the 'is_it_my_turn' function from the main game
        '''
        self._isit_myturn = is_it_my_turn

    def set_make_move(self, make_move):
        '''
        setter function, sets the class method of 'make_move'
        :param make_move: make_move function from the main game file
        '''
        self._make_move = make_move

    def start(self):
        '''
        this function runs the game as well as playing the main theme song
        '''
        if False:
            self._game_sound()
        self.root.mainloop()

    def mouse_click(self, event):
        '''
        this function is bound the the event of left mouse clicking. if the
        click is within the game area, it calls the make_move function with
        the relevant column as an argument.
        :param event: left mouse click
        '''
        #checks if the event occurred in the relevant area of the game
        if self.X_MIN_LIMIT < event.x < self.X_MAX_LIMIT and self.Y_MIN_LIMIT \
                < event.y < self.Y_MAX_LIMIT:
            #makes sure the game isn't over
            if self._isit_myturn() and not self._game_over:
                col = (event.x - self.X_MIN_LIMIT) // self.DELTA_COL
                #makes the move with the relevant column
                self._make_move(col)

    def draw_head(self, col, row, player):
        '''
        this function gets the player that made the move and the whereabouts
        of the move- row and column. the function creates an image of the
        player's head according to the above mentioned. after drawing, the
        function calls the 'turn_indication' function, which monitors the
        which-turn-is-it indication so it updates the indication.
        :param col: column of the move
        :param row: row of the move
        :param player: the player that made the move
        '''
        #if player is rick, draw rick's head in the relevant location:
        if not player:
            self._canvased.create_image(self.X_MID_CORD + col *
                                        self.DELTA_COL,
                                        self.Y_MID_CORD - row *
                                        self.DELTA_ROW,
                                        image=self.rick_img)
        #if player is morty, draw morty's head in the relevant location:
        else:
            self._canvased.create_image(self.X_MID_CORD + col *
                                        self.DELTA_COL,
                                        self.Y_MID_CORD - row *
                                        self.DELTA_ROW,
                                        image=self.morty_img)
        #turn indication will be updated:
        self.turn_indicator()

    def draw_col(self, event):
        '''
        this function is bound to mouse-motion inside the game area. it
        monitors the column indication -if needed, produces a new column
        indication, and deletes the indication for columns that are no longer
        relevant.
        :param event: the event of mouse motion on the screen
        '''
        # condition- if motion occurred in the game area
        if self.X_MIN_LIMIT < event.x < self.X_MAX_LIMIT and \
                                self.Y_MIN_LIMIT < event.y < self.Y_MAX_LIMIT:
            # checks on what column the motion occurred
            col = self.get_col(event)
            # checks that the current column indication doesn't exist
            # if it doesn't, it creates it:
            if not self._col_lst[col]:
                self._col_lst[col] = self._canvased.create_image(
                    self.X_MID_CORD + col * self.DELTA_COL, self.Y_COL_VAR,
                    image=self.col_img)
            # if it is, it checks that it is the only active indication
            for i in range(7):
                if i != col and self._col_lst[i]:
                    self._canvased.delete(self._col_lst[i])
                    self._col_lst[i] = None
        # if motion didn't occur in the game area, all indications are deleted
        else:
            for i in range(7):
                if self._col_lst[i]:
                    self._canvased.delete(self._col_lst[i])
                    self._col_lst[i] = None

    def turn_indicator(self):
        '''
        this function controls the whose-turn-is-it indication. it changes the
        indication according to the player.
        '''
        #if its the player's turn, show the 'your turn' indication
        if self._isit_myturn():
            self._canvased.create_image(self.IMAGE_WIDTH / 2,
                                        self.IMAGE_HEIGHT / 2,
                                        image=self.your_img)
        #if it is not the player's turn, show the 'not your turn' indication
        else:
            self._canvased.create_image(self.IMAGE_WIDTH / 2,
                                        self.IMAGE_HEIGHT / 2,
                                        image=self.not_your_img)

    def game_over(self, i_won):
        '''
        this function checks if a player has won of lost, shows
        the relevant win/lose visual indication and plays the relevant
        win/lose sounds according to the game state.
        :param i_won: the winning indication from the main game file
        '''
        self._game_over = True
        #if a player has won:
        if i_won:
            #shows the back round that indicates the victory
            self._canvased.create_image(self.IMAGE_WIDTH / 2,
                                        self.IMAGE_HEIGHT / 2,
                                        image=self.win_img)
            # plays the victorious sound, 'I like what you have got'
            self._win_sound()
        #if it didn't:
        else:
            #shows the back round that indicates the loss
            self._canvased.create_image(self.IMAGE_WIDTH / 2,
                                        self.IMAGE_HEIGHT / 2,
                                        image=self.lose_img)
            #plays the losing sound, 'disqualified'
            self._lose_sound()


# TODO winning quadret indication
# TODO sound- SHOW ME WHAT YOU'VE GOT
# TODO sound- long theme song
