# code for manipulating metadata

from typing import AnyStr, List, Dict, Any

import pytz
import datetime as dt


def metadata_to_dict(metadatalist: List[AnyStr]) -> Dict:
    """Take metadata in list-of-lines form, parse into dict"""
    metadict = {}
    for line in metadatalist:
        newitem = [item.strip() for item in line.split('=', 1)]
        try:
            metadict[newitem[0]] = metadict[newitem[0]] + ' ' + newitem[1]
        except KeyError:
            try:
                metadict[newitem[0]] = newitem[1]
                lastkey = newitem[0]
            except IndexError:
                metadict[lastkey] = metadict[lastkey] + ' ' + newitem[0]
    return metadict


def hdrfile_to_dict(fp) -> Dict:
    """Take file path, return dictionary"""
    with open(fp) as src:
        lines = src.readlines()
        metadata = metadata_to_dict(lines[1:])
    return metadata


def gen_band_names(bands: int) -> str:
    if bands == 457:
        bandnames = ([f"Band {item} (VNIR Band {item})" for item in range(1, 171)] +
                     [f"Band {item + 169} (SWIR Band {item})" for item in range(2, 289)])
    else:
        bandnames = [f"Band {item}" for item in range(1, bands + 1)]
    return '{ ' + ", ".join(bandnames) + ' }'


def get_utctime(timestr: AnyStr) -> Any:
    timestamp = dt.datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%S.0Z")
    tz = pytz.timezone("America/Anchorage")
    localtime = tz.localize(timestamp)
    return localtime.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.0Z")
