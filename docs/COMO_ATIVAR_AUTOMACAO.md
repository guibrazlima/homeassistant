# 🔄 RELOAD DE AUTOMAÇÕES - INSTRUÇÕES

## ✅ Automação Restaurada - Aguarda Ativação

A automação `bomba_piscina_dia` foi **adicionada ao ficheiro** `automations.yaml` mas ainda **não está ativa** no sistema.

---

## 🚀 COMO ATIVAR (escolha uma opção):

### Opção 1: Via Interface Web (RECOMENDADO)

1. **Abrir Home Assistant no browser:**
   - URL: http://localhost:8123 (ou IP da máquina)

2. **Ir ao Developer Tools:**
   - Menu lateral → ⚙️ **Developer Tools**
   - OU direto: http://localhost:8123/developer-tools/yaml

3. **Recarregar Automações:**
   - Clicar no separador **"YAML"**
   - Localizar secção **"Automations"**
   - Clicar no botão **"RELOAD AUTOMATIONS"** ou ícone 🔄
   - Aguardar confirmação (aparece notificação verde)

4. **Verificar:**
   - Ir a: **Settings** → **Automations & Scenes**
   - Procurar: **"🏊🏻 Piscina - Bomba Piscina Dia"**
   - Deve aparecer na lista com toggle **ON**

---

### Opção 2: Via Serviço (Developer Tools)

1. **Abrir Developer Tools → Services**

2. **Executar serviço:**
   ```yaml
   service: automation.reload
   ```

3. **Clicar em "CALL SERVICE"**

4. **Verificar confirmação**

---

### Opção 3: Reiniciar Home Assistant

Se preferir reiniciar todo o sistema:

1. **Via UI:**
   - Settings → System → ⚙️ (menu superior direito)
   - Clicar em **"Restart"**
   - Confirmar
   - Aguardar ~30-60 segundos

2. **Via Docker (terminal):**
   ```bash
   docker restart homeassistant
   ```

---

## ✅ Como Verificar que Funcionou

### 1. Verificar Automação Existe

**Via UI:**
- Settings → Automations & Scenes
- Procurar: "Bomba Piscina Dia"
- Deve mostrar:
  - 🏊🏻 **Piscina - Bomba Piscina Dia**
  - Estado: **ON** (toggle ativo)
  - Blueprint: **PV Excess Control**

### 2. Verificar Sem Erros

**Via Logs (Developer Tools → Logs):**
- Filtrar por: `bomba_piscina_dia`
- **Bom sinal:** "Initialized successfully" ou sem mensagens
- **Mau sinal:** "Error loading automation" ou "Blueprint not found"

**Via Terminal:**
```bash
tail -50 /data/homeassistant/home-assistant.log | grep -i "bomba_piscina_dia"
```

### 3. Verificar Sensores

**Via Developer Tools → States:**

Procurar e confirmar que têm valores:
- ✅ `sensor.emoncms_solar`
- ✅ `sensor.emoncms_export_power_positive`
- ✅ `sensor.emoncms_use`
- ✅ `sensor.bomba_piscina_switch_0_power`

Se algum mostrar `unavailable` ou `unknown`:
- Verificar integração EmonCMS
- Verificar configuração dos sensores

### 4. Verificar Entidade da Automação

**Via Developer Tools → States:**
- Procurar: `automation.bomba_piscina_dia`
- Estado deve ser: **`on`** (ou `off` se desativada manualmente)
- Atributos devem incluir:
  - `friendly_name`: "🏊🏻 Piscina - Bomba Piscina Dia"
  - `id`: "bomba_piscina_dia"

---

## 🎯 Próximos Passos Após Reload

### Imediato (nos primeiros 5 minutos)

1. ✅ Confirmar automação aparece na lista
2. ✅ Confirmar sem erros nos logs
3. ✅ Confirmar todos os sensores disponíveis

### Durante o Dia (quando houver sol)

1. **Observar comportamento:**
   - Quando excedente solar > threshold → bomba deve ligar
   - Quando consumir da rede → bomba deve desligar

