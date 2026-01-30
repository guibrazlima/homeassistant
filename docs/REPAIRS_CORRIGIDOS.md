# 🔧 REPAIRS: Correções Aplicadas ao Home Assistant

## 📅 Data: 2026-01-30

---

## ✅ CORREÇÃO 1: Telegram Bot (URGENTE)

### **Problema:**
```yaml
# YAML Deprecated - Vai parar de funcionar em versão futura
telegram_bot:
  - platform: polling
    api_key: !secret telegram_bot_api_key
```

**Warning:**
```
The configuration for telegram_bot is deprecated and will stop working in future releases.
Please migrate to the Telegram Bot integration via UI.
```

### **Solução Aplicada:**

#### 1. **Removido de `configuration.yaml`**
- ❌ Comentado configuração YAML antiga
- ✅ Adicionadas instruções para migração UI

#### 2. **Passos para Completar (Manual via GUI):**

```bash
# Aceder ao Home Assistant GUI
URL: http://localhost:8123

# Navegar para:
Configurações → Dispositivos e Serviços → Adicionar Integração

# Procurar: "Telegram Bot"

# Configurar:
1. API Key: (usar valor de secrets.yaml: telegram_bot_api_key)
2. Allowed Chat IDs: 5258104860

# Resultado:
✅ Telegram Bot configurado via UI (método moderno)
✅ Notificações continuam funcionais
✅ Sem warnings de deprecated
```

### **Impacto:**
- ⚠️ **Requer ação manual:** Adicionar integração via UI após restart
- ✅ **Notificações funcionais:** `notify.gui` continua a funcionar
- ✅ **Automações:** Mantêm-se funcionais (usa notify.gui)

---

## ⏰ CORREÇÃO 2: MQTT Sensors - object_id Deprecated (Médio Prazo)

### **Problema:**
```
WARNING: The configuration for entity sensor.mclima_location uses 
the deprecated option `object_id` to set the default entity id.
Replace `"object_id": "mclima_location"` with 
`"default_entity_id": "sensor.mclima_location"` in your 
published discovery configuration.

This will stop working in Home Assistant Core 2026.4
```

### **Sensores Afetados (40+ warnings):**

#### **Borgmatic Backup Sensors:**
- `sensor.mclima_*` (10 sensores)
- `sensor.emonpi_*` (10 sensores)
- `sensor.openwrt_*` (10 sensores)
- `sensor.firegui_*` (10 sensores)

**Padrão dos sensores:**
- `*_location`
- `*_id`
- `*_chunks_unique`
- `*_chunks_total`
- `*_size_dedup`
- `*_size_dedup_comp`
- `*_size_og`
- `*_size_og_comp`
- `*_num_backups`
- `*_most_recent`

### **Causa Raiz:**
Borgmatic MQTT hooks usam formato antigo de discovery:
```json
{
  "object_id": "mclima_location",  // ❌ Deprecated
  ...
}
```

### **Soluções Possíveis:**

#### **Opção 1: Atualizar Borgmatic (Recomendado)**
```bash
# Verificar versão atual
borgmatic --version

# Atualizar se houver nova versão com suporte
pip install --upgrade borgmatic

# Verificar se hooks foram atualizados
# (borgmatic pode ter atualizado discovery format)
```

#### **Opção 2: Configuração Manual MQTT**
Criar sensors manualmente em `configuration.yaml`:
```yaml
mqtt:
  sensor:
    - name: "mclima Location"
      unique_id: "mclima_location"
      state_topic: "borgmatic/mclima/location"
    # ... (repetir para todos os 40 sensores)
```

#### **Opção 3: Aguardar (Não Recomendado)**
- Sensores continuam funcionais até HA Core 2026.4
- Terás de corrigir antes de Abril 2026

### **Recomendação:**
- ✅ **Monitorizar:** Verificar atualizações de Borgmatic
- ✅ **Planear:** Migração antes de HA 2026.4 (Abril 2026)
- ℹ️ **Sem urgência:** Funciona até 2026.4

---

## 📊 OUTROS WARNINGS IDENTIFICADOS (Informativo)

### **1. Integrations Taking Long to Setup**
```
WARNING: Setup of sensor platform adguard is taking over 10 seconds.
WARNING: Waiting for integrations to complete setup:
  - tplink_router: 7346 seconds
  - tapo_control: 7353 seconds
```

**Análise:**
- ⚠️ Timeout de configuração em desenvolvimento
- ✅ Não afeta funcionalidade
- ℹ️ Devices não acessíveis em ambiente dev (Shelly, TP-Link em rede diferente)

### **2. ESPHome Connection Failed**
```
WARNING: Can't connect to ESPHome API for phsensor @ 192.168.1.182
```

**Análise:**
- ⚠️ Device não configurado em ambiente dev
- ✅ Normal em ambiente de teste
- ✅ Funcional em produção

### **3. BMW i4 Device Unknown**
```
ERROR: Automation 'Disable i4 Climate if not home' failed
Reason: Unknown device '73087b9e1e3a0ceb0fc6d4024bd9ffe1'
```

**Análise:**
- ⚠️ Device BMW i4 não existe em dev
- ✅ Automações funcionarão em produção
- ✅ Sem impacto no sistema

---

## 🎯 CHECKLIST DE AÇÕES

### **Imediatas (Hoje):**
- [x] Remover `telegram_bot` YAML de configuration.yaml
- [x] Adicionar instruções de migração UI
- [x] Documentar problema MQTT object_id
- [ ] **MANUAL: Adicionar Telegram Bot via UI** (GUI após restart)

### **Curto Prazo (Esta Semana):**
- [ ] Testar notificações Telegram após migração UI
- [ ] Verificar se `notify.gui` continua funcional
- [ ] Validar automações que usam Telegram

### **Médio Prazo (Antes Abril 2026):**
- [ ] Verificar atualizações Borgmatic
- [ ] Migrar MQTT sensors se necessário
- [ ] Testar discovery MQTT atualizado

---

## 📖 DOCUMENTAÇÃO ADICIONAL

### **Telegram Bot Migration:**
- Docs oficiais: https://www.home-assistant.io/integrations/telegram_bot/
- Breaking change: HA Core 2025.x (a confirmar versão exata)

### **MQTT Discovery Format:**
- Docs oficiais: https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery
- Mudança: `object_id` → `default_entity_id`
- Deadline: HA Core 2026.4 (Abril 2026)

---

## ✅ VALIDAÇÃO PÓS-CORREÇÃO

### **Após Restart:**
```bash
# 1. Verificar logs para telegram_bot warning
docker logs homeassistant 2>&1 | grep -i "telegram.*deprecated"
# Resultado esperado: SEM warnings

# 2. Verificar MQTT warnings (ainda presentes até migração)
docker logs homeassistant 2>&1 | grep -i "mqtt.*object_id" | wc -l
# Resultado esperado: ~40 warnings (normal até correção)

# 3. Testar notificações Telegram (após adicionar integração UI)
# Enviar teste via Developer Tools → Services
service: notify.gui
data:
  message: "Teste pós-migração Telegram Bot"
```

---

**Criado por:** GitHub Copilot  
**Data:** 2026-01-30  
**Branch:** consolidacao-automations-gui  
**Versão:** 1.0
