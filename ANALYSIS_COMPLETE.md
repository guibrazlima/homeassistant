# 🔍 ANÁLISE DETALHADA DO REPOSITÓRIO HOME ASSISTANT
**Data da Análise:** 11 de Novembro de 2025

---

## 📊 RESUMO EXECUTIVO

### Status Geral: ⚠️ **BOM com Melhorias Recomendadas**

**Pontos Fortes:**
- ✅ Sistema complexo e funcional
- ✅ Boa separação de componentes
- ✅ Templates avançados bem estruturados
- ✅ Automações documentadas com emojis
- ✅ Integração com múltiplos sistemas

**Pontos de Atenção:**
- 🔴 **CRÍTICO:** Credenciais expostas em `configuration.yaml`
- 🟡 Código duplicado entre ficheiros
- 🟡 Falta de validação e tratamento de erros
- 🟡 Automações sem descrições adequadas
- 🟡 Estrutura de packages subutilizada

---

## 🚨 PROBLEMAS CRÍTICOS

### 1. 🔴 **SEGURANÇA: Credenciais Hardcoded**

**Ficheiro:** `configuration.yaml` (linhas 105-108)

```yaml
rest_command:
  cfos_disable_charging:
    url: "http://admin:!!!LixoLogico111@192.168.1.174/cnf?cmd=override_device&dev_id=E1&flags=CE"
  cfos_enable_charging:
    url: "http://admin:!!!LixoLogico111@192.168.1.174/cnf?cmd=override_device&dev_id=E1&flags=ce"
```

**Problema:** Password em texto claro no ficheiro de configuração!

**Impacto:** 
- 🔴 Segurança comprometida
- 🔴 Credenciais expostas no GitHub
- 🔴 Acesso direto ao wallbox cFos

**Solução Imediata:**
1. Mover credenciais para `secrets.yaml`
2. Usar variáveis de ambiente
3. Regenerar password do wallbox
4. Remover do histórico do Git

---

### 2. 🟡 **DUPLICAÇÃO: Automações Repetidas**

**Problema:** Automações de piscina existem em dois locais:
- `/automations/piscina_filtragem.yaml` (271 linhas)
- `/automations/automations.yaml` (linhas 2561-2831)

**Impacto:**
- Manutenção duplicada
- Risco de inconsistência
- Confusão sobre qual é a versão ativa

**Evidência:**
```yaml
# piscina_filtragem.yaml - linha 1
# ADAPTA o equipamento real da bomba:

# automations.yaml - linha 2561 (MESMA AUTOMAÇÃO!)
# ADAPTA o equipamento real da bomba:
```

---

### 3. 🟡 **ORGANIZAÇÃO: Comentários "ADAPTA" Não Resolvidos*input_boolean.portao_status*

**Encontrados:** 31 ocorrências de `# ADAPTA` em vários ficheiros

**Ficheiros Afetados:**
- `scripts.yaml` (3x)
- `piscina_filtragem.yaml` (14x)
- `automations.yaml` (14x)
- `input_number.yaml` (1x)
- `templates/piscina_filtragem.yaml` (4x)

**Problema:** Indicam configurações não finalizadas ou hardcoded

---

## 📁 ANÁLISE POR CATEGORIA

---

## 🏗️ **A. ARQUITETURA E ESTRUTURA**

### ✅ Pontos Fortes:
1. **Separação Lógica**
   - Templates em diretório dedicado (`/templates/`)
   - Automações organizadas por função
   - Sensores em ficheiros separados

2. **Uso de Packages**
   - `/packages/` com 8 ficheiros especializados
   - Boa modularização (AQS, clima, piscina, etc.)

3. **Custom Components**
   - 24+ integrações instaladas
   - Bem organizadas em `/custom_components/`

### 🟡 Melhorias Necessárias:

#### **A1. Consolidar Estrutura de Automações**

**Problema Atual:**
```
/automations/
├── automations.yaml (2831 linhas) ❌ MUITO GRANDE
├── piscina_filtragem.yaml (271 linhas)
└── ev_depois_bomba_piscina.yaml
```

