import socket, ssl, json, re

def get_yt_streams():
    host = "www.youtube.com"
    context = ssl.create_default_context()
    with socket.create_connection((host, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            request = (
                "GET /@gothprods44/streams HTTP/1.1\r\n"
                "Host: www.youtube.com\r\n"
                "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"
                "Accept-Language: en-US,en;q=0.9\r\n"
                "Connection: close\r\n\r\n"
            )
            ssock.sendall(request.encode())
            
            response = b""
            while True:
                data = ssock.recv(4096)
                if not data:
                    break
                response += data
                
    html = response.decode('utf-8', errors='ignore')
    match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    if match:
        data = match.group(1)
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', data)
        print("Found titles in streams:")
        for t in titles[:15]:
            print(t)

get_yt_streams()
