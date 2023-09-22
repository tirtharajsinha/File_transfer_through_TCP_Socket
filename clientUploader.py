import os
import socket
from tqdm import tqdm
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "UTF-8"


def main(FILENAME, FILESIZE, FILEPATH):
    """TCP socket and connecting to the server"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"SENDING Connection request to {IP}:{PORT}....")
    client.connect(ADDR)

    client.send("/UPLOAD".encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)

    print(f"SERVER: {msg}")

    """ Sending the filename and filesize to the server. """
    data = f"{FILESIZE}_{FILENAME}"
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"SERVER: {msg}")

    """ Data transfer. """
    bar = tqdm(
        range(FILESIZE),
        f"Sending {FILENAME}",
        unit="B",
        unit_scale=True,
        unit_divisor=SIZE,
    )

    with open(FILEPATH, "rb") as f:
        while True:
            data = f.read(SIZE)

            if not data:
                break

            client.send(data)

            msg = client.recv(SIZE).decode(FORMAT)

            bar.update(len(data))
            # time.sleep(0.01)

    """ Closing the connection """
    client.close()


if __name__ == "__main__":
    filename = input("ENTER FILENAME YOU WANT TO SEND : ")
    if os.path.exists(filename):
        FILEPATH = filename
        FILESIZE = os.path.getsize(FILEPATH)
    elif os.path.exists(os.path.join("CLIENT_STORAGE", filename)):
        FILEPATH = os.path.join("CLIENT_STORAGE", filename)
        FILESIZE = os.path.getsize(FILEPATH)
    else:
        print("!!! File Does Not exists.")
        exit()

    FILENAME = os.path.basename(FILEPATH)

    main(FILENAME, FILESIZE, FILEPATH)
