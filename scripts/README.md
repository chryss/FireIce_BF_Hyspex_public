# Generating a FireRGB Overview Image

Using `generate_firergb_overview.py`, you can quickly generate overview images for your various raster files.

## Single File

If you only want to generate an overview image for one file, you can simply use:
```shell
generate_rgb_overview.py file path/to/file.bsq
```
The resultant overview image will have the same name as the file, but appended with `_firergb_byte_overview.tif`.
(i.e. `a.bsq` )
You can optionally change the output file name with the `-o` (or `--out_file`) flag.
Do note the output file name must end in `.tif`.
```shell
generate_rgb_overview.py file path/to/file.bsq --out_file out.tif
```
This will create the overview image at `path/to/out.tif`.

## A Directory

If you would rather generate overview images for every raster file within a directory, you can use the `dir` argument.
```shell
generate_rgb_overview.py dir path/to/dir/
```
The resultant overview images will follow the default naming pattern described above.
Currently, this cannot be changed.
However, the output directory that all of these images will be stored in can be changed.
Using the `-o` (or `--out_dir`) flag, you can specify what directory to write to.
`-o ./` would put the images in the same directory that the script is in.

## Other Optional Arguments

You can specify what bands to use as the red, green, and blue bands in the generated image(s).
These default to bands 290, 140, and 20 respectively.
Currently, you can only specify one set of bands that will be used for all images processed.
Do also note they must be specified before the `file` or `dir` arguments.
This can be done using `-r`, `-g`, `-b` to set each. For example:
```shell
generate_rgb_overview.py -r 1 -g 2 -b 3 file path/to/file.bsq
```
These optional arguments apply to both `file` and `dir` modes.