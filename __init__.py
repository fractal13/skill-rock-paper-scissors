from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context, removes_context
from mycroft.util.log import LOG

import time
from . import rock_paper_scissors

__author__ = 'fractal13'
LOGGER = LOG.create_logger( __name__ )

class RockPaperScissorsSkill( MycroftSkill ):

    def __init__( self ):
        super( RockPaperScissorsSkill, self ).__init__( name="RockPaperScissorsSkill" )
        self.rps = rock_paper_scissors.RockPaperScissors( )
        return

    @intent_handler(IntentBuilder('RockPaperScissorsIntent').require("RockKeyword").require("PaperKeyword").require("ScissorsKeyword"))
    @adds_context('RockPaperScissorsContext')
    def handle_play_game_intent(self, message):
        self.speak_dialog("challenge.accepted", data={})
        time.sleep( 0.5 )
        self.rps.setComputerChoice( )
        self.speak_dialog("computer.made.choice", data={})
        time.sleep( 0.5 )
        self.speak_dialog("what.is.your.choice", data={}, expect_response=True)
        return

    @intent_handler(IntentBuilder('UserChoiceRockIntent').require("RockKeyword").build())
    @removes_context('RockPaperScissorsContext')
    def handle_user_choice_rock_intent( self, message ):
        user_choice = "rock"
        self.rps.setUserChoice( user_choice )
        self.finish_game( )
        return

    @intent_handler(IntentBuilder('UserChoicePaperIntent').require("PaperKeyword").build())
    @removes_context('RockPaperScissorsContext')
    def handle_user_choice_paper_intent( self, message ):
        user_choice = "paper"        
        self.rps.setUserChoice( user_choice )
        self.finish_game( )
        return

    @intent_handler(IntentBuilder('UserChoiceScissorsIntent').require("ScissorsKeyword").build())
    @removes_context('RockPaperScissorsContext')
    def handle_user_choice_scissors_intent( self, message ):
        user_choice = "scissors"
        self.rps.setUserChoice( user_choice )
        self.finish_game( )
        return
    
    @intent_handler(IntentBuilder('UserChoiceIntent').require("Choice").build())
    @removes_context('RockPaperScissorsContext')
    @adds_context('RockPaperScissorsContext')
    def handle_user_choice_intent( self, message ):
        user_choice = message.data.get( "Choice" )
        self.speak_dialog("bad.choice", data={"user_choice": user_choice})
        time.sleep( 0.5 )
        self.speak_dialog("choose.options", data={})
        time.sleep( 0.5 )
        self.speak_dialog("what.is.your.choice", data={}, expect_response=True)
        return

    def finish_game( self ):
        user_choice = self.rps.getUserChoice( )
        self.speak_dialog("user.choice", data={"user_choice": user_choice})
        time.sleep( 0.5 )
        computer_choice = self.rps.getComputerChoice( )
        self.speak_dialog("computer.choice", data={"computer_choice": computer_choice})
        time.sleep( 0.5 )
        winner = self.rps.getWinner( )
        if winner == "user":
            self.speak_dialog("user.wins", data={"winner": winner})
        elif winner == "computer":
            self.speak_dialog("computer.wins", data={"winner": winner})
        elif winner == "tie":
            self.speak_dialog("tie.game", data={"winner": winner})
        else:
            self.speak_dialog("winner.error", data={"winner": winner})
        self.rps.resetGame( )
        return

def create_skill():
    return RockPaperScissorsSkill()

