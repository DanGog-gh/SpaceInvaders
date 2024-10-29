from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from Utility.observer import Observer


class BaseScreenView(Screen, Observer):
    """
    Базовый класс, который реализует визуальное представление данных модели.
    Класс view должен быть унаследован от этого класса.
    """

    controller = ObjectProperty()
    """
    Объект контроллера - :class:`~Controller.controller_screen.ClassScreenControler`.

    :attr:`controller` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    model = ObjectProperty()
    """
    Объект модели - :class:`~Model.model_screen.ClassScreenModel`.

    :attr:`model` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    manager_screens = ObjectProperty()
    """
    Объект менеджера экранов приложения - :class:`~kivymd.uix.screenmanager.MDScreenManager`.

    :attr:`manager_screens` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Добавление класса представления в качестве наблюдателя.
        self.model.add_observer(self)
