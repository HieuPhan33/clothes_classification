import os
import random
import config
from shutil import copyfile
import pandas as pd
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--source','-s',default="data_src")
args = parser.parse_args()

def img_train_test_split(img_source_dir,train_size,labels):
    if not (isinstance(img_source_dir, str)):
        raise AttributeError('img_source_dir must be a string')

    if not os.path.exists(img_source_dir):
        raise OSError('img_source_dir does not exist')

    if not (isinstance(train_size, float)):
        raise AttributeError('train_size must be a float')
    # Set up empty folder structure if not exists
    if not os.path.exists('data'):
        os.makedirs('data')
    else:
        if not os.path.exists('data/train'):
            os.makedirs('data/train')
        if not os.path.exists('data/validation'):
            os.makedirs('data/validation')
        # Get the subdirectories in the main image folder
    train_dir = os.path.join(config.BASE_PATH,config.TRAIN)
    val_dir = os.path.join(config.BASE_PATH,config.VAL)
    for label in config.CLASSES:
        train_label_dir = os.path.join(train_dir,label)
        val_label_dir = os.path.join(val_dir,label)
        # Create subdirectories in train and validation folders
        if not os.path.exists(train_label_dir):
            os.makedirs(train_label_dir)

        if not os.path.exists(val_label_dir):
            os.makedirs(val_label_dir)


    subdirs = [subdir for subdir in os.listdir(img_source_dir) if
               os.path.isdir(os.path.join(img_source_dir, subdir))]

    for subdir in subdirs: # Iterate each sub-directory
        subdir_fullpath = os.path.join(img_source_dir, subdir)

        for filename in os.listdir(subdir_fullpath):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                fileparts = filename.split('.')
                id = int(fileparts[0])
                label = str(labels[id])
                train_label_dir = os.path.join(train_dir,label,fileparts[0]+'.'+fileparts[1])
                validation_label_dir = os.path.join(val_dir,label,fileparts[0]+'.'+fileparts[1])


                if random.uniform(0, 1) <= train_size:
                    copyfile(os.path.join(subdir_fullpath, filename),
                             train_label_dir)
                else:
                    copyfile(os.path.join(subdir_fullpath, filename),
                             validation_label_dir)


def img_train_test_split_(img_source_dir, train_size):
    """
    Randomly splits images over a train and validation folder, while preserving the folder structure

    Parameters
    ----------
    img_source_dir : string
        Path to the folder with the images to be split. Can be absolute or relative path

    train_size : float
        Proportion of the original images that need to be copied in the subdirectory in the train folder
    """
    if not (isinstance(img_source_dir, str)):
        raise AttributeError('img_source_dir must be a string')

    if not os.path.exists(img_source_dir):
        raise OSError('img_source_dir does not exist')

    if not (isinstance(train_size, float)):
        raise AttributeError('train_size must be a float')

    # Set up empty folder structure if not exists
    if not os.path.exists('data'):
        os.makedirs('data')
    else:
        if not os.path.exists('data/train'):
            os.makedirs('data/train')
        if not os.path.exists('data/validation'):
            os.makedirs('data/validation')

    # Get the subdirectories in the main image folder
    subdirs = [subdir for subdir in os.listdir(img_source_dir) if os.path.isdir(os.path.join(img_source_dir, subdir))]

    for subdir in subdirs:
        if subdir == 'Test-Images': continue
        subdir_fullpath = os.path.join(img_source_dir, subdir)
        if len(os.listdir(subdir_fullpath)) == 0:
            print(subdir_fullpath + ' is empty')
            break

        train_subdir = os.path.join('data/train', subdir)
        validation_subdir = os.path.join('data/validation', subdir)

        # Create subdirectories in train and validation folders
        if not os.path.exists(train_subdir):
            os.makedirs(train_subdir)

        if not os.path.exists(validation_subdir):
            os.makedirs(validation_subdir)

        train_counter = 0
        validation_counter = 0

        # Randomly assign an image to train or validation folder
        for filename in os.listdir(subdir_fullpath):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                fileparts = filename.split('.')

                if random.uniform(0, 1) <= train_size:
                    copyfile(os.path.join(subdir_fullpath, filename),
                             os.path.join(train_subdir, str(train_counter) + '.' + fileparts[1]))
                    train_counter += 1
                else:
                    copyfile(os.path.join(subdir_fullpath, filename),
                             os.path.join(validation_subdir, str(validation_counter) + '.' + fileparts[1]))
                    validation_counter += 1

        print('Copied ' + str(train_counter) + ' images to data/train/' + subdir)
        print('Copied ' + str(validation_counter) + ' images to data/validation/' + subdir)

def main():
    df = pd.read_csv(os.path.join(argparse.source,'labels.csv'))
    labels = df["Expected"]
    img_train_test_split(argparse.source,0.8,list(labels))

if __name__ == '__main__':
    main()
