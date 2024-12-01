import socket
import pymongo
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://ianlee:1q2w3e4r@cluster0.ciur1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["test"]  # Replace with your actual database name
metadata_collection = db["table1_metadata"]
virtual_collection = db["table1_virtual"]

# Helper function to convert UTC to PST
def convert_to_pst(utc_time):
    pst_zone = ZoneInfo("America/Los_Angeles")
    return utc_time.replace(tzinfo=ZoneInfo("UTC")).astimezone(pst_zone)

# Helper function to convert timestamps
def convert_timestamp(epoch):
    return datetime.utcfromtimestamp(int(epoch))

# Process incoming queries
def process_query(query):
    now = convert_to_pst(datetime.utcnow())
    three_hours_ago = now - timedelta(hours=3)

    # Query 1: Average moisture for both fridges in the past 3 hours
    if "average moisture" in query:
        three_hours_ago = datetime.utcnow() - timedelta(hours=3)
        print(f"DEBUG: Fetching data since {three_hours_ago}")

        # Fetch metadata for both fridges
        fridge1_metadata = metadata_collection.find_one({"customAttributes.name": "SmartFridge1"})
        fridge2_metadata = metadata_collection.find_one({"customAttributes.name": "SmartFridge2"})

        if not fridge1_metadata:
            return "The fridges is missing metadata."

        fridge1_uid = fridge1_metadata["assetUid"]

        # Fetch data for each fridge from virtual_collection
        fridge1_data = list(virtual_collection.find({
            "payload.parent_asset_uid": fridge1_uid,
            "time": {"$gte": three_hours_ago}
        }))
        #print(f"DEBUG: Data for SmartFridge1: {fridge1_data}")

    

        # Extract moisture values from payload
        fridge1_moisture = [
            float(entry["payload"].get("Moisture Meter1", 0)) + float(entry["payload"].get("Moisture Meter2", 0))
            for entry in fridge1_data if "payload" in entry
        ]


        # Check if moisture data is available
        if not fridge1_moisture:
            return "No moisture data found for the fridge in the kitchen in the past 3 hours."

        # Calculate average moisture for each fridge
        fridge1_avg = sum(fridge1_moisture) / len(fridge1_moisture) if fridge1_moisture else 0
        # Debugging outputs
        #print(f"DEBUG: Average moisture for SmartFridge1: {fridge1_avg:.2f} RH%")

        # Return the average moisture values
        return (
            f"Average moisture for SmartFridge1(the fridge in the kitchen): {fridge1_avg:.2f} RH%, "
    )

    # Query 2: Average water consumption per cycle for dishwasher
    elif "average water consumption" in query:
        washer_metadata = metadata_collection.find_one({"customAttributes.name": "SmartWasher"})
        if not washer_metadata:
            return "No metadata found for the dishwasher."

        washer_uid = str(washer_metadata.get('assetUid'))
        #print("DEBUG: Uid3: ", washer_uid)
        washer_data = list(virtual_collection.find({
            'payload.parent_asset_uid': washer_uid
        }))
        
        #print(f"DEBUG: Data for SmartWasher: {washer_data[0]}")

        water_values = [float(entry['payload'].get("WaterSensor", 0)) for entry in washer_data if "payload" in entry]

        if not water_values:
            return "No water consumption data found."

        avg_water = sum(water_values) / len(water_values)
        return f"Average water consumption per cycle: {avg_water:.2f} gallons"

    # Query 3: Device with highest electricity consumption
    elif "consumed more electricity" in query:
        # Initialize a dictionary to store electricity consumption for specific devices
        device_consumption = {
            "SmartFridge1": 0,
            "SmartFridge2": 0,
            "SmartWasher": 0
        }

        # Retrieve all relevant data from the virtual collection
        device_data = list(virtual_collection.find())

        # Iterate over all entries in device_data
        for entry in device_data:
            if "payload" in entry:
                # Map Ammeter1 value to SmartFridge1
                device_consumption["SmartFridge1"] += float(entry['payload'].get("Ammeter1", 0))
                
                # Map Ammeter2 value to SmartFridge2
                device_consumption["SmartFridge2"] += float(entry['payload'].get("Ammeter2", 0))
                
                # Map Ammeter3 value to SmartWasher
                device_consumption["SmartWasher"] += float(entry['payload'].get("Ammeter3", 0))

        # If no consumption data is found, return a message
        if all(value == 0 for value in device_consumption.values()):
            return "No electricity consumption data found."

        # Find the device with the highest electricity consumption
        max_device = max(device_consumption, key=device_consumption.get)
        max_consumption = device_consumption[max_device]

        # Prepare a summary for all devices
        device_summary = "\n".join(
            f"{device}: {consumption:.2f} kWh"
            for device, consumption in device_consumption.items()
        )

        # Return detailed results
        return (
            f"The device with the highest electricity consumption is {max_device} with {max_consumption:.2f} kWh.\n\n"
            f"Electricity consumption breakdown:\n{device_summary}"
        )



# Start TCP server
def start_server():
    HOST = input("Enter the server ip address:")  # Server ip address
    PORT = int(input("Enter the server port number:"))     # Arbitrary port number

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print("Server is running...")

        while True:
            conn, addr = server.accept()
            with conn:
                query = conn.recv(1024).decode()
                response = process_query(query)
                conn.sendall(response.encode())

if __name__ == "__main__":
    start_server()