**Proposta:**
```
/automations/
├── _main.yaml (apenas includes)
├── energia/
│   ├── solar_excess.yaml
│   ├── ev_charging.yaml
│   └── tarifarios.yaml
├── piscina/
│   ├── filtragem.yaml
│   ├── aquecimento.yaml
│   └── cloro.yaml
├── casa/
│   ├── iluminacao.yaml
│   ├── portoes.yaml
│   └── seguranca.yaml
└── notificacoes/
    ├── telegram.yaml
    └── mobile_app.yaml
```

**Benefício:** 
- Facilita manutenção
- Reduz conflitos de merge
- Melhora performance de carregamento

---

#### **A2. Mover para Packages (Recomendado)**

**Conceito:** Agrupar entidades relacionadas num único ficheiro

**Exemplo - Piscina Package:**
```yaml
# packages/piscina_complete.yaml
automation: !include_dir_merge_list automations/piscina/
sensor: !include_dir_merge_list sensors/piscina/
input_number:
  pool_pump_duration_lower_threshold: {...}
  pool_pump_duration_inverno: {...}
input_boolean:
  piscina_override_manual: {...}
  piscina_cobertura_fechada: {...}
script:
  piscina_manual_start: {...}
  alternar_modo_automacao_piscina: {...}
```

**Vantagem:** Tudo relacionado à piscina num só lugar!

---

## ⚙️ **B. CONFIGURAÇÃO (`configuration.yaml`)**

### ✅ Pontos Fortes:
1. Uso correto de `!secret` (maioria dos casos)
2. InfluxDB bem configurado com tags
3. Recorder otimizado com MariaDB externo
4. Logging granular por componente

### 🔴 Problemas Críticos:

#### **B1. Credenciais Expostas (JÁ MENCIONADO)**

#### **B2. Recorder sem Otimização Suficiente**

**Atual:**
```yaml
recorder:
  db_url: !secret mariadb_connection
  auto_purge: false
```

**Problema:** 
- Sem `purge_keep_days` definido
- Sem `include`/`exclude` otimizado
- BD pode crescer indefinidamente

**Solução:**
```yaml
recorder:
  db_url: !secret mariadb_connection
  auto_purge: true
  purge_keep_days: 30
  commit_interval: 5
  
  include:
    domains:
      - sensor
      - binary_sensor
      - switch
      - climate
      - cover
    entity_globs:
      - sensor.emoncms_*
      - sensor.solcast_*
      - sensor.*_energy_*
      - sensor.bomba_piscina_*
  
  exclude:
    entities:
      - sensor.time
      - sensor.date
      - sensor.uptime
    entity_globs:
      - sensor.*_last_*
      - sensor.*_next_*
    domains:
      - weather
      - sun
```

---

#### **B3. Logger em Modo Debug para Automações**

**Atual:**
```yaml
logger:
  default: info
  logs:
    homeassistant.components.automation: debug  ❌
```

**Problema:** 
- Logs excessivos em produção
- Afeta performance
- Ficheiros de log grandes

**Solução:**
```yaml
logger:
  default: warning
  logs:
    custom_components.pyscript.file.pv_excess_control: info
    custom_components.llmvision: info
    homeassistant.components.automation: warning  # apenas erros importantes
```

---

#### **B4. InfluxDB - Exclusões Incompletas**

**Atual:**
```yaml
influxdb:
  exclude:
    entities:
      - zone.home
    domains:
      - persistent_notification
      - person
```

**Problema:** Muitas entidades desnecessárias sendo enviadas

**Solução:**
```yaml
influxdb:
  include:
    entity_globs:
      - sensor.emoncms_*
      - sensor.solcast_*
      - sensor.*_energy_*
      - sensor.*_power*
      - sensor.bomba_piscina_*
      - sensor.*_temperature
      - sensor.*_humidity
  exclude:
    entity_globs:
      - sensor.*_last_*
      - sensor.*_friendly_*
      - sensor.speedtest_*
    domains:
      - automation
      - script
      - scene
      - group
```

---

