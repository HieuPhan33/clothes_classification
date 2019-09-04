import os
CLASSES = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]
BASE_PATH='data'

# define the names of the training, testing, and validation
# directories
TRAIN = "training"
VAL = "validation"
TEST = "evaluation"
EXTTRAIN = "extension_training"

# set the batch size when fine-tuning
BATCH_SIZE = 32

# set the path to the serialized model after training
MODEL_PATH = os.path.sep.join(["output", "img.model"])

# define the path to the output training history plots
UNFROZEN_PLOT_PATH = os.path.sep.join(["output", "unfrozen.png"])
WARMUP_PLOT_PATH = os.path.sep.join(["output", "warmup.png"])