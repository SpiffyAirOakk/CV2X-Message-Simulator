# 🚗 CV2X Message Simulator

A simple and interactive simulation of **Cellular Vehicle-to-Everything (CV2X)** communication, visualizing vehicles broadcasting Basic Safety Messages (BSMs) to a Roadside Unit (RSU) and tracking their real-time movement on a map using a Tkinter-based GUI.

---

## 🗂 Project Structure

```
cv2x_message_simulator/
│
├── main.py               # Entry point: starts GUI, RSU, and vehicle threads
├── rsu.py                # RSU server to receive BSMs and update the map
├── vehicle.py            # Simulated vehicle class with destination-based movement
├── gui/
│   └── map_view.py       # Tkinter GUI with an interactive map showing vehicle positions
```

---

## ✨ Features

- Simulates multiple vehicles broadcasting BSM messages over TCP.
- Real-time vehicle location updates on a Tkinter map.
- Static destination markers displayed for each vehicle.
- Modular design: RSU, vehicle logic, and GUI are cleanly separated.
- Threaded architecture for responsive GUI and parallel vehicle behavior.

---

## 🧠 How it Works

1. **`main.py`**
   - Initializes the GUI (`MapUpdater`)
   - Starts the RSU server on a background thread
   - Creates and starts vehicle threads
   - Marks destinations on the map
   - Launches the main event loop for the GUI

2. **`vehicle.py`**
   - Each vehicle runs in its own thread
   - Moves gradually toward a target destination
   - Sends periodic BSMs (latitude, longitude, timestamp) to the RSU via TCP

3. **`rsu.py`**
   - TCP server that listens for incoming BSMs
   - Parses JSON messages
   - Updates vehicle positions on the map via `MapUpdater`

4. **`gui/map_view.py`**
   - A simple but powerful GUI using [`tkintermapview`](https://github.com/TomSchimansky/TkinterMapView)
   - Maintains a live map with vehicle markers and destination indicators
   - Updates markers based on messages received from the RSU

---

## 🧪 Requirements

- Python 3.7+
- [`tkintermapview`](https://github.com/TomSchimansky/TkinterMapView)

Install via:

```bash
pip install tkintermapview
```

---

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/yourusername/cv2x_message_simulator.git
cd cv2x_message_simulator
```

2. Install dependencies:

```bash
pip install tkintermapview
```

3. Run the simulator:

```bash
python main.py
```


---

## 🔧 Customization

You can easily modify:

- **Vehicle paths** in `main.py`
- **Number of vehicles** by creating more instances of `Vehicle`
- **Speed of simulation** via the `self.speed` parameter in `vehicle.py`
- **Map center or zoom** via `self.map_widget.set_position()` and `set_zoom()` in `map_view.py`

---

## 📦 Future Improvements

- Realistic GPS jitter / noise
- Dynamic vehicle-to-vehicle (V2V) messaging
- Performance testing with 100+ vehicles
- Log saving and replay
- Web-based GUI with live sockets

---

## 👨‍💻 Author

Abdullah Khalid  
Machine Learning Engineer | CV2X & Smart Mobility Enthusiast

---

## 📝 License

This project is licensed under the MIT License. See `LICENSE` file for details.
