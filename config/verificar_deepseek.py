# verificar_deepseek.py - Verificar saldo de DeepSeek
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY')

if not api_key:
    print('❌ DEEPSEEK_API_KEY no encontrada en .env')
    exit()

print(f'🔑 API Key: {api_key[:15]}...{api_key[-10:]}')

headers = {'Authorization': f'Bearer {api_key}'}

# 1. Verificar saldo
print('\n📊 1. Verificando saldo...')
try:
    response = requests.get('https://api.deepseek.com/user/balance', headers=headers, timeout=10)
    print(f'📥 Código: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print('✅ Saldo consultado:')
        for info in data.get('balance_infos', []):
            currency = info.get('currency', 'USD')
            total = info.get('total_balance', '0')
            topped = info.get('topped_up_balance', '0')
            granted = info.get('granted_balance', '0')
            print(f'   💰 {currency}: {total}')
            print(f'      - Recargado: {topped}')
            print(f'      - Regalado: {granted}')
    elif response.status_code == 401:
        print('❌ API Key inválida')
    elif response.status_code == 402:
        print('❌ Sin saldo')
    else:
        print(f'❌ Error: {response.text[:200]}')
except Exception as e:
    print(f'❌ Error de conexión: {str(e)}')

# 2. Verificar transacciones
print('\n📊 2. Verificando transacciones...')
try:
    response = requests.get(
        'https://api.deepseek.com/user/transactions',
        headers=headers,
        timeout=10
    )
    print(f'📥 Código: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        transactions = data.get('transactions', [])
        if transactions:
            print('📊 Transacciones recientes:')
            for tx in transactions[:5]:
                tx_type = tx.get('type', 'unknown')
                amount = tx.get('amount', '0')
                currency = tx.get('currency', 'USD')
                status = tx.get('status', 'unknown')
                print(f"   {tx_type}: {amount} {currency} - {status}")
        else:
            print('   No hay transacciones recientes')
    else:
        print(f'❌ Error: {response.text[:200]}')
except Exception as e:
    print(f'❌ Error de conexión: {str(e)}')

# 3. Probar chat con DeepSeek
print('\n📊 3. Probando chat con DeepSeek...')
try:
    url = 'https://api.deepseek.com/v1/chat/completions'
    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'user', 'content': 'Responde "DeepSeek funciona" en español.'}
        ],
        'max_tokens': 50
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f'📥 Código: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print('✅ DeepSeek funciona!')
        print(f'📝 Respuesta: {data["choices"][0]["message"]["content"]}')
    elif response.status_code == 402:
        print('❌ Error 402: Saldo insuficiente')
        print(f'📝 {response.text[:300]}')
    else:
        print(f'❌ Error: {response.text[:200]}')
except Exception as e:
    print(f'❌ Error de conexión: {str(e)}')