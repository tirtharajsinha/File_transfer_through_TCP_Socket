import socket
from tqdm import tqdm
import threading
import sys
import time
import string
import random
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "UTF-8"

ConnectionCount = 0


def handleServerinterruption(server):
    print("Server is ready. Close the server with CTRL+C")
    while True:
        try:
            input()
        except Exception as e:
            server.close()
            break


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverManagerThread = threading.Thread(target=handleServerinterruption, args=(server,))


def handleClient(conn, addr):
    try:
        print(
            f"[+] Client connected from {addr[0]}:{addr[1]} on THREAD:{threading.current_thread().name}"
        )
        conn.settimeout(10.0)
        PATH = conn.recv(SIZE).decode(FORMAT)

        if PATH == "/UPLOAD":
            print("Processing the upload request..")
            conn.send("[o]Processing the upload request".encode(FORMAT))
            fileid = "".join(random.choices(string.ascii_letters, k=10))
            handleClientUpload(conn, addr, fileid)

        if PATH == "/DOWNLOAD":
            print("[o] Processing the download request..")
            conn.send("Processing the download request".encode(FORMAT))
            handleClientDownload(conn, addr)
    except TimeoutError as e:
        conn.close()
        print(f"[-] TimeOut : Client {addr[0]}:{addr[1]} disconnected")
        if PATH == "/UPLOAD":
            if os.path.exists(f"SERVER_STORAGE/unfinished_{fileid}"):
                os.remove(f"SERVER_STORAGE/unfinished_{fileid}")
    except ConnectionResetError as e:
        print(f"[-]  Forcefully disconnected Client {addr[0]}:{addr[1]}")
        if PATH == "/UPLOAD":
            if os.path.exists(f"SERVER_STORAGE/unfinished_{fileid}"):
                os.remove(f"SERVER_STORAGE/unfinished_{fileid}")


def handleClientUpload(conn, addr, fileid):
    """Receiving the filename and filesize from the client."""
    data = conn.recv(SIZE).decode(FORMAT)
    item = data.split("_", 1)
    FILENAME = item[1]
    FILESIZE = int(item[0])

    print(f"[o] Filename and filesize received from the client:{addr[0]}:{addr[1]}")
    conn.send("Filename and filesize received".encode(FORMAT))
    # conn.settimeout(None)

    received = 0
    with open(f"SERVER_STORAGE/unfinished_{fileid}", "wb") as f:
        st = time.time()

        while True:
            newData = conn.recv(SIZE)
            # filedata += newData
            received += len(newData)
            if not newData:
                break

            f.write(newData)
            conn.send("Data received.".encode(FORMAT))

        et = time.time()
        elapsed_time = et - st

    if received == FILESIZE:
        if os.path.exists(f"SERVER_STORAGE/{FILENAME}"):
            os.remove(f"SERVER_STORAGE/{FILENAME}")
        os.rename(f"SERVER_STORAGE/unfinished_{fileid}", f"SERVER_STORAGE/{FILENAME}")
        transferSpeed, transferSpeedUnit = fileSizecalc(FILESIZE / elapsed_time)
        filesizeScaled, filesizeScaledUnit = fileSizecalc(FILESIZE)
        print(
            f"[o] {FILENAME} of size [{filesizeScaled}{filesizeScaledUnit}] received from {addr[0]}:{addr[1]} on [{transferSpeed}{transferSpeedUnit}/S]"
        )
    else:
        print("File transmission incomplete")
        os.remove(f"SERVER_STORAGE/unfinished_{fileid}")
    """ Closing connection. """
    print(f"[-] Client {addr[0]}:{addr[1]} disconnected")
    conn.close()


def handleClientDownload(conn, addr):
    """Receiving the filename and filesize from the client."""
    FILENAME = conn.recv(SIZE).decode(FORMAT)
    FILEPATH = os.path.join("SERVER_STORAGE", FILENAME)
    FILESIZE = 0
    if os.path.exists(os.path.join("SERVER_STORAGE", FILENAME)):
        FILESIZE = os.path.getsize(os.path.join("SERVER_STORAGE", FILENAME))
        print(f"[o] Requested File from the client {addr[0]}:{addr[1]} is valid")
        conn.send(f"filesize:{FILESIZE}".encode(FORMAT))
    else:
        print(f"[o] Requested File from the client {addr[0]}:{addr[1]} does not exist")
        conn.send(f"INVALID FILENAME".encode(FORMAT))
        print(f"[-] Client {addr[0]}:{addr[1]} disconnected")
        time.sleep(1)
        conn.close()
        return 0
    # conn.settimeout(None)

    with open(FILEPATH, "rb") as f:
        while True:
            data = f.read(SIZE)

            if not data:
                break

            conn.send(data)

            msg = conn.recv(SIZE).decode(FORMAT)

            # time.sleep(0.01)

    """ Closing connection. """
    print(f"[-] Client {addr[0]}:{addr[1]} disconnected")
    conn.close()


def fileSizecalc(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    for i in range(5):
        if (size) < 1024:
            return (round(size, 2), units[i])
        size /= 1024


def main():
    global ConnectionCount
    """Creating a TCP server socket"""

    server.bind(ADDR)
    server.listen(5)
    print(f"[+]Started TCP Server on {IP}:{PORT}...")

    # Starting the server closing handler on a new thread.
    serverManagerThread.start()

    """ Accepting the connection from the client. """
    while True:
        conn, addr = server.accept()
        ConnectionCount += 1
        # handleClient(conn, addr)
        print("new con")
        thread = threading.Thread(target=handleClient, args=(conn, addr))

        thread.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as msg:
        print(f"[+] Closing the TCP Server on {IP}:{PORT}")
        for thread in threading.enumerate():
            if thread is not threading.current_thread():
                print(thread.name)
                thread.join()
        exit()
    except Exception as e:
        print(e)
