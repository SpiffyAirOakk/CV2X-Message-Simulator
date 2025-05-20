import tkinter as tk
from tkintermapview import TkinterMapView
from queue import Queue, Empty

class MapUpdater:
    def __init__(self):
        self.vehicle_markers = {}
        self.queue = Queue()

        self.root = tk.Tk()
        self.root.title("CV2X Vehicle Map")
        self.root.geometry("800x600")
        self.destination_markers = {}

        self.map_widget = TkinterMapView(self.root, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(51.5, -0.1)  # Center on London
        self.map_widget.set_zoom(12)

        # Test marker to verify map loads
        self.map_widget.set_marker(51.5, -0.1, text="Center")

        self.root.after(1000, self.process_queue)

    def update_vehicle_location(self, vehicle_id, lat, lon):
        print(f"[MapUpdater] Queueing update for {vehicle_id}: ({lat}, {lon})")
        self.queue.put((vehicle_id, lat, lon))

    def add_destination_marker(self, vehicle_id, lat, lon):
        if vehicle_id not in self.destination_markers:
            marker = self.map_widget.set_marker(lat, lon, text=f"{vehicle_id} Dest", marker_color_circle="red", marker_color_outside="darkred")
            self.destination_markers[vehicle_id] = marker
            print(f"[MapUpdater] Added destination marker for {vehicle_id} at ({lat}, {lon})")

    def process_queue(self):
        try:
            while True:
                vehicle_id, lat, lon = self.queue.get_nowait()
                print(f"[MapUpdater] Processing {vehicle_id} at ({lat}, {lon})")
                if vehicle_id in self.vehicle_markers:
                    self.vehicle_markers[vehicle_id].set_position(lat, lon)
                else:
                    marker = self.map_widget.set_marker(lat, lon, text=vehicle_id)
                    self.vehicle_markers[vehicle_id] = marker
        except Empty:
            pass
        self.root.after(1000, self.process_queue)

    def run(self):
        self.root.mainloop()
