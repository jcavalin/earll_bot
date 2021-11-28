class Command:
    def __init__(self):
        self.origin = None
        self.state = None

    def responses(self, text, reply):
        input_text = str(text).lower()

        return "Hi! I'm Earll.\n\n" \
               "I can help you to convert some kinds of messages.\n" \
               "\t\t\t1. Send me a text and I will speak it to you.\n" \
               "\t\t\t2. Send me audio and I will transcribe it for you.\n" \
               "\t\t\t3. Send me a picture and I will describe it to you.\n"

