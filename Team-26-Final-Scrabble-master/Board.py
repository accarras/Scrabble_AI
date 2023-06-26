import numpy
import random

class Board(object):

    def __init__(self, height, width, players, dictionary):
        self.height = height
        self.width = width
        self.dictionary = dictionary
        self.players = [player for player in players]
        self.currentPlayer = self.players[0]
        self.boardWords = []
        self.bwOld = []
        self.boardIsEmpty = True
        self.boardOld = None
        self.cantMove = 0
        

        self.tileBag = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',
                        'b', 'b',
                        'c', 'c',
                        'd', 'd', 'd', 'd',
                        'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e',
                        'f', 'f',
                        'g', 'g', 'g',
                        'h', 'h',
                        'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i',
                        'j',
                        'k',
                        'l', 'l', 'l', 'l',
                        'm', 'm',
                        'n', 'n', 'n', 'n', 'n', 'n',
                        'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o',
                        'p', 'p',
                        'q',
                        'r', 'r', 'r', 'r', 'r', 'r',
                        's', 's', 's', 's',
                        't', 't', 't', 't', 't', 't',
                        'u', 'u', 'u', 'u',
                        'v', 'v',
                        'w', 'w',
                        'x',
                        'y', 'y',
                        'z']
        
        random.shuffle(self.tileBag)

        

        #Board built here.
        self.board = numpy.zeros([self.width, self.height], int)
        
    def letNumConvert(self, char):
        letToNumDict = {"a":1, "b":2, "c":3, "d":4,"e":5, "f":6,"g":7, "h":8,
                        "i":9, "j":10, "k":11, "l":12,"m":13, "n":14,"o":15,
                        "p":16, "q":17, "r":18, "s":19,"t":20, "u":21,"v":22,
                        "w":23, "x":24, "y":25, "z":26}
        
        numToLetDict = {num:let for let,num in list(letToNumDict.items())}
        
        if type(char) == int:
            return numToLetDict[char]
        elif type(char) == str:
            return letToNumDict[char]
        
    def nextPlayer(self):
