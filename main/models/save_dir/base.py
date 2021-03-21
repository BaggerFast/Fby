class BasePattern:
    """Базовый класс для сохранения данных из json в database"""
    def __init__(self, json):
        self.json = json

    def save(self):
        raise NotImplementedError
