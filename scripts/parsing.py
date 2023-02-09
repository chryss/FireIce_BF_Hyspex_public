# This is a central module for shared code in the image generation scripts.
from pathlib import Path
from argparse import ArgumentParser
from typing import Dict, List, Tuple, Any, Optional


def is_valid_raster_file(parser: ArgumentParser, arg: str) -> Path:
    """
    Checks if the file is a valid raster data file.
    Errors and exits the program if it fails.
    :param parser: The argument parser
    :param arg: the string representation of a path to verify
    :return: the verified path as a :class:`pathlib.Path`
    """
    path = Path(arg)
    if not path.exists() or not path.is_file():
        parser.error("The file %s does not exist!" % arg)
    elif 'atm' not in path.stem[-8:] or path.suffix not in {'.bsq', '.bil', '.bip'}:
        parser.error("The file %s is not a valid raster data file!" % path)
    else:
        return path


def is_valid_tif_filename(parser: ArgumentParser, arg: str) -> Path:
    """
    Checks if the filename is valid.
    The filename is valid if its path doesn't already exist and has the .tif extension.
    Errors and exits the program if it fails.
    :param parser: The argument parser
    :param arg: the string representation of a path to verify
    :return: the verified path as a :class:`pathlib.Path`
    """
    path = Path(arg)
    if path.exists():
        parser.error("The file %s already exists!" % arg)
    elif path.suffix != '.tif':
        parser.error("The file %s must be a .tif file!" % path)
    else:
        return path


# checks if the directory is valid.
def is_valid_dir(parser: ArgumentParser, arg: str) -> Path:
    """
    Checks if the directory is valid and creates it if it doesn't exist.
    Errors and exits the program if it fails.
    :param parser: The argument parser
    :param arg: the string representation of a path to verify
    :return: the verified path as a :class:`pathlib.Path`
    """
    path = Path(arg)
    if not path.exists():
        path.mkdir(parents=True)
    if not path.is_dir():
        parser.error("%s is not a directory!" % path)
    return path


def is_valid_output(parser: ArgumentParser, arg: str) -> Path:
    """
    Checks if the path is valid for an output.
    If its a file, see :func:`is_valid_tif_filename`.
    If its a directory, see :func:`is_valid_dir`.
    Errors and exits the program if it fails.
    :param parser: The argument parser
    :param arg: the string representation of a path to verify
    :return: the verified path as a :class:`pathlib.Path`
    """
    path = Path(arg)
    if path.suffix == '.tif':
        return is_valid_tif_filename(parser, arg)
    elif path.suffix == '':
        return is_valid_dir(parser, arg)


def get_parser(desc: str) -> ArgumentParser:
    """
    Creates an :class:`argparse.ArgumentParser` and adds 5 premade optional flags.
    An input file flag, an input directory flag, an output path flag, a prefix flag,
    and a flag to change what processing level of supercube was used
    (revert to Atmospheric correction. Default is BRDF correction).
    :param desc: The description for the parser
    :return: An :class:`argparse.ArgumentParser` with premade flags.
    """
    parser = ArgumentParser(description=desc)

    parser.add_argument('-f', '--file', help='Input file name', default=None, dest='file',
                        type=lambda x: is_valid_raster_file(parser, x))
    parser.add_argument('-d', '--dir', '--directory', help='Input directory', default=None, dest='dir',
                        type=lambda x: is_valid_dir(parser, x))
    parser.add_argument('-o', '--out', '--output', help='Output file or directory. File must end in .tif', default=None,
                        type=lambda x: is_valid_output(parser, x), dest='output')
    parser.add_argument('-p', '--prefix', default=None, dest='prefix', type=str,
                        help='Flightline prefix (e.g. 20200710-CPC)')
    parser.add_argument('--atm', help='Specifies to look for *atm.bsq files rather than *atm_bcor.bsq files',
                        dest='atm_only', action='store_true')

    return parser


def parse_args(parser: ArgumentParser) -> Dict[str, Any]:
    """
    Wraps around the regular :func:`~argparse.ArgumentParser.parse_args` call to provide custom handling for
    the default flags provided in :func:`get_parser`
    :param parser: :class:`argparse.ArgumentParser`
    :return: A dict equivalent to :class:`argparse.Namespace`
    """
    args = vars(parser.parse_args())
    if (not args['file'] and not args['dir']) or (args['file'] and args['dir']):
        parser.error('Must specify an input file OR an input directory!')
    else:
        if args['dir'] and args['output'].suffix != '':
            parser.error('Invalid arguments: Cannot specify an output file for an input directory!')
        args['input'] = args['file'] if args['file'] else args['dir']
    if not args['prefix']:
        # TODO Works as intended with DATE-LOCATION_* but not DATE_LOCATION_* (is the second something that happens?)
        args['prefix'] = args['input'].stem.split('_')[0]
    if not args['output']:
        args['output'] = args['file'].parent if args['file'] else args['dir']

    return args


def get_filenames(args: Dict, addtl_info: Optional[str]) -> Tuple[List[str], List[str]]:
    """
    Gets a list of filenames, representing each flightline.
    :param args: The command line arguments as a dict
    :param addtl_info: Any additional info that would be appended to the output filenames
    :return: A tuple containing all input files and their corresponding output filenames
    """
    if args['input'].is_file():
        in_file = args['input']
        if args['output'].is_dir():
            out_file = str(args['output'] / f"{in_file.stem}_{addtl_info + '_'}overview.tif")
        else:
            out_file = str(args['output'])
        return [in_file], [out_file]
    else:
        flightlines = list(args['input'].rglob(f"{args['prefix']}*{'atm.bsq' if args['atm_only'] else 'atm_bcor.bsq'}"))
        in_files = [str(pth) for pth in flightlines]
        out_files = [str(args['output'] / f"{pth.stem}_{addtl_info + '_'}overview.tif") for pth in flightlines]
        if len(in_files) != len(out_files):
            raise IndexError(f"The Number of input files {in_files} and output files {out_files} do not match!")
        return in_files, out_files
