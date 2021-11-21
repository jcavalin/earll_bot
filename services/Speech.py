from services.Audio import Audio
from services.TempFile import TempFile
import os
import uuid
import azure.cognitiveservices.speech as speechsdk
import azure.cognitiveservices.speech.audio as speechaudiosdk


class Speech:

    def __init__(self):
        self.temp = TempFile()
        self.speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv('SPEECH_KEY'),
            region=os.getenv('SPEECH_REGION')
        )
        # self.speech_config.speech_synthesis_language = "en-US"
        self.speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        # self.speech_config.speech_synthesis_voice_name = "en-US-EricNeural"

    def to_text(self, voice):
        file_path = self.temp.download(voice)
        file_wav_path = self.temp.get_filepath(f'{voice.file_unique_id}.wav')

        Audio.ogg_to_wav(file_path, file_wav_path)

        audio_input = speechsdk.AudioConfig(filename=file_wav_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_input)

        self.temp.delete_tmp_files()

        return speech_recognizer.recognize_once_async().get()

    def to_voice(self, text):
        filename = uuid.uuid4()
        file_wav_path = self.temp.get_filepath(f'{filename}.wav')
        audio_config = speechaudiosdk.AudioOutputConfig(filename=file_wav_path)

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)
        synthesizer.speak_text_async(text)

        file_path = self.temp.get_filepath(f'{filename}.ogg')
        duration = Audio.wav_to_ogg(file_wav_path, file_path)

        return {'path': file_path, 'duration': duration}

    def get_temp_file(self):
        return self.temp
