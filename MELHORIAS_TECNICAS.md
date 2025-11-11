# 🚀 Melhorias Técnicas Sugeridas

## 📋 Índice
1. [Boas Práticas YAML](#boas-práticas-yaml)
2. [Segurança e Validações](#segurança-e-validações)
3. [Performance e Otimização](#performance-e-otimização)
4. [Notificações e Alertas](#notificações-e-alertas)
5. [Integração com Outros Sistemas](#integração-com-outros-sistemas)
6. [Monitorização e Logs](#monitorização-e-logs)

---

## 1. Boas Práticas YAML

### ✅ IDs Descritivos vs Numéricos

**Problema Atual:**
```yaml
id: '1759864348160'  # Impossível saber o que faz
```

**Solução:**
```yaml
id: portao_botao_shelly_abrir  # Auto-explicativo
```

**Benefícios:**
- ✅ Fácil de ler e debugar
- ✅ Mantém histórico mesmo mudando alias
- ✅ Facilita referências em outras automações
- ✅ Melhor para git diff

---

### ✅ Modo de Execução

**Adicionar sempre:**
```yaml
mode: single          # Apenas uma execução de cada vez
max_exceeded: warning # Avisar se tentar executar novamente
```

**Opções disponíveis:**
- `single` - Uma execução (recomendado para portões, luzes)
- `restart` - Cancela anterior e reinicia (sensores)
- `queued` - Fila de espera (notificações)
- `parallel` - Múltiplas simultâneas (watchdogs)

---

### ✅ Descrições Completas

**Problema Atual:**
```yaml
description: ''  # Vazio
```

**Solução:**
```yaml
description: |
  Abre o portão principal quando botão é pressionado.
  
  Funcionamento:
  - Detecta pressão no botão Shelly
  - Aciona motor por 30 segundos
  - Envia notificação
  
  Dispositivos:
  - Trigger: binary_sensor.botao_shelly
  - Action: switch.portao_motor
```

---

## 2. Segurança e Validações

### 🔒 Condições de Segurança

**Adicionar sempre que aplicável:**

```yaml
condition:
  # 1. Sistema operacional
  - condition: state
    entity_id: binary_sensor.sistema_operacional
    state: 'on'
  
  # 2. Horário permitido
  - condition: time
    after: '06:00:00'
    before: '23:00:00'
  
  # 3. Modo casa (não ausente)
  - condition: state
    entity_id: input_select.modo_casa
    state: 'Normal'
  
  # 4. Não está em manutenção
  - condition: state
    entity_id: input_boolean.modo_manutencao
    state: 'off'
  
  # 5. Dispositivo disponível
  - condition: template
    value_template: "{{ states('switch.portao_motor') != 'unavailable' }}"
```

---

### 🔒 Timeouts e Limites

**Prevenir loops infinitos:**

```yaml
action:
  # Timeout em wait_for_trigger
  - wait_for_trigger:
      - platform: state
        entity_id: binary_sensor.portao_aberto
        to: 'on'
    timeout:
      seconds: 35
    continue_on_timeout: true
  
  # Verificar se timeout ocorreu
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ wait.trigger is none }}"
        sequence:
          - service: notify.mobile_app
            data:
              message: "⚠️ Timeout: Portão não respondeu"
```

---

### 🔒 Tratamento de Erros

**Capturar erros comuns:**

```yaml
action:
  # Tentar executar
  - service: switch.turn_on
    target:
      entity_id: switch.portao_motor
    continue_on_error: true
  
  # Verificar se funcionou
  - delay:
      seconds: 2
  
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ states('switch.portao_motor') == 'unavailable' }}"
        sequence:
          - service: persistent_notification.create
            data:
              title: "🚨 Erro Crítico"
              message: "Motor do portão não responde!"
              notification_id: erro_portao_motor
```

---

## 3. Performance e Otimização

### ⚡ Reduzir Triggers Desnecessários

**Problema:**
```yaml
# Trigger a cada mudança de estado
trigger:
  - platform: state
    entity_id: sensor.temperatura_piscina
```

**Solução:**
```yaml
# Trigger apenas quando passa limiar
trigger:
  - platform: numeric_state
    entity_id: sensor.temperatura_piscina
    above: 28
    for:
      minutes: 5  # Debounce de 5 minutos
```

---

### ⚡ Templates Eficientes

**Evitar:**
```yaml
# Recalcula a cada mudança
value_template: >
  {{ states.sensor | selectattr('state', 'eq', 'on') | list | count > 5 }}
```

**Preferir:**
```yaml
# Usa valor direto
value_template: "{{ states('sensor.count_devices_on') | int > 5 }}"
```

---

### ⚡ Agrupar Ações Similares

**Antes:**
```yaml
- service: light.turn_on
  target:
    entity_id: light.sala
- service: light.turn_on
  target:
    entity_id: light.cozinha
- service: light.turn_on
  target:
    entity_id: light.corredor
```

**Depois:**
```yaml
- service: light.turn_on
  target:
    entity_id:
      - light.sala
      - light.cozinha
      - light.corredor
```

---

## 4. Notificações e Alertas

### 📱 Notificações Estruturadas

**Boas práticas:**

```yaml
- service: notify.mobile_app
  data:
    title: "🚪 Portão Principal"
    message: "Portão aberto às {{ now().strftime('%H:%M') }}"
    data:
      # Tag para substituir notificação anterior
      tag: portao_estado
      
      # Grupo para organizar
      group: seguranca
      
      # Ícone
      notification_icon: mdi:gate-open
      
      # Canal Android
      channel: Portões
      
      # Prioridade
      importance: default
      
      # Som
      sound: default
      
      # Vibração
      vibrationPattern: "100, 200, 100"
      
      # Imagem
      image: /api/camera_proxy/camera.portao
      
      # Ações
      actions:
        - action: FECHAR_PORTAO
          title: "Fechar"
          icon: mdi:gate
        - action: VER_CAMERA
          title: "Ver Câmara"
          icon: mdi:cctv
```

---

### 📱 Níveis de Prioridade

```yaml
# 🔴 CRÍTICO - Emergências
importance: high
ttl: 0
priority: high

# 🟡 IMPORTANTE - Requer atenção
importance: default
ttl: 300

# 🟢 INFORMATIVO - Pode esperar
importance: low
ttl: 3600
```

---

## 5. Integração com Outros Sistemas

### 🔗 Google Home / Alexa

**Criar helpers para controlo por voz:**

```yaml
# input_boolean.yaml
portao_principal:
  name: "Portão Principal"
  icon: mdi:gate

# script.yaml
abrir_portao:
  alias: "Abrir Portão"
  sequence:
    - service: switch.turn_on
      target:
        entity_id: switch.portao_motor

# Depois usar no Google Home:
# "Ok Google, ligar portão principal"
```

---

### 🔗 Integrações Externas

**Webhooks para integrações:**

```yaml
# Receber comandos externos
trigger:
  - platform: webhook
    webhook_id: abrir_portao_webhook
    allowed_methods:
      - POST
    local_only: false

# Enviar para sistemas externos
action:
  - service: rest_command.notificar_portao_aberto
    data:
      timestamp: "{{ now().isoformat() }}"
      device: "portao_principal"
```

---

## 6. Monitorização e Logs

### 📊 Logs Estruturados

**Registar eventos importantes:**

```yaml
action:
  # Início
  - service: logbook.log
    data:
      name: "Sistema Portão"
      message: "Abertura iniciada ({{ trigger.to_state.attributes.friendly_name }})"
      entity_id: switch.portao_motor
      domain: automation
  
  # ... ações ...
  
  # Sucesso
  - service: logbook.log
    data:
      name: "Sistema Portão"
      message: "Abertura concluída com sucesso"
  
  # Erro (se aplicável)
  - service: logbook.log
    data:
      name: "Sistema Portão"
      message: "⚠️ ERRO: Timeout na abertura"
```

---

### 📊 Contadores e Estatísticas

**Criar sensores para monitorizar:**

```yaml
# sensor.yaml
- platform: history_stats
  name: "Portão - Aberturas Hoje"
  entity_id: binary_sensor.portao_aberto
  state: 'on'
  type: count
  start: "{{ now().replace(hour=0, minute=0, second=0) }}"
  end: "{{ now() }}"

# Usar em automação
condition:
  - condition: numeric_state
    entity_id: sensor.portao_aberturas_hoje
    below: 20  # Máximo 20 aberturas/dia
```

---

### 📊 Watchdogs Inteligentes

**Monitorizar saúde do sistema:**

```yaml
- id: watchdog_portao_motor
  alias: 🔧 Watchdog - Motor Portão
  description: Verifica se motor responde corretamente
  
  trigger:
    - platform: time_pattern
      minutes: '/30'  # A cada 30 minutos
  
  condition:
    - condition: template
      value_template: >
        {{ (as_timestamp(now()) - 
            as_timestamp(states.switch.portao_motor.last_changed)) 
            > 86400 }}  # 24 horas sem mudança
  
  action:
    - service: persistent_notification.create
      data:
        title: "⚠️ Watchdog - Portão"
        message: |
          Motor do portão sem atividade há mais de 24h.
          Última ativação: {{ states.switch.portao_motor.last_changed }}
        notification_id: watchdog_portao
```

---

## 📝 Checklist de Implementação

Ao reorganizar cada automação, verificar:

- [ ] ID descritivo (não numérico)
- [ ] Descrição completa com contexto
- [ ] Mode definido (single/restart/queued/parallel)
- [ ] Condições de segurança apropriadas
- [ ] Timeouts em wait_for_trigger
- [ ] Tratamento de erros
- [ ] Notificações estruturadas
- [ ] Logs em eventos importantes
- [ ] Templates otimizados
- [ ] Comentários em lógica complexa

---

## 🎯 Prioridades de Implementação

### Fase 1 - CRÍTICO (Fazer Sempre)
- ✅ IDs descritivos
- ✅ Mode e max_exceeded
- ✅ Descrições básicas

### Fase 2 - IMPORTANTE (Segurança)
- ✅ Condições de segurança
- ✅ Timeouts
- ✅ Tratamento de erros

### Fase 3 - RECOMENDADO (UX)
- ✅ Notificações estruturadas
- ✅ Logs detalhados
- ✅ Comentários

### Fase 4 - OPCIONAL (Avançado)
- ⭕ Watchdogs
- ⭕ Estatísticas
- ⭕ Integrações externas

---

**Próximo:** Ver `PROPOSTA_REORGANIZACAO.md` para estrutura completa!
