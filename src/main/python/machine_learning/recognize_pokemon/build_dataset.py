import os
from bing_image_downloader import downloader
import pandas as pd
import shutil

mfs_path = '../../../../../mfs'

dir_path = os.path.join(mfs_path, 'pokemon_images')

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

pokemon_df = pd.read_csv(os.path.join(mfs_path, 'pokedex_data.csv'))

pokemon_names_ls = set(pokemon_df['Name'].to_list())

for name in pokemon_names_ls:
    train_dir = os.path.join(dir_path, 'train')
    search_key = 'Pokemon {}'.format(name)
    test_dir_w_name = os.path.join(dir_path, 'test', search_key)

    # train set will have 50 images per mon, test set will have 5/mon
    downloader.download(search_key, limit=55, output_dir=train_dir,
                        adult_filter_off=False, force_replace=False, timeout=60)

    # Move five into the test folder
    file_names = os.listdir(os.path.join(train_dir, search_key))[:5]

    if not os.path.exists(test_dir_w_name):
        os.makedirs(test_dir_w_name)

    for file_name in file_names:
        shutil.move(os.path.join(train_dir, search_key, file_name),
                    os.path.join(test_dir_w_name, file_name))
