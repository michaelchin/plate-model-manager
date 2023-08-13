import os
import sys

import utils

model_path = utils.get_model_path(sys.argv, "paleomap")

# fetch Rotations
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/PALEOMAP/PALEOMAP_PlateModel.rot"
    ],
    model_path,
    "Rotations",
)


# fetch Coastlines
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/PALEOMAP/PALEOMAP_coastlines.gpmlz",
    ],
    model_path,
    "Coastlines",
)

# fetch StaticPolygons
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/PALEOMAP/PALEOMAP_PlatePolygons.gpmlz"
    ],
    model_path,
    "StaticPolygons",
)
