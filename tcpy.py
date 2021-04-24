#!/usr/bin/env python3
import sys
import socket
import argparse
import validators
from multiprocessing import Pool

parser = argparse.ArgumentParser(description="Accepts domains from stdin and checks if specified ports are open")
parser.add_argument("-w", "--workers", default=50, type=int, help="Amount of workers/processes to open (Default is 50)")

args = parser.parse_args()
workers = args.workers

# List of domains
try:
    domain_list = []
    for line in sys.stdin:
        domain_list.append(line)
except KeyboardInterrupt as e:
    print("\n[+] Cancelling")

# Time to wait
SEC = 3

def tcpy(d):
    try:
        domain = d.strip()
        HTTP   = 80
        HTTPS  = 443

        if not validators.domain(domain):
            return
        else:
            HOST = socket.gethostbyname_ex(domain)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if len(HOST[2]) == 1:
                IP = HOST[2][0]
                if IP != '':
                    http_result = s.connect_ex((IP, HTTP))
                    socket.setdefaulttimeout(SEC)
                else:
                    return

                if http_result == 0:
                    print(f"http://{domain}:80")
                    sys.stdout.flush()
                    IP=""

            elif len(HOST[2]) > 1:
                for IP in HOST[2]:
                    http_result = s.connect_ex((IP, HTTP))
                    socket.setdefaulttimeout(SEC)

                    if http_result == 0:
                        print(f"http://{domain}:80")
                        sys.stdout.flush()
                        IP=""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if len(HOST[2]) == 1:
                IP = HOST[2][0]
                if IP != '':
                    https_result = s.connect_ex((IP, HTTPS))
                    socket.setdefaulttimeout(SEC)
                else:
                   return

                if https_result == 0:
                    print(f"https://{domain}:443")
                    sys.stdout.flush()
                    IP=""

            elif len(HOST[2]) > 1:
                for IP in HOST[2]:
                    https_result = s.connect_ex((IP, HTTPS))
                    socket.setdefaulttimeout(SEC)

                    if https_result == 0:
                        print(f"https://{domain}:443")
                        sys.stdout.flush()
                        IP=""

    except KeyboardInterrupt as e:
        print("Cancelling...")
        sys.stdout.flush()
        sys.exit(1)
    except socket.gaierror as e:
        pass
    except socket.error as e:
        pass
    except socket.timeout as e:
        pass
    except Exception as e:
        print(f"[!] ERROR in: tcpy: {e}")
        sys.stdout.flush()
        pass

def main():
    with Pool(workers) as p:
        results = p.map(tcpy, domain_list)

if __name__ == "__main__":
    main()
