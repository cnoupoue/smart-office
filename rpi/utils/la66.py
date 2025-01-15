import serial

def read(ser):
    message = ser.readline().decode('utf-8').strip()
    decodedMessage = _decodeMessage(message)
    return decodedMessage
    
def _decodeMessage(msg):
    # Extract HEX data
    if "Data: (HEX:)" in msg:
        hex_data = msg.split("(HEX:)")[1].strip()
        ascii_data = None
        try:
            ascii_data = bytes.fromhex(hex_data.replace(" ", "")).decode('utf-8')
            print("RFID received: " + str(ascii_data))
        except ValueError:
            print("Invalid HEX data: " + hex_data)
        return ascii_data