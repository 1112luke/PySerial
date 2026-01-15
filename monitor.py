import serial
import time
from threading import Thread
from rich import print
from rich.console import Console
from pynput.keyboard import Listener, Key
from xplink import *
from fastapi import FastAPI, WebSocket
import uvicorn
import json, random, asyncio


#make console
console = Console()

ser = serial.Serial('/dev/tty.usbserial-110', 1000000)  # open serial port

recievedBytes = 0
start_time = 0
end_time = 0
xp = XPLink()

alphadata = {
    "temps": [None] * 4,
    "pressures": [None] * 12,
    "going": 0
}

def recieve():
    
    while(1):
        
        bytes = ser.read()
        packet = xp.XPLINK_UNPACK(bytes[0])
        if(packet):
            #print([hex(pac) for pac in packet.data])
            match xp_msg_t(packet.type).name:
                case "TEMP1":
                    celcius = packet.data[3]<<24 | packet.data[2]<<16 | packet.data[1]<<8 | packet.data[0]
                    print("TEMP1: ", celcius*1e-4*(9/5)+32)
                    alphadata["temps"][0] = celcius*1e-4*(9/5)+32
                case "TEMP2":
                    celcius = packet.data[3]<<24 | packet.data[2]<<16 | packet.data[1]<<8 | packet.data[0]
                    print("TEMP2: ", celcius*1e-4*(9/5)+32)
                    alphadata["temps"][1] = celcius*1e-4*(9/5)+32
                case "TEMP3":
                    celcius = packet.data[3]<<24 | packet.data[2]<<16 | packet.data[1]<<8 | packet.data[0]
                    print("TEMP3: ", celcius*1e-4*(9/5)+32)
                    alphadata["temps"][2] = celcius*1e-4*(9/5)+32
                case "TEMP4":
                    celcius = packet.data[3]<<24 | packet.data[2]<<16 | packet.data[1]<<8 | packet.data[0]
                    print("TEMP4: ", celcius*1e-4*(9/5)+32)
                    alphadata["temps"][3] = celcius*1e-4*(9/5)+32
                case "PRESSURE1":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure1: ", data, end='')
                    alphadata["pressures"][0] = data
                case "PRESSURE2":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure2: ", data, end='')
                    alphadata["pressures"][1] = data
                case "PRESSURE3":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure3: ", data, end='')
                    alphadata["pressures"][2] = data
                case "PRESSURE4":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure4: ", data, end='')
                    alphadata["pressures"][3] = data
                case "PRESSURE5":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure5: ", data, end='')
                    alphadata["pressures"][4] = data
                case "PRESSURE6":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure6: ", data, end='')
                    alphadata["pressures"][5] = data
                case "PRESSURE7":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure7: ", data, end='')
                    alphadata["pressures"][6] = data
                case "PRESSURE8":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure8: ", data, end='')
                    alphadata["pressures"][7] = data
                case "PRESSURE9":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure9: ", data, end='')
                    alphadata["pressures"][8] = data
                case "PRESSURE10":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure10: ", data, end='')
                    alphadata["pressures"][9] = data
                case "PRESSURE11":
                    #print([hex(pac) for pac in pa
                    # cket.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure11: ", data, end='')
                    alphadata["pressures"][10] = data
                case "PRESSURE12":
                    #print([hex(pac) for pac in packet.data])
                    data = packet.data[1]<<8 | packet.data[0]
                    print("Pressure12: ", data)
                    alphadata["pressures"][11] = data
                    


            #print("type:", xp_msg_t(packet.type).name)
            #print("sender:", packet.sender_id)
            




    ''' TIMER
    global recievedBytes
    global start_time
    global end_time
    while(1):
        line = ser.read()
        recievedBytes += 1
        #console.print(line.hex())
        if(line.hex() == "00"):
            #console.print("START")
            start_time = time.time()
        if(line.hex() == "ff"):
            #console.print("END")
            end_time = time.time()
            console.print("\rTime: ", end_time - start_time, "seconds")
            console.print("\rRate: ", recievedBytes/(end_time-start_time))
            console.print("\rBytes Recieved: ", recievedBytes)
            recievedBytes = 0
    '''


def inthread():

    def on_press(key):
        #print('{0} pressed'.format(key))
        if(key.char == 'f'):
            #send message
            pkt = xp_packet_t()
            pkt.END_BYTE = 0x00
            pkt.sender_id = 0xAA
            pkt.type = 1
            pkt.data = 10
            
            #send packet
            outpacket = xp.XPLINK_PACK(pkt)
        
            #serial transmit
            ser.write(bytes(outpacket))
            print("Transmitted\n")
        if(key.char == 'o'):
            #send message
            pkt = xp_packet_t()
            pkt.END_BYTE = 0x00
            pkt.sender_id = 0xAA
            pkt.type = 1
            pkt.data = 333
            
            #send packet
            outpacket = xp.XPLINK_PACK(pkt)
        
            #serial transmit
            ser.write(bytes(outpacket))
            print("Transmitted\n")

    def on_release(key):
        #print('{0} release'.format(key))
        if key == Key.esc:
            # Stop listener
            return False

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


app = FastAPI()

@app.websocket("/data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Make a copy to avoid thread race
        data = alphadata.copy()
        data["temps"] = alphadata["temps"][:]
        data["pressures"] = alphadata["pressures"][:]

        data["timestamp"] = time.time()
        
        await websocket.send_text(json.dumps(data))
        #stream at 250 hz
        await asyncio.sleep(1/250)




def timer():
    global recievedBytes
    last_time = time.time()
    while(1):
        if(time.time() > last_time + 1):
            console.print("Time: ", time.time())
            console.print("Recieved Bytes: ", recievedBytes)
            last_time = time.time()


if __name__ == "__main__":
    # Create main asyncio loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Start Uvicorn server as a coroutine
    async def start_server():
        # FIX: Pass the actual 'app' object, removing the string reference
        config = uvicorn.Config(app, host="127.0.0.1", port=3333, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

    # Schedule the server
    loop.create_task(start_server())

    # Start threads as daemon
    t1 = Thread(target=recieve, daemon=True)
    t3 = Thread(target=inthread, daemon=True)

    t1.start()
    t3.start()

    print("System Started. Press CTRL+C to stop.")

    # Run the asyncio loop forever
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        # Cleanup
        if ser.is_open:
            ser.close()
        loop.close()
