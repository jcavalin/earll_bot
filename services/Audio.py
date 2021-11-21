from pydub import AudioSegment


class Audio:

    @staticmethod
    def ogg_to_wav(source, destination):
        sound = AudioSegment.from_ogg(source)
        sound.export(destination, format="wav")
