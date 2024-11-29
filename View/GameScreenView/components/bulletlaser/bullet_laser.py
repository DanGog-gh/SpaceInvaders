import os

from kivy.lang import Builder
from kivy.uix.image import Image

with open(
    os.path.join(os.path.dirname(__file__), "bullet_laser.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class BulletLaser(Image):
    """Класс, реализующий лазер героя."""