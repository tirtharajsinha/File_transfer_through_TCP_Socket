import os
import random
import socket
import string
from tqdm import tqdm
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456


ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "UTF-8"


def fileSizecalc(size: int):
    units = ["B", "KB", "MB", "GB", "TB"]
    for i in range(5):
        if (size) < 1024:
            return (round(size, 2), units[i])
        size /= 1024


def main(FILENAME):
    """TCP socket and connecting to the server"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"SENDING Connection request to {IP}:{PORT}....")
    client.connect(ADDR)
    client.settimeout(10.0)

    client.send("/DOWNLOAD".encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)

    print(f"SERVER: {msg}")

    """ Sending the requested filename and filesize to the server. """
    data = f"{FILENAME}"
    client.send(data.encode(FORMAT))
    data = client.recv(SIZE).decode(FORMAT)

    if data == "INVALID FILENAME":
        print("SERVER : DENIED! File does not exists")
        client.close()
        return 0
    FILESIZE = int(data.split(":")[1])
    fileReqsizeScaled = fileSizecalc(FILESIZE)
    print(
        f"SERVER: FILESIZE of {FILENAME} is {fileReqsizeScaled[0]}{fileReqsizeScaled[1]}"
    )

    """ Data transfer. """
    bar = tqdm(
        range(FILESIZE),
        f"Sending {FILENAME}",
        unit="B",
        unit_scale=True,
        unit_divisor=SIZE,
    )

    received = 0
    fileid = "".join(random.choices(string.ascii_letters, k=10))
    with open(f"CLIENT_STORAGE/unfinished_{fileid}", "wb") as f:
        while True:
            newData = client.recv(SIZE)
            # filedata += newData
            received += len(newData)
            if not newData:
                break

            f.write(newData)
            client.send("Data received.".encode(FORMAT))
            bar.update(len(newData))

    if received == FILESIZE:
        if os.path.exists(f"CLIENT_STORAGE/{FILENAME}"):
            os.remove(f"CLIENT_STORAGE/{FILENAME}")
        os.rename(f"CLIENT_STORAGE/unfinished_{fileid}", f"CLIENT_STORAGE/{FILENAME}")

    else:
        print("File transmission incomplete")

    """ Closing the connection """
    client.close()


if __name__ == "__main__":
    FILENAME = input("ENTER FILENAME YOU WANT TO SEND : ")

    main(FILENAME)
