import random
import json
import logging



class EffectHandler:
    def __init__(self, game):
        self.game : Game = game
        
        
        # logging.info("Playing card '" + str(card) + "'")
        
        # # Remove the card from the player's hand and add it to the discard pile
        # self.current_player.remove_from_hand(card)
        # self.discard_pile.add_card(card)

        # # Resolve the card's effect
        # card.apply_effect(self.effect_handler)
        # #card.play()
        # self.effect_handler.handle_effect(card.effect, self.current_player)
        
        

    def handle_effect(self, card : 'Card'):
        
        logging.info("Applying effect '" + str(card.effect) + "'")

        if card.effect == "discard_unicorn_draw":
            card = self.game.current_player.stable.remove_card(self.game.current_player.stable.get_cards_by_type(UnicornCard)[0] or None)
            self.game.discard_pile.add_card(card)
            card = self.game.deck.draw_card()
            self.game.current_player.hand.add_card(card)
        elif card.effect == "max_5_unicorns_in_stable":
            if len(self.game.current_player.stable) > 5:
                card = self.game.current_player.stable.remove_card(self.game.current_player.stable.get_cards_by_type(UnicornCard)[0] or None)
                self.game.discard_pile.add_card(card)
        elif card.effect == "invincible_unicorns":
            cards = self.game.current_player.hand.get_cards_by_type(UnicornCard)
            cards.extend(self.game.current_player.stable.get_cards_by_type(UnicornCard))
            for card in cards:
                card.invincible = True
        elif card.effect == "unable_upgrade":
            cards = self.game.current_player.hand.get_cards_by_type(UpgradeCard)
            for card in cards:
                card.playable = False
        elif card.effect == "choose_top3_deck":
            cards : list[Card] = []
            for _ in range(3):
                card = self.game.deck.draw_card()
                cards.append(card)
            self.game.current_player.hand.add_card(cards.pop(0))
            self.game.deck.add_cards(cards)
            self.game.deck.shuffle()
        elif card.effect == "baby_unicorn_to_stable":
            card = self.game.nursery.draw_card()
            self.game.current_player.stable.add_card(card)
        elif card.effect == "discard_unicorn_unicorn_from_discard_pile":
            card = self.game.current_player.stable.remove_card(self.game.current_player.stable.get_cards_by_type(UnicornCard)[0] or None)
            self.game.discard_pile.add_card(card)
            card = self.game.discard_pile.remove_card(self.game.discard_pile.get_cards_by_type(UnicornCard)[0] or None)
            self.game.current_player.stable.add_card(card)
        elif card.effect == "destroy_upgrade_or_discard_downgrade":
            card = self.game.players[-1].stable.remove_card(self.game.players[-1].stable.get_cards_by_type(UpgradeCard)[0] or None)
            self.game.discard_pile.add_card(card)
            card = self.game.current_player.stable.remove_card(self.game.current_player.stable.get_cards_by_type(DowngradeCard)[0] or None)
            self.game.discard_pile.add_card(card)
        elif card.effect == "everyone_discard":
            for player in self.game.players:
                card = player.hand.remove_card(self.game.current_player.hand.cards[0])
                game.discard_pile.add_card(card)
            self.game.deck.add_cards(self.game.discard_pile.cards)
            self.game.discard_pile.clear()
            self.game.deck.shuffle()
        elif card.effect == "swap_stable":
            card1 = self.game.current_player.stable.remove_card(self.game.current_player.stable.cards[0])
            card2 = self.game.players[-1].stable.remove_card(self.game.current_player.stable.cards[0])
            self.game.current_player.stable.add_card(card2)
            self.game.players[-1].stable.add_card(card1)
        elif card.effect == "everyone_stable_to_hand":
            for player in self.game.players:
                card = player.stable.remove_card(self.game.current_player.stable.cards[0])
                player.hand.add_card(card)
        elif card.effect == "discard2_destroy_unicorn":
            for _ in range(2):
                card = self.game.current_player.hand.remove_card(self.game.current_player.hand.cards[0])
                self.game.discard_pile.add_card(card)
            self.game.players[-1].stable.remove_card(self.game.players[-1].stable.get_unicorn_cards()[0])
        elif card.effect == "discard_draw":
            card = self.game.current_player.hand.remove_card(self.game.current_player.hand.cards[0])
            self.game.discard_pile.add_card(card)
            card = self.game.deck.draw_card()
            self.game.current_player.hand.add_card(card)
        
