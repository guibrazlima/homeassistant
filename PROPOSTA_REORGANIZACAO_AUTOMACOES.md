# 🎯 PROPOSTA DE REORGANIZAÇÃO DAS AUTOMAÇÕES

## 📊 ESTADO ATUAL

### Ficheiros Existentes
```
/automations/
├── automations.yaml              (2404 linhas, 53 automações) ❌ MISTURADO
├── automations_root.yaml         (212 linhas, 10 automações)  ❌ MISTURADO  
├── piscina_filtragem.yaml        (270 linhas, 17 automações)  ✅ BEM ORGANIZADO
└── ev_depois_bomba_piscina.yaml  (81 linhas, 3 automações)    ✅ BEM ORGANIZADO

TOTAL: 88 automações em 4 ficheiros
```

### Problemas Identificados
1. ❌ **84% das automações sem descrição** (`description: ''`)
2. ❌ **Automações misturadas** (piscina, portões, luzes tudo junto)
3. ❌ **Alguns IDs numéricos pouco descritivos**
4. ❌ **Falta de consistência** nos nomes e emojis
5. ❌ **Difícil manutenção** com ficheiros grandes

---

## 🎯 NOVA ESTRUTURA PROPOSTA

```
/data/homeassistant/
└── automations/
    ├── README.md                         # Documentação da estrutura
    │
    ├── 01_piscina/
    │   ├── filtragem_automatica.yaml    # 10 automações - Bomba dia/noite
    │   ├── filtragem_solar.yaml         # 8 automações - Excedente FV  
    │   ├── controlo_manual.yaml         # 5 automações - Watchdogs + botões
    │   ├── monitorizacao.yaml           # 6 automações - pH, temp, cobertura
    │   └── accesorios.yaml              # 3 automações - Cascata, hidrojet
    │
    ├── 02_ev_carregamento/
    │   ├── carregamento_inteligente.yaml  # 7 automações - Smart charging
    │   ├── gestao_horario.yaml            # 3 automações - Horários vazio
    │   ├── notificacoes.yaml              # 2 automações - Alertas
    │   └── integracao_piscina.yaml        # 3 automações - Após bomba
    │
    ├── 03_portoes_acessos/
    │   ├── portao_principal.yaml        # 4 automações - Abrir/fechar
    │   ├── botoes_fisicos.yaml          # 2 automações - Shelly + Sala
    │   ├── notificacoes.yaml            # 3 automações - Chegada, porta aberta
    │   └── iluminacao_garagem.yaml      # 1 automação - Luz automática
    │
    ├── 04_iluminacao/
    │   ├── luzes_automaticas.yaml       # 4 automações - Corredor, escadas, exterior
    │   ├── candeeiros_sala.yaml         # 1 automação - Controlo sala
    │   └── estores.yaml                 # 5 automações - Abrir/fechar automático
    │
    ├── 05_energia/
    │   ├── monitorizacao_solar.yaml     # 2 automações - Nuvens, forecast
    │   ├── precos_tarifa.yaml           # 1 automação - Coopernico
    │   └── ventilador_solar.yaml        # 1 automação - Cave
    │
    ├── 06_climatizacao/
    │   ├── bomba_calor.yaml             # 2 automações - MQTT, erros
    │   └── agua_quente.yaml             # 1 automação - Melhor preço
    │
    ├── 07_sistema/
    │   ├── backups.yaml                 # 5 automações - Full/partial backups
    │   ├── notificacoes_sistema.yaml    # 1 automação - UPS
    │   ├── actualizacoes.yaml           # 2 automações - Solcast, weather
    │   └── testes.yaml                  # 2 automações - SpeedTest, MQTT
    │
    ├── 08_assistentes_ia/
    │   ├── openai.yaml                  # 2 automações - Piscina, environmental
    │   └── telegram_bot.yaml            # 1 automação - Conversation
    │
    ├── 09_utilizadores/
    │   ├── gblima.yaml                  # 2 automações - User + notificações
    │   └── cmouta.yaml                  # 2 automações - User + notificações
    │
    └── 99_temporarias/
        ├── teste_desenvolvimento.yaml   # 2 automações - teste2, New automation
        └── deprecadas.yaml              # Automações antigas a remover

TOTAL: 11 diretórios, 35 ficheiros organizados
```

