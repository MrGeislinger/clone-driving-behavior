import numpy as np
import os.path
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile


def load_ext_file(data_zip_url, data_path='data/'):
    '''Download the zip file from URL and extract it to path (if specified).
    '''
    # Check if path already exits
    if not os.path.exists(data_path):
        with urlopen(data_zip_url) as zip_resp:
            with ZipFile(BytesIO(zip_resp.read())) as zfile:
                # Extract files into the data directory
                zfile.extractall(path=None)


##### Data Augmentation #####
# We can do some data augmentation to the images to have more variety in the training material.

def flip_image(image, target):
    '''Horizontally flip image and target value.
    '''
    image_flipped = np.fliplr(image)
    target_flipped = -target
    return image_flipped, target_flipped
    

def adjust_offcenter_image(image, target, correction: float = 1e-2,
                                  img_camera_type: str = 'center'):
    '''
    Return an adjusted target based on type of image.
    
    img_camera_type: The type of camera image
    target: The target value (to be adjusted)
    '''
    # Adjust the target slightly for off-center image
    if img_camera_type == 'left':
        new_target = target + correction
    elif img_camera_type == 'right':
        new_target = target - correction
    # Don't make any correction if unknown or center
    else: 
        new_target = target
    return image, new_target


# Since the data is biased towards to low steering (driving straight), randomly drop some of the data to discourage simply driving straight.
def skip_low_steering(steer_value, steer_threshold=0.05, drop_percent=0.2):
    '''Return whether steering value should be used (within threshold; randomly
    determined).
    '''
    # Keep value if greater than threshold or by chance
    return (steer_value < steer_threshold['left']
            or steer_value > steer_threshold['right']
            or np.random.rand() > drop_percent)
        


def translate_image (image, target, correction=100, scale_factor=0.2):
    '''Randomly translates image horizontally and returns the image and adjusted
    target.
    '''
    # Translate the image randomly about correction factor (then scaled)
    adjustment = int(correction * np.random.uniform(-1*scale_factor, scale_factor))
    # Get a new
    target_new = target + (adjustment / correction)
    n,m,c=image.shape
    bigsquare=np.zeros((n,m+correction,c),image.dtype) 
    if adjustment < 0:
        bigsquare[:,:m+adjustment]=image[:,-adjustment:m]
    else:
        bigsquare[:,adjustment:m+adjustment]=image
    return bigsquare[:n,:m,:], target_new


##### Model Evaluation ######

import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')

def eval_model(model, model_history, X, y, show=True):
    '''Prints model history
    '''
    score = model.evaluate(X, y)
    print(f'Loss: {score:.2f}')

    if show:
        plt.plot(model_history.history['loss'], label='Loss (training data)')
        plt.plot(model_history.history['val_loss'], label='Loss (validation data)')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(loc='upper right')
        plt.show()
