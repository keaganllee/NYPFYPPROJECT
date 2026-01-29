import httpx

r = httpx.post(
    'https://api.fish.audio/v1/tts',
    json={
        'text': 'Hello world',
        'reference_id': '193f7f8f649b418382885c5fb4fb7109',
        'format': 'wav'
    },
    headers={
        'Authorization': 'Bearer (YOUR API KEY)', #this is the API key for Fish Audio change it accordingly 
        'Content-Type': 'application/json'
    },
    timeout=30
)

print(f'Status: {r.status_code}')
if r.status_code == 200:
    print(f'Audio received, size: {len(r.content)} bytes')
    with open('test_fish_audio.wav', 'wb') as f:
        f.write(r.content)
    print('Saved to test_fish_audio.wav')
else:
    print(f'Error: {r.text[:500]}')
