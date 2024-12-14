# **End-to-End IoT System with TCP Client-Server and Database Integration**

## **Overview**

This project implements a comprehensive end-to-end IoT system that integrates:

-   A **TCP client-server** for user query processing and response.
-   A **MongoDB database** for IoT device data and metadata storage.
-   Virtual IoT sensor data sourced from **Dataniz** for real-time processing and analysis.

The system supports three key user queries:

1.  What is the average moisture inside my kitchen fridge in the past three hours?
2.  What is the average water consumption per cycle in my smart dishwasher?
3.  Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?

The project highlights the integration of IoT sensors, metadata utilization, real-world unit conversions, and robust query handling.

----------

## **System Architecture**

The system consists of the following components:

1.  **TCP Client**:
    
    -   Accepts user queries via a command-line interface.
    -   Sends valid queries to the TCP server for processing.
    -   Receives and displays responses from the server.
2.  **TCP Server**:
    
    -   Processes incoming queries by fetching relevant data from the MongoDB database.
    -   Utilizes metadata from **Dataniz** to enhance query processing and data organization.
    -   Performs unit conversions (e.g., moisture to RH%, water to gallons, electricity to kWh) and calculations.
    -   Returns results to the client.
3.  **Database (MongoDB)**:
    
    -   Stores IoT device metadata (e.g., device IDs, attributes, and configurations).
    -   Stores real-time and historical IoT sensor data.
4.  **IoT Devices (Virtual)**:
    
    -   Includes two smart refrigerators and a smart dishwasher.
    -   Generates data for moisture levels, water consumption, and electricity usage.

----------

## **Features**

-   **Dynamic Query Handling**:
    
    -   Supports three predefined queries.
    -   Rejects invalid queries with a user-friendly message and displays valid options.
-   **Real-Time Data Processing**:
    
    -   Retrieves and analyzes IoT sensor data in real-time.
-   **Metadata Integration**:
    
    -   Leverages metadata from Dataniz for device-specific data processing and context-aware queries.
-   **Unit Conversions**:
    
    -   Converts moisture readings to RH%.
    -   Displays results in PST and imperial units (gallons, kWh).

----------

## **Usage Instructions**

### **1. Setting Up the Environment**

1.  **Install Required Libraries**: Run the following command to install Python dependencies:
    
    
    `pip install socket pymongo matplotlib zoneinfo` 
    
2.  **Set Up the Database**:
    
    -   Use MongoDB Atlas or a local MongoDB instance.
    -   Import the metadata and virtual IoT device data into the respective collections.
3.  **Start the TCP Server**:
    
    -   Run the server script:
        
        
        `python server.py` 
        
4.  **Run the TCP Client**:
    
    -   Execute the client script:
        
        
        `python client.py` 
        

----------

### **2. Client Usage**

-   Upon running the client, you will be prompted to:
    -   Enter the server's IP address and port number.
    -   Choose a query from the following options:
        1.  Average moisture in the kitchen fridge (past 3 hours).
        2.  Average water consumption per cycle (smart dishwasher).
        3.  Device with the highest electricity consumption.
-   Enter the query number, and the system will display the response.

----------

### **3. Server Functionality**
-   Upon running the server, you will also be prompted to:
    -   Enter the server's IP address and port number.
The server performs the following:

-   **Query 1**: Calculates the average relative humidity (RH%) inside the kitchen fridge over the past 3 hours.
-   **Query 2**: Determines the average water consumption per cycle for the smart dishwasher.
-   **Query 3**: Identifies the IoT device with the highest electricity consumption and provides a breakdown for all devices.

----------

## **Example Usage**

### **Client Interaction**:


`Enter the server ip address: 127.0.0.1
Enter the server port number: 65432
Choose a query:
1. What is the average moisture inside my kitchen fridge in the past three hours?
2. What is the average water consumption per cycle in my smart dishwasher?
3. Which device consumed more electricity among my three IoT devices?
Enter the number of your query: 1
Response from server: Average moisture for SmartFridge1 (kitchen fridge): 65.23 RH%` 

### **Server Debug Output**:


`Server is running...
DEBUG: Fetching data since 2024-11-30 12:00:00
DEBUG: Average moisture for SmartFridge1: 65.23 RH%` 

----------

## **Project Components**

### **1. TCP Client**

-   Handles user input and sends queries to the server.
-   Validates query input and rejects invalid queries with a helpful message.

### **2. TCP Server**

-   Processes valid queries by retrieving data from the MongoDB database.
-   Utilizes metadata for device-specific query handling and unit conversions.

### **3. MongoDB Database**

-   Stores IoT device metadata and virtual sensor data.
-   Provides a reliable backend for query processing.

### **4. IoT Devices**

-   Virtual devices created on Dataniz generate realistic sensor data for:
    -   **SmartFridge1** and **SmartFridge2**: Moisture and electricity consumption.
    -   **SmartWasher**: Water consumption and electricity usage.

----------

## **Challenges and Solutions**

-   **Challenge**: Integrating metadata for device-specific processing.
    -   **Solution**: Used Dataniz metadata to fetch unique device IDs and interpret sensor data.
-   **Challenge**: Converting sensor data into meaningful units.
    -   **Solution**: Implemented unit conversions (e.g., RH%, gallons, kWh) in server logic.

----------

## **Future Improvements**

1.  Expand the system to support additional IoT devices and queries.
2.  Incorporate real-time data streaming for continuous monitoring.
3.  Implement a user-friendly graphical interface for client interaction.
4.  Use advanced query optimization techniques for large datasets.

