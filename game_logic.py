import random
import json
import logging
from typing import Type
import inquirer
import arcade
import arcade.gui
from pyglet.image import load as pyglet_load


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

    def update(self):
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



SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()

class GUI(arcade.Window, UI):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Unstable Unicorns", resizable=False, fullscreen=True)
        self.set_icon(pyglet_load("images/icon.png"))

        players = [
            Player("Wout"),
            Player("Semih"),
            Player("Daan"),
        ]
        self.game = Game(self, players)

        menu_view = MainMenuView(self.game)
        self.show_view(menu_view)
        arcade.run()


class MainMenuView(arcade.View):
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.manager = arcade.gui.UIManager()
        self.player = None
        self.music = None
        
        self.texture = None

    def on_show(self):
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.texture = arcade.load_texture("images/background.jpg")

        center_box = arcade.gui.UIBoxLayout()
        bottom_box = arcade.gui.UIBoxLayout()

        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.AMETHYST,

            "bg_color_pressed": arcade.color.BRIGHT_LILAC,
            "border_color_pressed": arcade.color.WHITE,
            "font_color_pressed": arcade.color.BLACK,
        }

        ui_text_label = arcade.gui.UITextArea(
            text="Unstable Unicorns",
            width=568,
            height=60,
            font_size=32,
            font_name="Kenney Future",
            text_color=arcade.color.AMETHYST
        )
        center_box.add(ui_text_label.with_space_around(bottom=60))

        start_button = arcade.gui.UIFlatButton(
            text="Spel starten", width=200, style=default_style)
        start_button.on_click = self.on_click_start
        center_box.add(start_button.with_space_around(bottom=20))

        exit_button = arcade.gui.UIFlatButton(
            text="Afsluiten", width=200, style=default_style)
        exit_button.on_click = self.on_click_exit
        center_box.add(exit_button.with_space_around(bottom=20))

        ui_text_label = arcade.gui.UITextArea(
            text="Semih Barmaksiz, Wout Rombouts",
            width=226,
            height=20,
            font_size=8,
            font_name="Kenney Future",
            text_color=arcade.color.GRAY
        )
        bottom_box.add(ui_text_label.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=center_box)
        )

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                child=bottom_box)
        )

        self.music = arcade.Sound("sounds/soundtrack.mp3", streaming=True)
        self.player = self.music.play(0.3)

    def on_click_start(self, event):
        self.game.initialize_game()
        game_view = GameView(self.game)
        self.window.show_view(game_view)
        self.manager.disable()
        self.music.stop(self.player)

    def on_click_exit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        self.manager.draw()


class PauseMenuView(arcade.View):
    def __init__(self, game: Game):
        super().__init__()
        self.game = game

        self.texture = None
        self.buttons = []
        self.manager = arcade.gui.UIManager()

    def on_show(self):
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.texture = arcade.load_texture("images/background.jpg")

        center_box = arcade.gui.UIBoxLayout()
        bottom_box = arcade.gui.UIBoxLayout()

        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.AMETHYST,

            "bg_color_pressed": arcade.color.BRIGHT_LILAC,
            "border_color_pressed": arcade.color.WHITE,
            "font_color_pressed": arcade.color.BLACK,
        }

        ui_text_label = arcade.gui.UITextArea(
            text="Spel gepauzeerd",
            width=568,
            height=60,
            font_size=32,
            font_name="Kenney Future",
            text_color=arcade.color.AMETHYST
        )
        center_box.add(ui_text_label.with_space_around(bottom=60))

        start_button = arcade.gui.UIFlatButton(
            text="Hervatten", width=200, style=default_style)
        start_button.on_click = self.on_click_resume
        center_box.add(start_button.with_space_around(bottom=20))

        exit_button = arcade.gui.UIFlatButton(
            text="Afsluiten", width=200, style=default_style)
        exit_button.on_click = self.on_click_exit
        center_box.add(exit_button.with_space_around(bottom=20))

        ui_text_label = arcade.gui.UITextArea(
            text="Semih Barmaksiz, Wout Rombouts",
            width=226,
            height=20,
            font_size=8,
            font_name="Kenney Future",
            text_color=arcade.color.GRAY
        )
        bottom_box.add(ui_text_label.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=center_box)
        )

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                child=bottom_box)
        )

    def on_click_resume(self, event):
        game_view = GameView(self.game)
        self.window.show_view(game_view)
        self.manager.disable()

    def on_click_exit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        self.manager.draw()


PILE_COUNT = 27
PILE_OPPONENT_A_1 = 1
PILE_OPPONENT_A_2 = 2
PILE_OPPONENT_A_3 = 3
PILE_OPPONENT_A_4 = 4
PILE_OPPONENT_A_5 = 5
PILE_OPPONENT_A_6 = 6
PILE_OPPONENT_A_7 = 7
PILE_OPPONENT_B_1 = 8
PILE_OPPONENT_B_2 = 9
PILE_OPPONENT_B_3 = 10
PILE_OPPONENT_B_4 = 11
PILE_OPPONENT_B_5 = 12
PILE_OPPONENT_B_6 = 13
PILE_OPPONENT_B_7 = 14
PILE_TABLE_1 = 15
PILE_TABLE_2 = 16
PILE_TABLE_3 = 17
PILE_OWN_1 = 18
PILE_OWN_2 = 19
PILE_OWN_3 = 20
PILE_OWN_4 = 21
PILE_OWN_5 = 22
PILE_OWN_6 = 23
PILE_OWN_7 = 24
PILE_OWN_8 = 25
PILE_OWN_9 = 26
PILE_OWN_10 = 27

