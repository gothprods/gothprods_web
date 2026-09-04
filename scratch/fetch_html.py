import urllib.request
try:
    with urllib.request.urlopen('http://127.0.0.1:5001/') as response:
        html = response.read().decode('utf-8')
        if 'CANCELADO' in html.upper():
            print("Found CANCELADO in HTML")
        else:
            print("CANCELADO not found in HTML")
except Exception as e:
    print(e)
