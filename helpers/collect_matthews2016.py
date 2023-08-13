import os
import sys

import utils

model_path = utils.get_model_path(sys.argv, "matthews2016")

# fetch Rotations
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016/Global_EB_250-0Ma_GK07_Matthews_etal.rot",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016/Global_EB_410-250Ma_GK07_Matthews_etal.rot",
    ],
    model_path,
    "Rotations",
)

# fetch Topologies
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016/Global_EarthByte_Mesozoic-Cenozoic_plate_boundaries_Matthews_etal.gpmlz",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016/Global_EarthByte_Paleozoic_plate_boundaries_Matthews_etal.gpmlz",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016/TopologyBuildingBlocks_AREPS.gpmlz",
    ],
    model_path,
    "Topologies",
)

# fetch Coastlines
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016/Global_coastlines_2015_v1_low_res.gpmlz",
    ],
    model_path,
    "Coastlines",
)

# fetch StaticPolygons
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016/PresentDay_StaticPlatePolygons_Matthews++.gpmlz"
    ],
    model_path,
    "StaticPolygons",
)
