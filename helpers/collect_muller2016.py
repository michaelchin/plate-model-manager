import os
import sys

import utils

model_path = utils.get_model_path(sys.argv, "muller2016")

# fetch coastlines
utils.fetch_coastlines(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2016/Global_EarthByte_230-0Ma_GK07_AREPS_Coastlines.gpmlz",
    model_path,
    "Global_EarthByte_230-0Ma_GK07_AREPS_Coastlines.gpmlz",
)


# fetch static polygons
utils.fetch_static_polygons(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2016/Global_EarthByte_GPlates_PresentDay_StaticPlatePolygons_2015_v1.gpmlz",
    model_path,
    "Global_EarthByte_GPlates_PresentDay_StaticPlatePolygons_2015_v1.gpmlz",
)


# fetch rotations
utils.fetch_rotations(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2016/Global_EarthByte_230-0Ma_GK07_AREPS.rot",
    model_path,
    "Global_EarthByte_230-0Ma_GK07_AREPS.rot",
)

# fetch topologies
files = []
files.append(
    utils.fetch_file(
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2016/Global_EarthByte_230-0Ma_GK07_AREPS_PlateBoundaries.gpmlz",
        model_path,
    )
)
files.append(
    utils.fetch_file(
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2016/Global_EarthByte_230-0Ma_GK07_AREPS_Topology_BuildingBlocks.gpmlz",
        model_path,
    )
)
utils.zip_files(files, f"{model_path}/Topologies.zip", "Topologies")
for f in files:
    os.remove(f)
