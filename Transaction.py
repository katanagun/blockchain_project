class Transaction:
    def __init__(self, sender, receiver, token):
        self.sender = sender
        self.receiver = receiver
        self.token = token

    def __str__(self):
        return f"{self.sender}->{self.receiver}:{self.token.name}={self.token.value}"
