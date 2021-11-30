from pydub import AudioSegment


# Helper for audios
class Audio:

    @staticmethod
    def ogg_to_wav(source, destination):
        sound = AudioSegment.from_ogg(source)
        sound.export(destination, format="wav")
        return sound.duration_seconds

    @staticmethod
    def wav_to_ogg(source, destination):
        sound = AudioSegment.from_wav(source)
        sound.export(destination, format="ogg", codec="libopus")
        return sound.duration_seconds
