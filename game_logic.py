import random
import json
import logging
from typing import Type
import inquirer


class EffectHandler:
    def __init__(self, game):
        self.game: Game = game

    def handle_effect(self, card: 'Card'):

        logging.info("Applying effect '%s'", card.effect)

        if card.effect == "discard_unicorn_draw":
            card = self.game.ui.select_card("Please select a Unicorn card to discard",
                                            self.game.current_player.stable.get_cards_by_class_type(UnicornCard))
            if card == None:
                return
            self.game.current_player.stable.remove_card(card)
            self.game.discard_pile.add_card(card)
            card = self.game.deck.draw_card()
            self.game.current_player.hand.add_card(card)
        elif card.effect == "max_5_unicorns_in_stable":
            if len(self.game.current_player.stable) > 5:
                card = self.game.ui.select_card("You have more than 5 cards in your stable. Please select a Unicorn card to discard",
                                                self.game.current_player.stable.get_cards_by_class_type(UnicornCard))
                if card == None:
                    return
                self.game.current_player.stable.remove_card(card)
                self.game.discard_pile.add_card(card)
        elif card.effect == "invincible_unicorns":
            # TODO
            cards = self.game.current_player.hand.get_cards_by_class_type(
                UnicornCard)
            cards.extend(
                self.game.current_player.stable.get_cards_by_class_type(UnicornCard))
            for card in cards:
                card.invincible = True
        elif card.effect == "unable_upgrade":
            # TODO
            cards = self.game.current_player.hand.get_cards_by_class_type(
                UpgradeCard)
            for card in cards:
                card.playable = False
        elif card.effect == "choose_top3_deck":
            cards: 'list[Card]' = []
            for _ in range(3):
                card = self.game.deck.draw_card()
                cards.append(card)
            card = self.game.ui.select_card(
                "Please choose one of 3 cards from the top of the deck", cards)
            cards.remove(card)
            self.game.current_player.hand.add_card(card)
            self.game.deck.add_cards(cards)
            self.game.deck.shuffle()
        elif card.effect == "baby_unicorn_to_stable":
            card = self.game.nursery.draw_card()
            self.game.current_player.stable.add_card(card)
        elif card.effect == "discard_unicorn_unicorn_from_discard_pile":
            card = self.game.ui.select_card("Please select Unicorn card to discard",
                                            self.game.current_player.stable.get_cards_by_class_type(UnicornCard))
            if card == None:
                return
            self.game.current_player.stable.remove_card(card)
            self.game.discard_pile.add_card(card)
            card = self.game.ui.select_card("Please choose a Unicorn card from the discard pile you wish to take",
                                            self.game.discard_pile.get_cards_by_class_type(UnicornCard))
            if card == None:
                return
            self.game.discard_pile.remove_card(card)
            self.game.current_player.stable.add_card(card)
        elif card.effect == "destroy_upgrade_or_discard_downgrade":
            options = ["Destroy Upgrade Card from a Player",
                       "Remove a Downgrade Card from your Stable"]
            option = self.game.ui.select_option(
                "Please make your choice", options)
            if option == options[0]:
                player = self.game.ui.select_player(
                    "Please choose a player to apply the effect to", self.game.players)
                card = self.game.ui.select_card("Please select a card to destroy",
                                                player.stable.get_cards_by_class_type(UpgradeCard))
                if card == None:
                    return
                player.stable.remove_card(card)
                self.game.discard_pile.add_card(card)
            else:
                card = self.game.ui.select_card("Please select a card to discard",
                                                self.game.current_player.stable.get_cards_by_class_type(DowngradeCard))
                if card == None:
                    return
                self.game.current_player.stable.remove_card(card)
                self.game.discard_pile.add_card(card)
        elif card.effect == "everyone_discard":
            for player in self.game.players:
                card = self.game.ui.select_card(str(player) + ", please select a card to discard",
                                                self.game.current_player.hand.get_cards())
                if card == None:
                    return
                player.hand.remove_card(card)
                self.game.discard_pile.add_card(card)
            self.game.deck.add_cards(self.game.discard_pile.cards)
            self.game.discard_pile.clear()
            self.game.deck.shuffle()
        elif card.effect == "swap_stable":
            card1 = self.game.ui.select_card("Please select a card to swap with another player",
                                             self.game.current_player.stable.get_cards())
            if card1 == None:
                return
            self.game.current_player.stable.remove_card(card1)
            player = self.game.ui.select_player(
                "Please select player you wish to swap the card with", self.game.players)
            card2 = self.game.ui.select_card(
                "Please select a card from the players stable you want to swap with your card", player.stable.get_cards())
            if card2 == None:
                return
            player.stable.remove_card(card2)
            self.game.current_player.stable.add_card(card2)
            player.stable.add_card(card1)
        elif card.effect == "everyone_stable_to_hand":
            for player in self.game.players:
                card = self.game.ui.select_card(str(player) + ", please select a card to move to your hand",
                                                self.game.current_player.stable.get_cards())
                if card == None:
                    return
                player.stable.remove_card(card)
                player.hand.add_card(card)
        elif card.effect == "discard2_destroy_unicorn":
            for _ in range(2):
                card = self.game.ui.select_card("Please select a card to discard",
                                                self.game.current_player.hand.get_cards())
                if card == None:
                    return
                self.game.current_player.hand.remove_card(card)
                self.game.discard_pile.add_card(card)
            player = self.game.ui.select_player(
                "Please select a player to apply the effect to", self.game.players)
            card = self.game.ui.select_card("Please select a Unicorn card to destroy",
                                            player.stable.get_cards_by_class_type(UnicornCard))
            if card == None:
                return
            player.stable.remove_card(card)
        elif card.effect == "discard_draw":
            card = self.game.ui.select_card("Please select a card to discard",
                                            self.game.current_player.hand.get_cards())
            if card == None:
                return
            self.game.current_player.hand.remove_card(card)
            self.game.discard_pile.add_card(card)
            card = self.game.deck.draw_card()
            self.game.current_player.hand.add_card(card)


