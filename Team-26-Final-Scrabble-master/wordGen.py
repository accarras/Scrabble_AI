from collections import Counter

def main():
    dictionary = ['go','bat','me','eat','goal','boy','run'] 
    rack = ['e','o','b', 'a','m','g', 'l'] 
    possibleWords = wordGenerator(dictionary, rack)
    print(possibleWords)

def wordGenerator(dictionary, rack):
    words = []

    for word in dictionary: 
  
        # convert word into dictionary 
        dict = Counter(word) 
          
        # now check if all keys of current word  
        # are present in given character set 
        flag = 1 
        for key in dict.keys(): 
            if key not in rack: 
                flag = 0
          
        # if all keys are present ( flag=1 )
        # then print the word
        if flag==1:
            words.append(word)
    
    return words

main()