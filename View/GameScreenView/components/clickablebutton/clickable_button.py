from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from kivymd.uix.behaviors import TouchBehavior


class ClickableButton(TouchBehavior, Image, ButtonBehavior):
    """Класс, реализующий кликабельные кнопки"""

    direction = StringProperty()  # тип кнопки - "left/right"
    controller = ObjectProperty()  # инстанс контроллера

    def on_touch_up(self, touch):
        """Метод вызывается при отпускании касания к объекту."""

        if self.collide_point(touch.x, touch.y):
            self.controller.on_touch_button_up(self.direction)

    def on_long_touch(self, touch, *args):
        """Метод вызывается при долгом нажатии по кнопке."""

        self.controller.on_long_touch(self.direction)

    def on_touch_down(self, touch, *args):
        """Метод вызывается при долгом нажатии по кнопке."""

        if self.collide_point(touch.x, touch.y):
            if self.direction == "right":
                self.controller.on_tap_right_button()
            elif self.direction == "left":
                self.controller.on_tap_left_button()
            elif self.direction == "fire":
                self.controller.on_tap_fire_button()

            return super().on_touch_down(touch)