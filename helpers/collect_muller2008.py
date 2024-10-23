import sys

import utils

model_path = utils.get_model_path(sys.argv, "muller2008")

# fetch Rotations
utils.fetch_and_zip_files(
    [
        "https://earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2008/Global_Model_Rigid_Internal_Release_2010/Global_EarthByte_GPlates_Rotation_20100927.rot"
    ],
    model_path,
    "Rotations",
)


# fetch StaticPolygons
utils.fetch_and_zip_files(
    [
        "https://earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2008/Global_Model_Rigid_Internal_Release_2010/Global_EarthByte_GPlates_PresentDay_StaticPlatePolygons_20100927.gpml"
    ],
    model_path,
    "StaticPolygons",
)
