######################################################################################
# This sample is to run Sense HAT in IoT Edge Module
# it shows Microsoft Logo while sending SenseHAT data to Azure IoT Hub
# It shows a smileface when sending is completed.

# v0.1
# by tz
######################################################################################

# import necessary modules
from time import sleep
from sense_hat import SenseHat
import asyncio
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message



# Add the device connection string
# Use Azure Global
# CONNECTION_STRING = 'HostName=iothub-0707.azure-devices.net;DeviceId=RPI4-02;SharedAccessKey=UuZ************************qk='

# Use Azure China
CONNECTION_STRING = "HostName=iothub-0713.azure-devices.cn;DeviceId=RPI4-02;SharedAccessKey=pPc*************************RVE="

# Define message format
MSG_TXT = '{{"Temperature":{t}, "Humidity":{h}, "Pressure":{p}}}'

# Send interval - seconds
send_interval = 5

# Send num of messages
num_of_messages = 10

red = (255, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
cyan = (0, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
orange = (255, 215, 0)
nothing = (0, 0, 0)

##############
r = red
g = green
b = blue
o = orange
n = nothing
y = yellow

# Design Microsoft logo
microsoft_logo = [
    r, r, r, r, g, g, g, g,
    r, r, r, r, g, g, g, g,
    r, r, r, r, g, g, g, g,
    r, r, r, r, g, g, g, g,
    b, b, b, b, o, o, o, o,
    b, b, b, b, o, o, o, o,
    b, b, b, b, o, o, o, o,
    b, b, b, b, o, o, o, o
]

s = SenseHat()

# Display a smile face
def draw_smileface():
   s.clear() 
   #--------------------------------
   # Draw eyes
   s.set_pixel(2, 2, blue)
   sleep(0.1)
   s.set_pixel(5, 2, blue)
   sleep(0.1)

   # Draw nose
   s.set_pixel(3, 4, yellow)
   sleep(0.1)
   s.set_pixel(4, 4, yellow)
   sleep(0.1)

   # Draw mouth
   s.set_pixel(1, 5, red)
   sleep(0.1)
   s.set_pixel(2, 6, red)
   sleep(0.1)
   s.set_pixel(3, 7, red)
   sleep(0.1)
   s.set_pixel(4, 7, red)
   sleep(0.1)
   s.set_pixel(5, 6, red)
   sleep(0.1)
   s.set_pixel(6, 5, red)
   sleep(5)
   
   s.clear()
   #---------------------------------

# Initialize senseHAT
def init_SenseHat():
    # clear the display
    s.clear()

    # Display the images on Sensehat
    s.set_pixels(microsoft_logo)
    sleep(1)
    
    # create a module client to interact with Azure IoT Hub
    module_client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)

    return module_client
    
async def sensehat_send_telemetry(client):
    try:
        for i in range(1, num_of_messages + 1):
            temperature = round(s.get_temperature(), 2)
            humidity = round(s.get_humidity(), 2)
            pressure = round(s.get_pressure(),2)

            msg_txt_formatted = MSG_TXT.format(t=temperature, h=humidity, p=pressure)
            message = Message(msg_txt_formatted)

            print(f'Sending message # {num_of_messages}: {message}')
            await client.send_message(message)
            print(f'Message # {num_of_messages} sent successfully')
            sleep(send_interval)

    except KeyboardInterrupt:
        print('IoTHubModuleClient app stopped!')

async def main():

    # init SenseHAT
    module_client = init_SenseHat()
    print('SenseHAT is sending periodic messages, press Ctr-C to exit')


    # Connect the client
    await module_client.connect()
    
    # Send telemetry
    await sensehat_send_telemetry(module_client)

    # disconnect
    await module_client.disconnect()

    # display smileface
    draw_smileface()



if __name__ == '__main__':
    asyncio.run(main())