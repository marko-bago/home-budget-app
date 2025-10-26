import json

def json_output(logger, data, desc=""):
    logger.info(f"{desc}\n{json.dumps(data.json(), indent=4, sort_keys=True)}")
