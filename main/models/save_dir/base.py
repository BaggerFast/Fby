class BasePattern:
    def __init__(self, json):
        self.json = json

    def save(self):
        raise NotImplementedError
