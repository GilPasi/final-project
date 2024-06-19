class NoGyroscopeDataException(Exception):
    def __init__(self, message="No gyroscope data given at all."):
        self.message = message
        super().__init__(self.message)