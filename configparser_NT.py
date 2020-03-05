import configparser as cp
import os
import sys


ressources = os.path.dirname(sys.argv[0])
def conf(ini_file):
    config = cp.ConfigParser()
    try:
        config.read(os.path.join(ressources, ini_file ),encoding="utf-8")
    except Exception as e :
        print(str(e))

    return config