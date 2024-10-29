import os

from kivy.lang import Builder
from kivy.uix.image import Image

with open(
    os.path.join(os.path.dirname(__file__), "bullet_hero.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class BulletHero(Image):
    """Класс, реализующий пулю героя."""