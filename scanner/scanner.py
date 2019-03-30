import subprocess
import bluetooth
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

SECONDS_BETWEEN_BT_SCANS = config.getint("DEFAULT", "SECONDS_BETWEEN_BT_SCANS")


class Scanner:
    def count_bt_devices(self):
        """Scans for nearby Bluetooth devices"""
        bt_devices_count = len(bluetooth.discover_devices(
            duration=SECONDS_BETWEEN_BT_SCANS))
        return bt_devices_count

    def find_wifi_devices(self):
        """Scans for nearby WiFi devices"""
        # TODO: Implement this
        return None

    def start_bt(self):
        """Starts the Bluetooth device"""
        try:
            subprocess.check_output(['./scripts/start_bt.sh'])
        except subprocess.CalledProcessError:
            print("Error: Couldn't start the Bluetooth device")