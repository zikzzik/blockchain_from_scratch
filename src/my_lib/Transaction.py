class Transaction:

    def __init__(self, sender: str, receiver: str, mount: float, timestamp: int = None):
        self.sender = sender
        self.receiver = receiver
        self.mount = mount
        self.timestamp = timestamp

    def str_for_hash(self):
        return f"{self.sender}_{self.receiver}_{self.mount}_{self.timestamp}"

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return (self.sender == other.sender and
                    self.receiver == other.receiver and
                    self.mount == other.mount and
                    self.timestamp == other.timestamp)
        return False

    def __hash__(self):
        return hash(f"{self.sender}_{self.receiver}_{self.mount}_{self.timestamp}")

    def __str__(self):
        return f"{self.sender} to {self.receiver} : {self.mount}"
