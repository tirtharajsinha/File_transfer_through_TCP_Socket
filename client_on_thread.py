import os
import socket
from tqdm import tqdm
import threading

SIZE = 1024
FORMAT = "UTF-8"


IP = socket.gethostbyname(socket.gethostname())
PORT = 4456


ADDR = (IP, PORT)


def TCPclient(ADDR, FILEPATH):
    FILESIZE = os.path.getsize(FILEPATH)
    FILENAME = os.path.basename(FILEPATH)

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

    """ Closing the connection """
    client.close()


if __name__ == "__main__":
    client1 = threading.Thread(target=TCPclient, args=(ADDR, "CLIENT_STORAGE/test.txt"))
    client2 = threading.Thread(target=TCPclient, args=(ADDR, "CLIENT_STORAGE/test.pdf"))
    client3 = threading.Thread(
        target=TCPclient, args=(ADDR, "CLIENT_STORAGE/broute_force.c")
    )

    client1.start()
    client2.start()
    client3.start()

    client1.join()
    client2.join()
    client3.join()
