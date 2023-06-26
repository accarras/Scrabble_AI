import numpy
import random
from operator import itemgetter

class Player(object):

    def __init__(self):
        self.rack = [] #Fill rack with 7 letters from tile bag
        self.points = 0
        self.scoreDict = {'b': 3, 's': 1, 'd': 2, 'v': 4, 'j': 8, 'w': 4, 
                          'x': 8, 'u': 1, 'z': 10, 'p': 3, 'o': 1, 'm': 3,
                          'c': 3, 'l': 1, 'e': 1, 'r': 1, 'g': 2, 'f': 4,
                          'k': 5, 'y': 4, 'i': 1, 't': 1, 'a': 1, 'n': 1, 'h': 4, 'q' : 10}

    def removeTiles(self, move):
        #Removes correct tiles after move is made.
        for i in range(len(move[0])):
            if not i in move[2]:
                self.rack.remove(move[0][i])
    def validTiles(self, move):
        #Check if player has tiles to make move.
        boardLetters = [move[0][i] for i in move[2]]
        
        
        for letter in set(move[0]):
            #Second condition is to account for the tile(s) that are already on the board that
            #they don't need to have in their rack. This will also need to account for *
            #tiles which grant no points but count as any letter.
            if (move[0].count(letter) > self.rack.count(letter)) and (move[0].count(letter) - boardLetters.count(letter) > self.rack.count(letter)):
                if (move[0].count(letter) > self.rack.count(letter)):
                    pass
                    #print("Not enough in rack.")
                    #print("Rack:", self.rack)
                    #print("Word:", move[0])
                else:
                    pass
                    #print("Not enough in board + rack")
                return False
            
        return True
    def drawTiles(self, board):
        #draws correct number of tiles from bag
        missingTileCount = 7 - len(self.rack)
        
        if missingTileCount > 0:
            for i in range(missingTileCount):
                if board.tileBag:
                    self.rack.append(board.tileBag.pop())
                    
    def heuristic(self, move):
        #Maybe factor in getting the most value
        #out of the last of a vowel or other valuable
        #letter. Like a 4 letter word for the last of
        #a tile will be scored much higher than a 3
        #letter word so the tile isn't wasted.

        #Possibly 

        moveScore = getMoveScore(move) + len(move[0]-len(move[2]))*2
        

        

        return moveScore

    def testMove(self, move, board):
        #Get variables to reset to
        oldEmpty = board.boardIsEmpty
        oldPoints = self.points
        oldPlayer = board.currentPlayer
        oldRack = self.rack.copy()
        oldBoard = board.board.copy()
        oldTiles = board.tileBag.copy()

        #Make move
        tryMove = board.makeMove(move)

        #Undo move
        board.board = oldBoard
        self.rack = oldRack
        self.points = oldPoints
        board.currentPlayer = oldPlayer
        board.tileBag = oldTiles
        if oldEmpty == True:
            board.boardIsEmpty = True

        #If the move worked return true, else false.
        if tryMove:
            return True
        else:
            return False
        
    
    def addMoveScore(self, move, board, oldBoardWords):
        #Gives player points for current move.
        self.points += self.getMoveScore(move, board, oldBoardWords)
        

    def getMoveScore(self, move, board, oldBoardWords):
        points = 0

        for letter in move[0]:
            points += self.scoreDict[letter]

        #print(move[0],", ", self.points)
        newExtraWords = []

        for word in board.boardWords:
            #The first set of conditions grabs all the new unique words or each new instance of an existing word.
            #The second set of conditions after the and is to catch the case that the word is the same as move[0].

            #I am not 100% sure why you need to subtract 1 from the counts but you do and it works.
            if (word not in oldBoardWords or board.boardWords.count(word)-oldBoardWords.count(word)-1 > newExtraWords.count(word))and\
            (word != move[0] or board.boardWords.count(word)-oldBoardWords.count(word)-1 > newExtraWords.count(word)):
                newExtraWords.append(word)
        #print("New extra words:", newExtraWords)
        
        for word in newExtraWords:
            for letter in word:
                points += self.scoreDict[letter]
        
##            if move[0][i] in ["d", "g"]:
##                points += 2
##            elif move[0][i] in ["b", "c", "m", "p"]:
##                points += 3
##            elif move[0][i] in ["f", "h", "v", "w", "y"]:
##                points += 4
##            elif move[0][i] == "k":
##                points += 5
##            elif move[0][i] in ["j", "x"]:
##                points += 8
##            elif move[0][i] in ["q", "z"]:
##                points += 10
##            else:
##                points += 1

        return points
            
    def findMoves(self, board, limit):
        #Need to get something like 100 moves
        #for each player using makeMove then remove
        #the move after and this should return the list
        #of moves for both.
        moves = []

        #word is the word to be played

        #firstLetterCoOrds is a tuple of the board position
        #where the first letter of the word should be played.

        #intersectIndexes is a list of the indexes in the word already on
        #the board. These should be skipped when scoring the word.
        
        #orientation is left to right, or top to bottom. Could be
        #represented by r and d for right and down.

        if not board.boardIsEmpty:
            #Letters sorted by score low to high.
            letters = [letter[0] for letter in sorted(list(self.scoreDict.items()), key = itemgetter(1))]
            test = 0
            while True:
                #If the number of moves is at the limit
                #try making every move. If any move can't
                #be made because it's invalid, remove the
                #move from the list of moves. If no moves
                #were removed end the loop. (This is where
                #dynamic programming would be helpful so we
                #have a list of already validated moves and
                #it only checks each move once.)
                
                if len(moves) >= limit or not letters:
