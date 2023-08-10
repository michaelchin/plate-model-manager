from plate_model_manager import PlateModelManager

pm_manager = PlateModelManager(
    "https://www.earthbyte.org/webdav/ftp/gplately/models.json"
)
model = pm_manager.get_model("Muller2019")
model.download_all_layers()
model.download_time_dependent_rasters(
    "AgeGrids", [1, 2]
)  # only download 1Ma and 2Ma age grid rasters. too large to download all.

# model.download_all()#too much data to download, be careful