---

## 🆔 CONVENÇÃO DE IDs PROPOSTOS

### Formato Padrão
```yaml
id: 'categoria_funcionalidade_acao_numero'
```

### Exemplos por Categoria

#### 🏊 Piscina
```yaml
id: 'piscina_filtragem_dia_auto'
id: 'piscina_filtragem_noite_auto'
id: 'piscina_solar_arranque_fv'
id: 'piscina_solar_watchdog_2min'
id: 'piscina_manual_watchdog_1min'
id: 'piscina_monitor_ph_atualizar'
id: 'piscina_monitor_temp_atualizar'
id: 'piscina_monitor_cobertura_llm'
```

#### 🚗 EV Carregamento
```yaml
id: 'ev_smart_charging_start'
id: 'ev_smart_charging_stop'
id: 'ev_smart_charging_ac_limit'
id: 'ev_horario_permitir_2200'
id: 'ev_horario_reactivar_0800'
id: 'ev_notif_conectado'
id: 'ev_notif_ajuda_carregar'
```

#### 🚪 Portões
```yaml
id: 'portao_abrir_callback_mobile'
id: 'portao_abrir_botao_shelly'
id: 'portao_abrir_botao_sala'
id: 'portao_notif_chegada'
id: 'portao_notif_porta_aberta_alerta'
id: 'portao_ilum_garagem_auto'
```

#### 💡 Luzes
```yaml
id: 'luz_corredor_auto'
id: 'luz_escadas_superior_auto'
id: 'luz_exterior_auto'
id: 'luz_sala_candeeiros_control'
```

#### 🪟 Estores
```yaml
id: 'estore_sala_subir_manha'
id: 'estore_sala_baixar_sunset'
id: 'estore1_abrir_botao'
id: 'estore1_fechar_botao'
id: 'estore1_botao_sala_toggle'
```

---

## 📝 TEMPLATE DE DESCRIÇÃO

### Estrutura Padrão
```yaml
- id: 'automation_id_descritivo'
  alias: "🔰 Categoria: Nome Descritivo da Automação"
  description: |
    🎯 PROPÓSITO
    Descrição clara em 1-2 frases do que a automação faz.
    
    🔔 TRIGGERS (Quando executa)
    • Trigger 1: descrição
    • Trigger 2: descrição
    
    ✅ CONDITIONS (Se aplicável)
    • Condição 1
    • Condição 2
    
    ⚡ ACTIONS (O que faz)
    1. Ação principal
    2. Ação secundária
    3. Notificação (se aplicável)
    
    📊 ENTIDADES
    • entity_id1 - descrição
    • entity_id2 - descrição
    
    📌 NOTAS
    • Dependências: automation.xyz
    • Relacionado com: script.abc
    • Última atualização: YYYY-MM-DD
  
  trigger:
    - platform: state
      # ...
```

