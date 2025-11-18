import configparser
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

AES_KEY = config['Encryption']['AES_KEY']

def get_aes_key():
    return AES_KEY