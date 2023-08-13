import os
import sys

import utils

model_path = utils.get_model_path(sys.argv, "matthews2016_pmag_ref")

# fetch Rotations
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016_pmag_ref/Matthews_etal_PMAG_PacificCorrected_fixed_crossovers.rot",
    ],
    model_path,
    "Rotations",
)

# fetch Topologies
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016_pmag_ref/Matthews_etal_GPC_2016_MesozoicCenozoic_PlateTopologies_PMAG.gpmlz",
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016_pmag_ref/Matthews_etal_GPC_2016_Paleozoic_PlateTopologies_PMAG.gpmlz",
    ],
    model_path,
    "Topologies",
)

# fetch Coastlines
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016_pmag_ref/Matthews_etal_GPC_2016_Coastlines.gpmlz",
    ],
    model_path,
    "Coastlines",
)

# fetch StaticPolygons
utils.fetch_and_zip_files(
    [
        "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MATTHEWS2016_pmag_ref/Muller_etal_AREPS_2016_StaticPolygons.gpmlz"
    ],
    model_path,
    "StaticPolygons",
)