### Exemplo Completo (Piscina)
```yaml
- id: 'piscina_solar_arranque_fv'
  alias: "🏊 Piscina: Arranque com Excedente Solar"
  description: |
    🎯 PROPÓSITO
    Inicia a bomba da piscina quando há excedente de produção solar (FV),
    optimizando o consumo de energia e reduzindo custos.
    
    🔔 TRIGGERS
    • A cada 2 minutos (watchdog)
    • Quando excedente FV > threshold configurado
    
    ✅ CONDITIONS
    • Modo automático ativo (input_boolean.modo_automatico)
    • Sol acima do horizonte
    • Temperatura adequada (> 15°C)
    • Tempo de filtragem restante > 0
    
    ⚡ ACTIONS
    1. Liga bomba piscina (switch.pool_pump)
    2. Atualiza contador de minutos
    3. Regista no log: "Bomba iniciada por excedente FV"
    
    📊 ENTIDADES
    • sensor.solar_excess - Excedente FV em Watts
    • switch.pool_pump - Bomba da piscina
    • input_boolean.modo_automatico - Estado modo auto
    • sensor.pool_pump_remaining_time - Tempo restante
    
    📌 NOTAS
    • Relacionado com: piscina_solar_watchdog_2min
    • Depende de: PV Excess Control integration
    • Última atualização: 2025-11-11
  
  trigger:
    - platform: time_pattern
      minutes: "/2"
  
  condition:
    - condition: state
      entity_id: input_boolean.modo_automatico
      state: 'on'
    - condition: sun
      after: sunrise
      before: sunset
  
  action:
    - service: switch.turn_on
      target:
        entity_id: switch.pool_pump
    - service: system_log.write
      data:
        message: "🏊 Bomba piscina iniciada por excedente FV"
        level: info
  
  mode: single
```

---

## ✨ MELHORIAS ADICIONAIS PROPOSTAS

### 1. 🏷️ **Padronização de Emojis**
```yaml
🏊 Piscina
🚗 EV / Carregamento
🚪 Portões / Acessos
💡 Iluminação
🪟 Estores / Coberturas
⚡ Energia / Solar
♨️  Climatização / Aquecimento
🔔 Notificações
🤖 Automação / IA
👤 Utilizadores
🔧 Sistema / Manutenção
```

### 2. 📋 **Modes Consistentes**
```yaml
# Para automações que podem ser interrompidas
mode: restart

# Para automações que devem executar sequencialmente
mode: queued
max: 5

# Para automações únicas (não podem sobrepor)
mode: single

# Para automações paralelas
mode: parallel
max: 10
```

### 3. 🔄 **Trace Debugging**
```yaml
# Adicionar a TODAS as automações
trace:
  stored_traces: 5  # Guardar últimas 5 execuções
```

### 4. 🏷️ **Tags para Organização**
```yaml
# Adicionar tags para fácil filtragem na UI
tags:
  - piscina
  - energia
  - automatico
```

### 5. 📊 **Conditions como Choose**
```yaml
# Converter IF-THEN simples em Choose para melhor legibilidade
action:
  - choose:
      # Cenário 1: Dia
      - conditions:
          - condition: sun
            after: sunrise
            before: sunset
        sequence:
          - service: switch.turn_on
            target:
              entity_id: switch.pool_pump_day
      
      # Cenário 2: Noite
      - conditions:
          - condition: sun
            after: sunset
        sequence:
          - service: switch.turn_on
            target:
              entity_id: switch.pool_pump_night
    
    # Default: fazer nada
    default: []
```

### 6. 🛡️ **Error Handling**
```yaml
action:
  - service: cover.open_cover
    target:
      entity_id: cover.gate
    continue_on_error: true
  
  - delay: '00:00:02'
  
  # Validar se abriu
  - choose:
      - conditions:
          - condition: state
            entity_id: cover.gate
            state: 'open'
        sequence:
          - service: notify.telegram
            data:
              message: "✅ Portão aberto com sucesso"
    
    # Se falhou
    default:
      - service: notify.telegram
        data:
          message: "❌ ERRO: Portão não abriu!"
      - service: persistent_notification.create
        data:
          title: "Erro de Portão"
          message: "Verificar manualmente"
```

### 7. 📝 **Variables para Clareza**
```yaml
action:
  - variables:
      excess_threshold: 1500  # Watts
      min_temp: 15           # °C
      pump_entity: "switch.pool_pump"
  
  - condition: template
    value_template: >
      {{ states('sensor.solar_excess')|float(0) > excess_threshold }}
  
  - service: switch.turn_on
    target:
      entity_id: "{{ pump_entity }}"
```

