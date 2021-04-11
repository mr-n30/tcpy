#!/usr/bin/env python3
import sys
import socket
import validators
import concurrent.futures

# List of domains
domain_list = sys.argv[1]

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
                    socket.setdefaulttimeout(3.0)
                else:
                    return

                if http_result == 0:
                    print(f"http://{domain}:80/")
                    sys.stdout.flush()
                    IP=""

            elif len(HOST[2]) > 1:
                for IP in HOST[2]:
                    http_result = s.connect_ex((IP, HTTP))
                    socket.setdefaulttimeout(3.0)

                    if http_result == 0:
                        print(f"http://{domain}:80/")
                        sys.stdout.flush()
                        IP=""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if len(HOST[2]) == 1:
                IP = HOST[2][0]
                if IP != '':
                    https_result = s.connect_ex((IP, HTTPS))
                    socket.setdefaulttimeout(3.0)
                else:
                   return

                if https_result == 0:
                    print(f"https://{domain}:443/")
                    sys.stdout.flush()
                    IP=""

            elif len(HOST[2]) > 1:
                for IP in HOST[2]:
                    https_result = s.connect_ex((IP, HTTPS))
                    socket.setdefaulttimeout(3.0)

                    if https_result == 0:
                        print(f"https://{domain}:443/")
                        sys.stdout.flush()
                        IP=""
    except KeyboardInterrupt as e:
        print("Cancelling...")
    except socket.gaierror as e:
        #print(f"[!] ERROR in: main(): {e}")
        pass
    except socket.error as e:
        #print(f"[!] ERROR in: main(): {e}")
        pass
    except Exception as e:
        #print(f"[!] ERROR in: main(): {e}")
        pass

def main():
    with open(domain_list, "r") as f:
        domains = f.readlines()

    with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
        results = executor.map(tcpy, domains)
        success = list(filter(None, results))

    print("[+] Done...")

if __name__ == "__main__":
    main()
