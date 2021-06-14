# https://towardsdatascience.com/train-image-recognition-ai-with-5-lines-of-code-8ed0bdd8d9ba
from imageai.Classification.Custom import ClassificationModelTrainer, CustomImageClassification
import os
import glob
from pathlib import Path


class ImageRecognition:
    def __init__(self, image_dir, model_dir, test_img_path, run_stored_model_bool=False):
        self.image_dir = image_dir
        self.model_dir = model_dir
        self.run_stored_model_bool = run_stored_model_bool
        self.test_img_path = test_img_path

    def train_model(self):
        n = len(os.listdir(os.path.join(self.image_dir, 'train')))
        model = ClassificationModelTrainer()
        model.setModelTypeAsResNet50()
        model.setDataDirectory(self.image_dir, models_subdirectory=self.model_dir, json_subdirectory=self.model_dir)
        model.trainModel(num_objects=n, num_experiments=100, enhance_data=True, batch_size=10,
                         show_network_summary=True)

    def run_stored_model(self):
        pass

    def __call__(self, *args, **kwargs):
        if self.run_stored_model_bool:
            pass
        else:
            self.train_model()


if __name__ == '__main__':
    mfs_path = os.path.join(str(Path(__file__).parents[5]), 'mfs')

    dir_path = os.path.join(mfs_path, 'pokemon_images')

    model_output_path = 'model'
    if not os.path.exists(model_output_path):
        os.makedirs(model_output_path)

    x = ImageRecognition(image_dir=dir_path, model_dir=model_output_path, test_img_path=False,
                         run_stored_model_bool=False)
    x()