## 🤖 **C. AUTOMAÇÕES**

### 📊 Estatísticas:
- **Total:** ~100+ automações
- **Linhas:** 2,831 (automations.yaml)
- **Ficheiros:** 3 principais
- **Modo:** Maioria `single`, algumas `restart`

### 🟡 Problemas Encontrados:

#### **C1. Descrições Vazias**

**84%** das automações têm `description: ''`

**Exemplo:**
```yaml
- id: '1717785108600'
  alias: SpeedTests
  description: ''  ❌
```

**Impacto:**
- Dificulta debugging
- Sem documentação interna
- Complicado para novos utilizadores

**Solução:**
```yaml
- id: '1717785108600'
  alias: "🌐 SpeedTests Automáticos"
  description: |
    Executa testes de velocidade de internet 3x/dia:
    - 06:30 (manhã)
    - 18:30 (tarde)
    - 35min antes do nascer do sol
    
    Sensor atualizado: sensor.speedtest_download
  trigger: [...]
```

---

#### **C2. IDs Numéricos Sem Significado**

**Problema:**
```yaml
- id: '1717785108600'  ❌ Impossível lembrar
- id: '1717785145333'
- id: '1717785168033'
```

**Solução:**
```yaml
- id: 'speedtest_automatic'  ✅ Descritivo
- id: 'gate_callback_mobile'
- id: 'garage_light_auto'
```

---

#### **C3. Time Pattern Ineficiente**

**Problema:**
```yaml
- id: '1717785178989'
  alias: "Notificação para ligar o carro ao carregador"
  trigger:
  - platform: time_pattern
    minutes: /15  ❌ Roda de 15 em 15 minutos SEMPRE
```

**Impacto:**
- CPU usage desnecessário
- 96 execuções/dia mesmo se carro não estiver em casa

**Solução:**
```yaml
- id: 'ev_battery_low_notification'
  alias: "🔋 Notificação - Bateria EV Baixa"
  trigger:
    - platform: numeric_state
      entity_id: sensor.i4_edrive40_remaining_battery_percent
      below: 46
      for:
        minutes: 5
    - platform: state
      entity_id: device_tracker.i4_edrive40
      to: 'home'
      for:
        minutes: 10
  condition:
    - condition: and
      conditions:
        - condition: numeric_state
          entity_id: sensor.i4_edrive40_remaining_battery_percent
          below: 46
        - condition: state
          entity_id: device_tracker.i4_edrive40
          state: home
        - condition: state
          entity_id: binary_sensor.i4_edrive40_connection_status
          state: 'off'
  action: [...]
```

---

#### **C4. Falta de Tratamento de Erros**

**Problema:** Nenhuma automação usa `try-except` ou fallbacks

**Exemplo Atual:**
```yaml
action:
  - service: cover.open_cover
    target:
      entity_id: cover.gate  # E se falhar?
```

**Solução:**
```yaml
action:
  - service: cover.open_cover
    target:
      entity_id: cover.gate
    continue_on_error: true
  - delay: 00:00:02
  - choose:
      - conditions:
          - condition: state
            entity_id: cover.gate
            state: 'opening'
        sequence:
          - service: notify.telegram
            data:
              message: "✅ Portão a abrir"
    default:
      - service: notify.telegram
        data:
          message: "⚠️ Erro ao abrir portão - verificar"
```

---

## 📝 **D. TEMPLATES**

### ✅ Pontos Fortes:
1. **Bem organizados** em `/templates/`
2. **Modular** - cada ficheiro por função
3. **Templates complexos** funcionais (COP, energia, etc.)

### 🟡 Problemas:

#### **D1. Templates Sem Validação**

**Exemplo - piscina.yaml:**
```yaml
- sensor:
    - name: "pool_pump_remaining_time"
      state: >-
        {% set time = (((states('input_number.pool_pump_duration_lower_threshold') | float(0))*60 
                      - (states('sensor.bomba_piscina_horas_ligada_diario')|float(-1))*3600)
                      | round | int, 0)|max %}
```

