# 🔒 GUIA DE SEGURANÇA - Home Assistant

## ⚠️ FICHEIROS SENSÍVEIS - NUNCA VERSIONAR

Os seguintes ficheiros contêm informação sensível e **NUNCA** devem ser commitados:

### 🔴 Crítico
- `secrets.yaml` - Passwords, tokens, API keys
- `*.db`, `*.sqlite` - Bases de dados com dados pessoais
- `*.key`, `*.pem`, `*.crt` - Certificados e chaves SSL/TLS
- `solcast-*.json` - Contêm coordenadas GPS e API keys
- `known_devices.yaml` - Endereços MAC e nomes de dispositivos
- `.cloud`, `.uuid` - Identificadores únicos da instalação

### 🟡 Importante
- `*.log` - Podem conter IPs, tokens em plaintext
- `ip_bans.yaml` - Lista de IPs banidos
- `*.conf` - Configurações de dispositivos com credenciais
- `backups/*.tar` - Backups completos do sistema

### 🟢 Atenção
- `www/` - Pode conter imagens pessoais
- `tts/` - Cache de TTS com conteúdo pessoal
- `.storage/` - Configurações que podem ter dados sensíveis

## ✅ CHECKLIST DE SEGURANÇA

### Antes do Primeiro Commit
- [ ] Verificar que `secrets.yaml` está no `.gitignore`
- [ ] Confirmar que nenhum password está hardcoded nos ficheiros `.yaml`
- [ ] Remover tokens e API keys de ficheiros de configuração
- [ ] Criar ficheiros `.example` para documentação

### Manutenção Regular
- [ ] Revisar periodicamente o `.gitignore`
- [ ] Verificar se ficheiros sensíveis foram acidentalmente commitados
- [ ] Usar `git log --all -- secrets.yaml` para verificar histórico
- [ ] Auditar ficheiros públicos no repositório

## 🔍 VERIFICAÇÃO DE SEGURANÇA

### Comando para verificar ficheiros sensíveis versionados:
```bash
git ls-files | grep -E "(secrets\.yaml|\.db$|\.log|\.token|\.key$|\.pem$)"
```

### Remover ficheiro sensível do Git (mantém local):
```bash
git rm --cached ficheiro_sensivel.yaml
git commit -m "Remove sensitive file from repository"
```

### Remover completamente do histórico (CUIDADO!):
```bash
# Usar apenas se absolutamente necessário
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch secrets.yaml" \
  --prune-empty --tag-name-filter cat -- --all

# Forçar push (se repositório remoto)
git push origin --force --all
```

## 🛡️ BOAS PRÁTICAS

### 1. Usar Secrets Sempre
❌ **ERRADO:**
```yaml
telegram_bot:
  - platform: polling
    api_key: "123456:ABCdef..."  # Nunca fazer isto!
```

✅ **CORRETO:**
```yaml
telegram_bot:
  - platform: polling
    api_key: !secret telegram_bot_api_key
```

### 2. Documentar sem Expor
Criar ficheiros `.example` para documentação:
- `secrets.yaml.example`
- `solcast-sites.json.example`

### 3. Validar Antes de Commit
```bash
# Verificar o que será commitado
git diff --cached

# Verificar ficheiros não tracked
git status

# Verificar se há secrets expostos
grep -r "password\|token\|api_key" *.yaml
```

### 4. Configurar Git Hooks (Opcional)
Criar `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Verifica se secrets.yaml está sendo commitado

if git diff --cached --name-only | grep -q "secrets.yaml"; then
    echo "❌ ERRO: Tentativa de commitar secrets.yaml!"
    echo "Este ficheiro contém informação sensível."
    exit 1
fi

# Verifica por passwords hardcoded
if git diff --cached | grep -i "password.*:.*['\"]"; then
    echo "⚠️  AVISO: Possível password hardcoded detectado!"
    echo "Por favor revise o commit."
    exit 1
fi

exit 0
```

### 5. Usar Variáveis de Ambiente (Avançado)
Para ambientes Docker/Container:
```yaml
# Suporta variáveis de ambiente
mariadb_connection: !env_var DB_CONNECTION_STRING
```

## 📋 TEMPLATE DE secrets.yaml

```yaml
# ========================================
# SECRETS - NÃO VERSIONAR ESTE FICHEIRO!
# ========================================

# Base de Dados
mariadb_connection: "mysql://user:pass@host:3306/homeassistant"

# InfluxDB
influxdb_token: "your_token_here"

# Telegram
telegram_bot_api_key: "bot_token_here"

# Solcast (se aplicável)
solcast_api_key: "api_key_here"

# Outros
# Adicione aqui conforme necessário
```

## 🚨 SE ACIDENTALMENTE EXPÔS CREDENCIAIS

### Ação Imediata:
1. **Revogar/Regenerar** todas as credenciais expostas
2. **Remover do Git** usando os comandos acima
3. **Forçar push** se já foi para repositório remoto
4. **Atualizar** todas as instâncias com novas credenciais

### Serviços a Atualizar:
- [ ] Telegram Bot (regenerar token)
- [ ] Solcast API (regenerar key)
- [ ] MariaDB (alterar password)
- [ ] InfluxDB (regenerar token)
- [ ] Outros serviços externos

### Notificação:
- Se repositório público: considerar notificar utilizadores
- Monitorizar acessos suspeitos
- Verificar logs de autenticação

## 📞 RECURSOS

- [Home Assistant Security](https://www.home-assistant.io/docs/configuration/securing/)
- [Git Secrets Tool](https://github.com/awslabs/git-secrets)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) - Limpeza de histórico

---

**⚠️ LEMBRE-SE: Segurança é um processo contínuo, não um evento único!**

**Última atualização:** Novembro 2025
