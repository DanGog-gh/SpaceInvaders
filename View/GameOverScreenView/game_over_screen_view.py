from kivy.core.audio import SoundLoader

from View.GameScreenView.components.clickablebutton.clickable_button import (
    ClickableButton,
)  # NOQA
from View.GameScreenView.components.bullethero import BulletHero  # NOQA
from View.GameScreenView.components.hero import Hero  # NOQA
from View.base_view import BaseScreenView


class GameOverScreenView(BaseScreenView):
    """Главный игровой экран."""

    def __init__(self, **kwargs):
        """Метод вызывается при создании экземпляра класса GameScreenView."""

        super().__init__(**kwargs)
        # Загружаем фоновую мелодию игры.
        # self.background_sound = SoundLoader.load("resources/audio/soundtrack_3.m4a")

    def model_is_changed(self): ...
