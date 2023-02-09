# code for generating data mask

import numpy as np
import rasterio as rio

def getdatabounds(row, nodataval=0.0, reversesign=False):
    """
    If row has nodata at both edges, returns first and last data index
    Throws IndexError if only nodata
    """
    prefac = -1 if reversesign else 1
    cond = prefac * row > prefac * nodataval
    return np.nonzero(cond)[0][0], np.nonzero(cond)[0][-1]


def maskrow(row, lprop=0.0, rprop=0.0, nodataval=0):
    """
    Return boolean data row (0 = nodata). Optionally extend mask by 
    proportion between 0 and 1 into the data
    """
    newrow = np.ones(len(row))
    try:
        lbound, rbound = getdatabounds(row)
        newrow[:lbound] = nodataval
        newrow[rbound:] = nodataval
        return newrow
    except IndexError:
        return nodataval * newrow


def croprow(row, lprop=0.1, rprop=0.1, nodataval=0):
    """
    Return row cropped with 0 (= nodata).Eextend mask by 
    proportion between 0 and 1 into the data
    """
    try:
        lidx, ridx = getdatabounds(row)
        lidx = lidx + int((ridx - lidx) * lprop)
        ridx = ridx - int((ridx - lidx) * rprop)
        row[:lidx] = nodataval
        row[ridx:] = nodataval
    except IndexError:
        pass
    return row

def getflightlinemask(vnirpath, swirpath, vnirscapath, swirscapath):
    """
    Get flightline mask from all four _geo.bsq files
    """
    try:
        with rio.open(vnirpath) as vnir:
            with rio.open(swirpath) as swir:
                with rio.open(vnirscapath) as vnir_sca:
                    with rio.open(swirscapath) as swir_sca:
                        outmeta = vnir.meta.copy()
                        outmeta.update({
                            'dtype': 'int16',
                            'count': 1,
                            'nodata': 0
                        })
                        vnir_sampleband = vnir.read(1)
                        print("read vnir band")
                        swir_sampleband = swir.read(1)
                        print("read swir band")
                        vnir_alt = vnir_sca.read(3)
                        print("read vnir altitude")
                        swir_alt = swir_sca.read(3)
                        print("read swir altitude")
                        maskvnir = np.apply_along_axis(maskrow, 1, vnir_sampleband)
                        print("created vnir mask")
                        maskswir = np.apply_along_axis(maskrow, 1, swir_sampleband)
                        print("created swir mask")
                        maskvnir_alt = np.apply_along_axis(maskrow, 1, vnir_alt)
                        print("created vnir altitude mask")
                        maskswir_alt = np.apply_along_axis(maskrow, 1, swir_alt)
                        print("created swir altitude mask")
                        outdata = maskvnir * maskswir * maskvnir_alt * maskswir_alt
                        outdata = outdata.astype('int16')
    except:
        print(f"Didn't find all fines for flightline")
        raise
    return outdata, outmeta

