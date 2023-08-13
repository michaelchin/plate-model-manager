import os
import sys

import utils

model_path = utils.get_model_path(sys.argv, "seton2012")

# fetch coastlines
utils.fetch_coastlines(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/SETON2012/Seton_etal_ESR2012_Coastlines_2012.1_Polygon.gpmlz",
    model_path,
    "Seton_etal_ESR2012_Coastlines_2012.1_Polygon.gpmlz",
)


# fetch static polygons
utils.fetch_static_polygons(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/SETON2012/Seton_etal_ESR2012_StaticPolygons_2012.1.gpmlz",
    model_path,
    "Seton_etal_ESR2012_StaticPolygons_2012.1.gpmlz",
)


# fetch rotations
utils.fetch_rotations(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/SETON2012/Seton_etal_ESR2012_2012.1.rot",
    model_path,
    "Seton_etal_ESR2012_2012.1.rot",
)

# fetch continental polygons
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/SETON2012/Seton_etal_ESR2012_ContinentalPolygons_2012.1.gpmlz"
    ],
    model_path,
    "ContinentalPolygons",
)

# fetch COBs
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/SETON2012/Seton_etal_ESR2012_ContinentOceanBoundaries_2012.1.gpmlz"
    ],
    model_path,
    "COBs",
)
