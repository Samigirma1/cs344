import keras
from keras import models, layers
from keras.datasets import boston_housing

(train_data, train_targets), (test_data, test_targets) =  boston_housing.load_data()


mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std

test_data -= mean
test_data /= std


def build_model():
    # Because we will need to instantiate
    # the same model multiple times,
    # we use a function to construct it.
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu',
                           input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model

def build_wider_model():
    # Because we will need to instantiate
    # the same model multiple times,
    # we use a function to construct it.
    model = models.Sequential()
    model.add(layers.Dense(66, activation='relu',
                           input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(66, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model

def build_deeper_model():
    # Because we will need to instantiate
    # the same model multiple times,
    # we use a function to construct it.
    model_deeper = models.Sequential()
    model_deeper.add(layers.Dense(64, activation='relu',
                           input_shape=(train_data.shape[1],)))
    model_deeper.add(layers.Dense(64, activation='relu'))
    model_deeper.add(layers.Dense(64, activation='relu'))
    model_deeper.add(layers.Dense(1))
    model_deeper.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model_deeper


import numpy as np

k = 4
num_val_samples = len(train_data) // k
num_epochs = 100
all_scores_default = []
all_scores_wider = []
all_scores_deeper = []
for i in range(k):
    print('processing fold #', i)
    # Prepare the validation data: data from partition # k
    val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
    val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]

    # Prepare the training data: data from all other partitions
    partial_train_data = np.concatenate(
        [train_data[:i * num_val_samples],
         train_data[(i + 1) * num_val_samples:]],
        axis=0)
    partial_train_targets = np.concatenate(
        [train_targets[:i * num_val_samples],
         train_targets[(i + 1) * num_val_samples:]],
        axis=0)

    # Build the Keras model (already compiled)
    model = build_model()
    model_wider = build_wider_model()
    model_deeper = build_deeper_model()

    # Train the model (in silent mode, verbose=0)
    model.fit(partial_train_data, partial_train_targets,
              epochs=num_epochs, batch_size=1, verbose=0)
    model_wider.fit(partial_train_data, partial_train_targets,
                    epochs=num_epochs, batch_size=1, verbose=0)
    model_deeper.fit(partial_train_data, partial_train_targets,
                     epochs=num_epochs, batch_size=1, verbose=0)
    # Evaluate the model on the validation data
    val_mse, val_mae = model.evaluate(val_data, val_targets, verbose=0)
    all_scores_default.append(val_mae)

    val_mse, val_mae = model_wider.evaluate(val_data, val_targets, verbose=0)
    all_scores_wider.append(val_mae)

    val_mse, val_mae = model_deeper.evaluate(val_data, val_targets, verbose=0)
    all_scores_deeper.append(val_mae)

x = {
    "default": np.mean(all_scores_default),
    "wider": np.mean(all_scores_wider),
    "deeper": np.mean(all_scores_deeper)
}
print(x)