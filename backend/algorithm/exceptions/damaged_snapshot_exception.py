class DamagedSnapshotException(Exception):
    def __init__(self, message="Snapshot is corrupted or incomplete"):
        self.message = message
        super().__init__(self.message)