class Card:
    def __init__(self, name, image, effect, effect_trigger):
        self.name: str = name
        self.image: str = image
        self.effect: str = effect
        self.effect_trigger: str = effect_trigger
        self.card_type: str = None
        self.playable: bool = True
        self.invincible: bool = False

    def __repr__(self):
        return self.name + " (" + self.card_type + ")"


class Player:
    def __init__(self, name):
        self.name: str = name
        self.hand: Hand = Hand()
        self.stable: Stable = Stable()

    def __repr__(self):
        return self.name

    def add_to_hand(self, card: Card):
        logging.debug("Adding card '%s' to hand of player '%s'", card, self)
        self.hand.add_card(card)

    def remove_from_hand(self, card: Card):
        logging.debug(
            "Removing card '%s' from hand of player '%s'", card, self)
        self.hand.remove_card(card)

    def add_to_stable(self, card: Card):
        logging.debug("Adding card '%s' to stable of player '%s'", card, self)
        self.stable.add_card(card)

    def remove_from_stable(self, card: Card):
        logging.debug(
            "Removing card '%s' from stable of player '%s'", card, self)
        self.stable.remove_card(card)


class UnicornCard(Card):
    pass


class BasicUnicornCard(UnicornCard):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "basic_unicorn"


class BabyUnicornCard(UnicornCard):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "baby_unicorn"


class MagicalUnicornCard(UnicornCard):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "magical_unicorn"


class MagicCard(Card):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "magic"


class InstantCard(Card):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "instant"


class UpgradeCard(Card):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "upgrade"


class DowngradeCard(Card):
    def __init__(self, name, image, effect, effect_trigger):
        super().__init__(name, image, effect, effect_trigger)
        self.card_type = "downgrade"


class CardSpace:
    def __init__(self, cards=None):
        if cards == None:
            cards = []
        self.cards: 'list[Card]' = cards

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return str(self.cards)

    def add_card(self, card: Card):
        self.cards.append(card)

    def add_cards(self, cards: 'list[Card]'):
        for card in cards:
            self.add_card(card)

    def clear(self):
        self.cards.clear()

    def get_cards(self):
        return self.cards

    def remove_card(self, card: Card):
        self.cards.remove(card)
        return card

    def get_cards_by_class_type(self, class_type: Type[Card]):
        cards = []
        for card in self.cards:
            if isinstance(card, class_type):
                cards.append(card)
        return cards


