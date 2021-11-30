from src.utils.Audio import Audio
from src.utils.TempFile import TempFile
import os
import uuid
import azure.cognitiveservices.speech as speechsdk
import azure.cognitiveservices.speech.audio as speechaudiosdk


class Speech:

    def __init__(self, language, voice):
        self.temp = TempFile()
        self.speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv('SPEECH_KEY'),
            region=os.getenv('SPEECH_REGION')
        )
        self.speech_config.speech_recognition_language = Speech.get_language(language)
        self.speech_config.speech_synthesis_voice_name = Speech.get_voice(language, voice)

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

    @staticmethod
    def get_language(language):
        languages = {
            'en': 'en-US',
            'pt': 'pt-BR'
        }

        return languages.get(language, languages['en'])

    @staticmethod
    def get_voice(language, voice):
        languages = {
            'en_male': 'en-US-EricNeural',
            'en_female': 'en-US-JennyNeural',
            'pt_male': 'pt-BR-AntonioNeural',
            'pt_female': 'pt-BR-FranciscaNeural'
        }

        return languages.get(f"{language}_{voice}", languages['en_female'])
