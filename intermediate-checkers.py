from tkinter import *
from tkinter import messagebox

class CheckersBoard:
    '''represents a board of Checkers'''

    def __init__(self):
        '''CheckersBoard()
        creates a Checkersboard in starting position'''
        self.board = {} #dict to store position
        #create opening position
        for row in range(8):
            for column in range(8):
                coords = (row, column)
                if row%2 == 0 and row < 3:
                    if column%2 == 1:
                        self.board[coords] = 0
                    else:
                        self.board[coords] = None
                elif row%2 == 1 and row < 3:
                    if column%2 == 0:
                        self.board[coords] = 0
                    else:
                        self.board[coords] = None
                elif row%2 == 0 and row > 4:
                    if column%2 == 1:
                        self.board[coords] = 1
                    else:
                        self.board[coords] = None
                elif row%2 == 1 and row > 4:
                    if column%2 == 0:
                        self.board[coords] = 1
                    else:
                        self.board[coords] = None
                else:
                    self.board[coords] = None #empty
        self.currentPlayer = 0

    def get_piece(self,coords):
        '''CheckersBoard.get_piece(coords) -> int
        returns the piece at coords'''
        return self.board[coords]

    def get_player(self):
        '''CheckersBoard.get_player() -> int
        returns the current player'''
        return self.currentPlayer

    def get_legal_moves(self,coords,ifKing):
        '''CheckersBoard.get_legal_moves() -> (list,str)
        returns a list of the current player's legal moves'''
        legalMovesJump = []
        row = coords[0]
        column = coords[1]
        if self.board[coords] == 0 or ifKing == True: #going backwards
            if column+2 <= 7 and row+2 <= 7:
                if self.board[(row+1,column+1)] == 1-self.currentPlayer:#check opponent piece
                    if self.board[(row+2,column+2)] == None: 
                        legalMovesJump.append((row+2,column+2))
            if column-2 >= 0 and row+2 <= 7:
                if self.board[(row+1,column-1)] == 1-self.currentPlayer:#check opponent piece
                    if self.board[(row+2,column-2)] == None:
                        legalMovesJump.append((row+2,column-2))
        if self.board[coords] == 1 or ifKing == True: #going forwards
            if column+2 <= 7 and row-2 >= 0:
                if self.board[(row-1,column+1)] == 1-self.currentPlayer:#check opponent piece
                    if self.board[(row-2,column+2)] == None:
                        legalMovesJump.append((row-2,column+2))
            if column-2 >= 0 and row-2 >= 0:
                if self.board[(row-1,column-1)] == 1-self.currentPlayer:#check opponent piece
                    if self.board[(row-2,column-2)] == None:
                        legalMovesJump.append((row-2,column-2))
        return (legalMovesJump, 'Jump')

    def get_legal_walks(self,coords,ifKing):
        '''CheckersBoard.get_legal_moves() -> (list,str)
        returns a list of the current player's legal moves'''
        legalMovesWalk = []
        row = coords[0]
        column = coords[1]
        if self.board[coords] == 0 or ifKing == True: #walking backwards
            if column+1 <= 7 and row+1 <= 7:
                if self.board[(row+1,column+1)] == None:
                    legalMovesWalk.append((row+1,column+1))
            if column-1 >= 0 and row+1 <= 7:
                if self.board[(row+1,column-1)] == None:
                    legalMovesWalk.append((row+1,column-1))
        if self.board[coords] == 1 or ifKing == True: #walking forwards
            if column+1 <= 7 and row-1 >= 0:
                if self.board[(row-1,column+1)] == None:
                    legalMovesWalk.append((row-1,column+1))
            if column-1 >= 0 and row-1 >= 0:
                if self.board[(row-1,column-1)] == None:
                    legalMovesWalk.append((row-1,column-1))
        return (legalMovesWalk, 'Walk')

    def check_canJump(self,coords,squaresDict):
        '''CheckersBoard.check_canJump(coords,squaresDict)
        check the color is able to jump at all'''
        numPiece = 0
        color = self.board[coords]
        colorPlace = []
        for r in range(8):
            for c in range(8):
                if self.board[(r,c)] == color:#get all coords of the same color
                    colorPlace.append((r,c))
        for piece in colorPlace:
            ifKing = squaresDict[piece].isKing
            if len(self.get_legal_moves(piece,ifKing)[0]) != 0:
                return True #if any can jump return True
        return False #if none can jump return False

    def piece_walk(self,originalCoord,newCoord):
        '''CheckersBoard.change_board(originalCoord,newCoord)
        move the piece from originalCoord to newCoord'''
        self.board[newCoord] = self.board[originalCoord]
        self.board[originalCoord] = None

    def piece_jump(self,originalCoord,newCoord):
        '''CheckersBoard.change_board(originalCoord,newCoord)
        piece jump from originalCoord to newCoord
        remove opponent piece in middle'''
        self.board[newCoord] = self.board[originalCoord]
        self.board[originalCoord] = None
        row = (newCoord[0] + originalCoord[0])/2 #get middle piece coord
        column = (newCoord[1] + originalCoord[1])/2
        self.board[(row,column)] = None #remove middle piece

    def change_player(self):
        '''CheckersBoard.change_player()
        move to next player'''
        self.currentPlayer = 1-self.currentPlayer

    def check_ifEnd(self,squaresDict):
        '''CheckersBoard.check_ifEnd(squaresDict) -> tuple
        check if any of the two colors is unable to move'''
        canMoveRed = False
        canMoveWhite = False
        numPiece = 0
        colorPlaceRed = []
        colorPlaceWhite = []
        for r in range(8):
            for c in range(8):
                if self.board[(r,c)] == 0:
                    colorPlaceRed.append((r,c)) #get all red piece coords
                elif self.board[(r,c)] == 1:
                    colorPlaceWhite.append((r,c)) #get all white piece coords
        for piece in colorPlaceRed:
            ifKing = squaresDict[piece].isKing
            if len(self.get_legal_moves(piece,ifKing)[0]) != 0:
                canMoveRed = True #if any can jump return True
                break
            if len(self.get_legal_walks(piece,ifKing)[0]) != 0:
                canMoveRed = True #if any can jump return True
                break
        for piece in colorPlaceWhite:
            ifKing = squaresDict[piece].isKing
            if len(self.get_legal_moves(piece,ifKing)[0]) != 0:
                canMoveWhite = True #if any can jump return True
                break
            if len(self.get_legal_walks(piece,ifKing)[0]) != 0:
                canMoveWhite = True #if any can jump return True
                break
        return (canMoveRed,canMoveWhite)
        
