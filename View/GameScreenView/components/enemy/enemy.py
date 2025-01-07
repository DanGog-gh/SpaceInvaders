import os

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, NumericProperty, DictProperty
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window

from View.GameScreenView.components.bulletenemy import BulletEnemy

with open(
    os.path.join(os.path.dirname(__file__), "enemy.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class Enemy(Image):
    """Класс, реализующий врага."""

    view = ObjectProperty()
    model = ObjectProperty()
    controller = ObjectProperty()
    row = NumericProperty(0)
    col = NumericProperty(0)
    list_bullets = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enemy_last_direction = "right"
        self.animation_move_right = None
        self.animation_move_left = None
        self.animation_move_down = None

    def fire(self, *args):
        """Метод, реализующий движение пули."""

        bullet = BulletEnemy(y=self.y)
        bullet.x = (self.x + self.width / 2) - bullet.width / 2
        self.view.add_widget(bullet)
        method = Clock.schedule_interval(
            self.move_bullet, self.model.speed_bullet_enemy
        )
        self.list_bullets[bullet] = method

    def move_bullet(self, *args):
        """Метод, реализующий движение пуль."""

        for bullet, method in list(self.list_bullets.items()):
            bullet.y -= self.model.default_shift_bullet

            # Проверка на попадание пули в героя.
            self.model.check_bullet_hit_hero(bullet, self.view.ids.hero)
            if self.model.bullet_hit_hero and not self.model.hero_invincibility:
                self.controller.reset_enemies()
                self.remove_and_unbind_move_bullet()
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
                del self.list_bullets[bullet]

    def remove_and_unbind_move_bullet(self):
        """
        Удаляем объекты пули врагов с экрана и отвязываем метод move_bullet от
        бесконечного вызова.
        """

        for object_bullet, move_method in self.list_bullets.items():
            self.view.remove_widget(object_bullet)
            Clock.unschedule(move_method)

        self.list_bullets.clear()

    def move_right(self, *args):
        """Движение врага вправо."""

        if self.model.array_of_enemies:  # если враги существуют на экране
            x = (self.pos[0] + Window.width / 10) - 24  # сдвиг по оси x
            self.animation_move_right = Animation(
                x=x, duration=self.model.speed_enemy_right, transition="in_out_cubic"
            )
            # Привязываем событие окончания анимации к вызову методу move_down.
            self.animation_move_right.bind(
                on_complete=lambda *x: Clock.schedule_once(self.move_down, 0.2)
            )
            self.animation_move_right.start(self)  # старт анимации

    def move_left(self, *args):
        """Движение врага влево."""

        if self.model.array_of_enemies:  # если враги существуют на экране
            x = (self.pos[0] - Window.width / 10) + 24
            self.animation_move_left = Animation(
                x=x, duration=self.model.speed_enemy_left, transition="in_out_cubic"
            )
            self.animation_move_left.bind(
                on_complete=lambda *x: Clock.schedule_once(self.move_down, 0.2)
            )
            self.animation_move_left.start(self)

    def move_down(self, *args):
        """Движение врага вниз."""

        if self.model.array_of_enemies:  # если враги существуют на экране
            y = self.pos[1] - Window.height / 80
            self.controller.on_enemy_move_down(y)

            self.animation_move_down = Animation(
                y=y, duration=self.model.speed_enemy_down, transition="in_back"
            )
            if self.enemy_last_direction == "right":
                self.enemy_last_direction = "left"
                self.animation_move_down.bind(on_complete=self.move_left)
            else:
                self.enemy_last_direction = "right"
                self.animation_move_down.bind(on_complete=self.move_right)
            self.animation_move_down.start(self)
