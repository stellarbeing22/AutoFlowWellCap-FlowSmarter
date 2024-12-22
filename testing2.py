import socket
import time
import csv
from datetime import datetime

HOST = '0.0.0.0'  # Accept connections from any IP address
PORT = 11112  # The port the ESP32 will connect to

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections (max 1 connection at a time)
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}...")

# Open a CSV file to write the data (append mode)
with open('dataa.csv', mode='a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    while True:
        try:
            # Accept a connection from the ESP32
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            # Send and receive data continuously with a delay of 8 seconds
            while True:
                try:
                    # Receive data from the ESP32 with a buffer size of 1024 bytes
                    data = client_socket.recv(1024)
                    if not data:
                        print("Connection lost. Closing connection.")
                        break  # No more data, exit the loop

                    # Decode the received data and print it
                    data_str = data.decode('utf-8', errors='ignore').strip()  # Strip leading/trailing spaces
                    print(f"Received from ESP32: {data_str}")

                    # Check if the received data is empty or just whitespace
                    if not data_str:  # if data is empty or contains only whitespace
                        print("Received data is empty or whitespace. Skipping.")
                        continue  # Skip processing and go to the next iteration

                    # Parse the data (e.g., "0.008,0.005,0.005" -> ['0.008', '0.005', '0.005'])
                    parsed_data = data_str.split(',')
                    print(f"Parsed data: {parsed_data}")  # Print parsed data for debugging

                    # Convert parsed data to float values and write them to CSV
                    if len(parsed_data) == 9:
                        try:
                            # Convert the first four values to float
                            parsed_data_floats = [float(value) for value in parsed_data[:5]]
                            datev = datetime.strptime(parsed_data[5].strip(), "%Y-%m-%d %H:%M:%S")
                            print(datev)
                            parsed_data_floats.append(datev)

                            # Convert the last value to boolean
                            boolean_value = parsed_data[6].strip().lower() == 'true'  # "True" or "False"
                            boolean_value2 = parsed_data[7].strip().lower() == 'true'
                            boolean_value3 = parsed_data[8].strip().lower() == 'true'
                            # Append the boolean value to the float values list
                            parsed_data_floats.append(boolean_value)
                            parsed_data_floats.append(boolean_value2)
                            parsed_data_floats.append(boolean_value3)

                            # Write the data (4 floats + 2 booleans) to the CSV
                            csv_writer.writerow(parsed_data_floats)
                            csv_file.flush()  # Ensure the data is written immediately to disk
                            print(f"Saved to CSV: {parsed_data_floats}")
                        except ValueError as e:
                            print(f"Error parsing data: {e}")
                    else:
                        print(f"Received invalid data format: {parsed_data}")

                    # Send a response back to the ESP32
                    message = "Hello from Python server!"
                    client_socket.sendall(message.encode('utf-8'))
                    print(f"Sent to ESP32: {message}")

                    # Add an 8-second delay before the next cycle
                    time.sleep(8)

                except socket.error as e:
                    print(f"Socket error: {e}")
                    break  # If there's a socket error, break the inner loop

        except socket.error as e:
            print(f"Error accepting connection: {e}")
            continue  # Continue accepting new connections after handling the error

        finally:
            # Clean up the connection
            print("Closing client socket.")
            client_socket.close()