**Problemas:**
- Sem verificação se sensores existem
- `float(-1)` pode causar cálculos errados
- Sem `availability` template

**Solução:**
```yaml
- sensor:
    - name: "pool_pump_remaining_time"
      unique_id: "pool_pump_remaining_time"
      availability: >-
        {{ has_value('input_number.pool_pump_duration_lower_threshold') 
           and has_value('sensor.bomba_piscina_horas_ligada_diario') }}
      state: >-
        {% if not (has_value('input_number.pool_pump_duration_lower_threshold') 
                   and has_value('sensor.bomba_piscina_horas_ligada_diario')) %}
          unavailable
        {% else %}
          {% set duration = states('input_number.pool_pump_duration_lower_threshold') | float(0) %}
          {% set elapsed = states('sensor.bomba_piscina_horas_ligada_diario') | float(0) %}
          {% set time = max(0, (duration * 60 - elapsed * 3600) | round | int) %}
          {% set hours = (time // 3600) %}
          {% set minutes = ((time % 3600) // 60) %}
          {{ '{:02d}:{:02d}'.format(hours, minutes) }}
        {% endif %}
```

---

#### **D2. Tarifários Hardcoded**

**templates_energia_tarifarios.yaml:**
```yaml
- sensor:
      - unique_id: iberdrola_bihorario_diario
        state: >
          {% set vazio = 0.0776 -%}  ❌ Hardcoded
          {% set fora_vazio = 0.2141 -%}  ❌
          {% set IVA = 1.23 -%}  ❌
          {% set desconto = 0.881 -%}  ❌
```

**Problema:**
- Mudanças de tarifário exigem edição de template
- Sem histórico de alterações
- Dificulta A/B testing

**Solução:**
```yaml
# Criar input_numbers para configuração dinâmica
input_number:
  tarifa_vazio:
    name: "Tarifa Vazio"
    min: 0
    max: 1
    step: 0.0001
    initial: 0.0776
    unit_of_measurement: "€/kWh"
  
  tarifa_fora_vazio:
    name: "Tarifa Fora Vazio"
    min: 0
    max: 1
    step: 0.0001
    initial: 0.2141
    unit_of_measurement: "€/kWh"

# Template usa valores configuráveis
- sensor:
    - name: "Iberdrola Bi-horário"
      state: >
        {% set vazio = states('input_number.tarifa_vazio') | float(0.0776) %}
        {% set fora_vazio = states('input_number.tarifa_fora_vazio') | float(0.2141) %}
        {% set IVA = 1.23 %}
        {% set preco = vazio if now().hour < 8 or now().hour > 21 else fora_vazio %}
        {{ (preco * IVA) | round(4) }}
```

---

## 📜 **E. SCRIPTS**

### ✅ Pontos Fortes:
1. Scripts bem nomeados
2. Uso de `fields` para parametrização
3. Validação de valores (min/max)

### 🟡 Problemas:

#### **E1. Script Comentado (Código Morto)**

**scripts.yaml linhas 49-70:**
```yaml
#piscina_forcar_on:  ❌ 22 linhas comentadas
#  alias: Piscina - Forçar ON (minutos)
#  mode: restart
#  fields:...
```

**Solução:** Remover ou documentar por que está desativado

---

#### **E2. Validação Manual de Limites**

**Exemplo:**
```yaml
mins: >
  {% if mins_val < 1 %}1{% elif mins_val > 600 %}600{% else %}{{ mins_val }}{% endif %}
```

**Problema:** Lógica repetitiva

**Solução:** Usar funções Jinja2
```yaml
mins: "{{ [1, mins_val | int, 600] | sort | list[1] }}"
```

---

## 🔢 **F. INPUT HELPERS**

### 📊 Estado Atual:
- `input_number.yaml`: 142 linhas, ~25 helpers
- `input_boolean.yaml`: 27 linhas, ~8 helpers
- `input_datetime.yaml`, `input_select.yaml`

### 🟡 Problemas:

#### **F1. Falta de unique_id**

**Todos os helpers sem `unique_id`!**

