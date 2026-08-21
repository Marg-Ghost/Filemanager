from fastapi.testclient import TestClient
import server

client = TestClient(server.app)

print('notes_load_status', client.get('/notes_load').status_code)
print('notes_load_body', client.get('/notes_load').json())
print('notes_save_status', client.post('/notes_save', json={'content': 'Hallo Welt'}).status_code)
print('notes_save_body', client.post('/notes_save', json={'content': 'Hallo Welt'}).json())
print('media_load_status', client.get('/media_load').status_code)
print('media_load_body', client.get('/media_load').json())
print('media_add_status', client.post('/media_add', files={'file': ('test.txt', b'hello', 'text/plain')}).status_code)
print('media_add_body', client.post('/media_add', files={'file': ('test.txt', b'hello', 'text/plain')}).text)
