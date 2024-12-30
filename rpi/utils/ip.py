import socket

def read():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Try to connect to an external address to get the local IP
    try:
        s.connect(("8.8.8.8", 80))  # Google's DNS address (this is used to determine local network IP)
        ip = s.getsockname()[0]  # Get the local IP address
    except Exception as e:
        print(f"Error getting IP address: {e}")
        ip = None
    finally:
        s.close()  # Close the socket connection
    
    return ip