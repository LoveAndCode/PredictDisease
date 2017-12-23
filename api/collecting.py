from api import apis
import json

with open('../config/config.json') as config_file:
    info = json.load(config_file)

api = apis.MedicineAPI(info["medicine_api"]["api_key"], True)
api.debug_toggle()
api.parse("R05CA", "110000", "110001", "201703")
