import os
import socket
import threading

# Constants
DEFAULT_NUM_THREADS = 200

def scan_ips(start_ip, end_ip):
    ips = []
    start_ip_split = list(map(int, start_ip.split('.')))
    end_ip_split = list(map(int, end_ip.split('.')))

    for i in range(start_ip_split[0], end_ip_split[0] + 1):
        for j in range(start_ip_split[1], end_ip_split[1] + 1):
            for k in range(start_ip_split[2], end_ip_split[2] + 1):
                for l in range(start_ip_split[3], end_ip_split[3] + 1):
                    ip = f"{i}.{j}.{k}.{l}"
                    ips.append(ip)

    return ips

def test_ip(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((ip, port))
        return True
    except (socket.error, socket.timeout):
        return False

def find_cameras(start_ip, end_ip, port, num_threads=DEFAULT_NUM_THREADS):
    ips = scan_ips(start_ip, end_ip)
    total_ips = len(ips)
    scanned_ips = 0
    saved_ips = 0

    class CameraScanner(threading.Thread):
        def __init__(self, ip_list):
            super().__init__()
            self.ip_list = ip_list

        def run(self):
            nonlocal scanned_ips, saved_ips
            for ip in self.ip_list:
                if test_ip(ip, port):
                    with open("host.txt", "a+") as f:
                        existing_ips = set(line.strip() for line in f)
                        if ip not in existing_ips:
                            f.write(f"{ip}\n")
                            saved_ips += 1
                scanned_ips += 1
                progress = (scanned_ips / total_ips) * 100
                print(f"\rProgress: {progress:.2f}% | Saved IPs: {saved_ips}", end='', flush=True)

    threads = []
    chunk_size = len(ips) // num_threads
    for i in range(num_threads):
        thread_ips = ips[i * chunk_size:(i + 1) * chunk_size]
        thread = CameraScanner(thread_ips)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\nScan completed.")

if __name__ == '__main__':
    start_ip = input("Enter the start IP address range: ")
    end_ip = input("Enter the end IP address range: ")
    port = int(input("Enter the port to scan: "))
    find_cameras(start_ip, end_ip, port)


