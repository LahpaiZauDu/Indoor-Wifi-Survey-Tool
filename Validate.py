import numpy as np
from sklearn.model_selection import KFold
from pykrige.ok import OrdinaryKriging

# Generate some random data
x = np.random.rand(50)
y = np.random.rand(50)
z = np.sin(x * 2 * np.pi) * np.cos(y * 2 * np.pi)

# Set up k-fold cross-validation
n_splits = 5
kf = KFold(n_splits=n_splits)

# Perform cross-validation
mse = []
for train_index, test_index in kf.split(x):
    # Split the data into training and validation sets
    x_train, y_train, z_train = x[train_index], y[train_index], z[train_index]
    x_test, y_test, z_test = x[test_index], y[test_index], z[test_index]

    # Fit the kriging model to the training set
    OK = OrdinaryKriging(x_train, y_train, z_train)

    # Make predictions on the validation set
    z_pred, ss_pred = OK.execute('points', x_test, y_test)

    # Calculate the mean squared error (MSE) between predicted and true values
    mse.append(np.mean((z_pred - z_test) ** 2))

# Calculate the mean and standard deviation of the MSE across folds
mean_mse = np.mean(mse)
std_mse = np.std(mse)

print("Mean MSE:", mean_mse)
print("Std MSE:", std_mse)
