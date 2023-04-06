# this is a game, where you guess a password until you can open the lock.
from random import choice, shuffle, sample, randint
from difflib import SequenceMatcher
import os
import time
from ANSIcolors import colors, fg, bg #self made class that holds some ansi color codes

class Interface:
    def __init__(self, GameLogic_object):
        self.__object = GameLogic_object

    def create_interface(self, feedback):
        print("\n\n")
        hex = self.generate_hex()
        for r,m,l in zip(hex[0], self.generate_text(feedback), hex[1]):
            print(r, m, l)
        print("\n")

    def no_option(self,guess):
        txt = [
            "             " + fg.bold + fg.red + "NOT AN OPTION, TRY AGAIN!\033[00m            ",
            "                                                  ",
            f"                YOU HAVE {self.__object.get_guesses() - self.__object.get_guessed()} GUESSES                ",
            "                   REMAINING.                     ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  "
        ]
        
        print("\n\n")
        hex = self.generate_hex()
        for r,m,l in zip(hex[0], txt, hex[1]):
            print(r,m,l)
        print("\n")

    def create_start(self):
        txt = [
                "                  " + fg.bold + fg.red + "ENTRY LOCKED!\033[00m                   ",
                "                  ENTER PASSWORD                  ",
                f"                YOU HAVE {self.__object.get_guesses() - self.__object.get_guessed()} GUESSES                ",
                "                     REMAINING.                   ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                                                  "
            ]
        print("\n\n")
        hex = self.generate_hex()
        for r,m,l in zip(hex[0], txt, hex[1]):
            print(r,m,l)
        print("\n")

    def create_end(self):
        txt = [
                "                   " + fg.bold + fg.red + "ACCESS DENIED!\033[00m                 ",
                "                                                  ",
                "                    " + fg.bold + fg.red + "GAME OVER!\033[00m                    ",
                "                                                  ",
                "                  TO TRY AGAIN                    ",
                "                  TYPE 'reset'!                   ",
                "                                                  ",
                "                 TO EXIT THE GAME                 ",
                "                   TYPE 'exit'!                   ",
                "                                                  "
            ]
        print("\n\n")
        hex = self.generate_hex()
        for r,m,l in zip(hex[0], txt, hex[1]):
            print(r,m,l)
        print("\n")

    def create_happy_end(self):
        txt = [
                "                  " + fg.bold + fg.green + "ACCESS GRANTED!\033[00m                 ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                  TO PLAY AGAIN                   ",
                "                  TYPE 'reset'!                   ",
                "                                                  ",
                "                 TO EXIT THE GAME                 ",
                "                   TYPE 'exit'!                   ",
                "                                                  "
            ]
        print("\n\n")
        hex = self.generate_hex()
        for r,m,l in zip(hex[0], txt, hex[1]):
            print(r,m,l)
        print("\n")

    def generate_text(self, feedback):
        txt = []
        if self.__object.get_guessed() == 0:
            txt = [
                "                  " + fg.bold + fg.red + "ENTRY LOCKED!" + fg.reset + "                   ",
                "                  ENTER PASSWORD                  ",
                f"                YOU HAVE {self.__object.get_guesses() - self.__object.get_guessed()} GUESSES                ",
                "         REMAINING.           ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
            ]

        if feedback[0] == False:
            txt = [
                "                   " + fg.bold + fg.red + "ACCESS DENIED!" + fg.reset + "                 ",
                "                                                  ",
                f"                  {feedback[2]}/{self.__object.get_length()}  CORRECT                    ",
                f"                YOU HAVE {self.__object.get_guesses() - self.__object.get_guessed()} GUESSES                ",
                "                   REMAINING.                     ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                                                  ",
                "                                                  "
            ]
        return txt

    def generate_hex(self):
        options = self.__object.get_options()
        shuffle(options)
        y = ["a","b","c","d","e","1","2","3","4","5","6","7","8","9","0"] * 2
        l = 20 - self.__object.get_length()
        left = [True,False,False,True,True,False,True,False,True,False]
        right = [True,True,False,True,False,True,False,False,True,False]
        o = 0
        for pos, i in enumerate(right):
            if i:
                x = randint(1,l)
                right[pos] = fg.reset + "".join(sample(y, x)) + options[o] + "".join(sample(y, (l-x)))
                o += 1
            else:
                right[pos] = "".join(sample(y, 20))
        for pos, i in enumerate(left):
            if i:
                x = randint(1,l)
                left[pos] = "".join(sample(y, x)) + options[o] + "".join(sample(y, (l-x)))
                o += 1
            else:
                left[pos] = "".join(sample(y, 20))

        x = [left] + [right]
        return x

class GameLogic:
    def __init__(self, length, guesses) -> None:
        self.__length = length
        self.__guesses = guesses
        self.__guessed = 0
        self.__words = []
        with open("/Users/moritzmantel/Python/words.txt") as f:
            self.__words += [w.upper() for w in f.read().splitlines() if len(w) == length]
        self.__password = choice(self.__words)
        self.__options = self.create_options()

    def create_options(self):
        o = []
        for x in self.__words:
            if not x in o and not x == self.__password:
                if len(o) < 9:
                    if self.is_similar(x, self.__password, 0.5):
                        o.append(x)
        o.append(self.__password)
        y = 10 - len(o)
        if y != 0:
            while len(o) < 10:
                p = choice(self.__words)
                if not p in o:
                    o.append(p)
        return o

    def is_similar(self, a, b, threshold):
        x = SequenceMatcher(None, a, b).ratio()
        return x > threshold


    def get_length(self):
        x = self.__length
        return x

    def get_guesses(self):
        x = self.__guesses
        return x

    def get_guessed(self):
        x = self.__guessed
        return x
    
    def get_options(self):
        return self.__options

    def get_password(self):
        return self.__password[:]

    def add_guess(self):
        self.__guessed += 1

    def feedback(self, guess):
        
        if guess == self.__password:
            x = self.__options.index(guess)
            self.__options[x] = fg.green + guess + fg.reset
            return (True, guess, 100)
        else:
            x = self.__options.index(guess)
            self.__options[x] = fg.lightgrey + guess + fg.reset
        corr = 0
        for x in guess:
            if x in self.__password:
                corr += 1
        self.__guessed += 1
        return (False, guess, corr)


class Interaction:
    def __init__(self, difficulty):
        self.__diff = int(difficulty)

    def create(self):
        x = GameLogic(self.__diff, 5)
        y = Interface(x)
        os.system('clear')
        y.create_start()
        self.interaction(x,y)

    def interaction(self,x,y):
        while x.get_guessed() < x.get_guesses():
            p = input("").upper()
            if not p in x.get_options():
                time.sleep(0.5)
                os.system('clear')
                y.no_option(p)
                self.interaction(x,y)
            f = x.feedback(p)
            time.sleep(0.5)
            os.system('clear')
            y.create_interface(f)
            if f[0] == True:
                break
        if f[0] != True:
            self.end_of_game(y)
        else:
            self.end_of_happy_game(y)
    
    def end_of_game(self,b):
        os.system('clear')
        b.create_end()
        x = input("")
        if x == "reset":
            self.create()
        elif x == "exit": 
            os.system('clear')
            pass
        else:
            self.end_of_game(b)

    def end_of_happy_game(self,b):
        os.system('clear')
        b.create_happy_end()
        x = input("")
        if x == "reset":
            self.create()
        elif x == "exit": 
            os.system('clear')
            pass
        else:
            self.end_of_happy_game(b)
os.system('clear')
a = Interaction(7)
a.create()
os.system('clear')