class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''

    def __init__(self,master,r,c):
        '''CheckersSquare(master,r,c)
        creates a new blank Checkers square at coordinate (r,c)'''
        #create and place the widget
        if r%2 == 0:
            if c%2 == 1:
                Canvas.__init__(self,master,width=50,height=50,bg='dark green')
                self.grid(row=r,column=c)
            else:
                Canvas.__init__(self,master,width=50,height=50,bg='blanched almond')
                self.grid(row=r,column=c)
        else:
            if c%2 == 0:
                Canvas.__init__(self,master,width=50,height=50,bg='dark green')
                self.grid(row=r,column=c)
            else:
                Canvas.__init__(self,master,width=50,height=50,bg='blanched almond')
                self.grid(row=r,column=c)
        #set the attributes
        self.position = (r,c)
        self.isKing = False
        #bind button click to placing a piece
        self.bind('<Button>',self.master.get_click)

    def get_position(self):
        '''CheckersSquare.get_position() -> (int,int)
        returns (row,column) of square'''
        return self.position

    def make_color(self,color):
        '''CheckersSquare.make_color(color)
        changes color of piece on sqare to specified color'''
        ovalList = self.find_all()
        for oval in ovalList: #remove existing piece first
            self.delete(oval)
        self.create_oval(10,10,44,44,fill=color)

    def make_king(self):
        '''CheckersSquare.make_color(color)
        changes color of piece on sqare to specified color and add asterisk'''
        self.create_text(27.25,37,text="*",font=('Arial',32))

    def remove_piece(self):
        '''CheckersSquare.remove_piece()
        remove piece from a specific square'''
        ovalList = self.find_all()
        for oval in ovalList:
            self.delete(oval)

