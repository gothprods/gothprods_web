from app import app
with app.test_client() as client:
    response = client.get('/')
    print("Status:", response.status_code)
    if response.status_code == 500:
        print(response.text)
