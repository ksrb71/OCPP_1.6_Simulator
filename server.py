import asyncio
from datetime import datetime
from typing import Dict
from ocpp.v16 import call

try :
    import websockets
except ModuleNotFoundError :
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print( )
    print(" $ pip install websockets")
    import sys

    sys.exit(1)

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import *
from ocpp.v16 import call_result, call
