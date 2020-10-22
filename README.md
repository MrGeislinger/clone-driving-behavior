# Cloning Driving Behavior

> Project for the Udacity - Self-Driving Car NanoDegree [![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

# Overview

This project uses a convolutional neural network (CNN) of a simulated car driving on a track to clone driving behavior. The model can be used to output steering angle to an autonomous car.

# Running the Project

## Setup

To reproduce the autonomous driving in the simulation, having the same 
environment as when the model was trained will be helpful.

### Using `requirements.txt`

```sh
pip install -r requirements.txt
```

### Using `conda`

```sh
conda env create -f environment.yml
```

## Training the model

To train the model provided you can use this command:

```sh
python model.py
```

This will automatically download the data & uncompress the files (if not already downloaded) and train the model to produce `model.h5`. Note the the data are deleted at the end of the script.


## Running the simulator 

To run the simulator, please check out this public repo: https://github.com/udacity/self-driving-car-sim

### `drive.py`

After the model has been trained and saved to `model.py`, you can run this command after starting the simulatior:

```sh
python drive.py model.h5
```

### Produce video `video.py` 

You can also produce save images while the model drives the car (autonomously). We do this by adding to the earlier command a directory to save images:

```sh
python drive.py model.h5 auto_run
```

These images can then be used to produce a video with this command:


```sh
python video.py auto_run
```

This will produce a video `auto_run.mp4`