class Card:
    def __init__(self, name, image, effect, effect_trigger):
        self.name : str = name
        self.image : str = image
        self.effect : str = effect
        self.effect_trigger : str = effect_trigger
        self.card_type : str = None
        self.playable : bool = True
        self.invincible : bool = False
        
    def __repr__(self):
        return self.name + " (" + self.card_type + ")"
        

class Player:
    def __init__(self, name):
        self.name : str = name
        self.hand : Hand = Hand()
        self.stable : Stable = Stable()
        
    def __repr__(self):
        return self.name

    def add_to_hand(self, card : Card):
        logging.debug("Adding card '" + str(card) + "' to hand of player '" + str(self) + "'")
        self.hand.add_card(card)

    def remove_from_hand(self, card : Card):
        logging.debug("Removing card '" + str(card) + "' from hand of player '" + str(self) + "'")
        self.hand.remove_card(card)
        
    def add_to_stable(self, card : Card):
        logging.debug("Adding card '" + str(card) + "' to stable of player '" + str(self) + "'")
        self.stable.add_card(card)

    def remove_from_stable(self, card : Card):
        logging.debug("Removing card '" + str(card) + "' from stable of player '" + str(self) + "'")
        self.stable.remove_card(card)
  

class UnicornCard(Card):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
                
class BasicUnicornCard(UnicornCard):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "basic_unicorn"

    def play(self, player : Player):
        player.add_to_stable(self)
        
class BabyUnicornCard(UnicornCard):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "baby_unicorn"

    def play(self, player : Player):
        player.add_to_stable(self)

class MagicalUnicornCard(UnicornCard):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "magical_unicorn"

    def play(self, player : Player):
        player.add_to_stable(self)
        player.check_for_unicorns_with_trigger_effect()

class MagicCard(Card):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "magic"

    def play(self, player : Player):
        effect_handler = EffectHandler()
        effect_handler.handle_effect(self.effect, player)

class InstantCard(Card):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "instant"

    def play(self, player : Player):
        effect_handler = EffectHandler()
        effect_handler.handle_effect(self.effect, player)


class UpgradeCard(Card):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "upgrade"

    def play(self, player : Player):
        target_card = player.choose_card_from_stable()
        if target_card is not None:
            target_card.add_upgrade(self)
            
class DowngradeCard(Card):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "downgrade"

    def play(self, player : Player):
        target_card = player.choose_card_from_stable()
        if target_card is not None:
            target_card.add_upgrade(self)
    
    
    
class CardSpace:
    def __init__(self, cards=None):
        if cards == None:
            cards = []
        self.cards : list[Card] = cards
        
    def __len__(self) -> int:
        return len(self.cards)
    
    def __repr__(self) -> str:
        return str(self.cards)
    
    def add_card(self, card : Card):
        self.cards.append(card)
    
    def add_cards(self, cards : 'list[Card]'):
        for card in cards:
            self.add_card(card)
            
    def clear(self):
        self.cards.clear()
        
    def get_cards(self):
        return self.cards

    def remove_card(self, card : Card):
        self.cards.remove(card)
        return card
        
    def get_cards_by_type(self, type):
        cards = []
        for card in self.cards:
            if isinstance(card, type):
                cards.append(card)
        return cards

    
class Hand(CardSpace):
    def __init__(self, cards=None):
        super().__init__(cards)
        
    def add_card(self, card):
        if isinstance(card, BabyUnicornCard):
            logging.error("Failed to add card '" + str(card) + "' to Hand")
            raise Exception("Failed to add card '" + str(card) + "' to Hand. Baby Unicorn cards can only be added to a Stable or the Nursery!")
        self.cards.append(card) 
    
class Stable(CardSpace):
    def __init__(self, cards=None):
        super().__init__(cards)
        
    def add_card(self, card):
        if len(self.cards) < 7:
            self.cards.append(card)
        else:
            raise Exception("Stable is full")
        
    def get_unicorn_count(self):
        count = 0
        for card in self.cards:
            if isinstance(card, UnicornCard):
                count = count + 1
        return count
    
