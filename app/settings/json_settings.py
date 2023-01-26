import json


def load_settings():
    """
        Charge les paramètres à partir d'un fichier json. Si le 
        fichier n'existe pas, il est créé à partir des paramètres par défaut.
    """
    # Vérification de l'existence de "settings.json"
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except Exception:
        # Création de "settings.json" à partir des paramètres par défaut
        with open("settings.json", "w") as f:
            json.dump(write_default_json(), f, indent=4)
        with open("settings.json", "r") as f:
            settings = json.load(f)
    return settings


def write_default_json():
    return json.loads('''{
    "VID": 9494,
    "PID": 123
}''')