##        pIndex = self.players.index(self.currentPlayer)
##
##        if pIndex < len(self.players) - 1:
##            self.currentPlayer = self.players[pIndex + 1]
##        else:
##            self.currentPlayer = self.players[0]
        if self.currentPlayer == self.players[0]:
            self.currentPlayer = self.players[1]
        else:
            self.currentPlayer = self.players[0]

    def updateWords(self):
        #Needs to get every word currently on the board.
        #To make this faster it should store the words in
        #a list so it doesn't have to iterate over everything
        #multiple times.

        #Gets horizontal words. 
        for i in range(len(self.board)):
            word = ""
            for j in range(len(self.board[i])):
                if self.board[i][j]:
                    word += self.letNumConvert(int(self.board[i][j]))
                    if j == self.width-1 and len(word) > 1:
                        self.boardWords.append(word)
                        word = ""
                elif word and len(word) > 1: #and word not in self.boardWords removed
                                             #so you get a correct count of duplicate words.
                    #When it gets to a 0 but some letters have been
                    #added to word then it adds the word to the list and
                    #resets the variable.
                    self.boardWords.append(word)
                    word = ""
                else:
                    #If there's a 0 and either the word is already in the
                    #list or the variable is blank just reset the variable.
                    word = ""
                    
        #Gets vertical words
        #Currently adding some words twice.
        for i in range(len(self.board)):
            word = ""
            colList = [self.board[j][i] for j in range(self.height)]
            for j in range(len(colList)):
                #print(len(colList))
                #print("Letter:", letter)
                
                if colList[j]:
                    #print(letter)
                    word += self.letNumConvert(int(colList[j]))
                    if j == self.height-1 and len(word) > 1:
                        self.boardWords.append(word)
                        word = ""
                    #print("Word:", word)
                    #print("Word not in list:", word not in self.boardWords)
                    #print(word)
                elif word and len(word) > 1:#and word not in self.boardWords removed
                                            #so you get a correct count of duplicate words.
                    #When it gets to a 0 but some letters have been
                    #added to word then it adds the word to the list and
                    #resets the variable.
                    self.boardWords.append(word)
                    word = ""
                else:
                    #If there's a 0 and either the word is already in the
                    #list or the variable is blank just reset the variable.
                    #if word in self.boardWords:
                        #print("No:", word)
                    word = ""
        #print(self.boardWords)

    def isEmptyTile(self, coord, board):
        return board[(coord[1])][(coord[0])] == 0


    
    def isValid(self, move, oldBoard): #Make sure to account for human players messing things up

   #TODO:#Still needs to check that unless the board is empty the word is
         #being played off of another word.
        if not self.boardIsEmpty:
            if len(move[2]) == 0:
                #print("Move must intersect another word.")
                return False
         #Also need to make sure the word isn't replacing any letters in
         #another word.
            for i in range(len(move[0])):
                if move[3] == "r":
                    if not self.isEmptyTile(((move[1][0]+i),(move[1][1])), oldBoard) and not i in move[2]:
                        #print("Move would be played on top of an existing word.")
                        return False
                if move[3] =="d":
                    if not self.isEmptyTile(((move[1][0]),(move[1][1]+i)), oldBoard) and not i in move[2]:
                        #print("Move would be played on top of an existing word.")
                        return False

        
        if move[0] in self.dictionary and self.currentPlayer.validTiles(move):
            #This is inefficient right now. It checks
            #the same words over and over again.
            for word in self.boardWords:
                if word not in self.dictionary and len(word) > 1:
                    #print("Move makes invalid word: ", word)
                    return False
        else:
            if not move[0] in self.dictionary:
                pass
                #print("Not in dict.")
            if not self.currentPlayer.validTiles(move):
                pass
                #print("Invalid tiles.")
            #print("You can't play that word.")
            return False

        #print("Word played:", move[0])
        self.boardIsEmpty = False
        return True
        
    def makeMove(self, move):
        if move != -1:
            
            #print(move)
            posCol = move[1][0]
            posRow = move[1][1]

            #Get current words on the board.
            self.updateWords()
            
            #Copy board to revert to if move invalid.
            self.boardOld = self.board.copy()
            
            #Change board
            for i in range(len(move[0])):
                if i not in move[2]:
                    self.board[posRow][posCol] = self.letNumConvert(move[0][i])
                if move[3] == "r":
                    posCol += 1
                else:
                    posRow += 1
                
            #Copy list of current words to check against.
            self.bwOld = self.boardWords.copy()
            
            #Update word list so isValid can check that the move does not make illegal words.
            self.boardWords = []
            self.updateWords()

            #If it is, run the player functions.
            if self.isValid(move, self.boardOld):
                self.cantMove = 0
                self.currentPlayer.removeTiles(move)
                self.currentPlayer.drawTiles(self)
                self.currentPlayer.addMoveScore(move, self, self.bwOld)
                self.nextPlayer()
            else:
                #Revert board if move invalid.
                self.board = self.boardOld.copy()
                self.boardWords = []
                return False

            #Resets the list of words in the board. This will force it to get the list
            #of words all over again every time a move is made but not doing this makes it
            #break some things. Hopefully this fixes it.
            self.boardWords = []
            #self.boardOld = self.board.copy()
            return True
        else:
            self.nextPlayer()
            self.cantMove += 1
            #print("test:", self.cantMove)
            #print("One player no moves")
            return False
            
    def gameOver(self):
        if not self.tileBag or self.cantMove == 2:
            #Game ends when one player runs out of tiles or no one can make move.
            for player in self.players:
                #Don't run this every time use the else in makeMove
                if not player.rack or self.cantMove == 2:
                    if self.players[0].points > self.players[1].points:
                        print(self)
                        print("Player 1 won!")
                        print("Final Scores:")
                        print("    Player 1:", self.players[0].points)
                        print("    Player 2:", self.players[1].points)
                        return 1
                    if self.players[1].points > self.players[0].points:
                        print(self)
                        print("Player 2 won!")
                        print("Final Scores:")
                        print("    Player 1:", self.players[0].points)
                        print("    Player 2:", self.players[1].points)
                        return -1
                    else:
                        print(self)
                        print("It's a draw.")
                        print("Final Scores:")
                        print("    Player 1:", self.players[0].points)
                        print("    Player 2:", self.players[1].points)
                        return 0
        return 2
        

    
    #Turns board into string.
    def __str__(self):
        bString = "---"*(self.width + (self.width//2)-1)
        if self.width % 3 == 0:
            bString = bString[:-2]
        elif self.width % 2 == 1:
            bString += "--"
        bString += "\n"
        for i in range(self.height):
            row = i
            
            
            for j in range(self.width):
                col = j
                if self.isEmptyTile((col, row), self.board):
                    tile = " "
                else:
                    tile = self.letNumConvert(int(self.board[row][col]))
                bString += "| " + tile + " "
            bString += "|\n" + "---"*(self.width+ (self.width//2)-1)
            if self.width % 3 == 0:
                bString = bString[:-2]
            elif self.width % 2 == 1:
                bString += "--"
            bString += "\n"
        return bString
                



