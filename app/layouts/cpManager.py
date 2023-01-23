import sys
import importlib

import os.path, sys
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)
from settings.json_settings import load_settings

class cpTuning(sys.__class__): 
    settings =  load_settings()
    _cpVID = settings.get('VID', 0x2516)
    _cpPID = settings.get('PID', 0x007B)

    # VID
    @property
    def cpVID(self):        
        return self._cpVID

    @cpVID.setter
    def cpVID(self, value):
        self._cpVID = value

    # PID
    @property
    def cpPID(self):       
        return self._cpPID

    @cpPID.setter
    def cpPID(self, value):
        self._cpPID = value

    def get_cp_keys(self):
        lib_name = f"{str(hex(self._cpVID))[2:]}_{str(hex(self._cpPID,))[2:]}"
        print(lib_name.upper())
        module = importlib.import_module(f'layouts.{lib_name.upper()}')
        return module.KEYS


sys.modules[__name__].__class__ = cpTuning
