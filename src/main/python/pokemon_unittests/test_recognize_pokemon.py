import os
import unittest
from pathlib import Path

from src.main.python.machine_learning.recognize_pokemon.image_recognition import ImageRecognition


class ImageRecognitionUnitTests(unittest.TestCase):
    def setUp(self):
        self.model_path = os.path.join(str(Path(__file__).parents[1]), 'machine_learning', 'recognize_pokemon',
                                       'model_starters')

    def test_recognize_bulbasaur(self):
        test_img_path = os.path.join(str(Path(__file__).parents[0]), 'pokemon_unittests_data', 'Bulbasaur.png')

        x = ImageRecognition(image_dir=False, model_dir=self.model_path, test_img_path=test_img_path,
                             run_stored_model_bool=True)
        res_dict = x()
        self.assertEqual('Bulbasaur', res_dict['FINAL_CHOICE'])

    # todo work on a model that passes the next two unittests
    # def test_recognize_charmander(self):
    #     test_img_path = os.path.join(str(Path(__file__).parents[0]), 'pokemon_unittests_data', 'Charmander.png')
    #
    #     x = ImageRecognition(image_dir=False, model_dir=self.model_path, test_img_path=test_img_path,
    #                          run_stored_model_bool=True)
    #     res_dict = x()
    #     self.assertEqual('Charmander', res_dict['FINAL_CHOICE'])
    #
    # def test_recognize_squirtle(self):
    #     test_img_path = os.path.join(str(Path(__file__).parents[0]), 'pokemon_unittests_data', 'Squirtle.png')
    #
    #     x = ImageRecognition(image_dir=False, model_dir=self.model_path, test_img_path=test_img_path,
    #                          run_stored_model_bool=True)
    #     res_dict = x()
    #     self.assertEqual('Squirtle', res_dict['FINAL_CHOICE'])
