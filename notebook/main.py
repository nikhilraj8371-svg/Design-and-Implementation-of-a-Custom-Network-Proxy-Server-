import socket
import threading
import os
import logging
import json

# --- CONFIGURATION LOADER ---
def load_config():
    with open('config/settings.json', 'r') as f:
        return json.load(f)

CONFIG = load_config()

# --- SETUP LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG['log_file']),
        logging.StreamHandler()
    ]
)

def load_blocked_domains():
    path = CONFIG['blocked_domains_file']
    if not os.path.exists(path): return []
    with open(path, "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

def relay_data(src, dst):
    """
    Relays raw data between two sockets. 
    Used for bidirectional communication in HTTPS tunnels.
    """
    try:
        while True:
            data = src.recv(4096)
            if not data: break
            dst.sendall(data)
    except:
        pass

def handle_client(client_socket, client_address):
"""
    Main worker function. Parses requests, checks the blacklist,
    and manages the forwarding/tunneling logic.
    """

    try:
        client_socket.settimeout(CONFIG['timeout'])
        request_data = client_socket.recv(4096)
        if not request_data: return

        # 1. PARSE
        request_text = request_data.decode('utf-8', errors='ignore')
        lines = request_text.split('\n')
        if not lines: return
        
        parts = lines[0].split(' ')
        if len(parts) < 2: return
        method, url = parts[0].upper(), parts[1]

        # 2. EXTRACT HOST/PORT
        if method == "CONNECT":
            host = url.split(':')[0]
            port = int(url.split(':')[1]) if ":" in url else 443
        else:
            http_pos = url.find("://")
            temp = url if http_pos == -1 else url[(http_pos + 3):]
            webserver_pos = temp.find("/")
            if webserver_pos == -1: webserver_pos = len(temp)
            host_part = temp[:webserver_pos]
            host = host_part.split(':')[0]
            port = int(host_part.split(':')[1]) if ":" in host_part else 80

        # 3. FILTER (The Security Step)
        clean_host = host.lower()
        blocked_list = load_blocked_domains()
        if any(clean_host == b or clean_host.endswith("." + b) for b in blocked_list):
            logging.info(f"BLOCKED: {client_address} -> {clean_host}")
            client_socket.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\nBlocked by Proxy.")
            return

        # 4. FORWARD
        logging.info(f"PROXYING: {method} {host}:{port} for {client_address}")
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.settimeout(CONFIG['timeout'])
        
        remote_socket.connect((host, port))
        
        if method == "CONNECT":
            client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        else:
            remote_socket.sendall(request_data)

        # 5. BIDIRECTIONAL TUNNEL
        t = threading.Thread(target=relay_data, args=(remote_socket, client_socket), daemon=True)
        t.start()
        relay_data(client_socket, remote_socket)

    except Exception as e:
        logging.error(f"Error handling {client_address}: {e}")
    finally:
        client_socket.close()

def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((CONFIG['host'], CONFIG['port']))
        server.listen(CONFIG['thread_pool_size'])
        logging.info(f"Proxy ready at {CONFIG['host']}:{CONFIG['port']}")

        while True:
            client_sock, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        logging.info("Shutting down the proxy server...")
    finally:
        server.close()
         # This ensures the port is released immediately
if __name__ == "__main__":
    start_proxy()
