import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials


class Vision:

    def __init__(self):
        self.computervision_client = ComputerVisionClient(
            os.getenv('VISION_ENDPOINT'),
            CognitiveServicesCredentials(os.getenv('VISION_KEY'))
        )

    def to_text(self, image):
        file = image.get_file()
        description = self.computervision_client.describe_image(file.file_path)
        return description.captions[-1]
