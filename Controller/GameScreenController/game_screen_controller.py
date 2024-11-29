from kivy.clock import Clock

from View.GameScreenView.components.bigenemy.big_enemy import BigEnemy
from View.GameScreenView.components.enemy import Enemy
from View.GameScreenView.components.hero import Hero
from View.GameScreenView.game_screen_view import GameScreenView

class GameScreenController:
    def __init__(self, model):
        # Model.GameScreenModel.game_screen_model.GameScreenModel
        self.model = model
        self.view = GameScreenView(controller=self, model=self.model)

    def on_enemy_move_down(self, y):
        """Метод проверяет столкновение героя с врагами при движении врагов вниз."""
        self.model.check_collision(y, self.view.ids.hero.y + self.view.ids.hero.height / 2)

    def on_tap_left_button(self, *args):
        """Метод вызывается при тапе по кнопке движения влево."""

        self.model.move_hero_to_left(self.view.width, self.view.ids.hero.width)

    def on_tap_right_button(self, *args):
        """Метод вызывается при тапе по кнопке движения вправо."""

        self.model.move_hero_to_right(self.view.width, self.view.ids.hero.width)

    def check_exists_enemies(self, *args):
        """Проверяет количество оставшихся врагов."""

        if len(self.model.array_of_enemies) == 0:
            self.view.add_enemy()
            self.model.change_enemy_speed()

    def on_bullet_hit_target(self, enemy, x=0, y=0):
        """Метод вызывается при попадании пули героя во врага."""

        # Удаляем врага и пулю.
        if isinstance(enemy, Enemy):
            self.model.array_of_enemies.remove(enemy)
        if isinstance(enemy, BigEnemy):
            self.view.big_enemy.state = "exploding"
            self.view.spawn_premium_gun(self.view.big_enemy.x, self.view.big_enemy.y)
        self.view.animation_explosion_enemy(enemy)

    def on_bullet_hit_hero(self, hero, x=0, y=0):
        """Метод вызывается при попадании пули врага в героя."""

        # Уменьшает количество жизней героя.
        self.model.reduce_hero_hp()

        # Удаляем героя и пулю.
        self.view.animation_explosion_hero(self.view.ids.hero)  # Анимация взрыва героя

        # Сброс настроек премиального оружия.
        self.model.reset_premium_gun()

        self.view.ids.type_gun.text = self.model.premium_guns[self.model.current_gun_index]

    def on_bullet_hit_block(self, block, x=0, y=0):
        """Метод вызывается при попадании пуль в препятствие."""

        self.model.array_of_blocks.remove(block)
        self.view.block_explosion(block)

    def picked_weapon(self, premium_gun):
        """Метод вызывается когда подбирает премиальное оружие."""

        self.model.upgrade_gun()  # изменить номер текущего оружия героя
        self.view.upgrade_gun()
        self.view.remove_premium_gun(premium_gun)

    def on_tap_fire_button(self, *args):
        """Метод вызывается при тапе по кнопке огня."""

        self.view.ids.hero.fire()

    def on_hero_killed(self):
        """Обрабатывает ситуацию, когда враги достигли героя."""

        self.view.on_hero_killed()

    def reset_enemies(self):
        """Метод перезагружает врагов."""

        self.model.reset_enemies()

    def on_long_touch(self, direction):
        """Метод вызывается при долгом тапе по кнопке."""

        if direction == "right":
            Clock.schedule_interval(self.on_tap_right_button, 0.1)
        elif direction == "left":
            Clock.schedule_interval(self.on_tap_left_button, 0.1)

    def on_touch_button_up(self,  direction):
        """Метод вызывается при отпускании касания к объекту кнопки."""

        if direction == "right":
            Clock.unschedule(self.on_tap_right_button)
        elif direction == "left":
            Clock.unschedule(self.on_tap_left_button)

    def get_view(self) -> GameScreenView:
        return self.view
