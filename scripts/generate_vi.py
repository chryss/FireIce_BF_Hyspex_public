#!/usr/bin/env python
###############################################################################
#                                                                             #
#       Script for generating an overview of various indexes of raster data.  #
#       Defaults to the NDVI index.                                           #
#                                                                             #
#   Script written for Python 3.6 and higher                                  #
#   Needs standard extension  plus:                                           #
#      gdal                                                                   #
#      matplotlib                                                             #
#                                                                             #
#   Originally written by Edward Hazelton                                     #
#   Alaska EPSCoR Fire & Ice                                                  #
#                                                                             #
###############################################################################

from typing import List
from osgeo import gdal, gdalconst
from parsing import parse_args, get_parser, get_filenames
import numpy as np

indices_to_wavelengths = {
    'ndvi': [645.0, 857.0],
    'evi': [469.0, 645.0, 857.0],
    'vig': [555.0, 645.0],
    'vari': [469.0, 555.0, 645.0],
    'ndii6': [857.0, 1640.0],
    'ndii7': [857.0, 2130.0],
    'wi': [900.0, 970.0],
    'ndwi': [857.0, 1240.0]
}


def get_nearest_bands(bands: List[float], target_wavelengths: List[float]) -> List[int]:
    band_indices = [0]*len(target_wavelengths)
    for idx in range(len(bands)):
        for target_idx, target_wavelength in enumerate(target_wavelengths):
            if bands[idx] <= target_wavelength <= bands[idx + 1]:
                band_indices[target_idx] = idx
    return band_indices


def get_band_info(hdr_file: str, target_wavelengths: List[float]) -> List[int]:
    with open(hdr_file) as file:
        for line in file.readlines():
            if line.startswith('wavelength'):
                bands = [float(band.strip(' {}\n')) for band in line.split('=')[1].split(',')]
                return get_nearest_bands(bands, target_wavelengths)


def generate_images(input_files: List[str], output_files: List[str], vi_type: str):
    for in_file, out_file in zip(input_files, output_files):
        generate_vi(in_file, out_file, vi_type)


def generate_vi(input_file: str, output_file: str, vi_type: str):
    # gdal only likes strings
    dataset = gdal.Open(str(input_file), gdalconst.GA_ReadOnly)

    if not dataset:
        print('tried to open file %s but could not.' % str(input_file))
        return

    global indices_to_wavelengths

    target_bands = get_band_info(f"{''.join(input_file.rsplit('.', 1)[0])}.hdr", indices_to_wavelengths[vi_type])

    bands = []
    for band in target_bands:
        bands.append(dataset.GetRasterBand(band).ReadAsArray())
    y_size, x_size = bands[0].shape

    with np.errstate(divide='ignore', invalid='ignore'):
        if vi_type == 'ndvi':
            vi_index = np.divide((bands[1] - bands[0]), (bands[1] + bands[0]))
        elif vi_type == 'evi':
            vi_index = 2.5 * np.divide(bands[2] - bands[1], bands[2] + 6 * bands[2] - 7.5 * bands[0] + 1)
        elif vi_type == 'vig':
            vi_index = np.divide((bands[1] - bands[0]), (bands[1] + bands[0]))
        elif vi_type == 'vari':
            vi_index = np.divide((bands[2] - bands[1]), (bands[2] + bands[1] - bands[0]))
        elif vi_type == 'wi':
            vi_index = np.divide(bands[0], bands[1])
        elif vi_type == 'ndwi':
            vi_index = np.divide((bands[0] - bands[1]), (bands[0] + bands[1]))

    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(output_file, x_size, y_size, 1, gdal.GDT_Float32)
    outdata.SetGeoTransform(dataset.GetGeoTransform())  # sets same geotransform as input
    outdata.SetProjection(dataset.GetProjection())  # sets same projection as input
    outdata.GetRasterBand(1).WriteArray(vi_index)
    outdata.FlushCache()  # saves to disk


if __name__ == '__main__':
    # getting the arguments
    parser = get_parser('This is a script for generating an overview of various vegetation indices of raster data.')
    parser.add_argument('-v', '--veg-idx', '--vegetation-index', default='ndvi', type=str.lower, dest='vi_type',
                        choices=['ndvi', 'evi', 'vig', 'vari', 'ndii6', 'ndii7', 'wi', 'ndwi'],
                        help='''
                        Specify what vegetation index to calculate.
                        NDVI: Normalized Difference Vegetation Index
                        EVI: Enhanced Vegetation Index
                        VIg: Visible Green Index
                        VARI: Visible Atmospherically Resistant Index
                        NDII6: Normalized Difference Infrared Index 6
                        NDII7: Normalized Difference Infrared Index 7
                        WI: Water Index
                        NDWI: Normalized Difference Water Index
                        ''')

    arguments = parse_args(parser)

    input_files, output_files = get_filenames(arguments, f"{arguments['vi_type']}")

    generate_images(input_files, output_files, arguments['vi_type'])
