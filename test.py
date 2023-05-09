import random
import json

class Game:
    def __init__(self):
        self.players : list(Player) = []
        
        self.nursery : CardSpace = None
        self.deck : CardSpace = None
        self.discard_pile : CardSpace = None
        
        self.active_player : Player = None
        self.turn_phase = None
        
        self.start()
        
    def start(self):
        # Check if game ready to start
        #assert len(self.players) >= 2
        #assert len(self.players) < 6
        
        # Initialise game
        cards = []
        with open('cards.json', 'r') as file:
            file_contents = file.read()
            for card in json.loads(file_contents):
                cards.append(
                    Card(
                        card['name'],
                        card['type'],
                        card['image']
                    )
                )
        
        # Seperate Baby Unicorn cards from other cards
        baby_unicorn_cards = [item for item in cards if item == "BABY_UNICORN"]
        
        baby_unicorn_cards = []
        for i in range(len(cards.copy())):
            if cards[i].type == "BABY_UNICORN":
                baby_unicorn_cards.append(cards.pop(i))
        
        # Shuffle the cards
        random.shuffle(cards)
        
        # Deal each player 5 cards
        for player in self.players:
            for i in range(5):       
                player.hand.add(cards.pop())
                
        # Place remaining cards in deck
        self.deck = cards
        
        # Give each player Baby Unicorn card
        for player in self.players:
            player.stable.add(baby_unicorn_cards.pop())
            
        # Place remaining Baby Unicorn cards in the Nursery
        self.nursery = baby_unicorn_cards
        
        
    def pause(self):
        pass
    
    def end(self):
        pass
    
    def quit(self):
        pass
    
    def save(self):
        pass
        
    def add_player(self, player):
        self.players.append(player)
    
    
    
class Card:
    def __init__(self, name, type, image):
        self.name = name
        self.type = type
        self.image = image
    
    def sacrifice(card):
        pass
    
    def destroy(card):
        pass
        
    def return_to_hand(card):
        pass

class CardSpace:
    def __init__(self):
        self.cards : list(Card) = []
        
    def add(self, card):
        self.cards.append(card)
        
        
game = Game()