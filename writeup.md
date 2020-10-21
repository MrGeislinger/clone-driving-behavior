# Overview

> For a more interactive process of the model trainig process and decisions, please see the associated Jupyter notebook [model.ipynb](model.ipynb)

# Method

## Data for Model Training

An important aspect of the model training is to have sufficient data. Without a good variety of data, the model will not be able to perform well in a variety of situations that the vehicle may find itself in.

There were approximately 3 runs of the course as well as additional runs of difficult turns and course corrections (returning to middle of the road when straying to the shoulder of the road.

### Data Generation

Since we are limited by the amount of data already collected, we can generate more data by tweaking the images (and targets/steering values) to produce more data.

The data will be then be produced by an image generator for training and validation to make it easier for the model to train with the available computing resources.

#### Flipping images

We can add more variety to the data set by flipping the image. We adjust the target

#### Using off-center images

Since the simulated car has three cameras mounted on the left, center, and right, we can use the off-center camera images as templates of driving too far left and right. This involved modifying the target values by $\pm 0.25$. This allows more variety of course correcting situations to an overall smooth-driving training set.

#### Translate images

Translating images allows us to use simulate how to correct when the car is going off the middle of the track. We randomly translated images left and right randomly up to 50 pixels. We also correct the target values to represent this adjustment. The target value was adjusted according to how much translation.

#### Filtering Data

We noticed that many of the steering angles were small and slightly negative (straight driving and slight left turning respectively). To avoid this bias in the model, we randomly removed steering between $-0.010$ and $0.005$ $30\%$ of the time.

### Final Data

Below are three random images that are representative of the training, validation, and testing sets:

![Three images of data used](images/example_data_images.png)

## Model Architecture

This model was inspired by the work done by [NVIDIA for autonomous vehicles](https://developer.nvidia.com/blog/deep-learning-self-driving-cars/). The model consists of 9 layers, including a normalization layer, 6 convolutional layers, and 4 fully connected layers.

### Normalization Layer

The first layer of the network performs image normalization and was hard-coded so doesn't get tuned during the training process. The goal of this layer was to help optimize GPU processing for training process.

### Cropping Layer

The next layer is included to crop the images to focus on just the road section of the image. This layer doesn't change during the training process.

### Convolutional Layers

The convolutional layers perform feature extraction; layers progressively reduce dimensionality of the feature maps but increase complexity. We use initialeze weights with He normalization and ELU activations to add nonlinearity. The number of filters go like 24-36-46-48-64-64 where the first three layers use a kernel size of 5 and the rest of the layers use a kernel size of 3. After each layer, we add a max pooling layer (size 2) to help reduce complexity.

To reduce overfitting, we use add dropout layers after the 2nd 36-filter layer and 2nd 48-filter layer. We dropout neurons with a 40% chance in each epoch.

### Fully-Connected Layers

After the convolutional layers, we flatten the feature maps and pass it through 4 fully-connected layers. It progressively decreases the number of neurons; the number of neurons for each filter goes like 1024-128-64-16 neurons. Each layer uses the RELU activation function. To reduce overfitting, we include dropout layers after the first two layers.


## Training

To help with hyperparameter tuning, the Adam optimizer was used with Nesterov momentum. This has been shown to perform well on many systems and the Nesterov momentum helps the model converge even faster.

The data was split by using training and validation generators and ultimately evaluated with a testing generator. This allowed the model to be trained in batches for each epoch

Early stopping was also implemented so that after the model doesn't improve after a number epochs, the training will stop and retain the best results (according to the training loss). This helps the model from overfitting as the model's weights are tuned during the training process.

# Results

## Model Evaluation