from kivy.app import App

from View.GameOverScreenView.game_over_screen_view import GameOverScreenView
from View.GameScreenView.components.block.block import Block
from View.GameScreenView.components.enemy import Enemy


class GameOverScreenController:
    def __init__(self, model):
        # Model.GameOverScreenModel.game_over_screen_model.GameOverScreenModel
        self.model = model
        self.view = GameOverScreenView(controller=self, model=self.model)

    def on_tap_reset_game_button(self):
        """
        Метод вызывается при нажатии по кнопки RESET на экране
        GameOverScreenView.
        """

        self.view.manager.current = "game screen"
        view = self.view.manager.get_screen("game screen")
        model = self.view.manager.get_screen("game screen").model

        for widget in view.children[:]:
            if isinstance(widget, Block):
                view.remove_widget(widget)

        for widget in view.children[:]:
            if isinstance(widget, Enemy):
                view.remove_widget(widget)

        model.reset_enemies()
        model.reset_hero_hp()
        view.update_hero_hp_display()
        view.rebuild_game()
        view.reload_hero()

    def on_tap_quit_game_button(self):
        """
        Метод вызывается при нажатии по кнопке QUIT на экране
        GameOverScreenView.
        """

        App.get_running_app().stop()

    def get_view(self) -> GameOverScreenView:
        return self.view
