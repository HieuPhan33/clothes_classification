import os
import random
import config
from shutil import copyfile
import pandas as pd
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--source','-s',default="data_src")
args = parser.parse_args()

def img_train_test_split(img_source_dir,splits,labels):
    if not (isinstance(img_source_dir, str)):
        raise AttributeError('img_source_dir must be a string')

    if not os.path.exists(img_source_dir):
        raise OSError('img_source_dir does not exist')

    if not (isinstance(splits[0], float) or isinstance(splits[1], float) ):
        raise AttributeError('train_size must be a float')
    # Set up empty folder structure if not exists

        # Get the subdirectories in the main image folder
    train_dir = os.path.join(config.BASE_PATH,config.TRAIN)
    val_dir = os.path.join(config.BASE_PATH,config.VAL)
    test_dir = os.path.join(config.BASE_PATH,config.TEST)

    if not os.path.exists(config.BASE_PATH):
        os.makedirs(config.BASE_PATH)
    else:
        if not os.path.exists(train_dir):
            os.makedirs(train_dir)
        if not os.path.exists(val_dir):
            os.makedirs(val_dir)
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
    for label in config.CLASSES:
        train_label_dir = os.path.join(train_dir,label)
        val_label_dir = os.path.join(val_dir,label)
        test_label_dir = os.path.join(test_dir,label)
        # Create subdirectories in train and validation folders
        if not os.path.exists(train_label_dir):
            os.makedirs(train_label_dir)

        if not os.path.exists(val_label_dir):
            os.makedirs(val_label_dir)

        if not os.path.exists(test_label_dir):
            os.makedirs(test_label_dir)


    subdirs = [subdir for subdir in os.listdir(img_source_dir) if
               os.path.isdir(os.path.join(img_source_dir, subdir))]

    for subdir in subdirs: # Iterate each sub-directory
        if subdir == 'Test-Images':
            continue
        subdir_fullpath = os.path.join(img_source_dir, subdir)

        for filename in os.listdir(subdir_fullpath):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                fileparts = filename.split('.')
                id = int(fileparts[0])
                label = str(labels[id])
                train_label_dir = os.path.join(train_dir,label,filename)
                validation_label_dir = os.path.join(val_dir,label,filename)
                test_label_dir = os.path.join(test_dir, label, filename)

                seed = random.uniform(0,1)
                if seed <= splits[0]:
                    copyfile(os.path.join(subdir_fullpath, filename),
                             train_label_dir)
                elif seed > splits[0] and seed < splits[0] + splits[1]:
                    copyfile(os.path.join(subdir_fullpath, filename),
                             validation_label_dir)
                else:
                    copyfile(os.path.join(subdir_fullpath, filename),
                             test_label_dir)



def main():
    df = pd.read_csv(os.path.join(args.source,'labels.csv'))
    labels = df["Expected"]
    img_train_test_split(args.source,[0.6,0.2],list(labels))

if __name__ == '__main__':
    main()