class Deck(CardSpace):
    def __init__(self, cards=None):
        super().__init__(cards)

    def shuffle(self):
        logging.debug("Shuffling Deck")
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        card = self.cards.pop(0)
        logging.debug("Drawing card '" + str(card) + "' from Deck")
        return card

    def add_card(self, card : Card):
        logging.debug("Adding card '" + str(card) + "' to Deck")
        if isinstance(card, BabyUnicornCard):
            logging.error("Failed to add card '" + str(card) + "' to Deck")
            raise Exception("Failed to add card '" + str(card) + "' to Deck. Baby Unicorn cards can only be added to a Stable or the Nursery!")
        self.cards.append(card)

class DiscardPile(CardSpace): 
    def __init__(self, cards=None):
        super().__init__(cards)
              
    def add_card(self, card : Card):
        logging.debug("Adding card '" + str(card) + "' to Discard Pile")
        if isinstance(card, BabyUnicornCard):
            logging.error("Failed to add card '" + str(card) + "' to Discard Pile")
            raise Exception("Failed to add card '" + str(card) + "' to Discard Pile. Baby Unicorn cards can only be added to a Stable or the Nursery!")
        self.cards.append(card)
        
class Nursery(CardSpace):
    def __init__(self, cards=None):
        super().__init__(cards)
        
    def draw_card(self) -> Card:
        card = self.cards.pop(0)
        logging.debug("Drawing card '" + str(card) + "' from Nursery '" + str(self) + "'")
        return card

    def add_card(self, card : Card):
        logging.debug("Adding card '" + str(card) + "' to Nursery '" + str(self) + "'")
        if not isinstance(card, BabyUnicornCard):
            logging.error("Failed to add card '" + str(card) + "' to Nursery")
            raise Exception("Failed to add card '" + str(card) + "' to Nursery. Can only add Baby Unicorn cards!")
        self.cards.append(card)
        
        
        

