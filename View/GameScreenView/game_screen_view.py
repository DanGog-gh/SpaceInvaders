from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.image import Image

from View.GameScreenView.components.bigenemy.big_enemy import BigEnemy
from View.GameScreenView.components.block.block import Block
from View.GameScreenView.components.clickablebutton.clickable_button import ClickableButton  # NOQA
from View.GameScreenView.components.bullethero import BulletHero  # NOQA
from View.GameScreenView.components.enemy import Enemy
from View.GameScreenView.components.hero import Hero  # NOQA
from View.GameScreenView.components.premiumgun.premium_gun import PremiumGun
from View.base_view import BaseScreenView

import random


class GameScreenView(BaseScreenView):
    """Главный игровой экран."""

    def __init__(self, **kwargs):
        """Метод вызывается при создании экземпляра класса GameScreenView."""

        super().__init__(**kwargs)
        # Инстанс большого врага.
        self.big_enemy = None
        # Инстанс премиального оружия.
        self.premium_gun = None
        # Номер спрайта взрыва врага.
        self.explosion_number_sprite = 0
        # Загружаем фоновую мелодию игры.
        self.background_sound = SoundLoader.load("resources/audio/soundtrack_3.mp3")
        self.background_sound.loop = True
        self.blaster_enemy_sound = SoundLoader.load("resources/audio/blaster_enemy.mp3")
        # Находится ли перемещение объекта героя в процессе анимации.
        self.amin_move_hero_is_progress = False

        if self.background_sound:
            self.background_sound.play()

        Clock.schedule_once(self.add_enemy, 2)
        Clock.schedule_once(self.add_wall)
        Clock.schedule_interval(self.check_time_big_enemy, 1)

    def spawn_premium_gun(self, x, y):
        """Метод создает премиальное оружие на экране."""

        self.premium_gun = PremiumGun(view=self, model=self.model, controller=self.controller)
        self.premium_gun.pos = (x, y)
        self.add_widget(self.premium_gun)
        self.premium_gun.move_down()

    def upgrade_gun(self):
        """Метод обновляет текст текущего оружия на экране."""

        self.ids.type_gun.text = self.model.premium_guns[self.model.current_gun_index]

    def check_time_big_enemy(self, interval):
        """Метод создаёт большого врага каждые 5 секунд."""

        score_container = self.ids.score_container

        self.model.interval_big_enemy += interval
        if self.model.interval_big_enemy > 5:
            # Создаём большого врага.
            self.big_enemy = BigEnemy(view=self, model=self.model, controller=self.controller)
            self.big_enemy.x = -self.big_enemy.width
            self.big_enemy.y = self.height - (self.big_enemy.height + dp(20)) - self.ids.score_container.height
            self.add_widget(self.big_enemy)
            self.big_enemy.move_right()
            self.model.interval_big_enemy = 0

    def animation_explosion_enemy(self, enemy):
        """Метод анимации взрыва врага."""

        def set_sprite(*args):
            if self.explosion_number_sprite > 7:
                self.explosion_number_sprite = 0
                if isinstance(enemy, Enemy):
                    self.remove_widget(enemy)
                elif isinstance(enemy, BigEnemy):
                    self.remove_big_enemy(enemy)
                    enemy.state = "default"
                Clock.unschedule(set_sprite)
                self.controller.check_exists_enemies()

            self.explosion_number_sprite += 1
            enemy.source = f"resources/images/explosion-{self.explosion_number_sprite}.PNG"
            enemy.reload()

        Clock.schedule_interval(set_sprite, 0.1)

    def animation_explosion_hero(self, hero):
        """Метод анимации взрыва героя."""

        def set_sprite(*args):
            if self.explosion_number_sprite > 7:
                self.explosion_number_sprite = 0
                hero.opacity=0
                Clock.unschedule(set_sprite)
                Clock.schedule_once(lambda x: self.on_hero_killed(), 0.2)

            self.explosion_number_sprite += 1
            hero.source = f"resources/images/explosion-{self.explosion_number_sprite}.PNG"
            hero.reload()

        Clock.schedule_interval(set_sprite, 0.1)

    def block_explosion(self, block):
        """Метод анимации взрыва блока."""

        self.remove_widget(block)

    def remove_big_enemy(self, big_enemy):
        """Метод удаляет большого врага с экрана."""

        self.remove_widget(big_enemy)
        self.big_enemy = None
        if big_enemy.mothership_move_sound and big_enemy.mothership_move_sound.state:
            big_enemy.mothership_move_sound.stop()

    def remove_premium_gun(self, premium_gun):
        """Метод удаляет премиальное оружие с экрана."""

        self.remove_widget(premium_gun)
        premium_gun.have_picked_up_weapon = False
        self.premium_gun = None

    def add_wall(self, *args):
        """
        Начало игрового процесса. Добавление препятствий на экран.
        """

        if self.model.total_hero_hp != 3:
            return

        screen_width = Window.width  # ширина экрана
        spacing_block = dp(40)  # отступ между блоками препятствий
        width = (screen_width - spacing_block * 2) / 9  # ширина одного препятствия в блоке
        # Размер кубика в блоке препятствий.
        cube_width = width
        cube_height = width

        rows = 3
        cols = 3

        y_offset = cube_width
        texture = "resources/images/alien_texture_8.jpg"

        block_width = cols * cube_width  # ширина блока с кубиками препятствий
        left_x_offset = 0  # положение первого блока с кубиками препятствий
        # Положение второго блока с кубиками препятствий.
        center_x_offset = (((screen_width - block_width) // 2) + y_offset) - cube_width
        # Положение третьего блока с кубиками препятствий.
        right_x_offset = (screen_width - block_width + (y_offset * 2)) - (cube_width * 2)

        # Перед созданием препятствий удаляем старые препятствия.
        for widget in self.children[:]:
            if isinstance(widget, Block):
                self.remove_widget(widget)

        def create_wall(x_offset):
            """Метод создаёт стену из блоков 3x3."""
            for row in range(rows):
                for col in range(cols):
                    cube_wall = Block(
                        x=(x_offset + col * cube_width),
                        y=(row * cube_height) + (self.ids.hero.y + self.ids.hero.height + dp(48)),
                        size_hint=(None, None),
                        size=(cube_width, cube_height),
                        background_normal=texture,
                        opacity=0
                    )
                    self.add_widget(cube_wall)
                    self.model.array_of_blocks.append(cube_wall)

        create_wall(left_x_offset)
        create_wall(center_x_offset)
        create_wall(right_x_offset)

        for widget in self.children[:]:
            if isinstance(widget, Block):
                Animation(opacity=1, d=0.2).start(widget)

    def add_enemy(self, *args):
        """
        Начало игрового процесса. Добавление врагов на экран.
        """

        score_container = self.ids.score_container

        # Параметры для расположения врагов
        num_rows = 4
        num_cols = 5
        spacing = 6  # отступ между врагами

        # Вычисляем размеры врагов с учетом отступов
        enemy_width = ((self.width - (num_cols + 1) * spacing) / num_cols) - 10
        enemy_height = enemy_width  # враги квадратные
        x_start = spacing  # начальный отступ слева
        y_start = self.height - score_container.height - spacing - enemy_height  # начальный отступ сверху

        for row in range(num_rows):
            for col in range(num_cols):
                enemy = Enemy(
                    view=self,
                    row=row,
                    col=col,
                    model=self.model,
                    controller=self.controller
                )
                enemy.size = (enemy_width, enemy_height)
                x_pos = x_start + col * (enemy_width + spacing)
                y_pos = y_start - row * (enemy_height + spacing)
                enemy.pos = (x_pos, y_pos)
                self.model.array_of_enemies.append(enemy)
                self.add_widget(enemy)
                enemy.move_right()

        Clock.schedule_interval(self.enemies_shoot, 1)

    def enemies_shoot(self, interval):
        """Метод стрельбы врагов."""

        if self.blaster_enemy_sound:
            Clock.schedule_once(lambda x: self.blaster_enemy_sound.play(), 0.2)

        # Сортируем врагов по рядам, начиная с нижнего ряда.
        sorted_enemies = sorted(self.model.array_of_enemies, key=lambda enemy: enemy.row)

        # Список врагов, которые могут стрелять.
        eligible_enemies = []

        # Проверяем, чтобы стреляли только те враги, под которыми нет других врагов.
        for enemy in sorted_enemies:
            can_shoot = True  # Изначально предполагаем, что враг может стрелять.

            # Проверка на наличие врага ниже в том же столбце.
            for other_enemy in self.model.array_of_enemies:
                if other_enemy.col == enemy.col and other_enemy.row > enemy.row:
                    # Если враг ниже найден, запрещаем стрельбу.
                    can_shoot = False
                    break

            # Если враг может стрелять, добавляем его в список доступных для стрельбы.
            if can_shoot:
                eligible_enemies.append(enemy)

        # Выбираем три случайных врага для стрельбы.
        if len(eligible_enemies) > 0:
            enemies_to_shoot = random.sample(eligible_enemies, min(3, len(eligible_enemies)))
            for enemy in enemies_to_shoot:
                enemy.fire()

    def on_bullet_hit_hero(self):
        """Обрабатывает ситуацию, когда пули врагов достигли героя."""

        Clock.unschedule(self.enemies_shoot)

    # def on_size(self, *args):
    #     # Обновляем положение врагов при изменении размера окна
    #     self.add_enemy()

    def model_is_changed(self):
        def amin_move_hero_complete(*args):
            self.amin_move_hero_is_progress = False

        if self.model.collision_with_hero is True and self.model.array_of_enemies:
            self.controller.on_hero_killed()
        if self.model.bullet_hit_hero:
            print("ddddd")
            
        if self.amin_move_hero_is_progress:
            return
        
        amin_move_hero = Animation(
            x=self.model.hero_pos_x, duration=0.6, transition="out_sine"
        )
        amin_move_hero.bind(on_complete=amin_move_hero_complete)
        amin_move_hero.start(self.ids.hero)
        self.amin_move_hero_is_progress = True

    def on_hero_killed(self, *args):
        """Обрабатывает ситуацию, когда враги/пули врагов достигли героя."""

        for widget in self.children[:]:
            if isinstance(widget, Enemy):
                self.remove_widget(widget)

        if self.model.total_hero_hp > 0:
            self.update_hero_hp_display()
            self.reload_hero()
            Clock.schedule_once(self.add_enemy, 1)
            Clock.schedule_once(self.add_wall, 1)
        else:
            Clock.unschedule(self.check_time_big_enemy)
            for widget in self.children[:]:
                if isinstance(widget, BigEnemy):
                    self.remove_widget(widget)
                    break
            self.manager.current = 'game over screen'

    def reload_hero(self):
        """Обновляет отображение прозрачности и текстуры героя."""

        self.ids.hero.opacity = 1
        # FIXME: Не обновляется изображение героя.
        self.ids.hero.source = "resources/images/hero.png"
        self.ids.hero.reload()

    def update_hero_hp_display(self):
        """Обновляет количество жизней героя на экране."""

        self.ids.lives_box.clear_widgets()
        for hp in range(self.model.total_hero_hp):
            self.ids.lives_box.add_widget(
                Image(
                    source='resources/images/life.png',
                    size_hint=(None, None),
                    size=("25dp", "25dp")
                )
            )