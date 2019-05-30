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
        self.waiting_for_user_choice = False
        if "wins" not in self.settings:
            self.settings[ "wins" ] = 0
        if "losses" not in self.settings:
            self.settings[ "losses" ] = 0
        if "ties" not in self.settings:
            self.settings[ "ties" ] = 0
        if "debug" not in self.settings:
            self.settings[ "debug" ] = 0

        if self.settings[ "debug" ]:
            LOGGER.info( "__init__" )
        return

    @intent_handler(IntentBuilder('RockPaperScissorsDebugIntent')
                    .require("DebugKeyword")
                    .require("RockPaperScissorsKeyword"))
    def handle_debug_intent(self, message):
        
        if self.settings[ "debug" ] == 0:
            self.settings[ "debug" ] = 1
            self.speak_dialog("debug.is.on", data={})
        else:
            self.settings[ "debug" ] = 0
            self.speak_dialog("debug.is.off", data={})
            
        LOGGER.info( "Debug is " + str( self.settings[ "debug" ] ) )
        return

    @intent_handler(IntentBuilder('RockPaperScissorsScoreIntent')
                    .require("ShowKeyword")
                    .require("RockPaperScissorsKeyword")
                    .require("ScoreKeyword"))
    def handle_score_intent(self, message):
        self.speak_dialog("score", data={ "wins": self.settings[ "wins" ],
                                          "losses": self.settings[ "losses" ],
                                          "ties": self.settings[ "ties" ]})
        if self.settings[ "debug" ]:
            LOGGER.info( "Score Intent" + str( self.rps ) )
        return
    
    @intent_handler(IntentBuilder('RockPaperScissorsGameIntent')
                    .require("ChallengeKeyword")
                    .require("RockPaperScissorsKeyword"))
    def handle_play_game_intent(self, message):
        self.speak_dialog("challenge.accepted", data={})
        time.sleep( 0.5 )
        self.rps.setComputerChoice( )
        self.speak_dialog("computer.made.choice", data={})
        time.sleep( 0.5 )
        self.speak_dialog("what.is.your.choice", data={}, expect_response=True)
        self.waiting_for_user_choice = True
        if self.settings[ "debug" ]:
            LOGGER.info( "Game Intent" + str( self.rps ) )
        return

    # @intent_handler(IntentBuilder('UserChoiceRockIntent').require("RockKeyword"))
    # @removes_context('RockPaperScissorsGameContext')
    # def handle_user_choice_rock_intent( self, message ):
    #     if self.settings[ "debug" ]:
    #         LOGGER.info( "Rock Intent" + str( self.rps ) )
    #     user_choice = "rock"
    #     self.rps.setUserChoice( user_choice )
    #     self.finish_game( )
    #     return

    # @intent_handler(IntentBuilder('UserChoicePaperIntent').require("PaperKeyword"))
    # @removes_context('RockPaperScissorsGameContext')
    # def handle_user_choice_paper_intent( self, message ):
    #     if self.settings[ "debug" ]:
    #         LOGGER.info( "Paper Intent" + str( self.rps ) )
    #     user_choice = "paper"        
    #     self.rps.setUserChoice( user_choice )
    #     self.finish_game( )
    #     return

    # @intent_handler(IntentBuilder('UserChoiceScissorsIntent').require("ScissorsKeyword"))
    # @removes_context('RockPaperScissorsGameContext')
    # def handle_user_choice_scissors_intent( self, message ):
    #     if self.settings[ "debug" ]:
    #         LOGGER.info( "Scissors Intent" + str( self.rps ) )
    #     user_choice = "scissors"
    #     self.rps.setUserChoice( user_choice )
    #     self.finish_game( )
    #     return
    
    @intent_handler(IntentBuilder('UserChoiceIntent').require("Throw").require("Choice"))
    def handle_user_choice_intent( self, message ):
        if not self.waiting_for_user_choice:
            LOGGER.info( "UserChoiceIntent without expecting user choice " + str( self.rps ) )
            return
        
        user_choice = message.data.get( "Choice" )
        if self.settings[ "debug" ]:
            LOGGER.info( "User Choice Intent " + user_choice + str( self.rps ) )

        if self.rps.setUserChoice( user_choice ):
            self.waiting_for_user_choice = False
            self.finish_game( )
        else:
            self.speak_dialog("bad.choice", data={"user_choice": user_choice})
            time.sleep( 0.5 )
            self.speak_dialog("choose.options", data={})
            time.sleep( 0.5 )
            self.speak_dialog("what.is.your.choice", data={}, expect_response=True)
        return

    def finish_game( self ):
        """
        Restates the choices, then declares the winner.
        """
        if self.settings[ "debug" ]:
            LOGGER.info( "game over " + str( self.rps ) )

        user_choice = self.rps.getUserChoice( )
        self.speak_dialog("user.choice", data={"user_choice": user_choice})
        time.sleep( 0.5 )
        computer_choice = self.rps.getComputerChoice( )
        self.speak_dialog("computer.choice", data={"computer_choice": computer_choice})
        time.sleep( 0.5 )

        winner = self.rps.getWinner( )
        if winner == "user":
            self.speak_dialog("user.wins", data={"winner": winner})
            self.settings[ "wins" ] += 1
        elif winner == "computer":
            self.speak_dialog("computer.wins", data={"winner": winner})
            self.settings[ "losses" ] += 1
        elif winner == "tie":
            self.speak_dialog("tie.game", data={"winner": winner})
            self.settings[ "ties" ] += 1
        else:
            self.speak_dialog("winner.error", data={"winner": winner})
        self.rps.resetGame( )
        self.waiting_for_user_choice = False
        return

    def stop( self ):
        if self.settings[ "debug" ]:
            LOGGER.info( "stop " + str( self.rps ) )
        self.rps.resetGame( )
        self.waiting_for_user_choice = False
        if self.settings[ "debug" ]:
            LOGGER.info( "reset " + str( self.rps ) )
        return

def create_skill():
    return RockPaperScissorsSkill()