class Game:
    def __init__(self, players):
        self.players : list[Player] = players
        self.current_player : Player = None
        
        self.effect_handler : EffectHandler = None

        self.deck : Deck = None
        self.discard_pile : DiscardPile = None
        self.nursery : Nursery = None

    def initialize_game(self):
        # Initialise logging
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)8s | %(lineno)4s | %(message)s')
        logging.info("Initialising game")

        # Initialise classes
        self.effect_handler = EffectHandler(self)
        self.discard_pile = DiscardPile()
        
        # Read all cards from JSON and put in deck
        with open('cards.json', 'r') as file:
            file_contents = file.read()
            cards = json.loads(file_contents)
            card_objs = []
            baby_unicorn_objs = []
            
            for card in cards:
                if card['type'] == "BABY_UNICORN":
                    card_obj = BabyUnicornCard(card['name'], card['image'], card['effect'], card['effect_trigger'])
                    baby_unicorn_objs.append(card_obj)
                    continue
                    
                elif card['type'] == "MAGICAL_UNICORN":
                    card_obj = MagicalUnicornCard(card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "NORMAL_UNICORN":
                    card_obj = BasicUnicornCard(card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "UPGRADE":
                    card_obj = UpgradeCard(card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "DOWNGRADE":
                    card_obj = DowngradeCard(card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "MAGIC":
                    card_obj = MagicCard(card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "INSTANT":
                    card_obj = InstantCard(card['name'], card['image'], card['effect'], card['effect_trigger'])
                    
                card_objs.append(card_obj)
                
            self.deck = Deck(card_objs)
            self.nursery = Nursery(baby_unicorn_objs)

        logging.info("Dealing cards")
        # Shuffle the deck and deal 5 cards to each player
        self.deck.shuffle()
        for player in self.players:
            for _ in range(5):
                card = self.deck.draw_card()
                player.add_to_hand(card)
                
        # Place 1 baby unicorn card in each player's stable
        for player in self.players:
            card = self.nursery.draw_card()
            player.add_to_stable(card)

        # Determine the starting player
        self.current_player = self.players[0]
        
        logging.info("Game initialised!")
        logging.info("---")

    def start_turn(self):
        logging.info("Starting turn")
        
        logging.info("Current player is '" + str(self.current_player) + "'")
        logging.info("Player has stable '" + str(self.current_player.stable) + "'")
        logging.info("Player has hand '" + str(self.current_player.hand) + "'")
        
        # Phase 1: Apply effects in stable that trigger on the beginning of turn
        logging.info("Turn phase 1: Apply effects in stable")
        for card in self.current_player.stable.get_cards():
            if card.effect_trigger == "on_turn_begin":
                card.apply_effect(self.effect_handler)

        # Phase 2: Draw a card and add it to the current player's hand
        logging.info("Turn phase 2: Draw from Deck")
        card = self.deck.draw_card()
        self.current_player.add_to_hand(card)
        
        # Phase 3: Play or draw a card
        logging.info("Turn phase 3: Play or Draw")
        card = self.current_player.hand.cards[0]
        logging.info("Player selected " + str(card))
        if isinstance(card, MagicCard):
            # If card is a Magic card, apply effect and move card to discard pile
            self.effect_handler.handle_effect(card)
            self.current_player.remove_from_hand(card)
            self.discard_pile.add_card(card)
        elif isinstance(card, MagicalUnicornCard):
            # If card is a Magical Unicorn card, move card to stable and apply effect
            self.current_player.remove_from_hand(card)
            self.current_player.stable.add_card(card)
            self.effect_handler.handle_effect(card)
        elif isinstance(card, (DowngradeCard, UpgradeCard)):
            # If card is Upgrade or Downgrade, move card to selected player stable
            self.current_player.remove_from_hand(card)
            self.current_player.add_to_stable(card)
        elif isinstance(card, BasicUnicornCard):
            # If card is Basic Unicorn, move card to stable
            self.current_player.remove_from_hand(card)
            self.current_player.add_to_stable(card)
        
        # Phase 4: Discard until hand does not exceed 7 cards
        logging.info("Turn phase 4: Discard until max 7")
        while len(self.current_player.hand) > 7:
            self.current_player.hand.remove_card(self.current_player.hand.cards[0])
            
            
        # Check for victory conditions
        if self.current_player.stable.get_unicorn_count() >= 7:
            print(f"{self.current_player.name} wins!")
            exit()
        # Hand turn to next player
        self.next_player()

    def next_player(self):
        # Find the next player in the list of players
        current_index = self.players.index(self.current_player)
        next_index = (current_index + 1) % len(self.players)
        self.current_player = self.players[next_index]
        logging.info("Advancing player '" + str(self.players[current_index]) + "' to '" + str(self.players[next_index]) + "'")
        logging.info("---")
        
    # def get_player_input(self, prompt, valid_inputs):
    #     # Helper function to get input from the current player
    #     while True:
    #         user_input = input(prompt).lower()
    #         if user_input in valid_inputs:
    #             return user_input
    #         print("Invalid input. Please try again.")

    # def choose_card_from_hand(self):
    #     # Ask the current player to choose a card from their hand
    #     prompt = f"{self.current_player.name}, choose a card from your hand: "
    #     valid_inputs = [str(i+1) for i in range(len(self.current_player.hand))]
    #     index = int(self.get_player_input(prompt, valid_inputs)) - 1
    #     return self.current_player.hand[index]

    # def choose_card_from_stable(self):
    #     # Ask the current player to choose a card from their stable
    #     prompt = f"{self.current_player.name}, choose a card from your stable: "
    #     valid_inputs = [str(i+1) for i in range(len(self.current_player.stable))]
    #     index = int(self.get_player_input(prompt, valid_inputs)) - 1
    #     return self.current_player.stable[index]

    # def choose_player(self):
    #     # Ask the current player to choose another player
    #     prompt = f"{self.current_player.name}, choose another player: "
    #     valid_inputs = [str(i+1) for i in range(len(self.players)) if self.players[i] != self.current_player]
    #     index = int(self.get_player_input(prompt, valid_inputs)) - 1
    #     return self.players[index]
            
            



        
        
        
        
# Create players
players = [
    Player("Alice"),
    Player("Bob")
]

game = Game(players)
game.initialize_game()
game.start_turn()
game.start_turn()
