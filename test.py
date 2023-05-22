import random
import json
import logging

class Game:
    def __init__(self, players):
        self.players = players
        self.current_player = None
        self.deck = None
        self.discard_pile = None
        self.effect_handler = None

    def initialize_game(self):
        # Initialise logging
        logging.basicConfig(level=logging.INFO, format='%(levelname)8s | %(lineno)4s | %(message)s')
        logging.info("Initialising game")

        # Initialise EffectHandler
        self.effect_handler = EffectHandler(self)
        self.discard_pile = DiscardPile()
        
        # Read all cards from JSON and put in deck
        with open('cards.json', 'r') as file:
            file_contents = file.read()
            cards = json.loads(file_contents)
            card_objs = []
            
            for card in cards:
                if card['type'] == "MAGICAL_UNICORN":
                    card_obj = MagicalUnicornCard(card['name'], card['image'], card['effect'])
                elif card['type'] == "BABY_UNICORN":
                    card_obj = BabyUnicornCard(card['name'], card['image'], card['effect'])
                elif card['type'] == "NORMAL_UNICORN":
                    card_obj = BasicUnicornCard(card['name'], card['image'], card['effect'])
                elif card['type'] == "UPGRADE":
                    card_obj = UpgradeCard(card['name'], card['image'], card['effect'])
                elif card['type'] == "DOWNGRADE":
                    card_obj = DowngradeCard(card['name'], card['image'], card['effect'])
                elif card['type'] == "MAGIC":
                    card_obj = MagicCard(card['name'], card['image'], card['effect'])
                elif card['type'] == "INSTANT":
                    card_obj = InstantCard(card['name'], card['image'], card['effect'])
                    
                card_objs.append(card_obj)
                
            self.deck = Deck(card_objs)
        
        # Shuffle the deck and deal 5 cards to each player
        logging.info("Dealing cards")
        self.deck.shuffle()
        for player in self.players:
            for i in range(5):
                card = self.deck.draw_card()
                player.add_to_hand(card)

        # Determine the starting player
        self.current_player = self.players[0]
        
        logging.info("Game initialised!")
        logging.info("---")

    def start_turn(self):
        logging.info("Starting turn")

        # Draw a card and add it to the current player's hand
        card = self.deck.draw_card()
        self.current_player.add_to_hand(card)

        # Play the first card from the current player's hand automatically
        card = self.current_player.hand.cards[0]
        self.play_card(card)

    def next_player(self):
        # Find the next player in the list of players
        current_index = self.players.index(self.current_player)
        next_index = (current_index + 1) % len(self.players)
        self.current_player = self.players[next_index]
        logging.info("Advancing player '" + str(self.players[current_index]) + "' to '" + str(self.players[next_index]) + "'")
        logging.info("---")

    def play_card(self, card):
        logging.info("Playing card '" + str(card) + "'")
        
        # Remove the card from the player's hand and add it to the discard pile
        self.current_player.remove_from_hand(card)
        self.discard_pile.add_card(card)

        # Resolve the card's effect
        #card.play()
        self.effect_handler.handle_effect(card.effect, self.current_player)

        # Check for victory conditions
        if len(self.current_player.stable) >= 7:
            print(f"{self.current_player.name} wins!")
        else:
            self.next_player()

    def get_player_input(self, prompt, valid_inputs):
        # Helper function to get input from the current player
        while True:
            user_input = input(prompt).lower()
            if user_input in valid_inputs:
                return user_input
            print("Invalid input. Please try again.")

    def choose_card_from_hand(self):
        # Ask the current player to choose a card from their hand
        prompt = f"{self.current_player.name}, choose a card from your hand: "
        valid_inputs = [str(i+1) for i in range(len(self.current_player.hand))]
        index = int(self.get_player_input(prompt, valid_inputs)) - 1
        return self.current_player.hand[index]

    def choose_card_from_stable(self):
        # Ask the current player to choose a card from their stable
        prompt = f"{self.current_player.name}, choose a card from your stable: "
        valid_inputs = [str(i+1) for i in range(len(self.current_player.stable))]
        index = int(self.get_player_input(prompt, valid_inputs)) - 1
        return self.current_player.stable[index]

    def choose_player(self):
        # Ask the current player to choose another player
        prompt = f"{self.current_player.name}, choose another player: "
        valid_inputs = [str(i+1) for i in range(len(self.players)) if self.players[i] != self.current_player]
        index = int(self.get_player_input(prompt, valid_inputs)) - 1
        return self.players[index]
            
            




