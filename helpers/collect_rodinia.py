import os
import sys

import utils

model_path = utils.get_model_path(sys.argv, "rodinia")

# fetch Rotations
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/RODINIA2013/Li_Rodinia_v2013.rot"
    ],
    model_path,
    "Rotations",
)


# fetch Coastlines
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/RODINIA2013/Li_Rodinia_v2013_Coastlines.gpmlz",
    ],
    model_path,
    "Coastlines",
)

# fetch StaticPolygons
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/RODINIA2013/Li_Rodinia_v2013_StaticPolygons.gpmlz"
    ],
    model_path,
    "StaticPolygons",
)
