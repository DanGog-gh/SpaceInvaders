from kivy.app import App

from View.GameOverScreenView.game_over_screen_view import GameOverScreenView


class GameOverScreenController:
    def __init__(self, model):
        # Model.GameOverScreenModel.game_over_screen_model.GameOverScreenModel
        self.model = model
        self.view = GameOverScreenView(controller=self, model=self.model)

    def on_tap_reset_game_button(self):
        """Метод вызывается при нажатии по кнопке RESET на экране GameOverScreenView."""

        self.view.manager_current = "game screen"
        self.view.manager.get_screen("game screen").model.reset_hero_hp()
        self.view.manager.get_screen("game screen").update_hero_hp_display()
        self.view.manager.get_screen("game screen").add_enemy()
        self.view.manager.get_screen("game screen").add_wall()

    def on_tap_quit_game_button(self):
        """Метод вызывается при нажатии по кнопке QUIT на экране GameOverScreenView."""

        App.get_running_app().stop()

    def get_view(self) -> GameOverScreenView:
        return self.view