class CheckersGame(Frame):
    '''represents a game of Checkers'''

    def __init__(self,master):
        '''CheckersGame(master,[computerPlayer])
        creates a new Checkers game'''
        #initialize the Frame
        Frame.__init__(self,master,bg='white')
        self.grid()
        #set up game data
        self.colors = ('red','white') #players' colors
        self.JumpInProgress = False
        #create board in starting position, player 0 going first
        self.board = CheckersBoard()
        self.squares = {}
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                self.squares[rc] = CheckersSquare(self,row,column)
        self.rowconfigure(8,minsize=3) #leave a little space
        #create indicator squares
        self.turnLabel = (Label(self,text='Turn:',font=('FreeMono',15),bg='white'))
        self.turnLabel.grid(row=9,column=1)
        self.jumpLabel = (Label(self,text='',font=('FreeMono',15),bg='white'))
        self.jumpLabel.grid(row=9,column=3,columnspan=4)
        self.squares[(9,2)] = CheckersSquare(self,9,2)
        self.squares[(9,2)]['bg'] = 'gray70'
        self.squares[(9,2)].make_color(self.colors[0]) #Player 1 plays first
        self.update_display()

    def update_display(self):
        '''CheckersGame.update_display()
        updates squares to match board'''
        #update squares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                piece = self.board.get_piece(rc)
                if piece == 0 or piece == 1:
                    self.squares[rc].make_color(self.colors[piece])
                    if self.squares[rc].isKing == True:
                        self.squares[rc].make_king()
                else:
                    self.squares[rc].remove_piece()
        #update the turn indicator
        self.player = self.board.get_player()
        self.squares[(9,2)].make_color(self.colors[self.player])

    def get_click(self,event):
        '''CheckersGame.get_click(event)
        event handler for mouse click
        gets click data and checks legal moves'''
        coords = event.widget.get_position()
        self.coords = coords
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                self.squares[rc]['highlightbackground'] = 'white'
        if self.board.check_canJump(coords, self.squares) == True: #if any of the same color can jump have to jump
            legalMoves = self.board.get_legal_moves(coords,self.squares[coords].isKing)
        else: #if none of the same color can jump can walk
            legalMoves = self.board.get_legal_walks(coords,self.squares[coords].isKing)
        if self.board.get_piece(coords) == self.player and len(legalMoves[0]) != 0: #make sure the piece can move
            self.squares[coords]['highlightbackground'] = 'black'
            for squareCoord in legalMoves[0]:
                self.squares[squareCoord].bind('<Button>',self.move_piece)
                if legalMoves[1] == 'Jump':
                    self.JumpInProgress = True

    def move_piece(self,event):
        '''CheckersGame.move_piece(event)
        event handler for mouse clicks
        move the piece to corresponding square'''
        self.jumpLabel['text'] = ''
        coords = event.widget.get_position() #get new position
        #move piece
        if self.JumpInProgress == False:
            self.board.piece_walk(self.coords,coords)
        else:
            self.board.piece_jump(self.coords,coords)
            self.squares[(self.coords[0]+coords[0])//2,(self.coords[1]+coords[1])//2].isKing = False #eaten piece cannot be king
        if self.squares[self.coords].isKing == True:
            self.squares[coords].isKing = True
            self.squares[self.coords].isKing = False
        self.squares[self.coords]['highlightbackground'] = 'white' #change background highlight
        self.squares[coords]['highlightbackground'] = 'black'
        for r in range(8): #make sure nobody is binded with self.move_piece
            for c in range(8):
                rc = (r,c)
                self.squares[rc].unbind('<Button>')
                self.squares[rc].bind('<Button>',self.get_click)
        if coords[0] != 0 or coords[0] != 7:
            if self.JumpInProgress == False: #if first step was walk
                self.board.change_player()
            elif self.JumpInProgress == True:
                legalMoves = self.board.get_legal_moves(coords,self.squares[coords].isKing)
                if len(legalMoves[0]) != 0: #continuous jump
                    self.jumpLabel['text'] = '  Must continue jump!'
                    for squareCoord in legalMoves[0]:
                        self.coords = coords
                        self.squares[squareCoord].bind('<Button>',self.move_piece)
                else: #if no continuous jump
                    self.JumpInProgress = False
                    self.board.change_player()
        if coords[0] == 0 or coords[0] == 7:
            self.squares[coords].isKing = True
        self.update_display()
        self.check_endgame()

    def check_endgame(self):
        '''CheckersGame.check_endgame(self)
        check if game ends and print things accordingly'''
        movesLeft = self.board.check_ifEnd(self.squares)
        if movesLeft[0] == False:
            messagebox.showinfo('Checkers','White wins the game',parent=self)
            for r in range(8): #make sure nobody is binded with self.move_piece
                for c in range(8):
                    self.squares[(r,c)].unbind('<Button>')
        if movesLeft[1] == False:
            messagebox.showinfo('Checkers','Red wins the game!',parent=self)
            for r in range(8): #make sure nobody is binded with self.move_piece
                for c in range(8):
                    self.squares[(r,c)].unbind('<Button>')
                    
def play_checkers():
    '''play_checkers()
    starts a new game of Checkers'''
    root = Tk()
    root.title('Checkers')
    CG = CheckersGame(root)
    CG.mainloop()

play_checkers()
