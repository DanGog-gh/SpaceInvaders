import os

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.image import Image
from kivy.lang import Builder

from View.GameScreenView.components.bullethero import BulletHero
from View.GameScreenView.components.bulletlaser.bullet_laser import BulletLaser
from View.GameScreenView.components.bullettriple.bullet_triple import BulletTriple

# Загружаем KV файл со свойствами класса Hero.
with open(
    os.path.join(os.path.dirname(__file__), "hero.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class Hero(Image):
    """Класс реализующий героя."""

    view = ObjectProperty()
    controller = ObjectProperty()
    model = ObjectProperty()
    list_bullets = DictProperty()

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        # Инициализируем переменную с именем self.blaster_hero_sound класса SoundLoader с треком blaster_hero.mp3.
        self.blaster_hero_sound = SoundLoader.load("resources/audio/blaster_hero.mp3")
        # Инициализируем переменную с именем self.enemy_dead_sound класса SoundLoader с треком enemy_dead.mp3.
        self.enemy_dead_sound = SoundLoader.load("resources/audio/enemy_dead.mp3")

    def fire(self, *args):
        """Реализует движение пули."""

        # Воспроизвести звук self.blaster_hero_sound.
        if self.blaster_hero_sound:
            self.blaster_hero_sound.play()

        # Получаем тип текущего оружия из модели
        current_gun_type = self.model.get_current_gun()

        bullet_type = BulletHero
        if current_gun_type == "laser":
            bullet_type = BulletLaser
        elif current_gun_type == "triple":
            bullet_type = BulletTriple

        bullet = bullet_type(y=self.y + self.height)
        bullet.x = (self.x + self.width / 2) - bullet.width / 2
        self.view.add_widget(bullet)
        method = Clock.schedule_interval(self.move_bullet, self.model.speed_bullet_hero)
        self.list_bullets[bullet] = method

    def move_bullet(self, *args):
        """Метод реализует движение пуль."""

        for bullet, method in list(self.list_bullets.items()):
            bullet.y += self.model.default_shift_bullet

            # Проверка на попадание пули во врага.
            for enemy in self.model.array_of_enemies:
                self.model.check_bullet_hit_target(bullet, enemy)

                if self.model.bullet_hit_target:
                    # Воспроизвести звук self.enemy_dead_sound.
                    self.remove_and_unbind_move_bullet(bullet, method)
                    if self.enemy_dead_sound:
                        self.enemy_dead_sound.play()
                    self.controller.on_bullet_hit_target(enemy)
                    break

            # Проверка на попадание пули в препятствие.
            for block in self.model.array_of_blocks:
                self.model.check_bullet_hit_block(bullet, block)
                if self.model.bullet_hit_block:
                    self.controller.on_bullet_hit_block(block)
                    self.view.remove_widget(bullet)
                    del self.list_bullets[bullet]
                    break

            # Проверка на попадание пули в большого врага.
            if self.view.big_enemy:
                self.model.check_bullet_hit_target(bullet, self.view.big_enemy)
                if self.model.bullet_hit_target and self.view.big_enemy.state == "default":
                    self.controller.on_bullet_hit_target(self.view.big_enemy, self.view.big_enemy.x, self.view.big_enemy.x)

            # Проверка на выход пули за пределы экрана.
            if self.model.bullet_hit_target or bullet.y > self.view.height:
                self.remove_and_unbind_move_bullet(bullet, method)

    def remove_and_unbind_move_bullet(self, bullet, method):
        """Удаляем объект пули героя с экрана и отвязываем метод move_bullet от бесконечного вызова."""

        self.view.remove_widget(bullet)
        Clock.unschedule(method)

        if bullet in self.list_bullets:
            del self.list_bullets[bullet]