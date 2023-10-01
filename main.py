# Load standard modules
import statistics

import numpy as np
from matplotlib import pyplot as plt
from orbit_determination import perform_orbit_determination

from utility_functions.tle import *


# Define import folder
data_folder = 'delfiC3/'

# Files to be uploaded
metadata = ['Delfi-C3_32789_202309240829.yml', 'Delfi-C3_32789_202309241900.yml']
data = ['Delfi-C3_32789_202309240829.csv', 'Delfi-C3_32789_202309241900.csv']

# Perform orbit determination
process_strategy = "per_day"
original_parameters, updated_parameters, errors, residuals = perform_orbit_determination(data_folder, metadata, data, process_strategy, nb_iterations=15, old_yml=False, old_obs_format=False)


# Retrieve indices and sizes for different parameters
nb_parameters = len(original_parameters)
nb_passes = len(data)
nb_state_parameters = int(nb_parameters - 2.0 * nb_passes)
ind_biases = nb_state_parameters
ind_time_drifts = nb_state_parameters + nb_passes

# Compute residuals statistics
mean_residuals = statistics.mean(residuals)
std_residuals = statistics.stdev(residuals)
rms_residuals = math.sqrt(np.square(residuals).mean())
print('mean_residuals', mean_residuals)
print('std_residuals', std_residuals)
print("rms_residuals", rms_residuals)

# Retrieve estimated parameter values
estimated_states = updated_parameters[:nb_state_parameters]
estimated_biases = updated_parameters[ind_biases:ind_biases+nb_passes]
estimated_time_drifts = updated_parameters[ind_time_drifts:ind_time_drifts+nb_passes]
print('update initial state', estimated_states - original_parameters[:nb_state_parameters])
print('estimated_biases', estimated_biases)
print('estimated_time_drifts', estimated_time_drifts)

# Retrieve estimation errors
sig_states = errors[:nb_state_parameters]
sig_biases = errors[ind_biases:ind_biases+nb_passes]
sig_time_drifts = errors[ind_time_drifts:ind_time_drifts+nb_passes]


fig = plt.figure()
fig.tight_layout()
plt.plot(residuals, color='blue', linestyle='-.')
plt.xlabel('Time [s]')
plt.ylabel('Residuals [m/s]')
plt.grid()
plt.show()

# Plot residuals histogram
fig = plt.figure()
fig.tight_layout()
plt.hist(residuals, 100)
plt.xlabel('Doppler residuals [m/s]')
plt.ylabel('Nb occurrences []')
plt.grid()
plt.show()

