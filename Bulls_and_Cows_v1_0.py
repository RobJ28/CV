# 1 /First of all, the computer will generate a 4-digit secret number. The digits must be all different.
# 2/ Then, in turn, the user tries to guess their computer's number. The computer prompts the user for a number
# and after the input has been received, the computer responds with the number of matching digits.
# 3/ If the matching digits are in their right positions, they are "bulls", if in different positions, they are "cows".
# Bonus
# Extend the functionality of the program as you wish. For example
# Counting time it took to guess the number
# Count the number of guesses and store them in a file and at the end depict user's stats (the best player etc.)


import random
import time
import os
import os.path
from operator import itemgetter


def generate_4num():
    '''
    generate random number (4 length) to the list with different numbers (0 - 9)
    '''
    four_num = []
    while len(four_num) < 4:
        num = random.randint(0,9)
        if num not in four_num:
            four_num.append(num)
    return (four_num)

def compare_num(gen_num, user_num):
    '''
    compare two number with with same length
    gen_num = searching number
    user_num = input from user
    '''
    bulls, cows = [0,0]
    for i, num in enumerate(gen_num):
        for j, unum in enumerate(user_num):
                #kdyz se indexy a hodnoty na indexech rovnaji pricti k bulls +1
            if (i == j) and (num == unum):
                bulls += 1
                #kdyz se indexy nerovnaji a hodnoty rovnaji pricti k bulls +1
            elif (i != j) and (num == unum):
                cows += 1
            else:
                pass
    return bulls, cows

play_game = False
while not play_game:
    line = 62 * '-'
    print(line)
    print("|{0:^60}|".format("Hi there!") + "\n" + "|{0:^60}|".format("I've generated a random 4 different digit number for you.") + "\n" + "|{0:^60}|".format("Let's play a Bulls and Cows game. Good luck :)"))
    print(line)
    name = input('Enter your name: ')
    # generate searching number
    gen_num = generate_4num()
    # print('Generated number is:',gen_num)

    result = [0,0]
    attempts = 0

    # create file with header if file not exists
    if not os.path.exists('all_results.txt'):
        with open('all_results.txt', mode = 'a') as tab_header:
            table = tab_header.write(f'Name, Attempts, Searching time\n')

    # start counting time
    start = time.time()
    while result[0] != 4:
        #transfer string input to list with int - map(function, iterables)
        try:
            user_number = list(map(int, input('Enter a 4 digits number with different numbers: ')))
            attempts += 1
            if len(user_number) != len(gen_num):
                print(line)
                print("Your entered number didn't has 4 digits. Try again.")
                print(line)
            elif len(user_number) == len(set(user_number)):
                result = compare_num(gen_num, user_number)
                print(f'BULLS {result[0]} and COWS {result[1]}')
                print(line)
            else:
                print(line)
                print('You are enter number which contain same digits. Try it again.')
                print(line)
        except ValueError:
            print(line)
            print("You didn't enter number. Try it again.")
            print(line)

    #score results
    if attempts == 1:
        score = 'You are GOD of all Cow and Bulls'
    elif attempts <= 10:
        score = 'Amazing'
    elif attempts <= 15:
        score = 'Good'
    elif attempts <= 20:
        score = 'Average'
    elif attempts > 20:
        score = 'Not so good'

    #merged list numbers to string numbers
    look_num = ''.join(str(i) for i in gen_num)
    elapsed_time = time.time() - start
    # transform to time hours:minutes:seconds
    r_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    # adding results to file
    with open('all_results.txt', mode = 'a') as ap_f:
        complete_results = ap_f.write(f'{name}, {attempts}, {r_time}\n')

    print(f"{score}, you've guessed number {look_num} in {attempts} guesses! \nGuessed time for number is {r_time}")
    print(line)

    ############# result parts #############
    #print row in all_results.txt
    def row_table (top_score):
        '''
        Generate table from nested list with 3 items in list
        '''
        for index,value in enumerate(top_score):
            if index < 10:
                print("|{0:^12}|{1:^12}|{2:^18}|".format(*top_score[index]))
            else: break
        print(t_line)

    with open('all_results.txt') as rs:
        result_line = rs.readlines()

    # remove next line \n
    result_line = [line.strip('\n') for line in result_line]

    # convert to list from file - row is one item in list
    to_list = [item.split(', ') for item in result_line]

    # transform str to int on index 1 on attempts
    for x in to_list[1:]:
        x[1] = int(x[1])

    #sort list by first index - attempts
    top_score = sorted(to_list[1:], key=itemgetter(1))
    #sort list by second index - time
    top_time = sorted(to_list[1:], key=itemgetter(2))

    #counting length header
    len_header = len(("|{0:^12}|{1:^12}|{2:^18}|".format(*to_list[0])))
    #horizontal table line
    t_line = len_header * '-'

    #loop for menu after game
    again = False
    while not again:
        #set of choices in menu
        choices = {'a','r','q','A', 'R', 'Q'}
        print("What do you want to do next?\n[A] - Play again, [R] - Show best results, [Q] - Quit Game")
        what_next = input('Enter letter for your choice: ').lower()
        if what_next in choices:
            #quit game
            if what_next == 'q':
                play_game = True
                again = True
                break
            #print best results
            elif what_next == 'r':
                #header table top by attempts
                print()
                print('{0:^46}'.format('TOP TEN SCORE BY ATTEMPTS'))
                print(t_line)
                print("|{0:^12}|{1:^12}|{2:^18}|".format(*to_list[0]))
                print(t_line)
                row_table(top_score)
                #header table top by time
                print()
                print('{0:^46}'.format('TOP TEN SCORE BY TIME'))
                print(t_line)
                print("|{0:^12}|{1:^12}|{2:^18}|".format(*to_list[0]))
                print(t_line)
                row_table(top_time)
            #play again
            elif what_next == 'a':
                again = True
                # clear screen for windows
                os.system('cls')
                # clear screen for linux
                # os.system('clear')
            else:
                print('You are enter unknow choice. Try again.')
                continue
        else:
            print('Your enter is not correct. Try again.')
