# 🎯 MELHORIAS SUGERIDAS POR TÓPICO
**Para escolher o que implementar**

---

## 📋 ÍNDICE DE TÓPICOS

1. [🔒 Segurança](#-1-segurança)
2. [⚡ Performance e Otimização](#-2-performance-e-otimização)
3. [🏗️ Arquitetura e Organização](#️-3-arquitetura-e-organização)
4. [🤖 Automações](#-4-automações)
5. [📝 Templates](#-5-templates)
6. [📜 Scripts](#-6-scripts)
7. [🔢 Input Helpers](#-7-input-helpers)
8. [📊 Monitorização](#-8-monitorização)
9. [📚 Documentação](#-9-documentação)
10. [🧹 Limpeza de Código](#-10-limpeza-de-código)

---

## 🔒 **1. SEGURANÇA**

### 🔴 **CRÍTICO - S1: Remover Credenciais Expostas**

**Problema:** Password do wallbox cFos em texto claro

**Ficheiro:** `configuration.yaml` linhas 105-108

**Impacto:** 🔴 CRÍTICO
- Acesso não autorizado ao wallbox
- Credenciais no GitHub público
- Violação de segurança

**Solução:**

```yaml
# configuration.yaml
rest_command:
  cfos_disable_charging:
    url: !secret cfos_disable_url
  cfos_enable_charging:
    url: !secret cfos_enable_url

# secrets.yaml (adicionar)
cfos_disable_url: "http://admin:!!!LixoLogico111@192.168.1.174/cnf?cmd=override_device&dev_id=E1&flags=CE"
cfos_enable_url: "http://admin:!!!LixoLogico111@192.168.1.174/cnf?cmd=override_device&dev_id=E1&flags=ce"
```

**Passos:**
1. ✅ Adicionar URLs ao `secrets.yaml`
2. ✅ Atualizar `configuration.yaml`
3. ✅ Validar configuração (`ha core check`)
4. ✅ Reiniciar HA
5. ✅ Testar wallbox
6. ✅ **Regenerar password do wallbox**
7. ✅ Remover do histórico Git (se necessário)

**Esforço:** ⏱️ 15 minutos  
**Benefício:** 🎯 Máximo  
**Prioridade:** 🔴 **URGENTE**

---

### 🟡 S2: Auditar Exposição de IPs e Dados Pessoais

**Problema:** IPs privados podem estar expostos

**Ficheiros a verificar:**
- `configuration.yaml` (192.168.1.0/24, 192.168.1.174)
- Templates com coordenadas GPS
- Logs com informação pessoal

**Solução:**
- Criar variável para rede interna
- Usar `!secret` para IPs de dispositivos
- Verificar logs antes de partilhar

**Esforço:** ⏱️ 30 minutos  
**Benefício:** 🎯 Alto  
**Prioridade:** 🟡 Importante

---

### 🟢 S3: Implementar Autenticação de 2 Fatores

**Objetivo:** Adicionar camada extra de segurança

**Passos:**
1. Ativar 2FA para utilizadores
2. Configurar trusted networks
3. Implementar notificações de login

**Esforço:** ⏱️ 1 hora  
**Benefício:** 🎯 Alto  
**Prioridade:** 🟢 Recomendado

---

## ⚡ **2. PERFORMANCE E OTIMIZAÇÃO**

### 🟡 **P1: Otimizar Recorder (Base de Dados)**

**Problema:** BD pode crescer indefinidamente, sem purge automático

**Configuração Atual:**
```yaml
recorder:
  db_url: !secret mariadb_connection
  auto_purge: false  ❌
```

**Solução Proposta:**

```yaml
recorder:
  db_url: !secret mariadb_connection
  auto_purge: true  ✅
  purge_keep_days: 30  # Manter 30 dias
  commit_interval: 5
  
  # Incluir apenas o essencial
  include:
    domains:
      - sensor
      - binary_sensor
      - switch
      - climate
      - cover
      - light
    entity_globs:
      # Energia
      - sensor.emoncms_*
      - sensor.solcast_*
      - sensor.*_energy_*
      - sensor.*_power*
      # Piscina
      - sensor.bomba_piscina_*
      - sensor.pool_*
      - sensor.piscina_*
      # Casa
      - sensor.*_temperature
      - sensor.*_humidity
      - binary_sensor.*_motion
      # Carros
      - sensor.i4_*
      - sensor.x1_*
  
  exclude:
    entities:
      # Sensores temporais
      - sensor.time
      - sensor.date
      - sensor.uptime
    entity_globs:
      # Atributos desnecessários
      - sensor.*_last_*
      - sensor.*_next_*
      - sensor.*_friendly_*
      # SpeedTest (mantém só o último)
      - sensor.speedtest_*
    domains:
      # Não gravar
      - weather
      - sun
      - updater
      - person
```

**Benefícios:**
- ✅ BD mantém tamanho controlado
- ✅ Queries mais rápidas
- ✅ Backups menores
- ✅ Melhor performance geral

**Impacto estimado:**
- Redução de ~60-70% no tamanho da BD
- Queries 2-3x mais rápidas
- Backups 50% menores

**Esforço:** ⏱️ 30 minutos  
**Benefício:** 🎯 Muito Alto  
**Prioridade:** 🟡 **Importante**

---

### 🟡 **P2: Reduzir Logging em Produção**

**Problema:** Logs demasiado verbosos afetam performance

**Atual:**
```yaml
logger:
  default: info
  logs:
    homeassistant.components.automation: debug  ❌ Demasiado verbose
```

**Solução:**
```yaml
logger:
  default: warning  # Apenas avisos e erros
  logs:
    # Apenas info para componentes críticos
    custom_components.pyscript.file.pv_excess_control: info
    custom_components.llmvision: warning
    custom_components.solcast_solar: info
    custom_components.omie: info
    
    # Debug apenas quando necessário
    # homeassistant.components.automation: debug  # Descomentar para debug
```

**Benefícios:**
- ✅ Ficheiros de log 80% menores
- ✅ Melhor performance I/O
- ✅ Mais fácil encontrar erros reais

**Esforço:** ⏱️ 5 minutos  
**Benefício:** 🎯 Médio  
**Prioridade:** 🟡 Recomendado

---

### 🟡 **P3: Otimizar InfluxDB**

**Problema:** Dados desnecessários sendo enviados para InfluxDB

**Solução:**
```yaml
influxdb:
  api_version: 2
  ssl: false
  host: influxdb
  port: 8086
  token: !secret influxdb_token
  organization: gl
  bucket: homeassistant
  
  tags:
    source: HomeAssistant
    installation: production  ✅
    location: home  ✅
  
  tags_attributes:
    - friendly_name
    - device_class
    - unit_of_measurement  ✅
  
  default_measurement: units
  
  ignore_attributes:
    - icon
    - entity_picture
    - supported_features  ✅
  
  # USAR INCLUDE em vez de EXCLUDE
  include:
    entity_globs:
      # Energia - crítico
      - sensor.emoncms_*
      - sensor.solcast_*
      - sensor.*_energy_*
      - sensor.*_power*
      - sensor.*_cost*
      - sensor.electricity_spend
      
      # Piscina
      - sensor.bomba_piscina_*
      - sensor.pool_*
      - sensor.piscina_*
      
      # Clima e Conforto
      - sensor.*_temperature
      - sensor.*_humidity
      - sensor.*_thermal_*
      - sensor.*_dew_point
      
      # Bomba de Calor
      - sensor.hpsu_*
      
      # Carros
      - sensor.i4_*
      - sensor.x1_*
      
  exclude:
    entity_globs:
      - sensor.*_last_*
      - sensor.*_friendly_*
      - sensor.speedtest_*
      - sensor.time*
      - sensor.date*
    domains:
      - automation
      - script
      - scene
      - group
      - zone
      - person
      - weather
      - sun
```

**Benefícios:**
- ✅ Queries InfluxDB mais rápidas
- ✅ Armazenamento reduzido
- ✅ Dashboards Grafana mais responsivos

**Esforço:** ⏱️ 45 minutos  
**Benefício:** 🎯 Alto  
**Prioridade:** 🟡 Recomendado

---

### 🟢 **P4: Otimizar Time Patterns**

**Problema:** Automações com `time_pattern` executam constantemente

**Exemplo Problemático:**
```yaml
- alias: "Notificação para ligar o carro ao carregador"
  trigger:
  - platform: time_pattern
    minutes: /15  ❌ 96x por dia!
```

**Solução:**
```yaml
- alias: "🔋 Notificação - Bateria EV Baixa"
  trigger:
    # Trigger quando bateria baixa
    - platform: numeric_state
      entity_id: sensor.i4_edrive40_remaining_battery_percent
      below: 46
      for:
        minutes: 5
    # OU quando carro chega a casa
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
```

**Benefícios:**
- ✅ Reduz execuções de 96x/dia para ~2-3x/dia
- ✅ Menos carga no CPU
- ✅ Mais eficiente

**Esforço:** ⏱️ 20 minutos  
**Benefício:** 🎯 Médio  
**Prioridade:** 🟢 Recomendado

---

## 🏗️ **3. ARQUITETURA E ORGANIZAÇÃO**

### 🟡 **A1: Reorganizar Automações em Diretórios**

**Problema:** 2,831 linhas num único ficheiro

**Estrutura Atual:**
```
/automations/
├── automations.yaml (2831 linhas) ❌
├── piscina_filtragem.yaml
└── ev_depois_bomba_piscina.yaml
```

**Estrutura Proposta:**
```
/automations/
├── _automation.yaml (apenas !include_dir_merge_list)
├── energia/
│   ├── solar_excess.yaml
│   ├── ev_charging.yaml
│   ├── precos_energia.yaml
│   └── monitorizacao.yaml
├── piscina/
│   ├── filtragem_auto.yaml
│   ├── filtragem_manual.yaml
│   ├── aquecimento.yaml
│   └── quimica.yaml
├── casa/
│   ├── iluminacao.yaml
│   ├── portoes.yaml
│   ├── seguranca.yaml
│   └── clima.yaml
├── notificacoes/
│   ├── telegram.yaml
│   ├── mobile_app.yaml
│   └── alertas.yaml
└── sistema/
    ├── speedtest.yaml
    ├── backups.yaml
    └── manutencao.yaml
```

**Configuração:**
```yaml
# configuration.yaml
automation: !include_dir_merge_list automations/
```

**Benefícios:**
- ✅ Manutenção muito mais fácil
- ✅ Menos conflitos de merge
- ✅ Carregamento mais rápido
- ✅ Melhor organização mental

**Esforço:** ⏱️ 3-4 horas (uma única vez)  
**Benefício:** 🎯 Muito Alto  
**Prioridade:** 🟡 **Altamente Recomendado**

---

### 🟡 **A2: Consolidar com Packages**

**Objetivo:** Agrupar entidades relacionadas

**Exemplo - Package Piscina Completo:**

```yaml
# packages/piscina_sistema_completo.yaml

# Automações
automation: !include_dir_merge_list ../automations/piscina/

# Sensores
sensor:
  - platform: template
    sensors:
      pool_pump_remaining_time:
        [...]

# Scripts
script:
  piscina_manual_start:
    [...]
  alternar_modo_automacao_piscina:
    [...]

# Input Numbers
input_number:
  pool_pump_duration_lower_threshold:
    name: Pool Pump Duration Lower Threshold
    initial: 360
    min: 60
    max: 1440
    step: 1
    unit_of_measurement: minutes
  
  pool_pump_duration_inverno:
    [...]

# Input Booleans
input_boolean:
  piscina_override_manual:
    name: Piscina — Modo Manual
    icon: mdi:hand
  
  piscina_cobertura_fechada:
    name: Piscina — Cobertura fechada
    icon: mdi:shield-sun

# Timer
timer:
  piscina_manual:
    name: Piscina — Temporizador manual
    duration: "00:00:00"

# History Stats
sensor:
  - platform: history_stats
    name: Bomba Piscina Horas Ligada Diário
    entity_id: switch.bomba_piscina_switch_0
    state: "on"
    type: time
    start: "{{ now().replace(hour=0, minute=0, second=0) }}"
    end: "{{ now() }}"
```

**Vantagem:** Tudo relacionado à piscina num único lugar!

**Esforço:** ⏱️ 2-3 horas por package  
**Benefício:** 🎯 Alto  
**Prioridade:** 🟡 Recomendado

---

### 🟢 **A3: Eliminar Duplicação (Piscina)**

**Problema:** Automações de piscina duplicadas

**Ficheiros:**
- `/automations/piscina_filtragem.yaml` (271 linhas)
- `/automations/automations.yaml` (linhas 2561-2831) ← MESMAS AUTOMAÇÕES

**Solução:**
1. Confirmar qual versão está ativa
2. Remover a duplicada
3. Manter apenas em `/automations/piscina/`

**Esforço:** ⏱️ 30 minutos  
**Benefício:** 🎯 Médio  
**Prioridade:** 🟡 Importante

---

## 🤖 **4. AUTOMAÇÕES**

### 🟡 **AU1: Adicionar Descrições às Automações**

**Problema:** 84% das automações têm `description: ''`

**Template de Descrição:**
```yaml
- id: 'automation_id_descritivo'
  alias: "📊 Nome Descritivo da Automação"
  description: |
    [Propósito]
    O que esta automação faz em 1-2 linhas.
    
    [Triggers]
    - Quando X acontece
    - Ou quando Y muda para Z
    
    [Actions]
    - Faz A
    - Depois B
    - Notifica se falhar
    
    [Notas]
    - Depende de: sensor.xyz
    - Relacionado com: automation.abc
  trigger: [...]
```

**Exemplo Completo:**
```yaml
- id: 'garage_light_auto'
  alias: "💡 Garagem - Luz Automática ao Abrir Portão"
  description: |
    [Propósito]
    Liga automaticamente a luz da garagem quando o portão abre/fecha,
    mas apenas à noite. Desliga após 5 minutos.
    
    [Triggers]
    - Portão muda de closed para open (após 2s)
    - Portão muda de open para closed (após 2s)
    
    [Conditions]
    - Sol abaixo do horizonte (noite)
    
    [Actions]
    - Se portão abriu: liga luz
    - Se portão fechou há 5min: desliga luz
    
    [Sensores]
    - cover.gate (Portão principal)
    - light.exterior (Luz garagem)
    - sun.sun (Posição solar)
  trigger: [...]
```

**Esforço:** ⏱️ 5 min por automação × ~100 = 8 horas total  
**Benefício:** 🎯 Alto (documentação)  
**Prioridade:** 🟡 Recomendado

---

### 🟡 **AU2: Usar IDs Descritivos**

**Problema:** IDs numéricos impossíveis de lembrar

**Antes:**
```yaml
- id: '1717785108600'  ❌
- id: '1717785145333'  ❌
- id: '1717785168033'  ❌
```

**Depois:**
```yaml
- id: 'speedtest_automatic'  ✅
- id: 'gate_callback_mobile'  ✅
- id: 'garage_light_auto'  ✅
- id: 'pool_filtration_night_start'  ✅
- id: 'ev_battery_low_notification'  ✅
```

**Convenção Sugerida:**
- `{componente}_{acao}_{condicao}`
- Usar underscores
- Máximo 40 caracteres
- Inglês para consistência

**Esforço:** ⏱️ 2 min por automação × ~100 = 3-4 horas  
**Benefício:** 🎯 Médio  
**Prioridade:** 🟢 Recomendado

---

### 🟢 **AU3: Adicionar Tratamento de Erros**

**Objetivo:** Automações mais robustas

**Exemplo:**
```yaml
- id: 'gate_open_safe'
  alias: "🚪 Portão - Abrir com Validação"
  trigger: [...]
  action:
    # Tentar abrir
    - service: cover.open_cover
      target:
        entity_id: cover.gate
      continue_on_error: true
    
    # Aguardar
    - delay: 00:00:03
    
    # Validar se abriu
    - choose:
        # Sucesso
        - conditions:
            - condition: or
              conditions:
                - condition: state
                  entity_id: cover.gate
                  state: 'opening'
                - condition: state
                  entity_id: cover.gate
                  state: 'open'
          sequence:
            - service: notify.telegram
              data:
                message: "✅ Portão a abrir"
      
      # Falha
      default:
        - service: notify.telegram
          data:
            message: |
              ⚠️ ERRO: Portão não respondeu!
              
              Estado atual: {{ states('cover.gate') }}
              Verificar manualmente.
            data:
              inline_keyboard:
                - "Tentar Novamente:/gate_retry"
                - "Ignorar:/gate_ignore"
```

**Benefícios:**
- ✅ Sistema mais robusto
- ✅ Notificação de problemas
- ✅ Possibilidade de retry

**Esforço:** ⏱️ 15 min por automação crítica  
**Benefício:** 🎯 Alto  
**Prioridade:** 🟢 Recomendado para automações críticas

---

### 🟢 **AU4: Adicionar Mode Adequado**

**Objetivo:** Controlar execução concorrente

**Modes Disponíveis:**
- `single`: Ignora novo trigger se já está a executar (default)
- `restart`: Cancela execução anterior e inicia nova
- `queued`: Coloca em fila e executa sequencialmente
- `parallel`: Executa múltiplas instâncias em paralelo

**Quando usar cada um:**

```yaml
# SINGLE - Maioria dos casos
- id: 'speedtest_auto'
  mode: single  # Não executar se já está a fazer speedtest

# RESTART - Quando nova informação invalida a anterior
- id: 'gate_light_auto'
  mode: restart  # Se portão abrir novamente, reiniciar timer

# QUEUED - Quando ordem importa
- id: 'backup_sequence'
  mode: queued
  max: 3  # Máximo 3 na fila

# PARALLEL - Notificações independentes
- id: 'notification_dispatch'
  mode: parallel
  max: 10
```

**Esforço:** ⏱️ 2 min por automação  
**Benefício:** 🎯 Médio  
**Prioridade:** 🟢 Recomendado

---

## 📝 **5. TEMPLATES**

### 🟡 **T1: Adicionar Validação e Availability**

**Problema:** Templates sem verificação de sensores

**Antes:**
```yaml
- sensor:
    - name: "pool_pump_remaining_time"
      state: >-
        {% set time = ((states('input_number.xxx') | float(0))*60 
                      - (states('sensor.yyy')|float(-1))*3600) %}
        ...
```

**Depois:**
```yaml
- sensor:
    - name: "pool_pump_remaining_time"
      unique_id: "pool_pump_remaining_time"
      availability: >-
        {{ has_value('input_number.pool_pump_duration_lower_threshold') 
           and has_value('sensor.bomba_piscina_horas_ligada_diario') 
           and states('input_number.pool_pump_duration_lower_threshold') | float(0) > 0 }}
      state: >-
        {% if not this.available %}
          unavailable
        {% else %}
          {% set duration = states('input_number.pool_pump_duration_lower_threshold') | float(0) %}
          {% set elapsed = states('sensor.bomba_piscina_horas_ligada_diario') | float(0) %}
          {% set remaining_seconds = max(0, (duration * 60 - elapsed * 3600) | round | int) %}
          
          {% set hours = (remaining_seconds // 3600) %}
          {% set minutes = ((remaining_seconds % 3600) // 60) %}
          
          {{ '{:02d}:{:02d}'.format(hours, minutes) }}
        {% endif %}
```

**Benefícios:**
- ✅ Sensor mostra 'unavailable' quando dados inválidos
- ✅ Evita cálculos com valores errados
- ✅ Melhor debugging

**Esforço:** ⏱️ 10 min por template  
**Benefício:** 🎯 Alto  
**Prioridade:** 🟡 Importante

---

### 🟡 **T2: Tornar Tarifários Configuráveis**

**Problema:** Preços hardcoded em templates

**Solução:**

```yaml
# 1. Criar input_numbers
input_number:
  tarifa_vazio:
    name: "Tarifa Vazio (€/kWh)"
    min: 0
    max: 1
    step: 0.0001
    initial: 0.0776
    mode: box
    icon: mdi:currency-eur
  
  tarifa_fora_vazio:
    name: "Tarifa Fora Vazio (€/kWh)"
    min: 0
    max: 1
    step: 0.0001
    initial: 0.2141
    mode: box
    icon: mdi:currency-eur
  
  tarifa_iva:
    name: "IVA (%)"
    min: 0
    max: 50
    step: 0.1
    initial: 23
    mode: box
  
  tarifa_iec:
    name: "IEC (€/kWh)"
    min: 0
    max: 0.01
    step: 0.0001
    initial: 0.001
    mode: box
  
  tarifa_desconto:
    name: "Desconto (%)"
    min: 0
    max: 100
    step: 0.1
    initial: 11.9
    mode: box

# 2. Template usa valores configuráveis
- sensor:
    - unique_id: iberdrola_bihorario_diario_v2
      name: "Iberdrola Bi-horário (Configurável)"
      unit_of_measurement: '€/kWh'
      state_class: total
      device_class: monetary
      state: >
        {% set vazio = states('input_number.tarifa_vazio') | float(0.0776) %}
        {% set fora_vazio = states('input_number.tarifa_fora_vazio') | float(0.2141) %}
        {% set iva_pct = states('input_number.tarifa_iva') | float(23) %}
        {% set iva = 1 + (iva_pct / 100) %}
        {% set iec = states('input_number.tarifa_iec') | float(0.001) %}
        {% set desconto_pct = states('input_number.tarifa_desconto') | float(11.9) %}
        {% set desconto = 1 - (desconto_pct / 100) %}
        
        {% set preco_base = vazio if now().hour < 8 or now().hour > 21 else fora_vazio %}
        {% set preco_final = ((preco_base * desconto) + iec) * iva %}
        
        {{ preco_final | round(4) }}
      attributes:
        config:
          vazio: "{{ states('input_number.tarifa_vazio') }}"
          fora_vazio: "{{ states('input_number.tarifa_fora_vazio') }}"
          iva: "{{ states('input_number.tarifa_iva') }}%"
          desconto: "{{ states('input_number.tarifa_desconto') }}%"
```

**Vantagens:**
- ✅ Alterar tarifários via UI
- ✅ Sem editar YAML
- ✅ Histórico de alterações
- ✅ A/B testing de fornecedores

**Esforço:** ⏱️ 1 hora  
**Benefício:** 🎯 Muito Alto  
**Prioridade:** 🟡 **Altamente Recomendado**

---

### 🟢 **T3: Adicionar unique_id a Todos os Templates**

**Objetivo:** Permitir configuração via UI

**Antes:**
```yaml
- sensor:
    - name: "Sensor Qualquer"  ❌ Sem unique_id
      state: "{{ ... }}"
```

**Depois:**
```yaml
- sensor:
    - name: "Sensor Qualquer"
      unique_id: "sensor_qualquer_01"  ✅
      state: "{{ ... }}"
```

**Benefícios:**
- ✅ Pode renomear via UI
- ✅ Personalizável
- ✅ Aparece em Energy Dashboard

**Esforço:** ⏱️ 1 min por sensor  
**Benefício:** 🎯 Médio  
**Prioridade:** 🟢 Recomendado

---

## 📜 **6. SCRIPTS**

### 🟢 **SC1: Remover Código Comentado**

**Problema:** 22 linhas de script comentado

**Ficheiro:** `scripts.yaml` linhas 49-70

```yaml
#piscina_forcar_on:  ❌ Dead code
#  alias: Piscina - Forçar ON (minutos)
#  mode: restart
#  [...]  22 linhas
```

**Soluções:**
1. **Se ainda é útil:** Mover para documentação
2. **Se obsoleto:** Remover completamente
3. **Se incerto:** Criar backup e remover

**Esforço:** ⏱️ 5 minutos  
**Benefício:** 🎯 Baixo (limpeza)  
**Prioridade:** 🟢 Opcional

---

### 🟢 **SC2: Simplificar Validações com Jinja2**

**Antes:**
```yaml
mins: >
  {% if mins_val < 1 %}1
  {% elif mins_val > 600 %}600
  {% else %}{{ mins_val }}
  {% endif %}
```

**Depois:**
```yaml
mins: "{{ [1, mins_val | int, 600] | sort | list[1] }}"
```

**Explicação:**
- Lista [1, valor, 600]
- Ordena
- Pega o elemento do meio
- = Clamp entre 1 e 600!

**Esforço:** ⏱️ 2 min por validação  
**Benefício:** 🎯 Baixo (elegância)  
**Prioridade:** 🟢 Opcional

---

## 🔢 **7. INPUT HELPERS**

### 🟡 **IH1: Adicionar unique_id a Todos os Helpers**

**Problema:** Nenhum helper tem `unique_id`

**Impacto:**
- Não pode renomear via UI
- Não aparece em algumas integrações
- Dificulta migração

**Solução:**

```yaml
# Antes
pool_pump_duration_lower_threshold:
  name: Pool Pump Duration Lower Threshold
  initial: 360
  min: 60
  max: 1440
  step: 1
  unit_of_measurement: minutes
  mode: box

# Depois
pool_pump_duration_lower_threshold:
  name: Pool Pump Duration Lower Threshold
  unique_id: pool_pump_duration_lower_01  ✅
  initial: 360
  min: 60
  max: 1440
  step: 1
  unit_of_measurement: minutes
  mode: box
  icon: mdi:timer-sand  ✅
```

**Esforço:** ⏱️ 1 hora (todos os helpers)  
**Benefício:** 🎯 Médio  
**Prioridade:** 🟡 Recomendado

---

### 🟢 **IH2: Remover Comentários "ADAPTA"**

**Problema:** `# ADAPTA` sugere configuração incompleta

**Exemplo:**
```yaml
piscina_volume:
  name: Piscina - Volume de Água
  initial: 1550   # ADAPTA  ❌
```

**Ações:**
1. Confirmar se 1550L é correto
2. Se sim, remover comentário
3. Se não, corrigir valor
4. Adicionar à documentação do package

**Esforço:** ⏱️ 15 minutos  
**Benefício:** 🎯 Baixo  
**Prioridade:** 🟢 Opcional

---

## 📊 **8. MONITORIZAÇÃO**

### 🟢 **M1: Adicionar Sensores de Sistema**

**Objetivo:** Monitorizar saúde do HA

**Criar:** `sensors/system_health.yaml`

```yaml
# System Monitor
- platform: systemmonitor
  resources:
    - type: disk_use_percent
      arg: /
    - type: memory_use_percent
    - type: processor_use
    - type: last_boot

# Uptime
- platform: uptime
  name: Home Assistant Uptime
  unit_of_measurement: hours

# Database Size
- platform: sql
  db_url: !secret mariadb_connection
  queries:
    - name: MariaDB Size
      query: "SELECT ROUND(SUM(data_length + index_length)) AS size 
              FROM information_schema.TABLES 
              WHERE table_schema = 'homeassistant';"
      column: 'size'
      unit_of_measurement: bytes

# Health Score Template
- platform: template
  sensors:
    system_health_score:
      friendly_name: "System Health"
      unit_of_measurement: "%"
      value_template: >
        {% set cpu = 100 - (states('sensor.processor_use') | float(0)) %}
        {% set mem = 100 - (states('sensor.memory_use_percent') | float(0)) %}
        {% set disk = 100 - (states('sensor.disk_use_percent') | float(0)) %}
        {{ ((cpu + mem + disk) / 3) | round(1) }}
```

**Esforço:** ⏱️ 30 minutos  
**Benefício:** 🎯 Alto  
**Prioridade:** 🟢 Recomendado

---

### 🟢 **M2: Alertas de Sistema**

**Criar automações para:**
- Disco > 85%
- Memória > 90%
- BD > 5GB
- HA restart inesperado

**Exemplo:**
```yaml
- id: 'system_disk_warning'
  alias: "💾 Sistema - Disco Quase Cheio"
  trigger:
    - platform: numeric_state
      entity_id: sensor.disk_use_percent
      above: 85
  action:
    - service: notify.telegram
      data:
        title: "💾 Aviso: Disco Quase Cheio"
        message: |
          Uso de disco: {{ states('sensor.disk_use_percent') }}%
          
          🧹 Sugestões:
          • Limpar logs antigos
          • Remover backups desnecessários
          • Purge da base de dados
```

**Esforço:** ⏱️ 1 hora  
**Benefício:** 🎯 Alto  
**Prioridade:** 🟢 Recomendado

---

## 📚 **9. DOCUMENTAÇÃO**

### 🟢 **D1: Criar Ficheiro de Configuração por Package**

**Objetivo:** Documentar cada package

**Exemplo:** `packages/README_piscina.md`

```markdown
# 🏊 Package Piscina

## Componentes

### Automações (5)
1. **Filtragem Noturna** - Executa no vazio (22:00-08:00)
2. **Filtragem Solar** - Usa excedente FV
3. **Modo Manual** - Override temporário
4. **Bomba Peristáltica** - Sincroniza com filtragem
5. **Watchdog** - Monitorização cada 2 min

### Sensores (8)
- `pool_pump_remaining_time` - Tempo restante
- `pool_pump_time` - Tempo hoje
- `bomba_piscina_horas_ligada_diario` - History stats
- [...]

### Input Helpers (4)
- `pool_pump_duration_lower_threshold` - Minutos mínimos/dia
- `piscina_override_manual` - Flag modo manual
- [...]

### Scripts (2)
- `piscina_manual_start` - Iniciar modo manual
- `alternar_modo_automacao_piscina` - Toggle auto/manual

## Configuração

### Valores Recomendados
- Verão: 360 min/dia
- Inverno: 180 min/dia
- Volume: 1550L (ajustar conforme piscina)

### Dependências
- `switch.bomba_piscina_switch_0` - Switch da bomba
- `binary_sensor.piscina_excedente_fv_bomba` - Sensor excedente

## Troubleshooting

### Bomba não liga no vazio
1. Verificar `input_boolean.piscina_override_manual` (deve estar OFF)
2. Confirmar `input_number.piscina_filtracao_min_restantes` > 0
3. Ver logs da automação

### Modo manual não desliga
1. Verificar `timer.piscina_manual`
2. Confirmar automação de watchdog ativa
```

**Esforço:** ⏱️ 30 min por package  
**Benefício:** 🎯 Alto (manutenção futura)  
**Prioridade:** 🟢 Recomendado

---

### 🟢 **D2: Criar CHANGELOG**

**Objetivo:** Rastrear mudanças importantes

**Formato:**
```markdown
# Changelog

## [2025-11-11] - Melhorias de Segurança
### Changed
- Movido credenciais cFos para secrets.yaml
- Otimizado recorder com auto_purge

### Added
- Sensores de monitorização de sistema
- Alertas de disco/memória

### Fixed
- Corrigido duplicação de automações piscina

## [2025-10-06] - Backup Automações
### Added
- Backup automático de automations.yaml

[...]
```

**Esforço:** ⏱️ 10 min (manter atualizado)  
**Benefício:** 🎯 Médio  
**Prioridade:** 🟢 Opcional

---

## 🧹 **10. LIMPEZA DE CÓDIGO**

### 🟡 **CL1: Resolver Comentários "ADAPTA"**

**Total encontrado:** 31 ocorrências

**Ações por ficheiro:**

1. **scripts.yaml** (3x)
   - Confirmar `switch.bomba_piscina_switch_0` é correto
   - Remover comentários

2. **automations/piscina_filtragem.yaml** (14x)
   - Validar entidades
   - Atualizar documentação
   - Remover # ADAPTA

3. **input_number.yaml** (1x)
   - Confirmar volume piscina (1550L)
   - Documentar em package

4. **templates/piscina_filtragem.yaml** (4x)
   - Validar sensores de temperatura
   - Confirmar sensor de energia

**Esforço:** ⏱️ 1 hora  
**Benefício:** 🎯 Médio  
**Prioridade:** 🟡 Recomendado

---

### 🟢 **CL2: Remover Ficheiros .old**

**Encontrados:**
- `templates/espaltherma.yaml_old`
- `packages/solar_hp90_from_fs.yaml_old`

**Ações:**
1. Se obsoleto: remover
2. Se backup: mover para `/archive/`
3. Se ativo: renomear corretamente

**Esforço:** ⏱️ 10 minutos  
**Benefício:** 🎯 Baixo  
**Prioridade:** 🟢 Opcional

---

### 🟢 **CL3: Padronizar Nomes de Entidades**

**Problema:** Inconsistência nos nomes

**Exemplos:**
- `pool_pump_*` vs `bomba_piscina_*` ← Mistura inglês/português
- `i4_edrive40_*` vs `x1_*` ← Diferentes convenções

**Sugestão:**
1. Escolher convenção (inglês recomendado para compatibilidade)
2. Criar migration plan
3. Usar aliases para compatibilidade

**Esforço:** ⏱️ 2-3 horas  
**Benefício:** 🎯 Médio (longo prazo)  
**Prioridade:** 🟢 Opcional (baixa prioridade)

---

## 📊 **RESUMO POR PRIORIDADE**

### 🔴 **URGENTE - Fazer Agora**
1. ✅ **S1** - Remover credenciais expostas (15 min)
2. ⚠️ **A3** - Eliminar duplicação piscina (30 min)

### 🟡 **IMPORTANTE - Próximas 2 Semanas**
3. ✅ **P1** - Otimizar Recorder (30 min)
4. ✅ **P2** - Reduzir Logging (5 min)
5. ✅ **A1** - Reorganizar automações (3-4h)
6. ✅ **AU1** - Adicionar descrições (8h)
7. ✅ **T1** - Validação templates (2h)
8. ✅ **T2** - Tarifários configuráveis (1h)
9. ✅ **IH1** - unique_id helpers (1h)
10. ✅ **CL1** - Resolver "ADAPTA" (1h)

### 🟢 **RECOMENDADO - Quando Possível**
11. ✅ **P3** - Otimizar InfluxDB (45 min)
12. ✅ **P4** - Otimizar time_pattern (20 min)
13. ✅ **A2** - Consolidar packages (6h)
14. ✅ **AU2** - IDs descritivos (3h)
15. ✅ **AU3** - Tratamento de erros (críticas)
16. ✅ **T3** - unique_id templates (30 min)
17. ✅ **M1** - Sensores sistema (30 min)
18. ✅ **M2** - Alertas sistema (1h)
19. ✅ **D1** - Documentar packages (2h)
20. ✅ **S2** - Auditar exposição IPs (30 min)

### ⚪ **OPCIONAL - Melhorias Futuras**
21. SC1 - Remover código comentado (5 min)
22. SC2 - Simplificar Jinja2 (opcional)
23. IH2 - Limpar comentários (15 min)
24. CL2 - Remover .old files (10 min)
25. CL3 - Padronizar nomes (3h)
26. S3 - 2FA (1h)
27. D2 - CHANGELOG (10 min manutenção)

---

## 🎯 **PLANO DE AÇÃO SUGERIDO**

### **Fase 1 - Segurança (1 dia)**
- [ ] S1 - Credenciais secrets.yaml
- [ ] S2 - Auditar IPs
- [ ] Regenerar password wallbox
- [ ] Validar e testar

### **Fase 2 - Performance (1 dia)**
- [ ] P1 - Recorder otimizado
- [ ] P2 - Logger warning
- [ ] P3 - InfluxDB include
- [ ] Reiniciar e monitorizar

### **Fase 3 - Organização (1 semana)**
- [ ] A1 - Reorganizar automações
- [ ] A3 - Eliminar duplicação
- [ ] CL1 - Resolver ADAPTA
- [ ] Testar tudo

### **Fase 4 - Qualidade (2 semanas)**
- [ ] AU1 - Descrições
- [ ] AU2 - IDs descritivos
- [ ] T1 - Validação templates
- [ ] T2 - Tarifários configuráveis
- [ ] IH1 - unique_ids

### **Fase 5 - Monitorização (3 dias)**
- [ ] M1 - Sensores sistema
- [ ] M2 - Alertas
- [ ] D1 - Documentação packages

---

**Próximo Passo:** Escolher tópicos e prioridades para implementação! 🚀
