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
    
    @on(Action.StatusNotification)
    def on_status_notification ( self, **kwargs ) :
        return call_result.StatusNotificationPayload(

        )
    
     @on(Action.StartTransaction)
    def on_start_transaction ( self, **kwargs ) :
        return call_result.StartTransactionPayload(
            dict([('status', "Accepted"), ('expiryDate', "2023-09-17T10:44:33.638259"),
                  ('parentIdTag', "Rajansimulator")]),
            transaction_id=1
        )
    @on(Action.DiagnosticStatusNotification)
    def on_send_diagnos ( self, **kwargs ) :
        return call_result.DiagnosticStatusNotificationPayload(

        )
    
    
    @on(Action.FirmwareStatusNotification)
    def on_send_firmware_status ( self, **kwargs ) :
        return call_result.FirmwareStatusNotificationPayload(

        )
    #function  update need
    
    @on(Action.MeterValues)
    def on_send_meter_value(self,**kwargs):
        return call_result.MeterValuesPayload(

        )
    @on(Action.DataTransfer)
    def on_send_data_transfer ( self, **kwargs ) :
        return call_result.DataTransferPayload(
            status=DataTransferStatus.accepted,
            data="Charger request data"

        )
    #function for charger data transmited
    
    @on(Action.StopTransaction)
    def on_send_stop_transaction ( self, **kwargs ) :
        return call_result.StopTransactionPayload(
            id_tag_info=dict([('status', "Accepted"), ('expiryDate', "2023-09-17T10:44:33.638259"),
                              ('parentIdTag', "Rajansimulator")])
        )
#stop transaction added

    async def send_update_firmware ( self ) :
        request = call.UpdateFirmwarePayload(
            location="127.0.0.1:8001",
            retrieve_date=datetime.utcnow( ).isoformat( ),
            retries=3,
            retry_interval=45
        )
        
# firmware update request
    async def send_unlock ( self ) :
        request = call.UnlockConnectorPayload(
            connector_id=1
        )
        print("unlock connector send")
        print(request)
        response = await self.call(request)
        print(response)
        print("Unlock connector response received")
    
    
    
    
    
    
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
