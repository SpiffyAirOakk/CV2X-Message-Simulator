from vehicle import Vehicle
from rsu import RSU
from gui.map_view import MapUpdater
import threading
import time

def main():
    print("[Main] Starting CV2X Message Simulator")

    # Create map GUI (must run in main thread)
    map_updater = MapUpdater()

    # Start RSU server in background thread
    rsu = RSU(map_updater=map_updater)
    threading.Thread(target=rsu.start_server, daemon=True).start()

    # Small delay to ensure RSU is listening
    time.sleep(1)

    destinations ={
    "V1": (51.52, -0.10),
    "V2": (51.51, -0.09),
    }

    for vid, (dlat, dlon) in destinations.items():
        map_updater.add_destination_marker(vid, dlat, dlon)

    # Create and start vehicles with start/dest coordinates
    vehicle1 = Vehicle(id="V1", start_lat=51.50, start_lon=-0.12, dest_lat=51.52, dest_lon=-0.10)
    vehicle2 = Vehicle(id="V2", start_lat=51.49, start_lon=-0.14, dest_lat=51.51, dest_lon=-0.09)

    vehicle1.start()
    vehicle2.start()

    # Start GUI main loop (blocks main thread)
    map_updater.run()

if __name__ == "__main__":
    main()