---

## 📋 MAPEAMENTO DETALHADO (88 Automações)

### 🏊 PISCINA (32 automações)

#### **filtragem_automatica.yaml** (10)
1. `piscina_filtragem_dia_auto` - 🏊🏻 Bomba Piscina Dia
2. `piscina_filtragem_noite_auto` - 🏊🏻 Bomba Piscina Noite  
3. `piscina_filtragem_noite_horario` - 🏊 Actualizar Horario Bomba Piscina Noite
4. `piscina_filtragem_botao` - 🏊 Bomba piscina botão
5. `piscina_filtragem_automacao_toggle` - 🏊 Ligar/Desligar Automação Piscina
6. `piscina_filtragem_timer_variable` - 🏊 Variable Piscina timer
7. `piscina_filtragem_inicio_vazio` - 🏊🏻 Piscina - Início vazio 22:00
8. `piscina_filtragem_paragem_vazio` - 🏊🏻 Piscina - Paragem no vazio quando completar
9. `piscina_filtragem_paragem_0800` - 🏊🏻 Piscina - Paragem às 08:00
10. `piscina_filtragem_reset_diario` - 🏊🏻 Piscina - Reset diário minutos (08:00:05)

#### **filtragem_solar.yaml** (8)
1. `piscina_solar_arranque_fv` - 🏊🏻 Piscina - Arranque com excedente FV
2. `piscina_solar_watchdog_2min` - 🏊🏻 Piscina - Watchdog arranque FV (*/2min)
3. `piscina_solar_watchdog_2min_v2` - 🏊 Piscina - Watchdog arranque FV (*/2min) v2
4. `piscina_solar_paragem_objetivo` - 🏊🏻 Piscina - Paragem quando não há excedente ou objetivo cumprido
5. `piscina_solar_contador_minutos` - 🏊🏻 Piscina - Contador de minutos
6. `piscina_solar_restantes_calculo` - 🏊🏻 Piscina - Restantes = Recomendado − Corridos (auto)
7. `piscina_solar_optimization_old` - Pool Pump Solar Optimizationsdsdsd
8. `piscina_solar_arranque_fv_old` - 🏊 Piscina - Arranque com excedente FV (versão antiga)

#### **controlo_manual.yaml** (5)
1. `piscina_manual_watchdog_1min` - 🏊🏻 Piscina - Watchdog manual (*/1min)
2. `piscina_manual_terminou_auto` - 🏊🏻 Piscina - Manual terminou (voltar ao automático)
3. `piscina_manual_terminou_override` - Piscina - Manual terminou (desligar e sair do override)
4. `piscina_manual_snapshot_5min` - Piscina - Snapshot 5min
5. `piscina_automacao_bomba` - 🏊 Automação Bomba Piscina

#### **monitorizacao.yaml** (6)
1. `piscina_monitor_ph_atualizar` - 🏊Atualizar pH filtrado com bomba ligada
2. `piscina_monitor_temp_atualizar` - 🏊Atualizar Temperatura Piscina filtrado com bomba de
3. `piscina_monitor_cobertura_llm` - Piscina — Estado da cobertura (LLM Vision)
4. `piscina_monitor_bomba_peristaltica_sync` - 🏊🏻 Piscina - Sincronizar bomba piscina com bomba peristaltica
5. `piscina_monitor_bomba_peristaltica` - 🏊Bomba Peristaltica
6. `piscina_openai_daily` - OpenAI Daily: Piscina

#### **acessorios.yaml** (3)
1. `piscina_acessorio_cascata` - 🏊 Cascata
2. `piscina_acessorio_hidrojet` - 🏊 Hidrojet
3. `piscina_acessorio_ventilador_cave` - Ventilador Cave Solar

---

### 🚗 EV CARREGAMENTO (15 automações)

