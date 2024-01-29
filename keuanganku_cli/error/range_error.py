class KErrorRange(Exception):
    def __init__(self, expectedRange : range = None):
        if self.message is None:
            self.message = f"KErrorRange: Range error"
        else:
            self.message = f"Error, input a number between {expectedRange.start}-{expectedRange.stop-1}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
