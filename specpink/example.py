from specpink.pipeline import Pipeline

# change according to needs
data_path = './raw_data'
target_path_stacked = './stacked'
target_path_reduced = './reduced'
spectrum_path = '/reduced/spectrum.txt'

# run pipeline
pipe = Pipeline(data_path, target_path_stacked, target_path_reduced, spectrum_path)
pipe.full()
