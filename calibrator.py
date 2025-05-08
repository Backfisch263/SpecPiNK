import os
import numpy as np
from scipy.ndimage import gaussian_filter
from .utils import load_fits_file, get_imagetype, save_fits_file

class CalibrationCreator:
    def __init__(self, files):
        self.files = files
        self.stacks = {'bias': None, 'dark': None, 'flat': None, 'lamp': None, 'light': None}
        self.stack_headers = {'bias': None, 'dark': None, 'flat': None, 'lamp': None, 'light': None}
        self.master_frames = {'bias': None, 'dark': None, 'flat': None, 'lamp': None, 'light': None}

    def create_stacks(self):
        groups = {'bias': [], 'dark': [], 'flat': [], 'lamp': [], 'light': []}
        headers = {'bias': [], 'dark': [], 'flat': [], 'lamp': [], 'light': []}
        # Group files by IMAGETYP
        for file in self.files:
            data, header = load_fits_file(file)
            imagetyp = get_imagetype(header)
            if 'bias' in imagetyp:
                groups['bias'].append(data)
                headers['bias'].append(header)
            elif 'dark' in imagetyp:
                groups['dark'].append(data)
                headers['dark'].append(header)
            elif 'flat' in imagetyp:
                groups['flat'].append(data)
                headers['flat'].append(header)
            elif 'lamp' in imagetyp:
                groups['lamp'].append(data)
                headers['lamp'].append(header)
            elif 'light' in imagetyp:
                groups['light'].append(data)
                headers['light'].append(header)

        # Combine using median
        for key in groups:
            if groups[key]:
                stack = np.stack(groups[key], axis=0)
                self.stacks[key] = np.median(stack, axis=0)

                stack_header = headers[key][0].copy()   # Copy header, so the original header is not modified
                self.stack_headers[key] = stack_header
                print(f"Created {key} stack from {len(groups[key])} files")
            else:
                self.stacks[key] = None
                print(f"No {key} frames provided.")

        return self.stacks
    '''
    Normalize flat field
    '''
    def normalize_flat(self):
        if self.stacks['flat'] is not None:
            flat = np.copy(self.stacks['flat'])
            flat_gaussfiltered = gaussian_filter(flat, sigma=5)
            flat_normal = flat - flat_gaussfiltered
            flat_normal = flat_normal - np.min(flat_normal)
            flat_normal = flat_normal / np.max(flat_normal)
            return flat_normal
        else:
            print('No flat field images provided to create normalized flat field.')
            return None

    def create_master_frames(self):
        if not self.stacks:
            print('No stacks created yet. Run create_stacks() first.')
            return None
        else:
            for key in self.stacks:
                if self.stacks[key] is not None:
                    self.master_frames[key] = self.stacks[key]

                flat_normal = self.normalize_flat()
                if flat_normal is not None:
                    self.master_frames['flat'] = flat_normal
                    print('Normalized flat field added to master frames.')
                else:
                    print('No flat field image provided to add to master frames.')
            return self.master_frames

    def save_master_frames(self, output_dir='calibration_files'):
        for key, frame in self.master_frames.items():
            if frame is not None:
                header = self.stack_headers[key]
                filename = os.path.join(output_dir, f"master_{key}.fits")
                save_fits_file(filename, frame, header)
            else:
                print(f"No master frame to save for {key}")
