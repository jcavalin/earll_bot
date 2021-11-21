from services.Audio import Audio
from services.TempFile import TempFile
import os
import uuid
import azure.cognitiveservices.speech as speechsdk
import azure.cognitiveservices.speech.audio as speechaudiosdk


class Speech:

    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECH_KEY'),
                                                    region=os.getenv('SPEECH_REGION'))
        self.speech_config.speech_synthesis_language = "en-US"

        self.temp = TempFile()

    def to_text(self, voice):
        file_path = self.temp.download(voice)
        file_wav_path = self.temp.get_filepath(f'{voice.file_unique_id}.wav')

        Audio.ogg_to_wav(file_path, file_wav_path)

        audio_input = speechsdk.AudioConfig(filename=file_wav_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_input)

        self.temp.delete_tmp_files()

        return speech_recognizer.recognize_once_async().get()

    def to_voice(self, text):
        file_wav_path = self.temp.get_filepath(f'{uuid.uuid4()}.wav')
        audio_config = speechaudiosdk.AudioOutputConfig(filename=file_wav_path)

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)
        synthesizer.speak_text_async(text)

        return {'path': file_wav_path, 'duration': Audio.get_wav_duration(file_wav_path)}

    def get_temp_file(self):
        return self.temp
