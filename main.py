import socket
import network
import time

def load_html():
    with open("index.html", "r") as f:
        return f.read()
    
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a WiFi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print("Conectado, IP:", wlan.ifconfig())

connect_wifi("FLIA_ACUNA", "03251979")

def run_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # CORREGIDO
    s.bind(addr)
    s.listen(1)
    print('Servidor escuchando en http://%s:%s' % addr)

    while True:
        cl, addr = s.accept()
        print('Cliente conectado desde', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        html = load_html()
        cl.send(b'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html.encode('utf-8'))
        cl.close()

run_server()