#### **carregamento_inteligente.yaml** (7)
1. `ev_smart_charging_start` - 🔋🚗⚡EV Smart Charging - Start
2. `ev_smart_charging_stop` - 🔋🚗⚡EV Smart Charging - Stop
3. `ev_smart_charging_ac_limit` - 🔋🚗⚡EV Smart Charging Set AC Current Limit
4. `ev_smart_soc_80` - 🔋🚗⚡EV Set SOC to 80%
5. `ev_smart_soc_dia` - 🔋🚗⚡EV Set Target SOC Dia
6. `ev_smart_completion_time` - 🔋🚗⚡Change charge completion time
7. `ev_climate_disable_away` - 🔋🚗⚡Disable i4 Climate if not home

#### **gestao_horario.yaml** (3)
1. `ev_horario_cfos_permitir_2200` - 🚗 EV (cFos) — Permitir às 22:00
2. `ev_horario_cfos_reactivar_0800` - 🚗 EV (cFos) — Reaplicar gate às 08:00
3. `ev_horario_cfos_depois_bomba` - 🚗 EV (cFos) — Só depois da bomba + Vazio 22:00–08:00

#### **notificacoes.yaml** (2)
1. `ev_notif_conectado` - 🔋🚗⚡EV Connected to Charger
2. `ev_notif_ajuda_carregar` - 🔋🚗⚡Help for charging at home
3. `ev_notif_ligar_carregador` - 💡🏡]Notificação para ligar o carro ao carregador

#### **integracao_piscina.yaml** (3)
- Ficheiro já existe: `ev_depois_bomba_piscina.yaml`
- Manter como está (bem organizado)

---

### 🚪 PORTÕES E ACESSOS (10 automações)

#### **portao_principal.yaml** (4)
1. `portao_abrir_callback_mobile` - 🏡 Callback to open gate from action
2. `portao_abrir_callback_notif` - 📢📲 Callback notification to open garage
3. `portao_status_monitor` - Status Portão
4. `portao_desligar_tudo_sala` - Desligar tudo Sala

#### **botoes_fisicos.yaml** (2)
1. `portao_botao_shelly_abrir` - 🏡 Botão shelly Abrir Portão
2. `portao_botao_sala_abrir` - 🏡Botão Sala Portão

#### **notificacoes.yaml** (3)
1. `portao_notif_chegada` - 📢🏡 Envia notificação para abrir o portão quando chega
2. `portao_notif_porta_aberta` - 📢🏡 Notify when garage door was left open for too long
3. `portao_notif_callback_garage` - 📢📲 Callback notification to open garage

#### **iluminacao_garagem.yaml** (1)
1. `portao_ilum_garagem_auto` - 💡🏡 Garage light on when gate opens/closes

---

### 💡 ILUMINAÇÃO (5 automações)

#### **luzes_automaticas.yaml** (4)
1. `luz_corredor_auto` - 💡Luz Corredor auto
2. `luz_escadas_superior_auto` - 💡Luz Escadas Superior Auto
3. `luz_exterior_auto` - 💡Luz Exterior Auto
4. `luz_sala_candeeiros` - 💡Candeeiros Ligar/Desligar

#### **estores.yaml** (5)
1. `estore_sala_subir_manha` - 🛋️ Sala: Subir estores manhã
2. `estore_sala_baixar_sunset` - 🛋️ Sala: Baixar Estores Sunset
3. `estore1_abrir` - 🪟Abrir Estore 1
4. `estore1_fechar` - 🪟Fechar Estore 1
5. `estore1_botao_sala` - 🪟Botão Sala Estore1

---

### ⚡ ENERGIA (4 automações)

#### **monitorizacao_solar.yaml** (2)
1. `energia_solar_nuvens_10_18` - ☁️Atualiza média de nuvens entre as 10:00 e as 18:00
2. `energia_solar_nuvens_8h` - ☁️Atualiza média de nuvens nas próximas 8h

