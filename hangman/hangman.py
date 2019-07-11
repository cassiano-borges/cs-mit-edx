# Problem Set 2, hangman.py
# Name:
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    if get_guessed_word(secret_word, letters_guessed) == secret_word:
        return True
    else:
        return False



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    letter_list = ['_ '] * len(secret_word)
    secret_list = list(secret_word)
    # iterate through letters_guessed to replace in word_guess with the actual letters
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:
            letter_list[i] = secret_word[i]

    # convert into string
    word_guess = ''
    for l in letter_list:
        word_guess += l
    return word_guess



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    not_guessed_letters = ''
    for letter in string.ascii_lowercase:
        if letter in letters_guessed:
            continue
        else:
            not_guessed_letters += letter
    return not_guessed_letters



def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    print('Welcome to the game Hangman!')
    secret_len = len(secret_word)
    print(f'I am thinking of a word that is {secret_len} letters long.')
    warnings = 3
    print(f'You have {warnings} warnings left.')
    print('-------------')

    letters_guessed = []
    guesses = 6
    vowels = 'aeiou'
    win = False
    score = 0
    while guesses:
        avaiable_letters = get_available_letters(letters_guessed)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print(f'You have {guesses} guesses left')
        print(f'Avaiable letters : {avaiable_letters}')
        # user play
        guessed_letter = input('Please guess a letter: ').lower()


        # rules of the game
        if guessed_letter not in string.ascii_lowercase:
            if warnings > 0:
                warnings -= 1
                print(f'Oops! That is not a valid letter. You have {warnings} warnings left:', guessed_word)
                print('-------------')
            else:
                guesses -= 1
                print(f'Oops! That is not a valid letter. You have no warnings left:', guessed_word)
                print('-------------')
            continue
        elif guessed_letter in letters_guessed:
            if warnings > 0:
                warnings -= 1
                print(f'Oops! That is not a valid letter. You have {warnings} warnings left:', guessed_word)
                print('-------------')
            else:
                guesses -= 1
                print(f"Oops! You've already guessed that letter. You have no warnings left:", guessed_word)
                print('-------------')
            continue

        # finding or not the letter on the secrete word
        letters_guessed.extend(guessed_letter)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        if guessed_letter in secret_word:
            print('Good guess:', guessed_word)
        else:
            print('Oops! That letter is not in my word:', guessed_word)
            if guessed_letter in vowels:
                guesses -= 2
            else:
                guesses -= 1
        if is_word_guessed(secret_word, letters_guessed):
            score = guesses * len(set(secret_word))
            guesses = 0
            win = True
        print('-------------')

    if win:
        print('Congratulations, you won!')
        print(f'Your total score for this game is: {score}')
    else:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}.')


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    word_list = [letter for letter in my_word if letter != ' ']
    other_list = list(other_word)
    if len(word_list) != len(other_list):
        return False
    result = True
    for i in range(len(word_list)):
        if word_list[i] == '_':
            continue
        elif word_list[i] == other_list[i]:
            continue
        else:
            result = False
    return result



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches.append(word)
    if len(matches) == 0:
        print('No matches found')
    else:
        print(' '.join(matches))




def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    print('Welcome to the game Hangman!')
    secret_len = len(secret_word)
    print(f'I am thinking of a word that is {secret_len} letters long.')
    warnings = 3
    print(f'You have {warnings} warnings left.')
    print('-------------')

    letters_guessed = []
    guesses = 6
    vowels = 'aeiou'
    win = False
    score = 0
    while guesses:
        avaiable_letters = get_available_letters(letters_guessed)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print(f'You have {guesses} guesses left')
        print(f'Avaiable letters : {avaiable_letters}')
        # user play
        guessed_letter = input('Please guess a letter: ').lower()

        # hint
        # at least 2 right answers to get a hint
        if guessed_letter == '*' and len(guessed_word) <= (2 * len(secret_word)) - 2:
            print('Possible word matches are:')
            show_possible_matches(guessed_word)
            print('-------------')
            continue
        elif guessed_letter == '*' and len(guessed_word) > (2 * len(secret_word)) - 2:
            print('Try getting at least 2 right guessings.')
            print('-------------')
            continue

        # rules of the game
        if guessed_letter not in string.ascii_lowercase:
            if warnings > 0:
                warnings -= 1
                print(f'Oops! That is not a valid letter. You have {warnings} warnings left:', guessed_word)
                print('-------------')
            else:
                guesses -= 1
                print(f'Oops! That is not a valid letter. You have no warnings left:', guessed_word)
                print('-------------')
            continue
        elif guessed_letter in letters_guessed:
            if warnings > 0:
                warnings -= 1
                print(f'Oops! That is not a valid letter. You have {warnings} warnings left:', guessed_word)
                print('-------------')
            else:
                guesses -= 1
                print(f"Oops! You've already guessed that letter. You have no warnings left:", guessed_word)
                print('-------------')
            continue

        # finding or not the letter on the secrete word
        letters_guessed.extend(guessed_letter)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        if guessed_letter in secret_word:
            print('Good guess:', guessed_word)
        else:
            print('Oops! That letter is not in my word:', guessed_word)
            if guessed_letter in vowels:
                guesses -= 2
            else:
                guesses -= 1
        if is_word_guessed(secret_word, letters_guessed):
            score = guesses * len(set(secret_word))
            guesses = 0
            win = True
        print('-------------')

    if win:
        print('Congratulations, you won!')
        print(f'Your total score for this game is: {score}')
    else:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}.')


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.
    secret_word = choose_word(wordlist)
    while True:
        print('Do you want to play Hangman with hints?')
        ans = input('<y/n> ')
        if ans == 'n' :
            hangman_with_hints(secret_word)
            input('Press any button to quit')
            break
        elif ans == 'y':
            hangman_with_hints(secret_word)
            input('Press any button to quit')
            break
        else:
            continue
