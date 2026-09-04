import urllib.request
url = "https://docs.google.com/spreadsheets/d/1FTb-EzMtCGoxb0tAjoVQtTTeGJFd6qCP/export?format=csv&gid=2129987380"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    csv_data = response.read().decode('utf-8')
    print(csv_data[:500])
