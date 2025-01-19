# windows_control
python script to control Windows or Linux 

## Requirements

pip install opencv-python-headless

pip install pycryptodome

## Build binary file for client

pip install nuitka

nuitka --standalone --onefile --windows-disable-console client_os.py

## Config file

config in settings.py

```python
def get_host():
    host = '127.0.0.1'
    return host
def get_port():
    port = 8888
    return port
def get_cam_port():
    port = 8001
    return port
def get_file_port():
    port = 8000
    return port
def get_key():
    key = b'd6hb59jf0xpt42m1'
    return key
```

host : your public IP address on VPS

key : RSA encryption key for encrypt and decrypt traffic

## Usages

Config public IP and build executable binary file, run on client's PC

Run server script on VPS or PC with public IP


