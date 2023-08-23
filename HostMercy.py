import os
import sys
import socket
import threading

# Constants
DEFAULT_NUM_THREADS = 200

def scan_ips(start_ip, end_ip):
    # Your existing scan_ips function here...

def test_ip(ip, port):
    # Your existing test_ip function here...

def find_cameras(start_ip, end_ip, port, num_threads=DEFAULT_NUM_THREADS):
    ips = scan_ips(start_ip, end_ip)
    total_ips = len(ips)
    scanned_ips = 0
    saved_ips = 0

    class CameraScanner(threading.Thread):
        def __init__(self, ip_list):
            threading.Thread.__init__(self)
            self.ip_list = ip_list

        def run(self):
            nonlocal scanned_ips, saved_ips
            for ip in self.ip_list:
                if test_ip(ip, port):
                    with open("host.txt", "a+") as f:
                        existing_ips = set(f.read().splitlines())
                        if ip not in existing_ips:
                            f.write(f"{ip}\n")
                            saved_ips += 1
                scanned_ips += 1
                progress = (scanned_ips / total_ips) * 100
                print(f"\rProgress: {progress:.2f}% | Saved IPs: {saved_ips}", end='', flush=True)

    threads = []
    chunk_size = len(ips) // num_threads
    for i in range(num_threads):
        thread_ips = ips[i*chunk_size:(i+1)*chunk_size]
        thread = CameraScanner(thread_ips)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\nScan completed.")

if __name__ == '__main__':
    start_ip = input("Enter the start IP address range: ")
    end_ip = input("Enter the end IP address range: ")
    port = input("Enter the port to scan: ")
    find_cameras(start_ip, end_ip, int(port))

