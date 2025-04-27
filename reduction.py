import os.path
import numpy as np

import pyreduce

# define parameters
instrument = 'LISA'
target = ''
mode = 'LISA'
night = '2025-04-04'
steps = (
    #"bias",
    #"flat",
    #"orders",
    #"norm_flat",
    #"wavecal",
    "wavecal_master",
    # "curvature",
    # "science",
    # "continuum",
    # "finalize",
)

# some basic settings
# Expected Folder Structure: base_dir/datasets/HD132205/*.fits.gz
# Feel free to change this to your own preference, values in curly brackets will be replaced with the actual values {}

# load dataset (and save the location)
base_dir = "/Data"
input_dir = "/Data/raw_float"
output_dir = "/Data/reduced"

config = pyreduce.configuration.get_configuration_for_instrument(instrument, plot=1)

pyreduce.reduce.main(
    instrument,
    target,
    night,
    mode,
    steps,
    base_dir=base_dir,
    input_dir=input_dir,
    output_dir=output_dir,
    configuration=config,
    order_range=(1, 21),
)

