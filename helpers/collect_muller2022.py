import sys

import utils


model_path = utils.get_model_path(sys.argv, "muller2022")

# fetch coastlines
utils.fetch_coastlines(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2022/shapes_coastlines_Merdith_et_al_v2.gpmlz",
    model_path,
    "shapes_coastlines_Merdith_et_al_v2.gpmlz",
)


# fetch static polygons
utils.fetch_static_polygons(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2022/shapes_static_polygons_Merdith_et_al.gpmlz",
    model_path,
    "shapes_static_polygons_Merdith_et_al.gpmlz",
)


# fetch rotations
utils.fetch_rotations(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2022/1000_0_rotfile_Merdith_et_al_optimised.rot",
    model_path,
    "1000_0_rotfile_Merdith_et_al_optimised.rot",
)
