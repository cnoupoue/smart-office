import serial

def read_from_lora(port='/dev/ttyUSB0', baudrate=9600):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            while True:
                if ser.in_waiting <= 0:
                    continue
                message = readMessage(ser)
                if message != None:
                    print("Decoded Message: " + message)

    except Exception as e:
        print("Error: " + e)

def readMessage(ser):
    message = ser.readline().decode('utf-8').strip()
    decodedMessage = decodeMessage(message)
    return decodedMessage
    

def decodeMessage(msg):
    # Extract HEX data
    if "Data: (HEX:)" in msg:
        hex_data = msg.split("(HEX:)")[1].strip()
        ascii_data = None
        try:
            ascii_data = bytes.fromhex(hex_data.replace(" ", "")).decode('utf-8')
        except ValueError:
            print("Invalid HEX data: " + hex_data)
        return ascii_data