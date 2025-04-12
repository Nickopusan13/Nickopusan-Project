import json

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    with open("config.json") as f:
        self.config = json.load(f)