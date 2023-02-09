#!/usr/bin/env python
###############################################################################
#                                                                             #
#       Script for generating an overview image of a raster data file.        #
#       Uses bands 290, 140, and 20 as RGB channels by default.               #
#                                                                             #
#   Script written for Python 3.6 and higher                                  #
#   Needs standard extension  plus:                                           #
#      gdal                                                                   #
#                                                                             #
#   Originally written by Edward Hazelton                                     #
#   Alaska EPSCoR Fire & Ice                                                  #
#                                                                             #
###############################################################################
from typing import List

from osgeo import gdal
from osgeo import gdalconst
from parsing import get_filenames, get_parser, parse_args


# scales the parameters of bands
def get_scale_params(dataset, output_channels,
                     scale_func=lambda min_val, max_val, mean, stddev: [min_val, mean + 2 * stddev, 0, 254]):
    num_bands = dataset.RasterCount
    num_channels = len(output_channels)

    # quick index error checking
    # TODO make this better than just cropping the top. (scale down to 1 through num_bands?)
    if num_bands < max(output_channels):
        output_channels = [channel if num_bands >= channel else num_bands for channel in output_channels]

    scale_params = [0] * num_channels

    # iterate through the number of channels (should just be RGB channels but may change in the future)
    for idx, channel in enumerate(output_channels):
        band = dataset.GetRasterBand(channel)

        # get the statistics of the specified bands for rescaling
        stats = band.ComputeStatistics(0)

        scale_params[idx] = scale_func(*stats)

    return scale_params


def generate_image(input_files: List[str], output_files: List[str], bands: List[int]):
    for idx, in_file in enumerate(input_files):
        print(f"Processing {idx + 1} / {len(input_files)}: {in_file}")

        # gdal only likes strings
        dataset = gdal.Open(str(in_file), gdalconst.GA_ReadOnly)

        if not dataset:
            print('tried to open file %s but could not.' % str(in_file))
            continue

        scale_params = get_scale_params(dataset, bands)

        translate_options = gdal.TranslateOptions(
            format='GTiff',
            bandList=bands,
            creationOptions=['COMPRESS=JPEG', 'TILED=YES', 'PHOTOMETRIC=YCBCR'],
            outputType=gdal.GDT_Byte,
            scaleParams=scale_params,
            noData=255
        )

        gdal.Translate(output_files[idx], dataset, options=translate_options)


if __name__ == '__main__':
    # getting the arguments
    parser = get_parser('This is a script for generating an RGB overview image of raster data.')
    parser.add_argument('-r', '--red', help='Red band', default=290, dest='red', type=int)
    parser.add_argument('-g', '--green', help='Green band', default=140, dest='green', type=int)
    parser.add_argument('-b', '--blue', help='Blue band', default=20, dest='blue', type=int)
    arguments = parse_args(parser)

    # TODO possibly support different band values for individual flightlines
    bands = [arguments['red'], arguments['green'], arguments['blue']]

    input_files, output_files = get_filenames(arguments, f"{'_'.join(map(str, bands))}")

    generate_image(input_files, output_files, bands)