MAT_FACTOR = 1.25
MAT_HEIGHT = 128 * MAT_FACTOR
MAT_WIDTH = 92 * MAT_FACTOR

X_FACTOR = 0.01 * SCREEN_WIDTH
Y_FACTOR = X_FACTOR / 92 * 128

Y1 = SCREEN_HEIGHT - MAT_HEIGHT / 2 - Y_FACTOR
Y2 = Y1 - MAT_HEIGHT - Y_FACTOR
Y3 = SCREEN_HEIGHT / 7 * 3
Y4 = MAT_HEIGHT / 2 + Y_FACTOR

X1 = MAT_WIDTH / 2 + X_FACTOR
X3 = ((SCREEN_WIDTH - 3 * MAT_WIDTH - 2 * X_FACTOR) + MAT_WIDTH) / 2
X4 = ((SCREEN_WIDTH - 10 * MAT_WIDTH - 9 * X_FACTOR) + MAT_WIDTH) / 2


class TestCard(arcade.Sprite):
    def __init__(self, group, number, scale = 0.12):
        self.group = group
        self.number = number
        self.image_file_name = "images/all_cards_lowres/"+self.group+"-"+self.number+".jpg"
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")

    def getGroup(self):
        return self.group

    def getNumber(self):
        return self.number

class GameView(arcade.View):

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.texture = None
        self.manager = arcade.gui.UIManager()
        self.background = arcade.load_texture("images/background.jpg")
        self.card_list = None
        self.held_cards = None
        self.held_card_original_position = None
        self.v_box = None
        self.pile_mat_list = None
        self.piles = None
        
        self.setup()
        
    def on_show(self):

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = None

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_card_original_position = None

        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        self.piles = None

        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.AMETHYST,
            "bg_color_pressed": arcade.color.BRIGHT_LILAC,
            "border_color_pressed": arcade.color.WHITE,
            "font_color_pressed": arcade.color.BLACK,
        }

        spelregels_button = arcade.gui.UIFlatButton(text="Spelregels", width=200, style=default_style)
        self.v_box.add(spelregels_button.with_space_around(bottom=10))

        exit_button = arcade.gui.UIFlatButton(text="Afsluiten", width=200, style=default_style)
        self.v_box.add(exit_button.with_space_around(bottom=10))

        @spelregels_button.event("on_click")
        def on_click_settings(event):
            print("Start:", event)

        @exit_button.event("on_click")
        def on_click_settings(event):
            arcade.exit()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="top",
                child=self.v_box)
        )
        
    def setup(self):
        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        # Create every card
        for i in range(1,14):
            card = TestCard("baby-eenhoorn" , str(i))
            card.position = 500, 500
            self.card_list.append(card)
            
        # Sprite list with all the mats the cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        self.piles = [[] for _ in range(PILE_COUNT)]

        #for card in self.card_list:
        #    self.piles[PILE_TABLE_1].append(card)

        for i in range(7):
            pile = arcade.SpriteSolidColor(int(MAT_WIDTH), int(MAT_HEIGHT), arcade.color.BRIGHT_LILAC)
            pile.position = X1 + i * (MAT_WIDTH + X_FACTOR), Y1
            self.pile_mat_list.append(pile)

        for i in range(7):
            pile = arcade.SpriteSolidColor(int(MAT_WIDTH), int(MAT_HEIGHT), arcade.color.BRIGHT_LILAC)
            pile.position = X1 + i * (MAT_WIDTH + X_FACTOR), Y2
            self.pile_mat_list.append(pile)

        for i in range(3):
            pile = arcade.SpriteSolidColor(int(MAT_WIDTH), int(MAT_HEIGHT), arcade.color.BRIGHT_LILAC)
            pile.position = X3 + i * (MAT_WIDTH + X_FACTOR) , Y3
            self.pile_mat_list.append(pile)

        for i in range(10):
            pile = arcade.SpriteSolidColor(int(MAT_WIDTH), int(MAT_HEIGHT), arcade.color.BRIGHT_LILAC)
            pile.position = X4 + i * (MAT_WIDTH + X_FACTOR), Y4
            self.pile_mat_list.append(pile)
        #print(self.pile_mat_list)
    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

        self.manager.draw()

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Might be a stack of cards, get the top one
            primary_card = cards[-1]

            # All other cases, grab the face-up card we are clicking on
            self.held_cards = [primary_card]
            # Save the position
            self.held_cards_original_position = [self.held_cards[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_cards[0])

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            # For each held card, move it to the pile we dropped on
            for i, dropped_card in enumerate(self.held_cards):
                # Move cards to proper position
                dropped_card.position = pile.center_x, pile.center_y

            # Success, don't reset position of cards
            reset_position = False

        # Geen twee kaarten op dezelfde stapel
        new_card_list = []
        for card in self.card_list:
            if card != self.held_cards[0]:
                new_card_list.append(card)

        for i in range (1,len(self.card_list)):
            if arcade.check_for_collision(self.held_cards[0], new_card_list[i-1]):
                reset_position = True

        for i in range (0,17):
            if arcade.check_for_collision(self.held_cards[0], self.pile_mat_list[i]):
                reset_position = True

            # Release on top play pile? And only one card held?
        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []

    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def remove_card_from_pile(self, card):
        """ Remove card from whatever pile it was in. """
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def move_card_to_new_pile(self, card, pile_index):
        """ Move the card to a new pile """
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)

    def on_show(self):
        self.manager.enable()

        self.texture = arcade.load_texture("images/background.jpg")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = PauseMenuView(self.game)
            self.window.show_view(menu_view)
            self.manager.disable()


def main():

    GUI()
    arcade.run()


main()
