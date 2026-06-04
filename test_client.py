from app import app
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['email'] = 'test@test.com'
    response = client.get('/admin/dashboard')
    html = response.data.decode('utf-8')
    for line in html.split('\n'):
        if 'onclick="edit' in line:
            print(line.strip())
