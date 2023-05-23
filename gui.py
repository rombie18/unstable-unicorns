"""
Example code showing how to create a button,
and the three ways to process button events.
"""
import random
import arcade
import arcade.gui
from arcade.experimental.uislider import UISlider
from arcade.gui import UIManager, UIAnchorWidget, UILabel
from arcade.gui.events import UIOnChangeEvent
from pyglet.image import load as pyglet_load

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 960

CARD_HEIGHT = 90
CARD_WIDTH = 65

CARD_SCALE = 0.05
CARD_SOORTEN = ["upgrade", "downgrade"]
CARD_NUMMERS = ["1","2","3","4","5","6","7","8"]

PILE_COUNT = 27
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
PILE_OPPONENT_A_1 = 2
PILE_OPPONENT_A_2 = 3
PILE_OPPONENT_A_3 = 4
PILE_OPPONENT_A_4 = 5
PILE_OPPONENT_A_5 = 6
PILE_OPPONENT_A_6 = 7
PILE_OPPONENT_A_7 = 8
PILE_OPPONENT_B_1 = 9
PILE_OPPONENT_B_2 = 10
PILE_OPPONENT_B_3 = 11
PILE_OPPONENT_B_4 = 12
PILE_OPPONENT_B_5 = 13
PILE_OPPONENT_B_6 = 14
PILE_OPPONENT_B_7 = 15
PILE_TABLE_1 = 16
PILE_TABLE_2 = 17
PILE_TABLE_3 = 18
PILE_OWN_1 = 19
PILE_OWN_2 = 20
PILE_OWN_3 = 21
PILE_OWN_4 = 22
PILE_OWN_5 = 23
PILE_OWN_6 = 24
PILE_OWN_7 = 25
PILE_OWN_8 = 26
PILE_OWN_9 = 27
PILE_OWN_10 = 28


# How big is the mat we'll place the card on?
MAT_HEIGHT = int(CARD_HEIGHT * 1.4)
MAT_WIDTH = int(CARD_WIDTH * 1.4)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.1
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row (7 piles)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT * 8

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

class Card(arcade.Sprite):
    def __init__(self, soort, nummer, scale =1):
        self.soort = soort
        self.nummer = nummer
        self.image_file_name = "images/all_cards/"+self.soort+"-"+self.nummer+".jpg"

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Unstable Unicorns", fullscreen=True)

        self.card_list = None

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.set_icon(pyglet_load("images/icon.png"))
        self.background = arcade.load_texture("images/background.jpg")

        self.v_box = arcade.gui.UIBoxLayout()

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
        #self.music = arcade.Sound("sounds/soundtrack.mp3", streaming=True)
        #self.current_player = self.music.play(0.5)

        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        self.card_list = arcade.SpriteList()

        for card_soort in CARD_SOORTEN:
            for card_nummer in CARD_NUMMERS:
                card = Card(card_soort, card_nummer, CARD_SCALE)
                card.position = 500 , 500
                self.card_list.append(card)

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Put all the cards in the bottom face-down pile
        for card in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card)

        for i in range(3):
            pile = arcade.SpriteSolidColor(int(MAT_WIDTH*1.5), int(MAT_HEIGHT*1.5), arcade.color.BRIGHT_LILAC)
            pile.position = 900 + i * X_SPACING*1.5, 1080 / 7 * 3
            self.pile_mat_list.append(pile)

        for i in range(5):
            pile = arcade.SpriteSolidColor(int(MAT_WIDTH*1.5), int(MAT_HEIGHT*1.5), arcade.color.BRIGHT_LILAC)
            pile.position = START_X * 1.45 + i * X_SPACING*1.5, BOTTOM_Y * 1.5
            self.pile_mat_list.append(pile)

        for i in range(5):
            pile = arcade.SpriteSolidColor(int(MAT_WIDTH*1.5), int(MAT_HEIGHT*1.5), arcade.color.BRIGHT_LILAC)
            pile.position = 860 + i * X_SPACING*1.5, BOTTOM_Y * 1.5
            self.pile_mat_list.append(pile)

        for i in range(7):
            pile = arcade.SpriteSolidColor(int(MAT_WIDTH*1.2), int(MAT_HEIGHT*1.2), arcade.color.BRIGHT_LILAC)
            pile.position = START_X + i * X_SPACING*1.3, MIDDLE_Y
            self.pile_mat_list.append(pile)

        for i in range(7):
            pile = arcade.SpriteSolidColor(int(MAT_WIDTH*1.2), int(MAT_HEIGHT*1.2), arcade.color.BRIGHT_LILAC)
            pile.position = START_X + i * X_SPACING*1.3, TOP_Y
            self.pile_mat_list.append(pile)

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

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
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


window = MyWindow()
window.setup()
arcade.run()