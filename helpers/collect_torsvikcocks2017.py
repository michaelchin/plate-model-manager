import os
import sys

import utils

model_path = utils.get_model_path(sys.argv, "torsvikcocks2017")

# fetch Rotations
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/TorsvikCocks2017/Torsvik_Cocks_HybridRotationFile.rot"
    ],
    model_path,
    "Rotations",
)


# fetch Coastlines
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/TorsvikCocks2017/Torsvik_Cocks_2016_Terranes.gpmlz",
    ],
    model_path,
    "Coastlines",
)

# fetch StaticPolygons
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/TorsvikCocks2017/Torsvik_Cocks_2016_Terranes.gpmlz"
    ],
    model_path,
    "StaticPolygons",
)