class Hand(CardSpace):
    def add_card(self, card):
        if isinstance(card, BabyUnicornCard):
            logging.error("Failed to add card '%s' to Hand", card)
            raise RuntimeError("Failed to add card '" + str(card) +
                               "' to Hand. Baby Unicorn cards can only be added to a Stable or the Nursery!")
        self.cards.append(card)


class Stable(CardSpace):
    def add_card(self, card):
        if len(self.cards) < 7:
            self.cards.append(card)
        else:
            raise RuntimeError("Stable is full")

    def get_unicorn_count(self):
        count = 0
        for card in self.cards:
            if isinstance(card, UnicornCard):
                count = count + 1
        return count


class Deck(CardSpace):
    def shuffle(self):
        logging.debug("Shuffling Deck")
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        card = self.cards.pop(0)
        logging.debug("Drawing card '%s' from Deck", card)
        return card

    def add_card(self, card: Card):
        logging.debug("Adding card '%s' to Deck", card)
        if isinstance(card, BabyUnicornCard):
            logging.error("Failed to add card '%s' to Deck", card)
            raise RuntimeError("Failed to add card '" + str(card) +
                               "' to Deck. Baby Unicorn cards can only be added to a Stable or the Nursery!")
        self.cards.append(card)


class DiscardPile(CardSpace):
    def add_card(self, card: Card):
        logging.debug("Adding card '%s' to Discard Pile", card)
        if isinstance(card, BabyUnicornCard):
            logging.error("Failed to add card '%s' to Discard Pile", card)
            raise RuntimeError("Failed to add card '" + str(card) +
                               "' to Discard Pile. Baby Unicorn cards can only be added to a Stable or the Nursery!")
        self.cards.append(card)


class Nursery(CardSpace):
    def draw_card(self) -> Card:
        card = self.cards.pop(0)
        logging.debug("Drawing card '%s' from Nursery '%s'", card, self)
        return card

    def add_card(self, card: Card):
        logging.debug("Adding card '%s' to Nursery '%s'", card, self)
        if not isinstance(card, BabyUnicornCard):
            logging.error("Failed to add card '%s' to Nursery", card)
            raise RuntimeError("Failed to add card '" + str(card) +
                               "' to Nursery. Can only add Baby Unicorn cards!")
        self.cards.append(card)