##                    print("Not first: None left or hit limit")
##                    for move in moves:
##                        testMove = self.testMove(move, board)
##                        if not testMove:
##                            moves.remove(move)
 
                    if len(moves) >= limit or not letters:
                        break

                #Gets the highest value letter of the end of letters.
                letter = letters.pop()
                
                letterBoardCoOrds = []
                
                
                #Gets the position of every tile on the board with the current letter
                for i in range(len(board.board)):
                    for j in range(len(board.board[i])):
                        if int(board.board[i][j]) and board.letNumConvert(int(board.board[i][j])) == letter:
                            letterBoardCoOrds.append((j,i))
                print(letter, letterBoardCoOrds)

                #Everything in this if statement runs if there are already words in the board.
                if letterBoardCoOrds:
                    #Gets every word with the current letter in it where the player
                    #has the rest of the letters of the word in their rack. (I verified
                    #that it does this properly)
                    words = [word for word in board.dictionary if letter in word and \
                            len([char for char in \
                             [word[i] for i in range(len(word)) if not word.index(letter)==i] \
                             if self.rack.count(char) >= \
                             [word[i] for i in range(len(word)) if not word.index(letter)==i].count(char)]) == len(word)-1]

                    #Goes through every tile on the board with the current letter
                    for coOrds in letterBoardCoOrds:
                        emptyLeft = 0
                        lookLeft = True
                        
                        emptyRight = 0
                        lookRight = True
                        
                        emptyDown = 0
                        lookDown = True
                        
                        emptyUp = 0
                        lookUp = True

                        
                        row = coOrds[1]
                        col = coOrds[0]
                        #Gets a count of empty spaces around the current tile.
                        for i in range(4):
                            offset = i+1

                            if not (col - offset) < 0 and not board.board[row][col-offset] and lookLeft:
                               emptyLeft += 1
                            else:
                                lookLeft = False
                                
                            if not (col + offset) > board.width-1 and not board.board[row][col+offset] and lookRight:
                                emptyRight += 1
                            else:
                                lookRight = False
                                
                            if not (row + offset) > board.height-1 and not board.board[row+offset][col] and lookDown:
                                emptyDown += 1
                            else:
                                lookDown = False
                                
                            if not (row - offset) < 0 and not board.board[row-offset][col] and lookUp:
                                emptyUp += 1
                            else:
                                lookUp = False

                        #Now it needs to go through possible placements of each word given
                        #the current tile co ords and surrounding empty spaces. Each valid
                        #move should be saved up to a limit. When the limit is reached,
                        #the while loop should break.

                        for word in words:
                            length = len(word)

                            #List of possible letter intersection indexes.
                            letIs = []
                            for i in range(len(word)):
                                if word[i] == letter:
                                    letIs.append(i)
                            
                            for i in letIs:
                                    
                                if length == 2:
                                    if i == 0:
                                        if emptyLeft >= 1 and emptyRight >= 2:
                                            #(word, coOrds, [i], "r")
                                            move = (word, coOrds, [i], "r")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                        if emptyDown >= 2 and emptyUp >= 1:
                                            #moves.append((word, coOrds, [i], "d"))
                                            move = (word, coOrds, [i], "d")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                    elif i == 1:
                                        if emptyLeft >= 2 and emptyRight >= 1:
                                            #moves.append((word, (col-i, row), [i], "r"))
                                            move = (word, (col-i, row), [i], "r")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                        if emptyDown >= 1 and emptyUp >= 2:
                                            #moves.append((word, (col, row-i), [i], "d"))
                                            move = (word, (col, row-i), [i], "d")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                            
                                elif length == 3:
                                    if i == 0:
                                        if emptyLeft >= 1 and emptyRight >= 3:
                                            #moves.append((word, coOrds, [i], "r"))
                                            move = (word, coOrds, [i], "r")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                        if emptyDown >= 3 and emptyUp >= 1:
                                            #moves.append((word, (col, row-i), [i], "d"))
                                            move = (word, (col, row-i), [i], "d")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                    elif i == 1:
                                        if emptyLeft >= 2 and emptyRight >= 2:
                                            #moves.append((word, (col-i, row), [i], "r"))
                                            move = (word, (col-i, row), [i], "r")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                        if emptyDown >= 2 and emptyUp >= 2:
                                            #moves.append((word, (col, row-i), [i], "d"))
                                            move = (word, (col, row-i), [i], "d")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                    elif i == 2:
                                        if emptyLeft >= 3 and emptyRight >= 1:
                                            #moves.append((word, (col-i, row), [i], "r"))
                                            move = (word, (col-i, row), [i], "r")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                        if emptyDown >= 1 and emptyUp >= 3:
                                            #moves.append((word, (col, row-i), [i], "d"))
                                            move = (word, (col, row-i), [i], "d")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                            
                                elif length == 4:
                                    if i == 0:
                                        if emptyLeft >= 1 and emptyRight >= 4:
                                            #moves.append((word, coOrds, [i], "r"))
                                            move = (word, coOrds, [i], "r")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                        if emptyDown >= 4 and emptyUp >= 1:
                                            #moves.append((word, (col, row-i), [i], "d"))
                                            move = (word, (col, row-i), [i], "d")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                    elif i == 1:
                                        if emptyLeft >= 2 and emptyRight >= 3:
                                            #moves.append((word, (col-i, row), [i], "r"))
                                            move = (word, (col-i, row), [i], "r")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                        if emptyDown >= 3 and emptyUp >= 2:
                                            #moves.append((word, (col, row-i), [i], "d"))
                                            move = (word, (col, row-i), [i], "d")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                    elif i == 2:
                                        if emptyLeft >= 3 and emptyRight >= 2:
                                            #moves.append((word, (col-i, row), [i], "r"))
                                            move = (word, (col-i, row), [i], "r")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                        if emptyDown >= 2 and emptyUp >= 3:
                                            #moves.append((word, (col, row-i), [i], "d"))
                                            move = (word, (col, row-i), [i], "d")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                    elif i == 3:
                                        if emptyLeft >= 4 and emptyRight >= 1:
                                            #moves.append((word, (col-i, row), [i], "r"))
                                            move = (word, (col-i, row), [i], "r")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)
                                        if emptyDown >= 1 and emptyUp >= 4:
                                            #moves.append((word, (col, row-i), [i], "d"))
                                            move = (word, (col, row-i), [i], "d")
                                            testMove = self.testMove(move, board)
                                            if testMove:
                                                moves.append(move)

        #If the board is empty our pool of letters is always just the rack.
        #So we just go through and get every move where we have the letters
        #and the first letter is in the middle.
        else:
            letters = [letter[0] for letter in sorted(list(self.scoreDict.items()), key = itemgetter(1)) if letter[0] in self.rack]
            test = 0
            while True:
                
                if len(moves) >= limit or not letters:
                    print("First move: None left or hit limit")
