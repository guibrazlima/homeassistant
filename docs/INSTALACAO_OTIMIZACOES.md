# 🚀 GUIA DE INSTALAÇÃO - OTIMIZAÇÕES PISCINA SOLAR

## 📋 Pré-requisitos

✅ Home Assistant instalado
✅ HACS instalado
✅ Integrações HACS necessárias:
- `mushroom` (Mushroom Cards)
- `apexcharts-card` (ApexCharts Card)
- `button-card` (Button Card)
- `power-flow-card-plus` (Power Flow Card Plus)
- `mini-graph-card` (Mini Graph Card)
- `bar-card` (Bar Card)
- `stack-in-card` (Stack In Card)
- `numberbox-card` (Numberbox Card)
- `dual-gauge-card` (Dual Gauge Card)

---

## 🔧 INSTALAÇÃO PASSO-A-PASSO

### **Passo 1: Verificar Estrutura de Pastas** ✅

Os ficheiros já foram criados em:
```
/data/homeassistant/
├── sensors/
│   ├── solar_smoothed.yaml
│   ├── house_consumption_weekday.yaml
│   └── piscina_weather_adjustment.yaml
├── packages/
│   └── piscina_solar_optimization.yaml
├── automations/
│   └── piscina_solar_notifications.yaml
└── lovelace/
    └── piscina_solar_dashboard.yaml
```

### **Passo 2: Verificar Configuration.yaml**

Certifica que tens estas linhas:
```yaml
sensor: !include_dir_merge_list sensors/
homeassistant:
  packages: !include_dir_named packages/
```

Se não tiveres a linha de `packages`, adiciona:
```yaml
homeassistant:
  packages: !include_dir_named packages/
```

### **Passo 3: Reiniciar Home Assistant**

1. **Via Terminal:**
   ```bash
   docker restart homeassistant
   ```

2. **Via UI:**
   - Configurações > Sistema > Reiniciar

3. **Aguardar 2 minutos** para todos os sensores carregarem

---

## 📊 INSTALAÇÃO DO DASHBOARD

### **Opção A: Dashboard Separado (Recomendado)**

1. **UI:** Configurações > Dashboards
2. Clicar **"+ Adicionar Dashboard"**
3. Nome: `Piscina Solar`
4. Ícone: `mdi:solar-power-variant`
5. Clicar **"Criar"**
6. Clicar nos **3 pontos** > **"Editar Dashboard"**
7. Clicar **"+ Adicionar Vista"**
8. Mudar para **"Editor de Código"** (3 pontos > Editar em YAML)
9. **Copiar conteúdo** de `/data/homeassistant/lovelace/piscina_solar_dashboard.yaml`
10. **Colar** e **Guardar**

### **Opção B: Adicionar ao Dashboard Principal**

1. Dashboard principal > **Editar**
2. **"+ Adicionar Vista"**
3. Título: `Piscina Solar`
4. Ícone: `mdi:solar-power-variant`
5. **3 pontos** > **"Editar em YAML"**
6. Copiar apenas a secção `cards:` do ficheiro
7. Colar e Guardar

---

## ⚙️ CONFIGURAÇÃO INICIAL

### **1. Ajustar Fator Fim-de-Semana**

No dashboard ou em:
- **Configurações > Devices & Services > Helpers**
- Encontrar: `input_number.piscina_weekend_consumption_factor`
- Ajustar baseado no teu padrão:
  - `0.7` = Casa vazia fim-de-semana (-30% consumo)
  - `1.0` = Consumo igual
  - `1.3` = Família toda em casa (+30% consumo)

### **2. Verificar Entidade Meteorologia**

Editar dashboard e procurar `weather.home`:
```yaml
weather_entity:
  entity: weather.home  # ← MUDAR PARA TUA ENTIDADE
```

Encontrar tua entidade:
- **Ferramentas Dev > Estados**
- Procurar `weather.`
- Copiar nome completo (ex: `weather.forecast_home`)

### **3. Configurar Notificações**

Editar `/data/homeassistant/automations/piscina_solar_notifications.yaml`:

