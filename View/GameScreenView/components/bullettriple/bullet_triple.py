import os

from kivy.lang import Builder
from kivy.uix.image import Image

with open(
    os.path.join(os.path.dirname(__file__), "bullet_triple.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class BulletTriple(Image):
    """Класс, реализующий тройную пулю героя."""
