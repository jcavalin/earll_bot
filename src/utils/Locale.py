import yaml


# Helper for multiple languages
class Locale:
    localedir = './locale'
    supported_languages = ['en', 'pt']
    texts = {}

    # Load language to memory
    @staticmethod
    def load(language=None):
        language = language or Locale.supported_languages[0]

        with open(f"{Locale.localedir}/{language}.yml", "r") as stream:
            try:
                Locale.texts = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    # Get a text according to defined language
    @staticmethod
    def get(key):
        return Locale.texts[key]
