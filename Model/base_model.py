class BaseScreenModel:
    """
    Базовый класс для модулей модели.
    Реализует методы добавления/удаления наблюдателей
    и константы для общения с сервером.
    """

    _observers = []  # список всех наблюдателей (представлений/view)

    def notify_observers(self, name_screen: str, bullet_hit_hero=False) -> None:
        """
        Метод, который будет вызываться наблюдателем при изменении данных
        модели.

        :param name_screen:
            имя представления, для которого должен быть вызван метод
            :meth:`model_is_changed`.
        """

        for observer in self._observers:
            if observer.name == name_screen:
                if bullet_hit_hero:
                    observer.on_bullet_hit_hero()
                else:
                    observer.model_is_changed()
                break

    def add_observer(self, observer) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer) -> None:
        self._observers.remove(observer)
