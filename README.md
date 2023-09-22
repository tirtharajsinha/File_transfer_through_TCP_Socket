# File_transfer_through_TCP_Socket

File transfer through TCP using socket programming in python.

### Prerequisite

- Python3

### Python dependency install

```
pip install tqdm
```

### Configure TARGET SERVER and PORT

For server.py:

```python
# Change if this port is used elsewhere
PORT = 4456
```

for client(clientUploader.py, clientDownloader.py and client_on_thread.py):

```python
# If server and client on diffrent server then keep it unchanged
# But if client and server on diffrent system find the server ip and port and put it here.

IP = socket.gethostbyname(socket.gethostname()) #  target server IP
PORT = 4456 # target server PORT
```

### Run with

```
python server.py
```

and

```
python clientUploader.py
```
