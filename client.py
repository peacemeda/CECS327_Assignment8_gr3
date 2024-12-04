import socket

def send_query(query, HOST, PORT):
    HOST = HOST  # Server ip address
    PORT = PORT  # Server Port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(query.encode())
        response = client.recv(1024).decode()
        print("Response from server:", response)

if __name__ == "__main__":
    HOST = input("Enter the server ip address:") # Server ip address
    PORT = int(input("Enter the server port number:")) # Server Port
    choice = 1
    while choice != 0:
        queries = [
            "What is the average moisture inside my kitchen fridge in the past three hours?",
            "What is the average water consumption per cycle in my smart dishwasher?",
            "Which device consumed more electricity among my three IoT devices?"
        ]
        print("Choose a query:")
        for i, q in enumerate(queries, 1):
            print(f"{i}. {q}")
        choice = int(input("Enter the number of your query: "))
        if 1 <= choice <= 3:
            send_query(queries[choice - 1], HOST, PORT)
        elif choice == 0:
            break
        else:
            print("Invalid query.")
