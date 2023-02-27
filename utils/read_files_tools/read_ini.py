import configparser
import os.path
from common.setting import root_path


def change_pytest_test_path(dir_name: str) -> None:
    root = root_path()
    ini_path = os.path.join(root, "pytest.ini")
    conf = configparser.ConfigParser()
    conf.read(ini_path)
    info = conf.items("pytest")
    for i in info:
        if i[0] == "testpaths":
            test_path_value = i[1]
            break
    else:
        test_path_value = "test_case"
    test_path_value += "/" + dir_name
    conf.set("pytest", "testpaths", test_path_value)
    with open(ini_path, "w+") as f:
        conf.write(f)

