import bluetooth
import time
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(database="your_database_name", user="user_name", password="******", host="host_name", port="5432")
cur = conn.cursor()

# Raspberry Pi Zero Bluetooth MAC address
pi_bt_address = "xx:xx:xx:xx:xx:xx"

# Establish a Bluetooth connection with the ESP32
esp32_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
esp32_socket.connect((pi_bt_address, 1))  # Replace 1 with the channel number used by your ESP32

# Function to send data to ESP32
def send_data_to_esp32(data):
    esp32_socket.send(data)

# Function to receive data from ESP32
def receive_data_from_esp32():
    return esp32_socket.recv(1024).decode("utf-8")  # Decode the received data as UTF-8

# Main loop
while True:
    # Send request for data every 20 seconds
    send_data_to_esp32("Get data")

    # Receive data from ESP32
    received_data = receive_data_from_esp32()
    print("Received data from ESP32:", received_data)

    # Insert received data into PostgreSQL database
    cur.execute("INSERT INTO your_table_name (column_name) VALUES (%s)", (received_data,))
    conn.commit()

    # Wait for 20 seconds
    time.sleep(20)

# Close the Bluetooth connection and the database connection
esp32_socket.close()
conn.close()
