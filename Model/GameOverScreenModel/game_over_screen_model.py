from Model.base_model import BaseScreenModel


class GameOverScreenModel(BaseScreenModel):
    """
    Реализует логику для класса представления
    :class:`~View.GameOverScreenView.game_over_screen_view.GameOverScreenView`.
    """

    def __init__(self, config, root_config=None):
        self.config = config
        self.root_config = root_config