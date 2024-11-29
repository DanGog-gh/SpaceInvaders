import os

from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, OptionProperty
from kivy.uix.image import Image
from kivy.lang import Builder

# Загружаем KV файл со свойствами класса PremiumGun.
with open(
    os.path.join(os.path.dirname(__file__), "premium_gun.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class PremiumGun(Image):
    """Класс реализующий бонусное оружие."""

    view = ObjectProperty()
    model = ObjectProperty()
    controller = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Подобрали ли премиальное оружие.
        self.have_picked_up_weapon = False
        self.picked_weapon_sound = SoundLoader.load("resources/audio/pick_up_weapon.mp3")

    def move_progress(self, animation, premium_gun, progress):
        """Метод проверяет, подобрано ли премиальное оружие героем."""

        if self.have_picked_up_weapon:
            return

        self.model.check_bullet_hit_target(self, self.view.ids.hero)
        if self.model.bullet_hit_target:
            self.have_picked_up_weapon = True
            animation.stop(self)
            self.controller.picked_weapon(self)
            if self.picked_weapon_sound:
                self.picked_weapon_sound.play()
            print("Подобрано премиальное оружие.")

    def move_down(self, *args):
        """Метод, реализующий движение премиального оружие вниз."""
        anim = Animation(y=0, d=self.model.speed_big_enemy)
        anim.bind(
            on_progress=self.move_progress,
            on_complete=lambda *x: self.view.remove_premium_gun(self),
        )
        anim.start(self)