Trocar `notify.mobile_app_iphone_de_guilherme` por:
```bash
# Descobrir nome do teu dispositivo:
cd /data/homeassistant
grep "mobile_app" .storage/core.device_registry | head -5
```

Ou no **UI:**
- Configurações > Companion App > Notificações
- Copiar nome do serviço

---

## 🧪 TESTES DE VALIDAÇÃO

### **Teste 1: Sensores de Média Móvel**

```bash
cd /data/homeassistant
curl -s http://localhost:8123/api/states/sensor.solar_power_5min_smooth | grep state
```

**Esperado:** Valor numérico (não `unknown` ou `unavailable`)

### **Teste 2: Indicador de Estabilidade**

Verificar no dashboard ou:
```bash
curl -s http://localhost:8123/api/states/sensor.solar_stability_indicator | grep state
```

**Esperado:** Percentagem (0-100)

### **Teste 3: Fator Dia Semana**

```bash
curl -s http://localhost:8123/api/states/sensor.house_consumption_weekday_factor | grep state
```

**Esperado:** 
- `1.0` (dias úteis)
- Valor configurado (fim-de-semana)

### **Teste 4: Dashboard Visível**

1. Ir a **`http://SEU_HA:8123/lovelace/piscina-solar`**
2. Verificar que vês:
   - ✅ Header com status bomba
   - ✅ Power Flow Card
   - ✅ Gráfico 24h
   - ✅ Indicadores de qualidade

---

## 🔄 ATUALIZAR BLUEPRINT PARA USAR SENSORES SUAVIZADOS

### **Opção 1: Via UI (Mais Fácil)**

1. **Configurações > Automações & Cenas**
2. Encontrar **"🏊 Piscina - Solar Inteligente v2"**
3. Clicar para editar
4. **Alterar sensores:**
   - `pv_power`: `sensor.solar_power_5min_smooth`
   - `house_power_no_pump`: `sensor.house_power_5min_smooth`
   - `net_power`: `sensor.import_export_5min_smooth` (se usares)
5. **Guardar**

### **Opção 2: Via YAML**

Editar `/data/homeassistant/automations.yaml`:

```yaml
- id: piscina_solar_v2
  use_blueprint:
    path: piscina_solar/piscina_solar_control_v2.yaml
    input:
      # ANTES:
      # pv_power: sensor.emoncms_solar
      # house_power_no_pump: sensor.emoncms_192_168_1_250_use_no_pool_pump
      
      # DEPOIS:
      pv_power: sensor.solar_power_5min_smooth
      house_power_no_pump: sensor.house_power_5min_smooth
      
      # ... resto da configuração igual
```

**Reiniciar automações:**
```bash
curl -X POST http://localhost:8123/api/services/automation/reload
```

---

## 📱 TESTAR NOTIFICAÇÕES

### **Enviar Notificação de Teste**

```yaml
# Ir a: Ferramentas Dev > Serviços
# Serviço: notify.mobile_app_SEU_DEVICE
# Dados:
message: "🧪 Teste: Sistema Piscina Solar"
title: "Teste Notificação"
data:
  actions:
    - action: "TEST_ACTION"
      title: "Testar Ação"
```

**Esperado:** Notificação no telemóvel com botão

---

## 🎨 PERSONALIZAÇÃO DO DASHBOARD

### **Trocar Cores**

Procurar no ficheiro `piscina_solar_dashboard.yaml`:
```yaml
color: '#4CAF50'  # Verde
color: '#FF9800'  # Laranja
color: '#2196F3'  # Azul
color: '#F44336'  # Vermelho
```

### **Adicionar Mais Cartões**

Exemplo - Adicionar temperatura água:
```yaml
- type: custom:mushroom-entity-card
  entity: sensor.temperatura_piscina_filtrado
  name: Temperatura
  icon: mdi:thermometer-water
  icon_color: blue
```

### **Ajustar Layout Mobile**

Procurar:
```yaml
mediaquery:
  "(max-width: 800px)":
    grid-template-columns: 100%  # Coluna única em mobile
```

