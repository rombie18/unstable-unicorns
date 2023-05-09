import random
import json

class Game:
    def __init__(self):
        self.players = []
        
        self.nursery = []
        self.deck  = []
        self.discard_pile = []
        
        self.active_player = None
        self.turn_phase = None
                
    def start(self):
        
        with open('cards.json', 'r') as file:
            file_contents = file.read()
            cards = json.loads(file_contents)
            
        random.shuffle(cards)
            
        baby_unicorn_cards = [card for card in cards if card['type'] == "BABY_UNICORN"]
        not_baby_unicorn_cards = [card for card in cards if card['type'] != "BABY_UNICORN"]            
        
        for player in self.players:
            player.stable.append(baby_unicorn_cards.pop())
            for _ in range(5):
                player.hand.append(not_baby_unicorn_cards.pop())
            
        self.nursery = baby_unicorn_cards
        self.deck = not_baby_unicorn_cards
    
        self.active_player = random.choice(self.players)
        self.turn_phase = "BEGINNING_OF_TURN"

        
    def next_turn_phase(self):
        if self.turn_phase == "BEGINNING_OF_TURN":
            self.turn_phase = "DRAW"
        elif self.turn_phase == "DRAW":
            self.turn_phase = "ACTION"
        elif self.turn_phase == "ACTION":
            self.turn_phase = "END_OF_TURN"
        elif self.turn_phase == "END_OF_TURN":
            current_index = self.players.index(self.active_player)
            if current_index == len(self.players - 1):
                self.active_player = self.players[0]
            else:
                self.active_player = self.players[current_index + 1]
            self.turn_phase = "BEGINNING_OF_TURN"
            
    def draw_card(self):
        game.active_player.hand.append(game.deck.pop())
    
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.stable = []
        
        
        
        
game = Game()

player1 = Player("Player 1")
player2 = Player("Player 2")

game.players.append(player1)
game.players.append(player2)

game.start()

## Beginning of turn phase
# Click on card in stable to execute effect, if any
#game.apply_effect(card)

game.next_turn_phase()

## Draw phase
# Draw a card
game.draw_card()

game.next_turn_phase()

## Action phase
# Play a card from hand or draw card
game.draw_card()

## End of turn phase
# Discard until number of cards in hand <= 7