import numpy as np
import os
import sys
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, Dropout
from keras.layers.advanced_activations import LeakyReLU
from keras.callbacks import ModelCheckpoint

#load data
print('load data')
train_data = np.load('train_data.npy')
val_data = np.load('val_data.npy')
output_file = sys.argv[1]

#split to x and y
print('split data')
train_x = train_data[:, :-1]
train_y = train_data[:, -1:]
val_x = val_data[:, :-1]
val_y = val_data[:, -1:]

#delete useless data
print('delete data')
del train_data
del val_data

#get mean and std
print('mean and std')
if os.path.exists('mean.npy'):
    mean = np.load('mean.npy')
else:
    mean = np.mean(train_x, axis = 0)
    np.save('mean', mean)
if os.path.exists('std.npy'):
    std = np.load('std.npy')
else:
    std = np.std(train_x, axis = 0)
    std[std == 0] = 1
    np.save('std', std)

#standardization
print('standardization')
train_x = (train_x - mean) / std
val_x = (val_x - mean) / std

#set model
print('set model')
model = Sequential()
model.add(Dense(units = 128, input_dim = train_x.shape[1]))
model.add(LeakyReLU())
model.add(BatchNormalization())
model.add(Dense(units = 64))
model.add(LeakyReLU())
model.add(BatchNormalization())
model.add(Dense(units = 32))
model.add(LeakyReLU())
model.add(BatchNormalization())
model.add(Dense(units = 1))

model.compile(optimizer = 'adam', loss = 'mean_squared_error')
checkpoint = ModelCheckpoint(output_file, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

#start training
print('training')
model.fit(train_x, train_y, batch_size = 64, epochs = 100, validation_data=(val_x, val_y), callbacks = callbacks_list)
