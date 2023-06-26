from Board import Board
from Player import Player
import random


def playMiniMax(board, limit):
    board.players[0].drawTiles(board)
    board.players[1].drawTiles(board)
    while True:
        gameOver = board.gameOver()
        if gameOver in [-1, 1, 0]:
            break
        move = board.currentPlayer.miniMax(board, board.currentPlayer, limit)[1]
        print(move)
        board.makeMove(move)
        print("Current Board")
        print(board)

def gameVsHuman(board):
    board.players[0].drawTiles(board)
    board.players[1].drawTiles(board)
    while True:
        gameOver = board.gameOver()
        if gameOver in [-1, 1, 0]:
            break
        if board.currentPlayer == board.players[1]:
            move = board.currentPlayer.miniMax(board, board.currentPlayer, 100)[1]
            print(move)
            board.makeMove(move)
        else:
            while True:
                print("Current Board")
                print(board)
                print("Letter Values: ", end="")
                scoreDisplayStr = ""
                for item in sorted(board.currentPlayer.scoreDict.items()):
                    scoreDisplayStr += item[0] + " = " + str(item[1]) + ", "
                print(scoreDisplayStr[:-2])
                print()
                print("Your rack: ", board.currentPlayer.rack)
                while True:
                    word = input("Enter the word you would like to play (or -1 to pass): ")

                    if word in board.dictionary or word == "-1":
                        break
                    else:
                        print("That word is not in my dictionary. Please try again.")
                        
                if word == "-1":
                    board.makeMove(-1)
                    break
                        
                while True:
                    coOrds = input("Enter the space where the first letter of your word will go like this (colNum, rowNum): ")
                    if coOrds:
                        coOrds = eval(coOrds)
                        if type(coOrds) == list or type(coOrds) == tuple:
                            break
                        else:
                            print("Please enter in the format (colNum, rowNum).")
                while True:
                    intersect = input("Enter the indexes of tiles in your word already on the board (if any) separated by commas (first letter is 0, second is 1, etc.): ")
                    if intersect and len(intersect) > 1:
                        intersect = eval(intersect)
                        break
                    elif len(intersect) == 1:
                        intersect = [eval(intersect)]
                        break
                    else:
                        intersect = []
                        break
                while True:
                    direction = input("Enter the direction your word will be played in (r for right, d for down): ")
                    if direction in ['r', 'd']:
                        break
                    else:
                        print("You did not enter r or d to indicate direction. Please try again.")

                move = (word, coOrds, intersect, direction)
                if board.currentPlayer.testMove(move, board)[0]:
                    board.makeMove(move)
                    break
                else:
                    print("That is not a valid move. Please try again.")
        print("Current Board")
        print(board)

words = []
with open('scrabble4LetterWords.txt', 'r') as wordFile:
    wordsLines = wordFile.readlines()
    for line in wordsLines:
        for word in line.split():
            words.append(word)

with open('scrabble3LetterWords.txt', 'r') as wordFile:
    threeLetter = wordFile.read()
    
    for i in range(len(threeLetter)):
        if (i-2)%3 == 0:
            words.append(threeLetter[i-2:i+1])

with open('scrabble2LetterWords.txt', 'r') as wordFile:
    twoLetter = wordFile.readlines()
    for word in twoLetter:
        words.append(word.strip())


print("START AI VS AI")
print("-"*50)
print()
#Demo 2 AI
miniMaxB = Board(15, 15, [Player(), Player()], words)
playMiniMax(miniMaxB, 5)
print("END AI VS AI")
print()
print("-" * 50)
print()
print("START HUMAN VS AI")

#Demo 1 AI 1 Human
vHumanB = Board(7, 7, [Player(), Player()], words)
gameVsHuman(vHumanB)
