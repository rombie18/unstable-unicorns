import arcade


WIDTH = 800
HEIGHT = 600


class MainMenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Menu Screen - click to advance", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

    
class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Menu Screen - click to advance", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            game_view = GameView()
            self.window.show_view(game_view)

    
class GameView(arcade.View):
    """ Manage the 'game' view for our program. """

    def __init__(self):
        super().__init__()
        # Create variables here

    def setup(self):
        """ This should set up your game and get it ready to play """
        # Replace 'pass' with the code to set up your game
        pass

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        """ Draw everything for the game. """
        self.clear()
        arcade.draw_text("Game - press SPACE to advance", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ Handle key presses. In this case, we'll just count a 'space' as
        game over and advance to the game over view. """
        if key == arcade.key.SPACE:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)
            
class SettingsView(arcade.View):



class StartingGameView(arcade.View):




def main():
    """ Startup """
    window = arcade.Window(WIDTH, HEIGHT, "Different Views Minimal Example")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()