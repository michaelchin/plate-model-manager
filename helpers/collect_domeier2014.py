import os
import sys

import utils

model_path = utils.get_model_path(sys.argv, "domeier2014")

# fetch Rotations
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_TPW.rot"
    ],
    model_path,
    "Rotations",
)


# fetch Coastlines
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.shp",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.dbf",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.prj",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.shx",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.shp.gplates.xml",
    ],
    model_path,
    "Coastlines",
)

# fetch StaticPolygons
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.shp",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.dbf",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.prj",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.shx",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_land.shp.gplates.xml",
    ],
    model_path,
    "StaticPolygons",
)

# fetch Topologies
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_topos.gpml",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_transform.gpml",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_ridge.gpml",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/DOMEIER2014/LP_subduction.gpml",
    ],
    model_path,
    "Topologies",
)