#### **precos_tarifa.yaml** (1)
1. `energia_precos_coopernico` - Update Coopernico Prices

#### **solcast.yaml** (1)
1. `energia_solcast_update` - Solcast update

---

### ♨️ CLIMATIZAÇÃO (3 automações)

#### **bomba_calor.yaml** (2)
1. `clima_bomba_calor_mqtt` - ♨️ Bomba de Calor Power MQTT Publish
2. `clima_bomba_calor_erro` - ♨️ Heat Pump Error

#### **agua_quente.yaml** (1)
1. `clima_agua_quente_melhor_preco` - ♨️ Hot Water Production Best price

---

### 🔧 SISTEMA (10 automações)

#### **backups.yaml** (5)
1. `sistema_backup_auto` - Automatic Backups
2. `sistema_backup_full_1` - Creating a full backup (default action) [1]
3. `sistema_backup_full_2` - Creating a full backup (default action) [2]
4. `sistema_backup_full_3` - Creating a full backup (default action) [3]
5. `sistema_backup_partial` - Creating a partial backup (default action)

#### **notificacoes_sistema.yaml** (1)
1. `sistema_ups_notif` - 🔋UPS - Notification

#### **actualizacoes.yaml** (2)
1. `sistema_weather_forecast` - Call a service 'Weather: Get Forecast'
2. `sistema_solcast_update` - Solcast update

#### **testes.yaml** (2)
1. `sistema_speedtest` - SpeedTests
2. `sistema_mqtt_publish` - MQTT Publish

---

### 🤖 ASSISTENTES IA (3 automações)

#### **openai.yaml** (2)
1. `ia_openai_environmental` - OpenAI Daily: Environmental Notification
2. `ia_openai_piscina` - OpenAI Daily: Piscina

#### **telegram_bot.yaml** (1)
1. `ia_telegram_conversation` - Telegram Bot: Conversation with Assist

---

### 👤 UTILIZADORES (4 automações)

#### **gblima.yaml** (2)
1. `user_gblima_login` - gblima
2. `user_gblima_notif` - gblima notificações

#### **cmouta.yaml** (2)
1. `user_cmouta_login` - cmouta
2. `user_cmouta_notif` - cmouta notificações

---

### 🧪 TEMPORÁRIAS (2 automações)

#### **teste_desenvolvimento.yaml** (2)
1. `dev_teste2` - teste2
2. `dev_new_automation` - New automation

---

## 📝 RESUMO DA PROPOSTA

### Benefícios
✅ **Organização Clara**: 11 categorias lógicas  
✅ **Ficheiros Pequenos**: Média de 2-6 automações por ficheiro  
✅ **Fácil Manutenção**: Encontrar automação em segundos  
✅ **Melhor Documentação**: Descrições completas em todas  
✅ **IDs Descritivos**: Fácil identificação sem abrir ficheiro  
✅ **Consistência**: Padrões uniformes em tudo  
✅ **Escalabilidade**: Fácil adicionar novas automações  

### Estatísticas
- **Antes**: 4 ficheiros, média 22 automações/ficheiro
- **Depois**: 35 ficheiros, média 2.5 automações/ficheiro
- **Redução**: Ficheiros 90% mais pequenos
- **Descrições**: 0% → 100% preenchidas
- **IDs**: Numéricos → Descritivos semânticos

---

## ⏭️ PRÓXIMOS PASSOS

1. **Revisão do Utilizador** ✋ (AGUARDAR APROVAÇÃO)
2. Criar backup completo
3. Criar estrutura de diretórios
4. Gerar ficheiros individuais com descrições
5. Atualizar `configuration.yaml`
6. Testar configuração (`ha core check`)
7. Commit e push
8. Remover ficheiros antigos (após validação)

---

**Criado por**: GitHub Copilot  
**Data**: 2025-11-11  
**Versão**: 1.0
