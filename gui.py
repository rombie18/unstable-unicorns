import arcade
import arcade.gui
from pyglet.image import load as pyglet_load

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Unstable Unicorns", resizable=False)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        
        self.set_icon(pyglet_load("images/icon.png"))
        self.background = arcade.load_texture("images/background.jpg")

        self.center_box = arcade.gui.UIBoxLayout()
        self.bottom_box = arcade.gui.UIBoxLayout()
        
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
        self.center_box.add(ui_text_label.with_space_around(bottom=60))

        start_button = arcade.gui.UIFlatButton(text="Spel starten", width=200, style=default_style)
        self.center_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Instellingen", width=200, style=default_style)
        self.center_box.add(settings_button.with_space_around(bottom=20))
        
        exit_button = arcade.gui.UIFlatButton(text="Afsluiten", width=200, style=default_style)
        self.center_box.add(exit_button.with_space_around(bottom=20))
        
        ui_text_label = arcade.gui.UITextArea(
            text="Semih Barmaksiz, Wout Rombouts",
            width=226,
            height=20,
            font_size=8,
            font_name="Kenney Future",
            text_color=arcade.color.GRAY
        )
        self.bottom_box.add(ui_text_label.with_space_around(bottom=20))

        @start_button.event("on_click")
        def on_click_settings(event):
            print("Start:", event)
            
        @settings_button.event("on_click")
        def on_click_settings(event):
            print("Settings:", event)
            
        @exit_button.event("on_click")
        def on_click_settings(event):
            arcade.exit()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.center_box)
        )
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.bottom_box)
        )
        
        self.music = arcade.Sound("sounds/soundtrack.mp3", streaming=True)
        self.current_player = self.music.play(0.6)
        
    def on_draw(self):
        self.clear()
        
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.manager.draw()


window = MyWindow()
arcade.run()