##                  for move in moves:
##                        if not self.testMove(move, board):
##                            moves.remove(move)
## 
                    if len(moves) >= limit or not letters:
                        break
                
                letter = letters.pop()

                words = [word for word in board.dictionary if letter in word and\
                         len([char for char in word if self.rack.count(char) >= list(word).count(char)]) == len(word)]

                for word in words:

                    if board.width % 2 == 1:
                        #moves.append((word, (int((board.height-1)/2), int((board.width-1)/2)), [], "r"))
                        #moves.append((word, (int((board.height-1)/2), int((board.width-1)/2)), [], "d"))
                        moveR = (word, (int((board.height-1)/2), int((board.width-1)/2)), [], "r")
                        moveD = (word, (int((board.height-1)/2), int((board.width-1)/2)), [], "d")
                        testMoveR = self.testMove(moveR, board)
                        testMoveD = self.testMove(moveD, board)
                        if testMoveR:
                            moves.append(moveR)
                        if testMoveD:
                            moves.append(moveD)
                    else:
                        #moves.append((word, (int((board.height)/2), int((board.width)/2)), [], "r"))
                        #moves.append((word, (int((board.height)/2), int((board.width)/2)), [], "d"))
                        moveR = (word, (int((board.height)/2), int((board.width)/2)), [], "r")
                        moveD = (word, (int((board.height)/2), int((board.width)/2)), [], "d")
                        testMoveR = self.testMove(moveR, board)
                        testMoveD = self.testMove(moveD, board)
                        if testMoveR:
                            moves.append(moveR)
                        if testMoveD:
                            moves.append(moveD)
                        
        print("Moves at return:", moves)
        return moves

    def miniMax(self, board, depth, player):
        #Should make one move for current player (max) on
        #board copy and then make one move for min based on
        #the new board. Add these together with the score for
        #max being positive and the score for min being negative.
        #Extra points should be added based on the length of the
        #word.
        
        initial = board.gameOver()
        if initial == 0:
            return 0, -1
        elif initial == board.players[0]:
            return math.inf, -1
        elif initial == board.players[1]:
            return -math.inf, -1
        if depth == 0:
            return self.heuristic(board), -1

        bestMove = -1

        if player == board.players[0]:
            bestValue = -math.inf
            for chld in board.children():
                move, child = chld
                value = self.miniMax(child, depth-1, board.players[1])[0]
                if value >= bestValue:
                    bestValue = value
                    bestMove = move
            return bestValue, bestMove

        else:
            bestValue = math.inf
            for chld in board.children():
                move, child = chld
                value = self.miniMax(child, depth-1, board.players[0])[0]
                if value <= bestValue:
                    bestValue = value
                    bestMove = move
            return bestValue, bestMove
