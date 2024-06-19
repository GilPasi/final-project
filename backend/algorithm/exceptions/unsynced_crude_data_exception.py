import json
class UnsyncedCrudeDataException(Exception):
    def __init__(self, threshold, message=None, *args):
        """
        Parameters:
        threshold   (number): maximum acceptable ratio between sources data count.
        message     (string): A custom message if needed.
        *args       (array of tuples in the structure (<source name>: string, <data count>: int))

        Returns:
        UnsyncedCrudeDataException: the configured exception
        """
        if message is None: 
            message = f"Data from several sources ({self._sources_names(*args)}) has deviation of over than {threshold}"
        self.message = message
        self.threshold = threshold
        self.sources = args
        super().__init__(self.message)

    @staticmethod
    def _sources_names(*args):
        return ', '.join([name for name, _ in args])

    def to_dictionary(self):
        """
        Converts the exception details into a dictionary.

        Returns:
        dict: A dictionary with exception details.
        """
        return {
            'message': self.message,
            'threshold': self.threshold,
            'sources': [{'name': name, 'data_count': data_count} for name, data_count in self.sources]
        }

    def to_json(self):
        """
        Converts the exception details into a JSON string.

        Returns:
        str: A JSON string with exception details.
        """
        return json.dumps(self.to_dictionary(), indent=4)