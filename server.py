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


class ChargePoint(cp) :
    @on(Action.BootNotification)
    def on_boot_notification ( self, charge_point_vendor, charge_point_model, **kwargs ) :
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow( ).isoformat( ),
            interval=10,
            status=RegistrationStatus.accepted
        )
    
    
    @on(Action.Authorize)
    def on_authorize ( self, **kwargs ) :
        return call_result.AuthorizePayload(
            dict([('status', "Accepted"), ('expiryDate', "2023-09-17T10:44:33.638259"),
                  ('parentIdTag', "Rajanbabu_simulator")])   ## Parent id taqge belongs to charger
        )


    
    @on(Action.Heartbeat)
    def on_heartbeat ( self, **kwargs ) :
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow( ).isoformat( )
        )
    
    
    
async def on_connect ( websocket, path ) :
    """ For every new charge point that connects, create a ChargePoint instance
   and start listening for messages.

   """
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    print("Client Connected")
    
    
    

    await asyncio.gather(cp.start(),cp.send_trigger_message())
    
  sync def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        5603,
        subprotocols=['ocpp1.6']
    )
    await server.wait_closed( )


if __name__ == '__main__' :
    try :
        # asyncio.run() is used when running this example with Python 3.7 and
        # higher.
        asyncio.run(main( ))
    except AttributeError :
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop( )
        loop.run_until_complete(main( ))
        loop.close( )
