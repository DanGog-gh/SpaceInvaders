from kivy.metrics import dp

from Model.base_model import BaseScreenModel


class GameScreenModel(BaseScreenModel):
    """
    Реализует логику для класса представления
    :class:`~View.GameScreenView.game_screen_view.GameScreenView`.
    """

    def __init__(self, config, root_config=None):
        self.config = config
        self.root_config = root_config
        self.default_shift = 50
        self.premium_guns = {
            0: "default",
            1: "laser",
            2: "triple",
        }  # словарь с типами премиального оружия
        self.current_gun_index = 0  # текущий тип оружия
        self.array_of_enemies = []  # список существующих врагов на экране
        self.array_of_blocks = (
            []
        )  # список типа self.array_of_enemies для блоков препятствий.
        self._hero_pos_x = 0  # начальное положение героя по оси X
        self._speed_enemy_right = 1.5  # скорость движения врага вправо
        self._speed_enemy_left = 1.5  # скорость движения врага влево
        self._speed_enemy_down = 0.8  # скорость движения врага вниз
        self._collision_with_hero = False  # столкнулись ли враги с героем
        self._speed_bullet_hero = 1 / 60
        self.speed_big_enemy = 3
        self._speed_bullet_enemy = 0.02
        self.interval_fire_enemies = 3  # интервал выстрелов врагов
        self.total_hero_hp = 3  # количество жизней героя
        self.default_shift_bullet = 10
        self._current_hero_hp = 3
        self.bullet_hit_target = False  # попала ли пуля во врага
        self.bullet_hit_hero = False  # попала ли пуля в героя
        self.bullet_hit_block = False  # попала ли пуля в препятствие
        self.hero_invincibility = False  # неуязвимость героя

        self.interval_big_enemy = 0

    # Встроенные методы, которые вызываются при изменении данных модели.

    @property
    def bullet_hit_hero(self) -> float:
        return self._bullet_hit_hero

    @bullet_hit_hero.setter
    def bullet_hit_hero(self, data: int):
        self._bullet_hit_hero = data
        self.notify_observers("game screen", data)

    @property
    def speed_bullet_enemy(self) -> float:
        return self._speed_bullet_enemy

    @speed_bullet_enemy.setter
    def speed_bullet_enemy(self, data: int):
        self._speed_bullet_enemy = data
        self.notify_observers("game screen")

    @property
    def speed_bullet_hero(self) -> float:
        return self._speed_bullet_hero

    @speed_bullet_hero.setter
    def speed_bullet_hero(self, data: int):
        self._speed_bullet_hero = data
        self.notify_observers("game screen")

    @property
    def speed_enemy_right(self) -> float:
        return self._speed_enemy_right

    @speed_enemy_right.setter
    def speed_enemy_right(self, data: int):
        self._speed_enemy_right = data
        self.notify_observers("game screen")

    @property
    def speed_enemy_left(self) -> float:
        return self._speed_enemy_left

    @speed_enemy_left.setter
    def speed_enemy_left(self, data: int):
        self._speed_enemy_left = data
        self.notify_observers("game screen")

    @property
    def speed_enemy_down(self) -> float:
        return self._speed_enemy_down

    @speed_enemy_down.setter
    def speed_enemy_down(self, data: int):
        self._speed_enemy_down = data
        self.notify_observers("game screen")

    @property
    def collision_with_hero(self) -> int:
        return self._collision_with_hero

    @collision_with_hero.setter
    def collision_with_hero(self, data: int):
        self._collision_with_hero = data
        self.notify_observers("game screen")

    @property
    def hero_pos_x(self) -> int:
        return self._hero_pos_x

    @hero_pos_x.setter
    def hero_pos_x(self, data: int):
        self._hero_pos_x = data
        self.notify_observers("game screen")

    ###########################################################################

    def move_hero_to_right(self, screen_width, hero_width):
        """Метод вызывается при тапе по кнопке движения вправо."""

        # Увеличиваем положение героя по оси x, если положение по оси x не превышает длину экрана.
        hero_pos_x = self.hero_pos_x + self.default_shift
        if not screen_width <= hero_pos_x + hero_width:
            self.hero_pos_x += self.default_shift

    def move_hero_to_left(self, screen_width, hero_width):
        """Метод вызывается при тапе по кнопке движения влево."""

        # Уменьшаем положение героя по оси x, если положение по оси x не меньше нуля.
        hero_pos_x = self.hero_pos_x - self.default_shift
        if hero_pos_x >= 0:
            self.hero_pos_x -= self.default_shift

    def upgrade_gun(self):
        """Улучшение оружия героя при подбирании премиального оружия."""

        if self.current_gun_index < len(self.premium_guns) - 1:
            self.current_gun_index += 1

    def get_current_gun(self):
        """Получение индекса текущего оружия героя."""

        return self.premium_guns[self.current_gun_index]

    def reset_enemies(self):
        """Метод перезагружает врагов."""

        self.bullet_hit_hero = False
        self.array_of_enemies = []

    def check_bullet_hit_target(self, bullet, enemy):
        """Метод проверяет попадание пулей героя во врага/большого врага."""

        # Проверяем, находится ли пуля в пределах врага по оси X
        if (bullet.x + bullet.width >= enemy.x) and (bullet.x <= enemy.x + enemy.width):
            # Проверяем столкновение по оси Y
            if (bullet.y >= enemy.y) and (bullet.y <= enemy.y + enemy.height):
                self.bullet_hit_target = True
        else:
            self.bullet_hit_target = False

            self.bullet_hit_target = False

    def check_bullet_hit_hero(self, bullet, hero):
        """Метод проверяет попадание пулей врага в героя."""

        if (bullet.x >= hero.x) and (bullet.x <= hero.x + hero.width):
            # Проверяем столкновение по оси Y
            if (bullet.y >= hero.y) and (bullet.y <= hero.y + hero.height):
                self.bullet_hit_hero = True
        else:
            self.bullet_hit_hero = False

    def check_bullet_hit_block(self, bullet, block):
        """Метод проверяет попадание пулей в блоки."""

        # Проверяем, пересекаются ли пуля и враг по оси X
        if (bullet.x + bullet.width >= block.x) and (bullet.x <= block.x + block.width):
            # Проверяем пересечение по оси Y
            if (bullet.y >= block.y) and (bullet.y <= block.y + block.height):
                self.bullet_hit_block = True
        else:
            self.bullet_hit_block = False

    def reset_premium_gun(self):
        """Метод сбрасывает настройки премиального оружия."""

        self.current_gun_index = 0

    def reduce_hero_hp(self):
        """Метод уменьшает жизнь героя на единицу."""

        self.total_hero_hp -= 1

    def reset_hero_hp(self):
        """Метод восстанавливает все жизни героя."""

        self.total_hero_hp = 3

    def check_collision(self, y_enemy, y_hero):
        """Проверяет столкновение героя с врагами."""

        if y_enemy >= y_hero:
            self.collision_with_hero = False
        # Произошло столкновение.
        else:
            self.reduce_hero_hp()  # уменьшаем жизнь героя на единицу
            self.collision_with_hero = True
            self.array_of_enemies.clear()

    def change_enemy_speed(self):
        """Увеличивает скорость движения врагов."""

        if self.speed_enemy_right > 0.2:
            self.speed_enemy_right -= 0.2
        if self.speed_enemy_left > 0.2:
            self.speed_enemy_left -= 0.2
        if self.speed_enemy_down > 0.2:
            self.speed_enemy_down -= 0.2
