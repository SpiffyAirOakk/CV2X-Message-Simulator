import tkinter as tk
from tkinter import scrolledtext
import threading
import socket
import json
from datetime import datetime

class Dashboard(tk.Tk):
    def __init__(self, host='127.0.0.1', port=6060):
        super().__init__()
        self.title("CV2X Simulator Dashboard")
        self.geometry("700x400")
        self.configure(bg="#f0f0f0")
        
        tk.Label(self, text="CV2X Message Feed", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

        self.log_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20, font=("Courier", 10))
        self.log_area.pack(padx=10, pady=10)
        self.log_area.config(state='disabled')

        self.message_count = 0
        self.host = host
        self.port = port

        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def log_message(self, message):
        self.message_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] #{self.message_count} - {json.dumps(message, indent=2)}\n"

        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, formatted)
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def listen_for_messages(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"[Dashboard] Listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(2048)
                    if data:
                        try:
                            message = json.loads(data.decode())
                            self.log_message(message)
                        except Exception as e:
                            print(f"[Dashboard] Error: {e}")

if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.mainloop()
