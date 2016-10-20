class Memo(object):
    to = ""
    sender = ""
    message = ""
    channel = ""

    def __init__(self, id, sender, message, channel):
        self.to = id
        self.sender = sender
        self.message = message
        self.channel = channel
