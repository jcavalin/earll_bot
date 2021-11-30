# Earll

![Earll](https://raw.githubusercontent.com/jcavalin/earll_bot/main/assets/avatar.png)

### About
Earll is a telegram bot that helps you with some kinds of messages:
1. Send him a text, and he will speak to you.
2. Send him audio, and he will transcribe it for you.
3. Send him a picture, and he will describe it to you.

Earll uses [Azure Speech](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/) and [Azure Computer Vision](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/) services to do that.

[Try it out!](https://telegram.me/earll_bot)

### How to run?
1. Create an `.env` file in the root path, based in `.env.example`.
   1. Create your [Telegram Bot](https://t.me/botfather) token.
   2. Create your [Azure Speech](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/) credential.
   3. Create your [Azure Computer Vision](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/) credential.
   4. Fill `.env` with your token and credentials.
2. Install [ffmpeg](https://www.ffmpeg.org/).
3. Run the following commands:
    ```
    pip install -r requirements.txt 
    python main.py
    ```