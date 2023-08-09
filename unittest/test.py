from plate_model_manager import PlateModelManager

pm_manager = PlateModelManager(
    "https://www.earthbyte.org/webdav/ftp/gplately/models.json"
)
model = pm_manager.get_model("Muller2019")
model.download_all(dst_path="plate-models-data-dir")