2. **Monitorizar logs:**
   ```bash
   tail -f /data/homeassistant/home-assistant.log | grep -i "bomba_piscina_dia"
   ```

3. **Verificar History:**
   - Abrir entidade `automation.bomba_piscina_dia`
   - Ver histórico de ativações
   - Verificar se responde ao excedente solar

### Esta Semana

1. **Decidir sobre automação redundante:**
   - `automacao_bomba_piscina` (ID diferente) faz algo similar
   - Se o blueprint funcionar bem → desativar a antiga
   - Ou ajustar horários para não conflitarem

2. **Afinar parâmetros se necessário:**
   - Power toggle margin (atual: 10W)
   - Horários de operação
   - Thresholds de potência

---

## 🆘 Troubleshooting

### Problema: Automação não aparece após reload

**Verificar sintaxe YAML:**
```bash
cd /data/homeassistant
grep -A25 "id: bomba_piscina_dia" automations.yaml
```

**Se houver erro de sintaxe:**
- Verificar indentação (espaços, não tabs)
- Verificar aspas e caracteres especiais
- Testar com validador YAML online

### Problema: "Blueprint not found"

**Verificar blueprint existe:**
```bash
find /data/homeassistant -name "*pv_excess_control.yaml" -type f
```

**Se não encontrar:**
1. Ir a Settings → Blueprints → Import Blueprint
2. URL: `https://github.com/panhans/HomeAssistant`
3. Importar blueprint PVExcessControl

### Problema: Sensores unavailable

**Verificar integração EmonCMS:**
1. Settings → Devices & Services
2. Procurar "EmonCMS"
3. Verificar estado: deve estar "OK" não "Failed"

**Se falhar:**
- Verificar configuração em `configuration.yaml`
- Verificar ligação ao servidor EmonCMS
- Verificar API key

### Problema: Automação não reage ao excedente solar

**Verificar:**
1. Sensores têm valores reais (não 0 ou null)
2. Thresholds configurados adequados
3. Horários permitidos (se houver condições de tempo)
4. Switch da bomba está acessível

**Ajustar se necessário:**
- Editar automação no UI
- Modificar inputs do blueprint
- Testar manualmente o switch primeiro

---

## 📊 Status Atual

### ✅ Concluído
- [x] Automação recuperada do Git
- [x] Código adicionado ao `automations.yaml`
- [x] Sintaxe YAML validada
- [x] Sensores verificados (existem)
- [x] Blueprint verificado (existe)
- [x] Documentação criada

### ⏳ Aguarda Ação Manual
- [ ] **RELOAD de automações via UI** ← VOCÊ ESTÁ AQUI
- [ ] Verificação pós-reload
- [ ] Teste durante horas solares
- [ ] Decisão sobre automação redundante

---

## 📞 Contacto Rápido

**Se precisar de ajuda adicional:**

1. **Verificar estado atual:**
   ```bash
   docker ps | grep homeassistant
   docker logs homeassistant --tail 50
   ```

2. **Ver configuração adicionada:**
   ```bash
   grep -A30 "id: bomba_piscina_dia" /data/homeassistant/automations.yaml
   ```

3. **Acesso direto à automação (após reload):**
   - URL: http://localhost:8123/config/automation/edit/bomba_piscina_dia

---

## 🎉 Resumo

### O Que Foi Feito Automaticamente:
✅ Recuperação do Git  
✅ Validação de dependências  
✅ Inserção no ficheiro  
✅ Criação de documentação  

### O Que Precisa Fazer Manualmente:
🔄 **Recarregar automações via Developer Tools → YAML**  
👁️ Verificar se aparece na lista  
📊 Observar comportamento durante dias com sol  

---

**Tempo estimado:** 2 minutos para reload + 5 minutos de verificação

**Próxima ação:** Abrir http://localhost:8123/developer-tools/yaml e clicar em "RELOAD AUTOMATIONS"

---

*Ficheiro gerado automaticamente pela restauração da automação `bomba_piscina_dia`*  
*Data: 1 Fevereiro 2026*
