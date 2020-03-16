from keras.datasets import boston_housing

val = boston_housing.load_data()


x_train = val[0][0]
y_train = val[0][1]
x_test  = val[1][0]
y_test  = val[1][1]

print("Number of training: ")
print("\tTraining examples and their features: ", x_train.size)
print("\t                   Training examples: ", y_train.size)

print("Number of Tests: ")
print("\tTest examples and their features: ", x_test.size)
print("\t                   Test examples: ", y_test.size)
print(" ------------------------------------------------")
print(
    ' Training examples and their features (axes: {}; shape: {}; type: {}): \n'.format(x_train.ndim, x_train.shape, x_train.dtype),
    'Training examples                     (axes: {}; shape: {}; type: {}):\n'.format(y_train.ndim, y_train.shape, y_train.dtype),
    'Test examples and their features      (axes: {}; shape: {}; type: {}): \n'.format(x_test.ndim, x_test.shape, x_test.dtype),
    'Test examples                         (axes: {}; shape: {}; type: {}): \n'.format(y_test.ndim, y_test.shape, y_test.dtype),
)

