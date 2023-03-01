import base64
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep
from utils.other_tools.models import Config
from variable import system

_data = GetYamlData(ensure_path_sep(f"\\common\\{system}\\config.yaml")).get_yaml_data()
decrypte_path = ensure_path_sep("\\Files\\keyDoc\\rsa.key")
config = Config(**_data)


def decrypte_info(value) -> str:
    # 解密
    with open(decrypte_path, 'r') as f:
        private_key = f.read()
        rsa_key_obj = RSA.importKey(private_key)
        cipher_obj = PKCS1_v1_5.new(rsa_key_obj)
        random_generator = Random.new().read
        return cipher_obj.decrypt(base64.b64decode(value), random_generator).decode("utf-8")


for db_name, db_info in config.mysql_db.items():
    config.mysql_db[db_name].password = decrypte_info(db_info.password)
config.redis.password = decrypte_info(config.redis.password)
