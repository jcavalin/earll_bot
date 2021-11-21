from services.Audio import Audio
from services.TempFile import TempFile
import os
import azure.cognitiveservices.speech as speechsdk


class SpeechToText:

    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECH_KEY'),
                                                    region=os.getenv('SPEECH_REGION'))

    def recognize(self, message):
        temp = TempFile()

        file_path = temp.download(message)
        file_wav_path = temp.get_filepath(f'{message.file_unique_id}.wav')

        Audio.ogg_to_wav(file_path, file_wav_path)
        audio_input = speechsdk.AudioConfig(filename=file_wav_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_input)

        temp.delete_tmp_files()

        return speech_recognizer.recognize_once_async().get()
