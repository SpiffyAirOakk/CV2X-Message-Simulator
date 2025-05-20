import threading
import time
import socket
import json
import math

class Vehicle(threading.Thread):
    def __init__(self, id, start_lat, start_lon, dest_lat, dest_lon, rsu_host='127.0.0.1', rsu_port=5050):
        super().__init__()
        self.id = id
        self.lat = start_lat
        self.lon = start_lon
        self.dest_lat = dest_lat
        self.dest_lon = dest_lon
        self.speed = 0.0003  # degrees per update step
        self.rsu_host = rsu_host
        self.rsu_port = rsu_port

    def run(self):
        while not self.reached_destination():
            self.move_towards_destination()
            self.send_bsm()
            time.sleep(1)
        print(f"[Vehicle {self.id}] Reached destination.")

    def move_towards_destination(self):
        dx = self.dest_lon - self.lon
        dy = self.dest_lat - self.lat
        dist = math.hypot(dx, dy)
        if dist < self.speed:
            self.lat = self.dest_lat
            self.lon = self.dest_lon
        else:
            self.lat += self.speed * (dy / dist)
            self.lon += self.speed * (dx / dist)

    def reached_destination(self):
        return math.isclose(self.lat, self.dest_lat, abs_tol=1e-4) and \
               math.isclose(self.lon, self.dest_lon, abs_tol=1e-4)

    def send_bsm(self):
        bsm = {
            "type": "BSM",
            "vehicle_id": self.id,
            "latitude": self.lat,
            "longitude": self.lon,
            "timestamp": time.time()
        }
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.rsu_host, self.rsu_port))
                s.sendall(json.dumps(bsm).encode('utf-8'))
            print(f"[Vehicle {self.id}] Sent BSM: {bsm}")
        except Exception as e:
            print(f"[Vehicle {self.id}] Failed to send BSM: {e}")
