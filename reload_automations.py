#!/usr/bin/env python3
"""Script para recarregar automações do Home Assistant."""
import requests
import json

# URL da API local
url = "http://localhost:8123/api/services/automation/reload"

# Headers (sem autenticação para localhost interno)
headers = {
    "Content-Type": "application/json"
}

try:
    # Tentar sem token primeiro (pode funcionar se permitido internamente)
    response = requests.post(url, headers=headers, json={})
    
    if response.status_code == 200:
        print("✅ Automações recarregadas com sucesso!")
        print(f"📄 Resposta: {response.text}")
    elif response.status_code == 401:
        print("❌ Erro 401: Não autorizado")
        print("ℹ️  Por favor, recarregue manualmente via UI:")
        print("   Developer Tools → YAML → AUTOMATIONS → Reload")
    else:
        print(f"⚠️  Status: {response.status_code}")
        print(f"📄 Resposta: {response.text}")
        
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    print("\nℹ️  Por favor, recarregue manualmente via UI:")
    print("   Developer Tools → YAML → AUTOMATIONS → Reload")
