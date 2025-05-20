import socket
import threading
import json

class RSU:
    def __init__(self, host='127.0.0.1', port=5050, map_updater=None):
        self.host = host
        self.port = port
        self.map_updater = map_updater
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"[RSU] Listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server.accept()
            print(f"[RSU] Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        with client_socket:
            data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                data += chunk
            try:
                msg = json.loads(data.decode('utf-8'))
                print(f"[RSU] Received message: {msg}")
                if msg.get("type") == "BSM":
                    vehicle_id = msg.get("vehicle_id")
                    lat = msg.get("latitude")
                    lon = msg.get("longitude")
                    if self.map_updater:
                        print(f"[RSU] Updating map for vehicle {vehicle_id} at ({lat}, {lon})")
                        self.map_updater.update_vehicle_location(vehicle_id, lat, lon)
            except Exception as e:
                print(f"[RSU] Failed to process message: {e}")