Mudar `800px` para outro valor se necessário.

---

## 🐛 TROUBLESHOOTING

### **Problema: Sensores `unknown`**

**Causa:** Sensores base não existem ou nomes diferentes

**Solução:**
```bash
# Listar sensores emoncms
cd /data/homeassistant
grep "sensor.emoncms" .storage/core.entity_registry | cut -d'"' -f4 | sort

# Editar solar_smoothed.yaml com nomes corretos
nano sensors/solar_smoothed.yaml
```

### **Problema: Dashboard em branco**

**Causa:** Falta integração HACS

**Solução:**
1. HACS > Frontend
2. Procurar: `mushroom`, `apexcharts-card`, etc.
3. Instalar todas as listadas
4. **IMPORTANTE:** Limpar cache browser (Ctrl+Shift+R)

### **Problema: Notificações não chegam**

**Causa:** Nome do dispositivo incorreto

**Solução:**
```bash
# Encontrar dispositivos mobile
cd /data/homeassistant
cat .storage/core.device_registry | grep mobile_app | grep -o '"name":"[^"]*"'

# Editar automations/piscina_solar_notifications.yaml
# Trocar notify.mobile_app_XXX
```

### **Problema: Input_number não aparece**

**Causa:** Packages não carregado

**Solução:**
```yaml
# Adicionar a configuration.yaml:
homeassistant:
  packages: !include_dir_named packages/

# Reiniciar HA
```

---

## 📊 MONITORIZAÇÃO PÓS-INSTALAÇÃO

### **Primeiras 24h - Verificar:**

✅ **Sensores suavizados** atualizam a cada 5min
✅ **Indicador estabilidade** varia entre 0-50%
✅ **Fator dia semana** muda sábado/domingo
✅ **Notificações** chegam quando esperado

### **Primeiros 7 dias - Analisar:**

📈 **Gráfico** mostra diferença instant vs smooth
📉 **Oscilações** reduziram 30-50%
💰 **Poupança** visível no card económico
🎯 **Filtragem** completa mais consistentemente

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ **Semana 1:** Ajustar fator fim-de-semana baseado em dados reais
2. 📊 **Semana 2:** Analisar gráfico histórico e optimizar
3. 🤖 **Semana 3:** Considerar implementar ML (opção 4 da lista)
4. 🔋 **Mês 2:** Se tiver bateria, implementar coordenação inteligente

---

## 📚 RECURSOS ADICIONAIS

- **Logs Blueprint:** `cat home-assistant.log | grep "🏊"`
- **Debug Sensors:** Ferramentas Dev > Estados > Procurar `piscina`
- **Reload Automations:** `curl -X POST http://localhost:8123/api/services/automation/reload`
- **Reload Templates:** Reiniciar HA

---

## 💬 SUPORTE

**Problema não resolvido?**

1. **Logs:** `tail -100 home-assistant.log | grep -i error`
2. **Check Config:** Configurações > Sistema > Verificar Configuração
3. **Screenshot do erro** + logs
4. **Versão HA:** Configurações > Sistema > Sobre

---

## ✅ CHECKLIST FINAL

- [ ] Todos os sensores em `sensors/` criados
- [ ] `packages/piscina_solar_optimization.yaml` existe
- [ ] Configuration.yaml tem `packages: !include_dir_named packages/`
- [ ] HA reiniciado
- [ ] Sensores suavizados funcionam (não `unknown`)
- [ ] Dashboard criado e visível
- [ ] Integrações HACS instaladas
- [ ] Cache browser limpo (Ctrl+Shift+R)
- [ ] Blueprint atualizado para usar sensores suavizados
- [ ] Notificações configuradas com device correto
- [ ] Teste notificação enviado e recebido
- [ ] Input_number.piscina_weekend_consumption_factor existe
- [ ] Fator fim-de-semana ajustado
- [ ] Entidade weather.home configurada
- [ ] Dashboard funciona em mobile

---

**🎉 Instalação Completa! Boa otimização!**
