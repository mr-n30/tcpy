#!/usr/bin/env python3
import sys
import socket
import validators
from multiprocessing import Pool

# List of domains
domain_list = sys.argv[1]
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
                    print(f"http://{domain}:80/")
                    sys.stdout.flush()
                    IP=""

            elif len(HOST[2]) > 1:
                for IP in HOST[2]:
                    http_result = s.connect_ex((IP, HTTP))
                    socket.setdefaulttimeout(SEC)

                    if http_result == 0:
                        print(f"http://{domain}:80/")
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
                    print(f"https://{domain}:443/")
                    sys.stdout.flush()
                    IP=""

            elif len(HOST[2]) > 1:
                for IP in HOST[2]:
                    https_result = s.connect_ex((IP, HTTPS))
                    socket.setdefaulttimeout(SEC)

                    if https_result == 0:
                        print(f"https://{domain}:443/")
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
    with open(domain_list, "r") as f:
        domains = f.readlines()

    with Pool(50) as p:
        results = p.map(tcpy, domains)
        success = list(filter(None, results))

    print("[+] Done...")

if __name__ == "__main__":
    main()
