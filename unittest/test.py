from plate_model_manager import PlateModelManager

pm_manager = PlateModelManager()
model = pm_manager.get_model("Muller2019")
model.set_data_dir("plate-models-data-dir")
print(model.get_rotation_model())