class Game:
    def __init__(self, ui, players):
        self.ui: UI = ui
        self.players: 'list[Player]' = players

        self.effect_handler: EffectHandler = None
        self.current_player: Player = None

        self.deck: Deck = None
        self.discard_pile: DiscardPile = None
        self.nursery: Nursery = None

    def initialize_game(self):
        # Initialise logging
        logging.basicConfig(
            level=logging.INFO, format='%(levelname)8s | %(lineno)4s | %(message)s')
        logging.info("Initialising game")

        # Initialise classes
        self.effect_handler = EffectHandler(self)
        self.discard_pile = DiscardPile()

        # Read all cards from JSON and put in deck
        with open('cards.json', 'r', encoding='utf-8') as file:
            file_contents = file.read()
            cards = json.loads(file_contents)
            card_objs = []
            baby_unicorn_objs = []

            for card in cards:
                if card['type'] == "BABY_UNICORN":
                    card_obj = BabyUnicornCard(
                        card['name'], card['image'], card['effect'], card['effect_trigger'])
                    baby_unicorn_objs.append(card_obj)
                    continue

                elif card['type'] == "MAGICAL_UNICORN":
                    card_obj = MagicalUnicornCard(
                        card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "NORMAL_UNICORN":
                    card_obj = BasicUnicornCard(
                        card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "UPGRADE":
                    card_obj = UpgradeCard(
                        card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "DOWNGRADE":
                    card_obj = DowngradeCard(
                        card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "MAGIC":
                    card_obj = MagicCard(
                        card['name'], card['image'], card['effect'], card['effect_trigger'])
                elif card['type'] == "INSTANT":
                    card_obj = InstantCard(
                        card['name'], card['image'], card['effect'], card['effect_trigger'])

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

        logging.info("Current player is '%s'", self.current_player)
        logging.info("Player has stable '%s'", self.current_player.stable)
        logging.info("Player has hand '%s'", self.current_player.hand)

        # Phase 1: Apply effects in stable that trigger on the beginning of turn
        logging.info("Turn phase 1: Apply effects in stable")
        for card in self.current_player.stable.get_cards():
            if card.effect_trigger == "on_turn_begin":
                self.effect_handler.handle_effect(card)

        # Phase 2: Draw a card and add it to the current player's hand
        logging.info("Turn phase 2: Draw from Deck")
        card = self.deck.draw_card()
        self.current_player.add_to_hand(card)

        # Phase 3: Play or draw a card
        logging.info("Turn phase 3: Play or Draw")
        options = ["Play a card", "Draw a card"]
        option = self.ui.select_option(
            "Do you want to play a card or draw a card?", options)
        if option == options[0]:
            card = self.ui.select_card(
                "Please pick a card to play", self.current_player.hand.get_cards())
            logging.info("Player selected %s", card)
            if isinstance(card, MagicCard):
                # If card is a Magic card, apply effect and move card to discard pile
                self.current_player.remove_from_hand(card)
                self.discard_pile.add_card(card)
                self.effect_handler.handle_effect(card)
            elif isinstance(card, MagicalUnicornCard):
                # If card is a Magical Unicorn card, move card to stable and apply effect
                self.current_player.remove_from_hand(card)
                self.current_player.stable.add_card(card)
                self.effect_handler.handle_effect(card)
            elif isinstance(card, (DowngradeCard, UpgradeCard)):
                # If card is Upgrade or Downgrade, move card to selected player stable
                player = self.ui.select_player(
                    "Please choose a player to put the Up/Downgrade card in their stable", self.players)
                self.current_player.remove_from_hand(card)
                player.add_to_stable(card)
            elif isinstance(card, BasicUnicornCard):
                # If card is Basic Unicorn, move card to stable
                self.current_player.remove_from_hand(card)
                self.current_player.add_to_stable(card)
        else:
            card = self.deck.draw_card()
            self.current_player.add_to_hand(card)

        # Phase 4: Discard until hand does not exceed 7 cards
        logging.info("Turn phase 4: Discard until max 7")
        while len(self.current_player.hand) > 7:
            self.current_player.hand.remove_card(
                self.current_player.hand.cards[0])

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
        logging.info("Advancing player '%s' to '%s'",
                     self.players[current_index], self.players[next_index])
        logging.info("---")


class UI:
    def __init__(self) -> None:
        pass

    def display_error(self, message: str):
        pass

    def display_message(self, message: str):
        pass

    def select_card(self, message: str, cards: 'list[Card]') -> 'Card':
        pass

    def select_player(self, message: str, players: 'list[Player]') -> 'Player':
        pass

    def select_option(self, message: str, options: 'list[str]') -> str:
        pass


class CLI(UI):

    def display_error(self, message: str):
        logging.error(message)

    def display_message(self, message: str):
        logging.info(message)

    def select_card(self, message: str, cards: 'list[Card]') -> 'Card':
        if len(cards) == 0:
            logging.warning("There are no valid Cards to select from")
            return

        questions = [
            inquirer.List('card',
                          message=message,
                          choices=cards,
                          ),
        ]
        answers = inquirer.prompt(questions)
        return answers["card"]

    def select_player(self, message: str, players: 'list[Player]') -> 'Player':
        if len(players) == 0:
            logging.warning("There are no valid Players to select from")
            return

        questions = [
            inquirer.List('player',
                          message=message,
                          choices=players,
                          ),
        ]
        answers = inquirer.prompt(questions)
        return answers["player"]

    def select_option(self, message: str, options: 'list[str]') -> str:
        if len(options) == 0:
            logging.warning("There are no valid Options to select from")
            return

        questions = [
            inquirer.List('option',
                          message=message,
                          choices=options,
                          ),
        ]
        answers = inquirer.prompt(questions)
        return answers["option"]


def main():
    players = [
        Player("Wout"),
        Player("Semih"),
        Player("Daan")
    ]

    ui = CLI()
    game = Game(ui, players)

    game.initialize_game()

    while True:
        game.start_turn()


main()
