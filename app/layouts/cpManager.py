import sys
import importlib

import os.path, sys
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)

class cpTuning(sys.__class__): 

    def get_cp_keys(self, cpVID, cpPID):
        lib_name = f"{str(hex(cpVID))[2:]}_{str(hex(cpPID,))[2:]}"
        module = importlib.import_module(f'layouts.{lib_name.upper()}')
        return module.KEYS

    def get_cp_map(self, cpVID, cpPID):
        lib_name = f"{str(hex(cpVID))[2:]}_{str(hex(cpPID,))[2:]}"
        module = importlib.import_module(f'layouts.{lib_name.upper()}')
        return module.MAPPING


sys.modules[__name__].__class__ = cpTuning
