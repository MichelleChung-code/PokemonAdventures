from machine_learning.recognize_pokemon.image_recognition import ImageRecognition
import unittest
import os
from pathlib import Path


class ImageRecognitionUnitTests(unittest.TestCase):
    def setUp(self):
        self.model_path = os.path.join(str(Path(__file__).parents[1]), 'machine_learning', 'recognize_pokemon',
                                       'model_demo')
        self.test_image_path = os.path.join(str(Path(__file__).parents[0]), 'pokemon_unittests_data', 'Charmander.png')

    def test_recognize(self):
        test_img_path = os.path.join(str(Path(__file__).parents[5]), 'images', 'Charmander.png')

        x = ImageRecognition(image_dir=False, model_dir=self.model_path, test_img_path=self.test_image_path,
                             run_stored_model_bool=True)
        res_dict = x()
        self.assertEqual('Charmander', res_dict['FINAL_CHOICE'])
