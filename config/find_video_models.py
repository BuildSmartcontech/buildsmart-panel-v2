import requests

print('🔍 Buscando modelos de video en Replicate...\n')

url = 'https://api.replicate.com/v1/models'
headers = {'Authorization': 'Token TU_REPLICATE_KEY_AQUI'}

try:
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        models = response.json().get('results', [])
        video_models = []
        for model in models:
            name = model.get('name', '').lower()
            owner = model.get('owner', '').lower()
            desc = model.get('description', '').lower()
            if 'video' in name or 'video' in desc or 'generate' in name:
                video_models.append({
                    'name': f"{model['owner']}/{model['name']}",
                    'description': model.get('description', '')[:100]
                })
        
        if video_models:
            print(f'✅ Se encontraron {len(video_models)} modelos de video:')
            for m in video_models[:20]:
                print(f'   - {m["name"]}')
                print(f'     {m["description"]}...\n')
        else:
            print('❌ No se encontraron modelos de video')
            
    else:
        print(f'❌ Error: {response.status_code}')
        print(response.text[:300])
        
except Exception as e:
    print(f'❌ Error: {str(e)}')
