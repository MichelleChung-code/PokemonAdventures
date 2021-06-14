# https://towardsdatascience.com/train-image-recognition-ai-with-5-lines-of-code-8ed0bdd8d9ba
from imageai.Classification.Custom import ClassificationModelTrainer, CustomImageClassification
import os
import glob
from pathlib import Path
from pprint import pprint
import operator


class ImageRecognition:
    def __init__(self, image_dir, model_dir, test_img_path, run_stored_model_bool=False):
        """
        Class that uses the Image AI (https://imageai.readthedocs.io/en/latest/) to train and run a model that
        classifies images

        Args:
            image_dir: <str> path to directory containing test and train images
            model_dir: <str> path to directory to output model results
            test_img_path: <str> path to image to test model on
            run_stored_model_bool: <bool> whether or not a model has already been created and trained.  If True, run
            using the model stored in model_dir.  Otherwise, train the model again.
        """
        self.image_dir = image_dir
        self.model_dir = model_dir
        self.run_stored_model_bool = run_stored_model_bool
        self.test_img_path = test_img_path

        assert self.test_img_path.endswith(('.png', '.jpg'))

        # Number of objects - different possibilities that the image could be in the dataset
        self.n = len(os.listdir(os.path.join(self.image_dir, 'train')))

    def train_model(self):
        """ Create and train a model using the """
        # make sure the output path is clear first
        for f in glob.glob('{}/*'.format(self.model_dir)):
            os.remove(f)

        model = ClassificationModelTrainer()
        model.setModelTypeAsResNet50()
        model.setDataDirectory(self.image_dir, models_subdirectory=self.model_dir, json_subdirectory=self.model_dir)
        model.trainModel(num_objects=self.n, num_experiments=50, enhance_data=True, batch_size=10,
                         show_network_summary=True)

    def run_stored_model(self):
        model_predict = CustomImageClassification()
        model_predict.setModelTypeAsResNet50()

        # get model paths
        file_names = os.listdir(self.model_dir)
        model_path = os.path.join(self.model_dir, sorted([f for f in file_names if f.endswith('.h5')], reverse=True)[0])
        model_json_path = os.path.join(self.model_dir, [f for f in file_names if f.endswith('.json')][0])

        model_predict.setModelPath(model_path)
        model_predict.setJsonPath(model_json_path)
        model_predict.loadModel(num_objects=self.n)

        predictions, probabilities = model_predict.classifyImage(self.test_img_path, result_count=5)
        return dict(zip(predictions, probabilities))

    def __call__(self, *args, **kwargs):
        if self.run_stored_model_bool:
            pass
        else:
            self.train_model()  # will take a long time...

        res_dict = self.run_stored_model()

        final = max(res_dict.items(), key=operator.itemgetter(1))[0]
        res_dict.update({'FINAL_CHOICE': final.split()[1]})

        return res_dict


if __name__ == '__main__':
    mfs_path = os.path.join(str(Path(__file__).parents[5]), 'mfs')

    dir_path = os.path.join(mfs_path, 'pokemon_images_original')

    model_output_folder = 'model'
    model_output_path = os.path.join(str(Path(__file__).parents[0]), model_output_folder)
    if not os.path.exists(model_output_path):
        os.makedirs(model_output_path)

    # test with McKale's drawn image
    test_img_path = os.path.join(str(Path(__file__).parents[5]), 'images', 'Charmander.png')

    x = ImageRecognition(image_dir=dir_path, model_dir=model_output_path, test_img_path=test_img_path,
                         run_stored_model_bool=False)
    pprint(x())
