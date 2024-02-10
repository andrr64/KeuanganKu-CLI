class KErrorInvalidInputType(Exception):
    def __init__(self, message="Invalid input type"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"

    @staticmethod
    def handler():
        input("Error, please type correctly...")