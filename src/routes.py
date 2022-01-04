from src.utils import Utils


class Routes:
    utils = Utils()

    def connect(self, id: str):
        self.utils.response(id, "Connected")

    def disconnect(self, id: str):
        return

    def default(self, id: str):
        self.utils.response(id, "Action not allowed")
