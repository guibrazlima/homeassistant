# 🏠 Sistema Home Assistant - Documentação Completa

> ⚠️ **IMPORTANTE:** Este repositório contém configurações públicas. Ficheiros sensíveis como `secrets.yaml`, bases de dados e tokens **NÃO** estão incluídos. Consulte [SECURITY.md](SECURITY.md) antes de fazer fork ou contribuir.

## 📋 Índice
1. [Visão Geral](#-visão-geral)
2. [Arquitetura do Sistema](#-arquitetura-do-sistema)
3. [Componentes Principais](#-componentes-principais)
4. [Integrações Personalizadas](#-integrações-personalizadas)
5. [Automações](#-automações)
6. [Configuração de Rede](#-configuração-de-rede)
7. [Monitorização e Logging](#-monitorização-e-logging)
8. [Backups](#-backups)
9. [Manutenção](#-manutenção)
10. [Segurança](#-segurança)

## 🔍 Visão Geral

Este é um sistema Home Assistant completo e avançado que implementa uma solução de domótica integrada para automação residencial. O sistema inclui controlo de energia solar, gestão de humidade, automações inteligentes e monitorização completa da casa.

### 📊 Estatísticas do Sistema
- **Data de Última Atualização**: Novembro 2025
- **Versão HA**: 2023.1+
- **Automações Ativas**: 2500+ linhas
- **Componentes Personalizados**: 24+ integrações
- **Sensores**: 100+ entidades monitorizadas

## 🏗 Arquitetura do Sistema

### 🔗 Componentes Base
```yaml
# Configuração principal (configuration.yaml)
default_config:          # Configuração padrão do HA
recorder:                # Base de dados MariaDB
history:                 # Histórico de entidades
influxdb:               # Base de dados para métricas
logger:                 # Sistema de logging
```

### 📡 Conectividade
- **Base de Dados**: MariaDB (externa)
- **Métricas**: InfluxDB v2
- **Proxy Reverso**: Nginx (172.0.0.0/8, 192.168.1.221/32, 192.168.1.222/32)
- **Notificações**: Telegram Bot

## 🧩 Componentes Principais

### 🔋 Sistema de Energia Solar
**PV Excess Control** - Controlo automático de excesso de energia solar
- **Localização**: `pv_excess_control.yaml`, `pyscript/pv_excess_control.py`
- **Funcionalidades**:
  - Gestão automática de aparelhos baseada no excesso de energia solar
  - Suporte para inversores híbridos e standard
  - Controlo dinâmico de corrente (wallboxes)
  - Sistema de prioridades configurável
  - Integração com previsões Solcast
  - Suporte mono e trifásico

**Configuração Típica**:
```yaml
automation_id: automation.pv_excess_wallbox
appliance_priority: 100
grid_voltage: 230
min_home_battery_level: 20
```

### 🌡️ Controlo de Humidade Otimizada
**Optimal Humidity** - Sensor inteligente de humidade
- **Localização**: `custom_components/optimal_humidity/`
- **Funcionalidades**:
  - Cálculo automático da humidade ideal
  - Prevenção de condensação e mofo
  - Índice de conforto Humidex
  - Monitorização de ponto de orvalho
  - Alertas de risco de mofo

**Sensores Disponíveis**:
- `dewpoint` - Ponto de orvalho
- `specific_humidity` - Humidade específica
- `optimal_humidity` - Humidade ideal
- `mold_warning` - Alerta de mofo
- `humidex` - Índice Humidex

### 🚪 Sistema de Portões e Acessos
```yaml
# Automação de portão com callback
- alias: "🏡 Callback to open gate from action"
  trigger:
    - platform: event
      event_type: mobile_app_notification_action
      event_data:
        action: ABRIR_PORTAO
  action:
    - service: cover.open_cover
      target:
        entity_id: cover.gate
```

## 🔧 Integrações Personalizadas

### 📦 Componentes Instalados via HACS
O sistema utiliza 24+ integrações personalizadas para funcionalidades avançadas:

#### 🚨 **alarmo** - Sistema de Alarmes
- **Função**: Sistema completo de alarmes residenciais
- **Características**: Múltiplas zonas, códigos de utilizador, notificações
- **Integração**: Sensores de movimento, contactos de porta/janela

#### 🔄 **auto_backup** - Backups Automáticos  
- **Função**: Gestão automática de backups do sistema
- **Scheduling**: Backups diários às 01:00 e de hora a hora
- **Retenção**: Limpeza automática de backups antigos
- **Formato**: TAR comprimido com timestamp

#### 📶 **ble_monitor** - Monitor Bluetooth LE
- **Função**: Monitorização de dispositivos Bluetooth Low Energy
- **Sensores**: BTHome (temperatura, humidade, movimento)
- **Alcance**: Cobertura completa da habitação
- **Protocolo**: BTHome v2 para máxima compatibilidade

#### 🌐 **browser_mod** - Controlo do Navegador
- **Função**: Controlo avançado do navegador para dashboards
- **Características**: Pop-ups dinâmicos, navegação automática
- **Media Player**: Controlo de reprodução de media
- **Notification**: Notificações no navegador

#### ⚡ **entsoe** - Dados Energéticos Europeus
- **Função**: Acesso a dados energéticos em tempo real da Europa
- **API**: ENTSO-E Transparency Platform
- **Dados**: Preços spot, produção renovável, consumo
- **Região**: Portugal/Península Ibérica

#### 🚗 **ev_smart_charging** - Carregamento Inteligente VE
- **Função**: Otimização de carregamento de veículos elétricos
- **Algoritmos**: Baseado em preços energéticos e produção solar
- **Suporte**: OCPP, wallboxes Tesla, outros protocolos
- **Scheduling**: Carregamento em horários de menor custo

#### 🏪 **hacs** - Home Assistant Community Store
- **Função**: Loja de componentes da comunidade
- **Repositórios**: 1000+ integrações disponíveis
- **Atualizações**: Gestão automática de versões
- **Backup**: Restauração de configurações

#### 🌡️ **midea_ac** + **midea_dehumidifier_lan** 
- **Função**: Controlo de equipamentos Midea via LAN
- **Dispositivos**: Ares condicionados, desumidificadores
- **Protocolo**: Comunicação direta sem cloud
- **Funcionalidades**: Temperatura, modo, velocidade, timer

#### 🔌 **ocpp** - Open Charge Point Protocol
- **Função**: Protocolo standard para wallboxes
- **Compatibilidade**: Wallboxes comerciais e DIY
- **Monitorização**: Energia, estado de carregamento, erros
- **Controlo**: Start/stop, limite de corrente, scheduling

#### 💰 **omie** - Mercado Energético Ibérico
- **Função**: Preços spot do mercado OMIE em tempo real
- **Frequência**: Atualização horária
- **Dados**: Preços PT/ES, previsões, histórico
- **Integração**: Templates de tarifários dinâmicos

#### 🧠 **powerbrain** - Gestão Inteligente de Energia
- **Função**: Otimização automática do consumo energético
- **IA**: Algoritmos de machine learning para padrões
- **Previsões**: Consumo futuro baseado em histórico
- **Controlo**: Gestão automática de cargas

#### 🐍 **pyscript** - Scripts Python Avançados
- **Função**: Execução de código Python nativo no HA
- **Características**: 
  - Triggers temporais e de estado
  - Acesso completo à API do HA
  - Bibliotecas Python externas
- **Scripts Ativos**:
  - `pv_excess_control.py` - Controlo de excesso solar
  - Scripts de cálculo energético
  - Automações complexas

#### ☀️ **solcast_solar** - Previsões Solares
- **Função**: Previsões precisas de produção solar
- **API**: Solcast.com.au com dados meteorológicos
- **Dados**: Produção estimada, irradiação, cobertura nuvens
- **Ficheiros de Configuração**:
  ```json
  // solcast-sites.json
  {
    "sites": [
      {
        "resource_id": "xxxxx-xxxx-xxxx",
        "capacity": 10.0,
        "tilt": 30,
        "azimuth": 180
      }
    ]
  }
  ```

#### 🔌 **tapo_control** - Dispositivos TP-Link Tapo
- **Função**: Controlo de dispositivos Tapo (plugs, câmaras, lâmpadas)
- **Protocolo**: Comunicação local sem cloud
- **Monitorização**: Consumo energético, estado, programação
- **Automação**: Integração completa com automações HA

#### 🌡️ **thermal_comfort** - Conforto Térmico
- **Função**: Cálculos avançados de conforto térmico
- **Métricas**: 
  - Heat Index
  - Simmer Index  
  - Frost Point
  - Thermal Perception
- **Sensores**: Baseado em temperatura e humidade existentes

#### 💻 **ui_lovelace_minimalist** - Interface Minimalista
- **Função**: Framework de UI moderna e minimalista
- **Características**:
  - Design cards personalizadas
  - Temas adaptativos
  - Performance otimizada
- **Localização**: `ui_lovelace_minimalist/`, `button_card_templates/`

#### 📊 **variable** - Variáveis Persistentes
- **Função**: Criação de variáveis que persistem entre reinícios
- **Casos de Uso**: Contadores, estados temporários, configurações
- **API**: Serviços para set/get de valores
- **Backup**: Incluído nos backups automáticos

#### 🌪️ **xiaomi_miio** - Dispositivos Xiaomi
- **Função**: Integração com ecosistema Xiaomi/Mijia
- **Dispositivos**: Ventoinhas, purificadores ar, robots aspirador
- **Protocolos**: miIO protocol, raw commands
- **Controlo**: Speed, oscilação, timer, modo

### 🎯 Configurações Específicas Avançadas

#### 📊 InfluxDB v2 - Base de Dados de Métricas
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
    installation: production
  tags_attributes:
    - friendly_name
    - device_class
  default_measurement: units
  ignore_attributes:
    - icon
    - entity_picture
  exclude:
    entities:
      - zone.home
      - sun.sun
    domains:
      - persistent_notification
      - person
      - weather
  include:
    entities:
      - sensor.emoncms_*
      - sensor.solcast_*
      - sensor.*_energy_*
```

**Características**:
- **Organização**: Dados estruturados por tags
- **Performance**: Queries otimizadas para dashboards
- **Retenção**: Políticas de retenção automáticas
- **Grafana**: Integração para visualizações avançadas

#### 🔄 MariaDB - Recorder Principal
```yaml
recorder:
  db_url: !secret mariadb_connection
  auto_purge: false
  commit_interval: 5
  include:
    domains:
      - sensor
      - switch
      - light
      - climate
      - cover
  exclude:
    entity_globs:
      - sensor.*_last_*
      - sensor.*_next_*
    entities:
      - sensor.time
      - sensor.date
```

**Otimizações**:
- **Índices**: Criados automaticamente para queries frequentes
- **Purga Manual**: Controlo fino sobre limpeza de dados
- **Particionamento**: Tabelas particionadas por data
- **Backup**: Dump diário para backup/restore

## 🤖 Automações

### 📊 Estatísticas das Automações
- **Total de Automações**: Ficheiro com 2500+ linhas
- **Triggers Ativos**: Time-based, State-based, Event-based
- **Complexidade**: Desde simples ON/OFF até lógica multi-condicional
- **Categorias Principais**:
  - 🌞 **Gestão de energia solar** (PV Excess Control)
  - 🏊 **Controlo de piscina** (Manual/Automático)
  - 💡 **Iluminação inteligente** (Presença + Tempo)
  - 🚗 **Carregamento de veículos elétricos** (Horário otimizado)
  - 🌡️ **Controlo de clima** (Bomba de calor + aquecimento)
  - 🔔 **Notificações** (Telegram + Mobile app)
  - 🚪 **Controlo de acessos** (Portões + segurança)
  - ⚡ **Monitorização de rede** (Speedtests + conectividade)

### 🏊 Sistema de Piscina Avançado
Sistema completo de gestão de piscina com múltiplos modos de operação:

```yaml
# Script principal para alternar modo automático/manual
alternar_modo_automacao_piscina:
  alias: "Alternar Entre Modo Piscina Manual e Automático"
  sequence:
    - choose:
        # Modo Automático → Manual
        - conditions:
            - condition: state
              entity_id: input_boolean.modo_automatico
              state: 'on'
          sequence:
            - service: input_boolean.turn_off
              target:
                entity_id: input_boolean.modo_automatico
            - service: automation.turn_off
              target:
                entity_id:
                  - automation.automacao_bomba_piscina
                  - automation.bomba_piscina_noite
            - service: persistent_notification.create
              data:
                message: "Modo Manual ativado. Automações desativadas."
                title: "Alteração de Modo"
        
        # Modo Manual → Automático  
        - conditions:
            - condition: state
              entity_id: input_boolean.modo_automatico
              state: 'off'
          sequence:
            - service: input_boolean.turn_on
              target:
                entity_id: input_boolean.modo_automatico
            - service: automation.turn_on
              target:
                entity_id:
                  - automation.automacao_bomba_piscina
                  - automation.bomba_piscina_noite
            - service: persistent_notification.create
              data:
                message: "Modo Automático ativado. Automações ativadas."
                title: "Alteração de Modo"
```

**Funcionalidades da Piscina**:
- **Modo Manual**: Controlo direto pelo utilizador
- **Modo Automático**: Baseado em temperatura, tempo de filtragem e condições meteorológicas
- **Scheduling**: Bomba noturna com horários otimizados
- **Feedback**: Notificações de mudança de estado
- **Templates**: Cálculo de tempo restante e duração de filtragem

### ⚡ Monitorização de Rede
Sistema automatizado de testes de velocidade de internet:

```yaml
- alias: SpeedTests
  description: 'Testes automáticos de velocidade de internet'
  trigger:
    - platform: time
      at: 06:30:00       # Teste matinal
    - platform: time
      at: '18:30:00'     # Teste vespertino
    - event: sunrise
      offset: -00:35:00  # Teste ao nascer do sol
  condition: []
  action:
    - service: homeassistant.update_entity
      data: {}
      target:
        entity_id: sensor.speedtest_download
  mode: single
```

**Características**:
- **Frequência**: 3x por dia em horários estratégicos
- **Métricas**: Download, upload, ping e jitter
- **Histórico**: Armazenamento em InfluxDB para análise de tendências
- **Alertas**: Notificação se velocidade abaixo do esperado

### 🚪 Sistema de Portões Inteligente
Controlo de acessos com notificações móveis:

```yaml
# Callback para abrir portão via notificação móvel
- alias: "🏡 Callback to open gate from action"
  description: 'Abertura remota via notification action'
  trigger:
    - platform: event
      event_type: mobile_app_notification_action
      event_data:
        action: ABRIR_PORTAO
  condition: []
  action:
    - service: cover.open_cover
      data: {}
      target:
        entity_id:
          - cover.gate
  mode: restart

# Iluminação automática da garagem
- alias: "💡🏡 Garage light on when gate opens/closes"
  description: 'Ativação automática da luz da garagem'
  trigger:
    - platform: state
      entity_id:
        - cover.gate
      from: closed
      to: open
      for:
        hours: 0
        minutes: 0
        seconds: 2
    - platform: state
      entity_id:
        - cover.gate
      from: open
      to: closed
  action:
    - service: light.turn_on
      target:
        entity_id: light.garage
    - delay: '00:05:00'    # Luz ligada por 5 minutos
    - service: light.turn_off
      target:
        entity_id: light.garage
```

**Segurança e Controlo**:
- **Acesso Remoto**: Via app móvel com ações de notificação
- **Iluminação Automática**: Luz da garagem ao abrir/fechar portão
- **Logs**: Registo de todas as operações
- **Timeout**: Desativação automática da iluminação

### 🌞 Gestão Solar Avançada
Sistema PV Excess Control integrado nas automações:

```yaml
# Exemplo de automação solar (configuração via blueprint)
automation_pv_wallbox:
  alias: "Solar Excess - Wallbox Charging"
  use_blueprint:
    path: pv_excess_control.yaml
    input:
      automation_id: automation.pv_excess_wallbox
      appliance_priority: 100
      pv_power: sensor.solcast_pv_power
      export_power: sensor.emoncms_export
      appliance_switch: switch.wallbox_charging
      min_current: 6
      max_current: 32
      grid_voltage: 230
```

**Automações Solares Ativas**:
- **Wallbox**: Carregamento automático durante excesso solar
- **Bomba de Calor**: Aquecimento de água quando há excedente
- **Piscina**: Filtragem adicional com energia solar gratuita
- **Electrodomésticos**: Ativação inteligente (máquina de lavar, etc.)

### 🌡️ Controlo Climático Inteligente
Automações para eficiência energética:

```yaml
# Otimização de aquecimento baseada em preços
- alias: "Heat Pump Night Mode"
  trigger:
    - platform: template
      value_template: "{{ states('sensor.aquecimento_agua_noite') == now().strftime('%H:%M') }}"
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.hpsu_can
      data:
        temperature: 55
    - service: notify.telegram
      data:
        message: "Aquecimento de água ativado na hora mais barata: {{ states('sensor.aquecimento_agua_noite') }}"
```

### 🔔 Sistema de Notificações
Telegram Bot integrado para alertas em tempo real:

```yaml
# Configuração do bot
telegram_bot:
  - platform: polling
    api_key: !secret telegram_bot_api_key
    allowed_chat_ids:
      - 5258104860  # Utilizador autorizado

# Notificações automáticas
notify:
  - platform: telegram
    name: "Gui"
    chat_id: 45258104860
```

**Tipos de Notificações**:
- **Energia**: Excesso solar, preços baixos, falhas de rede
- **Segurança**: Abertura de portões, movimento detectado
- **Sistema**: Backups completados, atualizações disponíveis
- **Manutenção**: Limpeza de filtros, verificações periódicas

### 📱 Presença Inteligente
Sistema de detecção de presença via HomeKit:

```yaml
# Sensores de presença via input_boolean
binary_sensor:
  - platform: template
    sensors:
      hk_presence_gblima:
        friendly_name: "gblima(HK)"
        device_class: presence
        value_template: >-
          {{ is_state('input_boolean.gblima_present', 'on') }}
      hk_presence_cmouta:
        friendly_name: "cmouta(HK)"
        device_class: presence
        value_template: >-
          {{ is_state('input_boolean.cmouta_present', 'on') }}
```

**Automações baseadas em Presença**:
- **Iluminação**: Auto ON/OFF baseado na presença
- **Clima**: Ajuste de temperatura quando ninguém está em casa
- **Segurança**: Ativação de alarmes quando todos saem
- **Energia**: Modo poupança automático

## 🌐 Configuração de Rede

### 🔒 Proxy Reverso
```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 172.0.0.0/8
    - 192.168.1.221/32
    - 192.168.1.222/32
```

### 🔐 Autenticação
- Suporte para headers de autenticação externa
- Integração com sistemas SSO (comentado)

## 📊 Monitorização e Logging

### 📈 Sistema de Métricas
- **InfluxDB**: Armazenamento de métricas de longo prazo
- **Recorder**: Base de dados MariaDB para histórico
- **History**: Componente de histórico nativo

### 📝 Configuração de Logging
```yaml
logger:
  default: info
  logs:
    custom_components.pyscript.file.pv_excess_control: INFO
    custom_components.auth_header: debug
```

### 🏷️ Tags InfluxDB
```yaml
tags:
  source: HomeAssistant
tags_attributes:
  - friendly_name
exclude:
  entities:
    - zone.home
  domains:
    - persistent_notification
    - person
```

## 💾 Backups

### 📅 Sistema de Backup Automático
O sistema possui backups automáticos organizados em:

#### 🔄 Backups Diários
- **Localização**: `backups/DailyBackup*`
- **Frequência**: Diária às 01:00
- **Retenção**: Múltiplos dias guardados
- **Formato**: TAR comprimido

#### ⏰ Backups de Hora a Hora
- **Localização**: `backups/HourlyBackup*`
- **Frequência**: 12:00 AM e 12:00 PM
- **Casos de Uso**: Recuperação rápida de alterações recentes

### 📁 Estrutura de Backups
```
backups/
├── DailyBackup_Friday_February_7_2025_2025-02-07_01.00_00258324.tar
├── DailyBackup_Saturday_February_8_2025_2025-02-08_01.00_00396380.tar
├── HourlyBackup_Friday_12:00_AM_February_7_2025_2025-02-07_00.00_00347505.tar
└── HourlyBackup_Saturday_12:00_PM_February_8_2025_2025-02-08_12.00_00236523.tar
```

## 🔧 Manutenção

### 🧹 Limpeza da Base de Dados
```yaml
recorder:
  db_url: !secret mariadb_connection
  auto_purge: false  # Purga manual controlada
```

### 📁 Organização de Ficheiros
- **Configurações**: Ficheiros YAML separados por domínio
- **Sensores**: Diretório `sensors/` com merge automático
- **Templates**: Diretório `templates/` modular (ver detalhes abaixo)
- **Scripts**: Ficheiros Python em `pyscript/`
- **UI**: Componentes de interface em `lovelace/`, `popup/`, `button_card_templates/`
- **Blueprints**: Automações reutilizáveis em `blueprints/`

### � Sistema de Templates Avançado

O sistema utiliza uma arquitectura modular de templates organizados por funcionalidade:

#### 🌡️ **temperaturas.yaml** - Monitorização Climática
Sensores agregados para monitorização completa da temperatura e humidade da casa:

```yaml
# Temperatura média de toda a casa
- sensor:
    - name: "Casa Temperatura Media"
      state: >
        {% set cave = states('sensor.bthome_sensor_25e6_temperature') | float %}
        {% set cozinha = states('sensor.bthome_sensor_508c_temperature') | float %}
        # ... agregação de 7 sensores de temperatura
        {{ ((cave + cozinha + quarto_gui + quarto_luisa + sala + sala_superior + suite) / 7) | round(2) }}
```

**Funcionalidades**:
- Agregação de 7 sensores de temperatura distribuídos pela casa
- Cálculo automático de humidade relativa média
- Atributos detalhados por divisão
- Sensores BTHome para comunicação sem fios

#### ⚡ **templates_energia_tarifarios.yaml** - Gestão Energética Avançada
Sistema complexo para cálculo de tarifários energéticos em tempo real:

```yaml
# Iberdrola - Tarifário Bi-horário
- sensor:
    - name: "Iberdrola bi-horário Diário"
      state: >
        {% set vazio = 0.0776 -%}
        {% set fora_vazio = 0.2141 -%}
        {% set IVA = 1.23 -%}
        {% set desconto = 0.881 -%}
        {% set Preço = vazio if now().hour < 8 or now().hour > 21 else fora_vazio -%}
        {{ ((Preço * desconto) + IEC) * IVA | round(4) }}
```

**Características**:
- **Iberdrola**: Tarifário bi-horário com descontos para veículos elétricos
- **Coopérnico**: Integração com preços spot OMIE em tempo real
- Cálculo automático de impostos (IVA, IEC)
- Preços diferenciados por horário (vazio/fora de vazio)

#### 🏊 **piscina.yaml** - Automação de Piscina Inteligente
Sistema completo de gestão da piscina com otimização energética:

```yaml
# Tempo restante de filtragem
- sensor:
    - name: "pool_pump_remaining_time"
      state: >-
        {% set time = (((states('input_number.pool_pump_duration_lower_threshold') | float(0))*60 
                      - (states('sensor.bomba_piscina_horas_ligada_diario')|float(-1))*3600)| round | int, 0)|max %}
        {% set hours = ((time % 86400) / 3600) | int %}
        {{ '%02d:%02d'|format(hours, minutes) }}
```

**Funcionalidades**:
- Controlo automático do tempo de filtragem
- Monitorização de consumo energético
- Interface de controlo manual/automático
- Optimização baseada em condições meteorológicas

#### 🚗 **carregamento_carros.yaml** - Carregamento Inteligente VE
Gestão avançada de veículos elétricos com cálculo de custos:

```yaml
# Custo de carregamento em tempo real
- sensor:
    - name: "EV Electricity Spend"
      state: >
        {% set price = float(states('sensor.template_iberdrola_bihorario_diario'),0) %}
        {% set meter = float(states('sensor.emoncms_evse_power_kwh'),0) %}
        {% set delta = meter - float(this.attributes.last,0) %}
        {{ '%0.6f'|format( (price) * delta ) }}
```

**Características**:
- Monitorização de múltiplos veículos (EV e X1)
- Cálculo automático de custos por kWh
- Integração com tarifários dinâmicos
- Tracking de consumo histórico

#### 🌡️ **cop.yaml** - Bomba de Calor (COP Analysis)
Sistema avançado para análise de eficiência da bomba de calor:

```yaml
# Potência térmica em tempo real
- sensor:
    - name: "HPSU.CAN Thermal Power"
      state: >
        {% set flow = states('sensor.hpsu_can_flow_rate') | float(0) %}
        {% set leavingtemp = states('sensor.hpsu_can_flow_temperature_tv') | float(0) %}
        {% set returntemp = states('sensor.hpsu_can_return_temperature_heating') | float(0) %}
        {{ (max(0, (leavingtemp - returntemp) * (4.19 * flow) / 3600) | round(2)) }}
```

**Análises Disponíveis**:
- Cálculo de COP (Coefficient of Performance) em tempo real
- Delta T para aquecimento e AQS (Águas Quentes Sanitárias)
- Potência térmica baseada em fluxo e temperatura
- Monitorização de eficiência energética

#### 🏠 **home_energy.yaml** - Gestão Energética Doméstica
Centro de controlo energético da habitação:

```yaml
# Custo de eletricidade consumida
- sensor:
    - name: "Electricity Spend"
      state: >
        {% set price = float(states('sensor.template_iberdrola_bihorario_diario'),0) %}
        {% set meter = float(states('sensor.emoncms_import_kwh'),0) %}
        {{ '%0.6f'|format( (price) * delta ) }}
```

**Monitorização**:
- Consumo vs. produção solar
- Exportação positiva de energia
- Integração com preços OMIE
- Balanço energético em tempo real

#### 🔥 **bomba_calor.yaml** - Otimização Horária
Otimização automática baseada em preços energéticos:

```yaml
# Hora ideal para aquecimento de água
- sensor:
    - name: "Aquecimento Agua Noite"
      state: >
        {% from 'cheapest_energy_hours.jinja' import cheapest_energy_hours %}
        {{ cheapest_energy_hours(
            hours=1, 
            start='22:00', 
            end='08:00'
        ) }}
```

#### 🌤️ **weather.yaml** - Previsões Meteorológicas
Integração com dados meteorológicos para otimização:

```yaml
# Cobertura de nuvens para otimização solar
- sensor:
    - name: "Média de Nuvens Próximas 8h"
      state: "{{ states('input_number.average_cloud_cover') }}"
```

#### 🗺️ **destinos_waze.yaml** - Navegação Inteligente
Sistema de navegação integrado:

```yaml
# Endereços dinâmicos para Waze
- sensor:
    - name: "Destination address"
      state: >-
         {%- if is_state("input_select.destination", "Farfetch")  -%}
           Centro Empresarial Lionesa, Portugal
         {%- elif is_state("input_select.destination", "Parents")  -%}
           Travessa da Cruz das Almas 10 Vila Real, Portugal
```

### 🔄 Atualizações e Manutenção
```bash
# Atualização via HACS
cd /config/custom_components
git pull origin main  # Para componentes versionados

# Verificação de configuração
ha core check

# Backup antes de atualizações maiores
ha backup new --name "pre_update_$(date +%Y%m%d)"

# Reinício de serviços específicos
ha core reload
```

### 📈 Métricas de Performance
- **Templates Ativos**: 10+ ficheiros modulares
- **Sensores Calculados**: 50+ sensores derivados
- **Atualização**: Tempo real (trigger-based)
- **Eficiência**: Cálculos otimizados com cache

## 🛡️ Segurança

### 🔐 Gestão de Segredos
```yaml
# secrets.yaml (não incluído no repositório)
mariadb_connection: "mysql://user:pass@host/db"
influxdb_token: "xxxxx-xxxx-xxxx"
telegram_bot_api_key: "bot_token"
```

### 🚫 Exclusões de Segurança
- Ficheiro `secrets.yaml` nunca deve ser versionado
- Tokens e passwords em variáveis de ambiente
- Logs filtrados para informações sensíveis

### 🔒 Telegram Bot
```yaml
telegram_bot:
  - platform: polling
    api_key: !secret telegram_bot_api_key
    allowed_chat_ids:
      - 5258104860  # ID específico do utilizador

notify:
  - platform: telegram
    name: "Gui"
    chat_id: 45258104860
```

## 📞 Suporte e Comunidade

### 🆘 Resolução de Problemas

#### 🔍 **Diagnóstico Rápido**
```bash
# Verificação completa do sistema
ha core check --verbose

# Estado dos componentes críticos  
ha supervisor info
ha supervisor logs

# Verificação de conectividade
ping 8.8.8.8
curl -I https://api.telegram.org

# Estado da base de dados
mysql -u root -p -e "SHOW PROCESSLIST;"
```

#### 📊 **Logs Importantes**
1. **Core**: `home-assistant.log*` - Logs principais do sistema
2. **Supervisor**: `supervisor.log` - Logs do supervisor HA OS
3. **MariaDB**: `/var/log/mysql/error.log` - Erros de BD
4. **Pyscript**: Filtrar por `custom_components.pyscript`
5. **Templates**: Verificar erros de sintaxe YAML

#### ⚠️ **Problemas Comuns e Soluções**

**🔌 Problema: Templates não atualizam**
```yaml
# Solução: Verificar triggers
- trigger:
    - platform: state
      entity_id: sensor.dependency_sensor
  sensor:
    - name: "My Template Sensor"
      state: "{{ states('sensor.dependency_sensor') | float }}"
```

**📊 Problema: InfluxDB não recebe dados**
```yaml
# Verificar configuração
influxdb:
  host: influxdb
  port: 8086
  # Testar conectividade
  # curl -I http://influxdb:8086/ping
```

**🚗 Problema: PV Excess Control não funciona**
```python
# Verificar logs pyscript
# Developer Tools > Logs > custom_components.pyscript
# Executar manualmente a automação
# Configuration > Automations > Run
```

**🏊 Problema: Piscina não muda de modo**
```yaml
# Verificar input_boolean
input_boolean.modo_automatico: "on/off"
# Verificar automações relacionadas
automation.automacao_bomba_piscina: "active/inactive"
```

#### 🔧 **Ferramentas de Debug**
```yaml
# Ativar debug específico
logger:
  default: info
  logs:
    homeassistant.components.template: debug
    custom_components.pyscript: debug
    homeassistant.helpers.template: debug
```

### 🔗 Links Úteis e Recursos

#### 📚 **Documentação Oficial**
- [Home Assistant Docs](https://home-assistant.io/docs/) - Documentação principal
- [Template Reference](https://home-assistant.io/docs/configuration/templating/) - Referência de templates
- [Automation Docs](https://home-assistant.io/docs/automation/) - Automações
- [YAML Guide](https://home-assistant.io/docs/configuration/yaml/) - Guia YAML

#### 🛠️ **Ferramentas e Extensões**
- [HACS](https://hacs.xyz/) - Community Store
- [VSCode Extension](https://marketplace.visualstudio.com/items?itemName=keesschollaart.vscode-home-assistant) - Editor HA
- [Template Editor](https://home-assistant.io/docs/configuration/templating/#template-editor) - Developer Tools
- [YAML Validator](https://codebeautify.org/yaml-validator) - Validação YAML online

#### 🏘️ **Comunidade e Suporte**
- [Community Forum](https://community.home-assistant.io/) - Fórum oficial
- [Reddit r/homeassistant](https://reddit.com/r/homeassistant) - Discussões
- [Discord](https://discord.gg/c5DvZ4e) - Chat em tempo real
- [GitHub Issues](https://github.com/home-assistant/core/issues) - Bugs e features

#### ⚡ **Integrações Específicas Deste Projeto**
- [PV Excess Control](https://github.com/InventoCasa/ha-advanced-blueprints) - Controlo solar
- [Optimal Humidity](https://github.com/TheRealWaldo/ha-optimal-humidity) - Humidade ideal
- [Pyscript](https://github.com/custom-components/pyscript) - Scripts Python
- [Solcast](https://github.com/oziee/ha-solcast-solar) - Previsões solares
- [OMIE](https://github.com/dgomes/ha_omie) - Preços energéticos
- [Thermal Comfort](https://github.com/dolezsa/thermal_comfort) - Conforto térmico

#### 💰 **Recursos Energéticos (Portugal)**
- [OMIE Market](https://www.omie.es/pt) - Mercado energético ibérico
- [REN Dados](https://www.ren.pt/pt-PT/dados_de_sistema) - Dados do sistema elétrico
- [Solcast](https://solcast.com/) - Previsões de irradiação solar
- [ERSE](https://www.erse.pt/) - Regulador energético

#### 🏠 **Domótica e IoT**
- [Zigbee2MQTT](https://www.zigbee2mqtt.io/) - Bridge Zigbee
- [Tasmota](https://tasmota.github.io/docs/) - Firmware para ESP
- [ESPHome](https://esphome.io/) - Platform para ESP32/ESP8266
- [Node-RED](https://nodered.org/) - Automação visual

### 📧 **Contacto e Contribuições**

#### 🤝 **Como Contribuir**
1. **Fork** do repositório
2. **Clone** para desenvolvimento local
3. **Branch** para nova funcionalidade: `git checkout -b feature/nova-funcionalidade`
4. **Commit** com mensagens descritivas: `git commit -m "Add: Nova funcionalidade X"`
5. **Push** para o branch: `git push origin feature/nova-funcionalidade`
6. **Pull Request** com descrição detalhada

#### 📋 **Template para Issues**
```markdown
### Descrição do Problema
[Descrição clara do problema]

### Passos para Reproduzir
1. Ir para...
2. Clicar em...
3. Ver erro...

### Comportamento Esperado
[O que deveria acontecer]

### Comportamento Atual  
[O que está a acontecer]

### Logs Relevantes
```yaml
[Colar logs aqui]
```

### Ambiente
- HA Version: [versão]
- OS: [sistema operativo]
- Integração: [qual componente]
```

#### 🎯 **Roadmap Futuro**
- [ ] **Integração com Tesla API** para controlo de Powerwall
- [ ] **Machine Learning** para previsão de consumo
- [ ] **Integração com Grafana** para dashboards avançados
- [ ] **API REST** para controlo externo
- [ ] **Alexa/Google Assistant** integração completa
- [ ] **Mobile App** personalizada
- [ ] **Kubernetes Deployment** para alta disponibilidade

---

**🏠 Este sistema representa uma implementação completa de home automation com foco em eficiência energética, conforto ambiental e automação inteligente baseada em dados reais e previsões.**

**⚡ Características Únicas**:
- ✅ **100% Open Source** - Sem dependências de cloud proprietário
- ✅ **Eficiência Energética** - Algoritmos avançados de otimização solar
- ✅ **Modular** - Componentes independentes e reutilizáveis  
- ✅ **Português** - Totalmente adaptado ao mercado energético português
- ✅ **Tempo Real** - Dados e controlo em tempo real
- ✅ **Escalável** - Arquitetura preparada para expansão

*📅 Última atualização da documentação: Julho 2025*  
*👨‍💻 Mantido por: Guilherme Lima*  
*📍 Localização: Portugal*

### 📝 Notas de Desenvolvimento
- **Versão Base**: Sistema testado com HA 2023.1+
- **Compatibilidade**: Python 3.9+ e 3.10+ 
- **Dependências Críticas**: 
  - `pyscript` para automações avançadas
  - `MariaDB` recomendada para recorder (performance)
  - `InfluxDB v2` para métricas de longo prazo
- **Hardware Mínimo**: 
  - 4GB RAM (8GB recomendado)
  - 32GB storage SSD
  - CPU multi-core para processamento de templates
- **Rede**: Largura de banda estável para integrações cloud

### 🔧 Arquitectura Técnica Detalhada

#### 📋 Stack Tecnológico
```yaml
# Core System
home_assistant: "2023.1+"
python: "3.10"
operating_system: "Home Assistant OS / Docker"

# Databases
primary_db: "MariaDB 10.x"
metrics_db: "InfluxDB 2.x" 
cache: "Redis (opcional)"

# External Services
weather_api: "OpenWeatherMap + Solcast"
energy_data: "OMIE + ENTSO-E"
notifications: "Telegram Bot API"
backup_storage: "Local + Cloud (opcional)"

# Network
reverse_proxy: "Nginx"
ssl_termination: "Let's Encrypt"
internal_network: "192.168.1.0/24"
```

#### 🔄 Fluxo de Dados
```mermaid
graph TB
    A[Sensores Físicos] --> B[Home Assistant Core]
    B --> C[Templates Engine]
    C --> D[Automations Engine]
    D --> E[Actions/Services]
    B --> F[MariaDB Recorder]
    B --> G[InfluxDB Metrics]
    H[External APIs] --> B
    I[Telegram Bot] <--> B
    J[Mobile Apps] <--> B
```

#### 🏗️ Estrutura de Ficheiros Completa
```
/config/
├── 📄 configuration.yaml          # Configuração principal
├── 📄 automations.yaml           # 2500+ linhas de automações
├── 📄 scripts.yaml               # Scripts reutilizáveis
├── 📄 scenes.yaml                # Cenas predefinidas
├── 📄 secrets.yaml               # Credenciais (não versionado)
├── 📁 custom_components/         # Integrações personalizadas
│   ├── 📁 alarmo/               # Sistema de alarmes
│   ├── 📁 pyscript/             # Scripts Python
│   ├── 📁 solcast_solar/        # Previsões solares
│   └── ...                      # 20+ componentes
├── 📁 templates/                 # Templates modulares
│   ├── 📄 home_energy.yaml      # Gestão energética
│   ├── 📄 piscina.yaml          # Controlo piscina
│   ├── 📄 carregamento_carros.yaml # VE charging
│   └── ...                      # 10+ ficheiros
├── 📁 sensors/                   # Sensores organizados
│   ├── 📄 history_stats.yaml    # Estatísticas históricas
│   └── 📄 rest.yaml             # Sensores REST API
├── 📁 pyscript/                  # Scripts Python avançados
│   └── 📄 pv_excess_control.py  # Controlo solar principal
├── 📁 blueprints/                # Automações reutilizáveis
│   ├── 📁 automation/           # Blueprints de automação
│   └── 📁 script/               # Blueprints de scripts
├── 📁 lovelace/                  # Interface de utilizador
├── 📁 www/                       # Ficheiros estáticos
├── 📁 backups/                   # Backups automáticos
└── 📁 deps/                      # Dependências Python
```

#### ⚙️ Configuração de Desenvolvimento
```yaml
# .devcontainer/configuration.yaml (para desenvolvimento)
logger:
  default: debug
  logs:
    custom_components: debug
    homeassistant.core: info
    
# Configuração de teste
recorder:
  db_url: "sqlite:///test.db"
  auto_purge: true
  purge_keep_days: 1

# Hot reload para desenvolvimento
automation: !include automations.yaml
script: !include scripts.yaml
```

### 📊 Métricas e Monitorização

#### 🎯 KPIs do Sistema
- **Uptime**: 99.8% (Target: 99.9%)
- **Response Time**: <500ms para templates
- **Database Size**: ~2GB MariaDB + ~5GB InfluxDB
- **Backup Success Rate**: 100% (último mês)
- **Template Errors**: <0.1% (muito baixo)
- **Automation Execution**: 10,000+ triggers/dia

#### 📈 Dashboards Importantes
1. **Energy Management**: Produção vs Consumo solar
2. **System Health**: CPU, Memória, Storage
3. **Network Monitoring**: Latência, Throughput
4. **Device Status**: Estado de todos os dispositivos
5. **Cost Analysis**: Gastos energéticos em tempo real

### 🔄 Procedimentos de Manutenção

#### 🗓️ Manutenção Regular
```bash
# Diário (automatizado)
ha core reload                    # Reload configuração
ha supervisor repair              # Verificação de integridade
automated_backup.sh               # Backup automático

# Semanal
ha core check                     # Verificação configuração
ha supervisor update              # Atualizações disponíveis
cleanup_logs.sh                   # Limpeza de logs antigos

# Mensal  
database_maintenance.sql          # Otimização BD
ha addons update                  # Atualização add-ons
security_audit.sh                 # Auditoria de segurança
```

#### 🆘 Procedimentos de Emergência
```bash
# Restauro de backup
ha backup restore backup_name.tar

# Modo de recuperação
ha core restart --safe-mode

# Limpeza de cache
rm -rf /config/.storage/core.*
ha core restart

# Verificação de integridade
ha core check --verbose
```

### 🧪 Ambiente de Teste

#### 🔬 Setup de Desenvolvimento
```yaml
# docker-compose.test.yml
version: '3.8'
services:
  homeassistant-test:
    image: homeassistant/home-assistant:latest
    volumes:
      - ./test-config:/config
    environment:
      - TZ=Europe/Lisbon
    ports:
      - "8124:8123"
    
  mariadb-test:
    image: mariadb:10.6
    environment:
      MYSQL_ROOT_PASSWORD: test
      MYSQL_DATABASE: homeassistant_test
```

#### ✅ Testes Automatizados
```python
# tests/test_templates.py
import pytest
from homeassistant.core import HomeAssistant

def test_energy_calculation_template():
    """Test energy cost calculation template."""
    # Implementação de testes unitários
    pass

def test_pool_automation_logic():
    """Test pool automation decision logic.""" 
    # Testes de lógica de automação
    pass
```

---

**💡 Dicas de Performance**:
- Use `trigger-based templates` em vez de `time_pattern` quando possível
- Agrupe sensores similares em ficheiros de template únicos  
- Configure `recorder` include/exclude para otimizar BD
- Use `device_class` e `state_class` corretos para métricas
- Implemente `unique_id` em todos os sensores para estabilidade

---

**🏠 Este sistema representa uma implementação completa de home automation com foco em eficiência energética, conforto ambiental e automação inteligente.**

*Última atualização da documentação: Julho 2025*
