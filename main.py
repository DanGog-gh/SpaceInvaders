"""
Точка входа в приложение.

Приложение использует шаблон MVC. Соблюдение принципов чистой архитектуры
гарантирует, что ваше приложение будет легко тестировать, поддерживать и
модернизировать в будущем.

Вы можете узнать больше об этом шаблоне по ссылкам ниже:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.joinpath("libs")))
os.environ["KIVY_ORIENTATION"] = "Portrait"

from kivy import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy import platform

# Только для тестирования.
# Устанавливает размер окна приложения и размещает его в правой стороне экрана.
if platform in ("macosx", "linux"):
    from PIL import ImageGrab

    resolution = ImageGrab.grab().size
    Config.set("graphics", "height", resolution[1] - 200)
    Config.set("graphics", "width", "400")

    from kivy.core.window import Window

    Window.top = 0
    Window.left = Window.width + 240
elif platform == "win":
    Config.set("graphics", "height", "720")
    Config.set("graphics", "width", "400")

from kivymd.app import MDApp

###############################################################################
from Model.GameScreenModel.game_screen_model import GameScreenModel
from Model.GameOverScreenModel.game_over_screen_model import GameOverScreenModel

from Controller.GameScreenController.game_screen_controller import \
    GameScreenController
from Controller.GameOverScreenController.game_over_screen_controller import \
    GameOverScreenController
###############################################################################


class SpaceInvaders(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Это диспетчер экранов, который будет содержать все экраны приложения.
        self.manager_screens = ScreenManager()

    def build(self):
        """
        Запускаться при старте приложения.
        Возвращает экранный менеджер с экранами приложения, который будет
        отображен пользователю.
        """

        # Загружаем макеты пользовательского UI игрового экрана.
        Builder.load_file("View/GameScreenView/game_screen_view.kv")
        # Создание модели.
        game_screen_model = GameScreenModel(config=self.config, root_config=Config)
        # Создание контроллера.
        game_screen_controller = GameScreenController(game_screen_model)
        # Получение представления/экрана/view.
        game_screen_view = game_screen_controller.get_view()
        # Добавляем представление в экранный менеджер.
        self.manager_screens.add_widget(game_screen_view)

        # Загружаем макеты пользовательского UI игрового экрана.
        Builder.load_file("View/GameOverScreenView/game_over_screen_view.kv")
        # Создание модели.
        game_over_screen_model = GameOverScreenModel(config=self.config, root_config=Config)
        # Создание контроллера.
        game_over_screen_controller = GameOverScreenController(game_over_screen_model)
        # Получение представления/экрана/view.
        game_over_screen_view = game_over_screen_controller.get_view()
        # Добавляем представление в экранный менеджер.
        self.manager_screens.add_widget(game_over_screen_view)

        return self.manager_screens

    def build_config(self, config):
        """Создает файл настроек spaceinvaders.ini."""

        config.adddefaultsection("General")

    def get_application_config(self) -> str:
        """Возвращает путь к файлу конфигурации."""

        try:
            my_app_conf = super().get_application_config(
                "{}/%(appname)s.ini".format(self.user_data_dir)
            )
        except PermissionError:
            my_app_conf = super().get_application_config(
                "{}/%(appname)s.ini".format(self.directory)
            )
        return my_app_conf


SpaceInvaders().run()