class EffectHandler:
    def __init__(self, game):
        self.game = game

    def handle_effect(self, effect, source_player, target_player=None):
        logging.info("Source player '" + str(source_player) + "' is applying effect '" + str(effect) + "' to target player '" + str(target_player) + "'")
        

        if effect == "discard_unicorn_draw":
            pass
        elif effect == "max_5_unicorns_in_stable":
            pass
        elif effect == "invincible_unicorns":
            pass
        elif effect == "unable_upgrade":
            pass
        elif effect == "choose_top3_deck":
            pass
        elif effect == "baby_unicorn_to_stable":
            pass
        elif effect == "discard_unicorn_unicorn_from_discard_pile":
            pass
        elif effect == "destroy_upgrade_or_discard_downgrade":
            pass
        elif effect == "everyone_discard":
            pass
        elif effect == "swap_stable":
            pass
        elif effect == "everyone_stable_to_hand":
            pass
        elif effect == "discard2_destroy_unicorn":
            self.game.discard_card(source_player)
            self.game.discard_card(source_player)
            self.game.draw_card(source_player)
        elif effect == "discard_draw":
            self.game.discard_card(source_player)
            self.game.draw_card(source_player)
  
  
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.stable = Stable()
        
    def __str__(self):
        return self.name

    def add_to_hand(self, card):
        logging.debug("Adding card '" + str(card) + "' to hand of player '" + str(self) + "'")
        self.hand.add_card(card)

    def remove_from_hand(self, card):
        logging.debug("Removing card '" + str(card) + "' from hand of player '" + str(self) + "'")
        self.hand.remove_card(card)
        
    def add_to_stable(self, card):
        logging.debug("Adding card '" + str(card) + "' to stable of player '" + str(self) + "'")
        self.stable.add_card(card)

    def remove_from_stable(self, card):
        logging.debug("Removing card '" + str(card) + "' from stable of player '" + str(self) + "'")
        self.stable.remove_card(card)
        
        
        
class Card:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect
        self.card_type = None
        
    def __str__(self):
        return self.name + " (" + self.card_type + ")"

    def play(self, effect_handler, player):
        logging.debug("Playing card '" + str(self) + "'")
        effect_handler.handle_effect(self.effect, player)
                
class BasicUnicornCard(Card):
    def __init__(self, name, description, effect):
        super().__init__(name, description, effect)
        self.card_type = "basic_unicorn"

    def play(self, player):
        player.add_to_stable(self)
        
class BabyUnicornCard(Card):
    def __init__(self, name, description, effect):
        super().__init__(name, description, effect)
        self.card_type = "baby_unicorn"

    def play(self, player):
        player.add_to_stable(self)


class MagicalUnicornCard(Card):
    def __init__(self, name, description, effect):
        super().__init__(name, description, effect)
        self.card_type = "magical_unicorn"

    def play(self, player):
        player.add_to_stable(self)
        player.check_for_unicorns_with_trigger_effect()

class MagicCard(Card):
    def __init__(self, name, description, effect):
        super().__init__(name, description, effect)
        self.card_type = "magic"

    def play(self, player):
        effect_handler = EffectHandler()
        effect_handler.handle_effect(self.effect, player)

class InstantCard(Card):
    def __init__(self, name, description, effect):
        super().__init__(name, description, effect)
        self.card_type = "instant"

    def play(self, player):
        effect_handler = EffectHandler()
        effect_handler.handle_effect(self.effect, player)


class UpgradeCard(Card):
    def __init__(self, name, description, effect):
        super().__init__(name, description, effect)
        self.card_type = "upgrade"

    def play(self, player):
        target_card = player.choose_card_from_stable()
        if target_card is not None:
            target_card.add_upgrade(self)
            
class DowngradeCard(Card):
    def __init__(self, name, description, effect):
        super().__init__(name, description, effect)
        self.card_type = "downgrade"

    def play(self, player):
        target_card = player.choose_card_from_stable()
        if target_card is not None:
            target_card.add_upgrade(self)
    
    
class Hand:
    def __init__(self):
        self.cards = []
        
    def __len__(self):
        return len(self.cards)

    def add_card(self, card):
        logging.debug("Adding card '" + str(card) + "' to Hand '" + str(self) + "'")
        self.cards.append(card)
        
    def remove_card(self, card):
        logging.debug("Removing card '" + str(card) + "' from Hand '" + str(self) + "'")
        self.cards.remove(card)

    
class Stable:
    def __init__(self):
        self.cards = []
        
    def __len__(self):
        return len(self.cards)

    def add_card(self, card):
        logging.debug("Adding card '" + str(card) + "' to Stable '" + str(self) + "'")
        if len(self.cards) < 7:
            self.cards.append(card)
        else:
            raise Exception("Stable is full")
        
    def remove_card(self, card):
        logging.debug("Removing card '" + str(card) + "' from Stable '" + str(self) + "'")
        self.cards.remove(card)
    
class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.shuffle()

    def shuffle(self):
        logging.debug("Shuffling Deck '" + str(self) + "'")
        random.shuffle(self.cards)

    def draw_card(self):
        card = self.cards.pop(0)
        logging.debug("Drawing card '" + str(card) + "' from Deck '" + str(self) + "'")
        return card

    def add_card(self, card):
        logging.debug("Adding card '" + str(card) + "' to Deck '" + str(self) + "'")
        self.cards.append(card)

    
class DiscardPile():
    def __init__(self):
        self.cards = []
        
    def add_card(self, card):
        logging.debug("Adding card '" + str(card) + "' to Discard Pile")
        self.cards.append(card)
        
        
# Create players
players = [
    Player("Alice"),
    Player("Bob")
]
game = Game(players)
game.initialize_game()
game.start_turn()
game.start_turn()