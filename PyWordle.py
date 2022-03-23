import csv
from tabnanny import check
from PyDictionary import PyDictionary
import random

"""
Class responsible for running the game
"""
class PyWordle():
    def __init__(self):
        self.__word = ""
        self.__dictionary = PyDictionary()
        self.__guess_attempts = 0

    def run_game(self):
        # Print the welcome message
        print('I have chosen a randome five letter word, can you guess what it is?\n'
        'I\'ll give you five tries. Along the way i\'ll tell you which letters you got right,\n'
        'which letters are in the word but in a different place,\n'
        'and which letters are not in the word you guessed.')

        self.__word = self.__get_random_word()
        self.__loop()

    """
    --------------------------------------------------------------------------------------------------------
    """

    def __loop(self):
        """
        The main loop that the player follows
        first check if the player has run out of guesses
        if not get a guess and check it
        """
        while True:
            if not self.__can_continue():
                print(f'That\'s it you\'ve had five guesses and not found my word.\n'
                f'My word was {self.__word}')
                break
            else:
                guess = self.__get_player_guess()
                self.__guess_attempts += 1
                # If the guess is correct then no need to continue
                if guess == self.__word:
                    print(f'{guess} that was my word. Great job.\n'
                    f'That only took you {self.__guess_attempts} guesses.')
                    break
                else:
                    guess_data = self.__evaluate_guess(guess)
                    formatted_data = self.__get_guess_formatted_string(guess_data, guess)
                    print(formatted_data)
                    print('Key: Underlined letters are correct and in the right place in the word.\n'
                          '     Letters that are not underlined appear in the word but in a different place.\n'
                          '     Stars mean that your letter wasn\'t in the word.')
                    continue

    def __get_words_list(self):
        """
        Use the words.csv file to select a random word. All words in the file are already formatted and fit 
        the necessary criteria
        """
        word_list = []
        file = open('words.csv')
        with file:
            reader = csv.reader(file)
            for word in reader:
                word_list.append(word[0])
        file.close()
        return word_list

    def __get_random_word(self):
        """
        Using the list of words, select a random word
        """
        words_list = self.__get_words_list()
        rand_index = random.randint(0, len(words_list))
        return words_list[rand_index]

    def __get_player_guess(self):
        """
        Use input to get a guess from the player. Check that it meets the necessary conditions
        of being 5 letters and a valid english word.
        """
        valid = False
        guess = ""
        while not valid:
            check_guess = input('Take a guess: ')
            if len(check_guess) != 5:
                print('Your guess must be a 5 letter word.')
                continue
            if not self.__check_english_word(check_guess):
                print('Your guess must be a real english word thats in the dictionary.')
                continue
            guess = check_guess
            valid = True

        return guess

            
    def __check_english_word(self, word):
        """
        Use PyDictionary to check if the supplied word is valid english or not
        """
        if self.__dictionary.meaning(word, disable_errors=True) != None:
            return True
        else:
            return False

    def __can_continue(self):
        """
        Checks if the player has already made 5 guesses and returns False
        """
        if self.__guess_attempts >= 5:
            return False
        else:
            return True

    def __evaluate_guess(self, guess):
        """
        Check each letter in the guess. Returns a list.
        If the letter is correct and in the right place return 2
        If the letter is in the word but in the wrong place return 1
        If the letter is not in the word return 0
        e.g [0, 2, 1, 1, 0]
        """
        data = [0, 0, 0, 0, 0]
        i = 0
        for letter in guess:
            if letter == self.__word[i]:
                data[i] = 2
            elif letter in self.__word:
                data[i] = 1
            else:
                data[i] = 0
            i += 1
        return data

    def __get_guess_formatted_string(self, guess_data, guess):
        """
        Print a formatted string to represent guess data.
        underline correct letter in correct position
        print letter if it's in the word
        print a star is the letter is not in the word
        """
        formatted = ""
        i = 0
        for d in guess_data:
            if d == 0:
                formatted += "*"
            if d == 1:
                formatted += guess[i]
            if d == 2:
                formatted += f'{guess[i]}\u0332'
            formatted += " "
            i += 1
        return formatted

"""
--------------------------------------------------------------------------------------------------------
"""
        
"""
Main entry point when called from terminal
"""
def main():
    wordle = PyWordle()
    wordle.run_game()

if __name__ == '__main__':
    main()