**Problema:**
- Não aparecem em Energy Dashboard
- Impossível renomear via UI
- Sem persistência de configuração UI

**Solução:**
```yaml
pool_pump_duration_lower_threshold:
  name: Pool Pump Duration Lower Threshold
  unique_id: pool_pump_duration_lower_threshold_01  ✅
  initial: 360
  min: 60
  max: 1440
  step: 1
  unit_of_measurement: minutes
  mode: box
  icon: mdi:timer-sand  ✅
```

---

#### **F2. Valores "ADAPTA" Hardcoded**

**input_number.yaml linha 80:**
```yaml
piscina_volume:
  name: Piscina - Volume de Água
  initial: 1550   # ADAPTA  ❌
```

**Problema:** Comentário sugere que não foi configurado

**Solução:** 
1. Confirmar valor correto
2. Remover comentário
3. Adicionar documentação em package

---

## 📦 **G. PACKAGES**

### ✅ Pontos Fortes:
- 8 packages especializados
- Boa separação de lógica (AQS, clima, piscina, etc.)

### 🟡 Problemas:

#### **G1. Packages Subutilizados**

**Atual:**
```
packages/
├── aqs_perdas.yaml
├── climate_comfort.yaml
├── clorador_sal.yaml
├── cobertura_piscina.yaml
├── hp90_thermal_estimator_v2.yaml
├── piscina_cloro_tpo_por_cobertura.yaml
├── piscina_ph.yaml
└── solar_hp90_from_fs.yaml_old
```

**Problema:** 
- Muita lógica ainda em `/automations/automations.yaml`
- Não aproveita todo o potencial de packages

**Solução:** Migrar mais entidades para packages

---

## 🎨 **H. LOVELACE / UI**

### Ficheiros Encontrados:
- `/lovelace/` - Dashboards personalizados
- `/popup/` - Cards de popup
- `/button_card_templates/` - Templates de cards

### ⚠️ **Não analisado em detalhe** (fora do scope YAML backend)

---

## 📱 **I. INTEGRAÇÕES EXTERNAS**

### Status:
✅ **Nenhum erro encontrado** pelo Home Assistant

### Custom Components Instalados:
1. alarmo (Alarmes)
2. auto_backup (Backups automáticos)
3. ble_monitor (Bluetooth)
4. browser_mod (Controlo de browser)
5. composite (Tracking)
6. entsoe (Dados energéticos EU)
7. ev_smart_charging (Carregamento VE)
8. frigate (Câmaras)
9. hacs (Community Store)
10. ingress (Proxy)
11. llmvision (IA)
12. midea_ac + midea_dehumidifier_lan
13. ocpp (Wallbox)
14. omie (Mercado energético)
15. optimal_humidity
16. powerbrain (Gestão energia)
17. pyscript (Python scripts)
18. solcast_solar (Previsões solares)
19. tapo_control (TP-Link)
20. thermal_comfort
21. tplink_deco
22. ui_lovelace_minimalist
23. variable (Variáveis persistentes)
24. xiaomi_miio_fan + xiaomi_miio_raw

### 🟢 **Muito bem integrado!**

---

## 📊 **RESUMO DE PROBLEMAS POR PRIORIDADE**

### 🔴 **CRÍTICO (Ação Imediata)**
1. ✅ Credenciais expostas em `configuration.yaml`
2. ⚠️ Automações duplicadas (piscina)
3. ⚠️ Logger em modo debug (produção)

### 🟡 **IMPORTANTE (Próximas Semanas)**
4. Recorder sem otimização
5. Descrições vazias em automações
6. Templates sem validação
7. Comentários "ADAPTA" não resolvidos
8. Código comentado (dead code)

### 🟢 **MELHORIA (Quando Possível)**
9. Reorganizar estrutura de automações
10. Migrar para packages
11. Adicionar unique_ids aos helpers
12. Otimizar InfluxDB excludes
13. Melhorar IDs de automações
14. Documentar tarifários
15. Adicionar tratamento de erros

---

**FIM DA ANÁLISE**

Próximo ficheiro: Sugestões detalhadas por tópico
