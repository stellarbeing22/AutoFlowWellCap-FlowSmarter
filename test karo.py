from flask import Flask, request
import csv
import io

app = Flask(__name__)


# Route to handle incoming POST requests
@app.route('/receive-data', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        # Get the raw CSV data from the request body
        csv_data = request.data.decode('utf-8')

        print("Received CSV data:")
        print(csv_data)

        try:
            # Parse the CSV data
            csv_file = io.StringIO(csv_data)
            csv_reader = csv.reader(csv_file)

            # Process each row (you can add your logic here)
            for row in csv_reader:
                print(f"Row data: {row}")

            # Optionally, save the data to a CSV file
            with open('received_data.csv', 'a', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerows(csv_reader)  # Write all rows

            # Send a response back to the client (ESP32)
            return "CSV data received and processed successfully", 200
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            return "Failed to parse CSV data", 500
    else:
        return "Invalid request method", 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
