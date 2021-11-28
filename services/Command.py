class Command:
    STATE_WAITING_KEYWORD = 'WAITING_KEYWORD'

    def __init__(self):
        self.origin = None
        self.state = None

    def responses(self, text, reply):
        input_text = str(text).lower()

        return 'Hi!'

