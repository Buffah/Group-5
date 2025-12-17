import tkinter as tk
from abc import ABC, abstractmethod
import math

#Base Station
class BaseStation:
    def __init__(self, bs_id, x, y, capacity):
        self.bs_id = bs_id
        self.location = (x, y)
        self.capacity = capacity
        self.connected_devices = []

    def connect_device(self, device):
        if len(self.connected_devices) >= self.capacity:
            raise Exception("Base Station Overloaded")
        self.connected_devices.append(device)

    def disconnect_device(self, device):
        if device in self.connected_devices:
            self.connected_devices.remove(device)

    def signal_strength(self, device_location):
        dx = self.location[0] - device_location[0]
        dy = self.location[1] - device_location[1]
        distance = math.sqrt(dx**2 + dy**2)
        load_penalty = len(self.connected_devices) * 5
        return max(0, 100 - distance * 2 - load_penalty)

# ---------------- Abstract Device ----------------
class Device(ABC):
    def __init__(self, device_id, x, y):
        self._id = device_id
        self._battery = 100
        self.location = (x, y)
        self.connected_bs = None

    def connect(self, base_station):
        if self._battery <= 5:
            raise Exception("Low battery")
        base_station.connect_device(self)
        self.connected_bs = base_station

    def disconnect(self):
        if self.connected_bs:
            self.connected_bs.disconnect_device(self)
            self.connected_bs = None

    def move(self, x, y, base_stations):
        self.location = (x, y)
        self.auto_handover(base_stations)

    def auto_handover(self, base_stations):
        best_bs = None
        best_signal = -1
        for bs in base_stations:
            signal = bs.signal_strength(self.location)
            if signal > best_signal:
                best_signal = signal
                best_bs = bs
        if best_bs and best_bs != self.connected_bs:
            self.disconnect()
            self.connect(best_bs)

    @abstractmethod
    def send_data(self):
        pass

# ---------------- Device Types ----------------
class SmartPhone(Device):
    def send_data(self):
        self._battery -= 5
        return f"SmartPhone {self._id}: Call/Data session"

class IoTDevice(Device):
    def send_data(self):
        self._battery -= 1
        return f"IoTDevice {self._id}: Sensor update"

class Drone(Device):
    def send_data(self):
        self._battery -= 10
        return f"Drone {self._id}: Video streaming"

# ---------------- GUI Application ----------------
class NetworkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Mobile Network Simulator")

        self.base_stations = [
            BaseStation("BS1", 0, 0, 3),
            BaseStation("BS2", 80, 80, 2)
        ]
        self.devices = {}

        # UI Elements
        tk.Label(root, text="Device ID").grid(row=0, column=0)
        tk.Label(root, text="Type").grid(row=1, column=0)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=0, column=1)

        self.device_type = tk.StringVar(value="SmartPhone")
        tk.OptionMenu(root, self.device_type, "SmartPhone", "IoT", "Drone").grid(row=1, column=1)

        tk.Button(root, text="Register Device", command=self.register_device).grid(row=2, column=0, columnspan=2)
        tk.Button(root, text="Send Data", command=self.send_data).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="Move Device", command=self.move_device).grid(row=4, column=0, columnspan=2)

        self.log = tk.Text(root, height=15, width=50)
        self.log.grid(row=5, column=0, columnspan=2)

    def register_device(self):
        device_id = self.id_entry.get()
        dtype = self.device_type.get()

        if device_id in self.devices:
            self.log.insert(tk.END, "Device already exists\n")
            return

        if dtype == "SmartPhone":
            device = SmartPhone(device_id, 10, 10)
        elif dtype == "IoT":
            device = IoTDevice(device_id, 10, 10)
        else:
            device = Drone(device_id, 10, 10)

        try:
            device.connect(self.base_stations[0])
            self.devices[device_id] = device
            self.log.insert(tk.END, f"{device_id} registered and connected\n")
        except Exception as e:
            self.log.insert(tk.END, str(e) + "\n")

    def send_data(self):
        for device in self.devices.values():
            self.log.insert(tk.END, device.send_data() + "\n")

    def move_device(self):
        for device in self.devices.values():
            device.move(90, 90, self.base_stations)
            self.log.insert(tk.END, f"{device._id} moved → Handover check\n")

# ---------------- Main ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkGUI(root)
    root.mainloop()
