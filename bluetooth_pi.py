import bluetooth
import time

# Bluetooth-Geräte mit den Namen "ESP1", "ESP2" oder "ESP3" suchen
def search_for_esp_devices():
    esp_devices = []
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    for addr, name in nearby_devices:
        if name.startswith("ESP"):
            esp_devices.append(addr)
    return esp_devices

# Verbindung zu einem Bluetooth-Gerät herstellen
def connect_to_device(device_addr):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    try:
        sock.connect((device_addr, port))
        return sock
    except Exception as e:
        print(f"Fehler beim Verbinden zu {device_addr}: {e}")
        return None

# Hauptfunktion zum Suchen und Verbinden mit ESP-Geräten
def main():
    while True:
        # Nach ESP-Geräten suchen
        esp_devices = search_for_esp_devices()
        if esp_devices:
            print("Gefundene ESP-Geräte:", esp_devices)
            # Mit jedem gefundenen ESP-Gerät verbinden
            for device_addr in esp_devices:
                sock = connect_to_device(device_addr)
                if sock:
                    try:
                        while True:
                            # Daten vom Gerät empfangen
                            received_data = sock.recv(1024)
                            if received_data:
                                print(f"Empfangene Daten von {device_addr}: {received_data}")
                                # Hier kannst du die empfangenen Daten weiterverarbeiten
                    except KeyboardInterrupt:
                        print("Verbindung getrennt.")
                        sock.close()
        else:
            print("Keine ESP-Geräte in der Nähe gefunden.")
        time.sleep(0.015)  # 15 Millisekunden warten

if __name__ == "__main__":
    main()