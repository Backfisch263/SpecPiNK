from reducer import Reducer
from calibrator import Calibrator
from pipeline import Pipeline
import matplotlib.pyplot as plt
import numpy as np

data_path = '/home/andreas/PycharmProjects/SpecPiNk/Data/prepared/'
target_path = '/home/andreas/PycharmProjects/SpecPiNk/Data/test'

raw = Calibrator(data_path)
stacks = raw.create_stacks()
stacks['flat'] = raw.normalize_flat()
