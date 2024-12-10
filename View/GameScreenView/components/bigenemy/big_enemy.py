import os
import random

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, NumericProperty, DictProperty, OptionProperty
from kivy.uix.image import Image
from kivy.lang import Builder

from View.GameScreenView.components.bulletbigenemy import BulletBigEnemy

# Загружаем KV файл со свойствами класса BigEnemy.
with open(
    os.path.join(os.path.dirname(__file__), "big_enemy.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class BigEnemy(Image):
    """Класс реализующий большого врага."""

    view = ObjectProperty()
    model = ObjectProperty()
    controller = ObjectProperty()
    list_bullets = DictProperty()
    state = OptionProperty("default", options=["default", "exploding"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Летит ли пуля.
        self.bullet_is_fly = False
        # Случайная позиция выстрела.
        self.random_fire_position = 0
        # Инициализируем переменную с именем self.mothership класса
        # SoundLoader с треком mothership.mp3.
        self.mothership_move_sound = SoundLoader.load("resources/audio/mothership.mp3")

    def fire(self, *args):
        """Реализует движение пули."""

        self.bullet_is_fly = True
        bullet = BulletBigEnemy(y=self.y)
        bullet.x = (self.x + self.width / 2) - bullet.width / 2
        self.view.add_widget(bullet)
        method = Clock.schedule_interval(self.move_bullet, self.model.speed_bullet_enemy)
        self.list_bullets[bullet] = method

    def move_progress(self, *args):
        """Метод реализует движение врага."""

        if self.view.big_enemy and self.random_fire_position < self.x + self.width and not self.bullet_is_fly:
            self.fire()

    def move_right(self, *args):
        """Метод реализует движение врага."""

        # Устанавливаем случайную позицию выстрела.
        self.random_fire_position = random.randint(self.width, self.view.width + (self.width * 2))

        if self.mothership_move_sound:
            Clock.schedule_once(lambda x: self.mothership_move_sound.play(), 0.2)

        anim = Animation(x=self.view.width, d=self.model.speed_big_enemy)
        anim.bind(
            on_progress=self.move_progress,
            on_complete=lambda *x: self.view.remove_big_enemy(self),
        )
        anim.start(self)

    def move_bullet(self, *args):
        """Метод реализует движение пуль."""

        for bullet, method in list(self.list_bullets.items()):
            bullet.y -= self.model.default_shift_bullet

            # Проверка на попадание пули в героя.
            self.model.check_bullet_hit_hero(bullet, self.view.ids.hero)
            if self.model.bullet_hit_hero and not self.model.hero_invincibility:
                self.controller.on_bullet_hit_hero(self.view.ids.hero)
                break

            # Проверка на попадание пули в препятствие.
            for block in self.model.array_of_blocks:
                self.model.check_bullet_hit_block(bullet, block)
                if self.model.bullet_hit_block:
                    self.controller.on_bullet_hit_block(block)
                    self.view.remove_widget(bullet)
                    del self.list_bullets[bullet]
                    break

            # Проверка на выход пули за пределы экрана.
            if bullet.y < 0:
                self.view.remove_widget(bullet)
                Clock.unschedule(method)
                self.bullet_is_fly = False
                del self.list_bullets[bullet]