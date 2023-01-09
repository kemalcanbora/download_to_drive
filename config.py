import yaml

def read_config():
    with open('config.yaml', 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
