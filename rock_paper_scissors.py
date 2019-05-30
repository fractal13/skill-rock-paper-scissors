#!/usr/bin/env python3

import random

class RockPaperScissors:
    _OPTIONS = [ "rock", "paper", "scissors" ]
    _WINNERS = [ "user", "computer", "tie", "none" ]

    def __init__( self ):
        self.user_choice = ""
        self.my_choice = ""
        self.resetGame( )
        return

    def getOptions( self ):
        # copy, so it won't be accidentally changed
        return self._OPTIONS[:]

    def getUserChoice( self ):
        return self.user_choice

    def getComputerChoice( self ):
        return self.my_choice

    def resetGame( self ):
        self.user_choice = ""
        self.my_choice = ""
        return

    def setUserChoice( self, choice ):
        if not self.user_choice:
            choice = choice.lower( )
            if choice in self._OPTIONS:
                self.user_choice = choice
                return True
            else:
                return False
        else:
            return False

    def setComputerChoice( self ):
        if not self.my_choice:
            self.my_choice = random.choice( self._OPTIONS )
            return True
        else:
            return False

    def getWinner( self ):
        if self.user_choice and self.my_choice:
            if self.user_choice == self.my_choice:
                return self._WINNERS[ 2 ]
            elif self.user_choice == "paper" and self.my_choice == "rock":
                return self._WINNERS[ 0 ]
            elif self.user_choice == "scissors" and self.my_choice == "paper":
                return self._WINNERS[ 0 ]
            elif self.user_choice == "rock" and self.my_choice == "scissors":
                return self._WINNERS[ 0 ]
            elif self.my_choice == "paper" and self.user_choice == "rock":
                return self._WINNERS[ 1 ]
            elif self.my_choice == "scissors" and self.user_choice == "paper":
                return self._WINNERS[ 1 ]
            elif self.my_choice == "rock" and self.user_choice == "scissors":
                return self._WINNERS[ 1 ]
            else:
                return self._WINNERS[ 3 ]
        else:
            return self._WINNERS[ 3 ]

def main( ):
    rps = RockPaperScissors( )
    ok = False
    while not ok:
        choice = input( "What do you choose? " + "|".join( rps.getOptions( ) ) + " " )
        ok = rps.setUserChoice( choice )

    ok = False
    while not ok:
        ok = rps.setComputerChoice( )

    print( "You: " + rps.getUserChoice( ) + "  Computer: " + rps.getComputerChoice( ) + "  Winner: " + rps.getWinner( ) )
    return

if __name__ == "__main__":
    main( )
