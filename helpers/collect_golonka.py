import os
import sys

import utils

model_path = utils.get_model_path(sys.argv, "golonka")

# fetch Rotations
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/GOLONKA/Phanerozoic_EarthByte.rot"
    ],
    model_path,
    "Rotations",
)


# fetch Coastlines
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/GOLONKA/Phanerozoic_EarthByte_Coastlines.gpmlz",
    ],
    model_path,
    "Coastlines",
)

# fetch StaticPolygons
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/GOLONKA/Phanerozoic_EarthByte_ContinentalRegions.gpmlz"
    ],
    model_path,
    "StaticPolygons",
)
