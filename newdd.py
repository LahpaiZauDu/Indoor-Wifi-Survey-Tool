from pykrige.ok import OrdinaryKriging
import numpy as np
import Functions as f

from sklearn.metrics import mean_absolute_error, mean_squared_error


xcoordinates, ycoordinates, rssi = f.Random_Validation_points(
    'Data/New_MAX.csv')
x_points = xcoordinates
y_points = ycoordinates
phi_values = rssi

# Calculate the start and stop values
x_start_val = np.min(x_points) - 1
x_stop_val = np.max(x_points) + 1

y_start_val = np.min(y_points) - 1
y_stop_val = np.max(y_points) + 1

p_start_val = np.min(phi_values) - 1
p_stop_val = np.max(phi_values) + 1

# Define the coordinates where you want to estimate the phi values
x_est = np.linspace(x_start_val, x_stop_val, 3)
y_est = np.linspace(y_start_val, y_stop_val, 3)
xx, yy = np.meshgrid(x_est, y_est)
x_coords = xx.flatten()
y_coords = yy.flatten()


# Perform ordinary kriging to estimate the phi values at the specified coordinates
ok = OrdinaryKriging(x_points, y_points, phi_values,
                     variogram_model='spherical', verbose=False, enable_plotting=False)
z, ss = ok.execute('grid', x_est, y_est)

# Calculate the MAE and RMSE
mae = mean_absolute_error(phi_values, z.flatten())
rmse = np.sqrt(mean_squared_error(phi_values, z.flatten()))

# Print the MAE and RMSE
print("MAE: ", mae)
print("RMSE: ", rmse)
