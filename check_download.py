from fastapi.testclient import TestClient
import server

client = TestClient(server.app)
response = client.get('/download_data')
print('status', response.status_code)
print('content-type', response.headers.get('content-type'))
print('content-disposition', response.headers.get('content-disposition'))
print('size', len(response.content))
