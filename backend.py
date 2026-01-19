import serial
import json
import time
import os

# INSTELLINGEN
POORT = '/dev/cu.usbserial-0001'
BAUD = 115200
BESTANDSNAAM = 'sensor_data.json'

print(f"Start backend verbinding op {POORT}...")

try:
    # Open de verbinding
    ser = serial.Serial(POORT, BAUD, timeout=1)
    print("Verbonden. Data wordt weggeschreven naar JSON bestand.")

    while True:
        try:
            if ser.in_waiting > 0:
                # Lees regel van Arduino
                raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Controleer of het JSON formaat lijkt te kloppen
                if raw_line.startswith('{') and raw_line.endswith('}'):
                    try:
                        data = json.loads(raw_line)
                        
                        # Schrijf data naar bestand
                        with open(BESTANDSNAAM, 'w') as f:
                            json.dump(data, f)
                            f.flush()
                            os.fsync(f.fileno())
                        
                        # Feedback in terminal om activiteit te tonen
                        print(f"Data ontvangen: {data}")
                        
                    except json.JSONDecodeError:
                        pass # Negeren van incomplete data
                        
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Fout tijdens lezen: {e}")
            time.sleep(1)

except KeyboardInterrupt:
    print("\nBackend gestopt.")
    ser.close()
except serial.SerialException as e:
    print(f"Kon poort niet openen: {e}")
