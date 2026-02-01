# 🚀 SUGESTÕES DE MELHORIAS

## Para o Sistema de Controlo Solar da Piscina

---

## ✅ Melhorias JÁ IMPLEMENTADAS no Blueprint

### 1️⃣ **Delays Configuráveis** (era hardcoded)
```yaml
# ANTES (binary_sensor):
delay_on: "00:00:20"   # Fixo
delay_off: "00:00:30"  # Fixo

# DEPOIS (blueprint):
delay_on: 30      # Configurável via UI (5-300s)
delay_off: 60     # Configurável via UI (5-300s)
```
**Benefício:** Ajuste fino sem editar YAML.

---

### 2️⃣ **Tempo Mínimo Ligada** (era inexistente)
```yaml
# ANTES: Podia desligar imediatamente
# DEPOIS:
min_on_time: 5  # Mínimo 5 minutos ligada
```
**Benefício:** Protege motor de ciclos curtos, reduz desgaste.

---

### 3️⃣ **Margem Extra para Arranque** (era inexistente)
```yaml
# ANTES: Ligava mesmo no limite
if predicted_import <= 700W: turn_on()

# DEPOIS: Margem de segurança
start_margin: 100W
if predicted_import <= (700 - 100): turn_on()  # <= 600W
```
**Benefício:** Evita ligar quando está "mesmo no limite" e depois desligar logo.

---

### 4️⃣ **Consumo Real da Bomba** (era só nominal)
```yaml
# ANTES: Sempre usava valor fixo
pump = 800W  # Estimativa

# DEPOIS: Usa sensor real se disponível
pump_actual_power: sensor.bomba_piscina_power
# Usa valor real quando disponível, fallback para nominal
```
**Benefício:** Cálculos mais precisos, detecta anomalias.

---

### 5️⃣ **Horários Configuráveis** (era hardcoded ou inexistente)
```yaml
# ANTES: Sempre sunrise/sunset fixo

# DEPOIS:
sun_offset_start: 30  # 30min após nascer
sun_offset_end: 30    # 30min antes pôr
```
**Benefício:** Ajusta janela de operação (ex: evitar sol fraco manhã cedo).

---

### 6️⃣ **Integração Completa** (era separado)
```yaml
# ANTES: Binary sensor + automação separada + watchdog

# DEPOIS: Tudo num único blueprint
- Sensores
- Lógica
- Ações
- Delays
- Condições
- Logs
```
**Benefício:** Manutenção mais fácil, menos código.

---

### 7️⃣ **Logs de Diagnóstico Opcionais** (era inexistente)
```yaml
enable_debug_logs: true

# Gera logs como:
🏊 Piscina Solar: source=house+pv, export=1820W, import_pred=0W, 
                  import_curr=0W, limit=700W, pump_on=false, should_on=true
```
**Benefício:** Debug fácil sem modificar código.

---

## 💡 SUGESTÕES PARA MELHORIAS FUTURAS

### 🔮 Nível 1: Fácil de Implementar

#### A) **Notificações Inteligentes**
```yaml
# Notificar quando:
- Bomba não liga há 2+ dias (possível falha)
- Sensor falhou (usando fallback)
- Filtragem diária não atingida
- Consumo anormal (muito alto ou muito baixo)
```

**Implementação:**
```yaml
- if:
    - condition: template
      value_template: "{{ pump_is_on and pump_actual_power < 100 }}"
  then:
    - service: notify.mobile
      data:
        title: "⚠️ Bomba Piscina"
        message: "Bomba ligada mas sem consumo! Verificar."
```

---

#### B) **Estatísticas Automáticas**
```yaml
# Criar sensores de estatísticas:
- sensor.piscina_tempo_filtragem_solar_hoje
- sensor.piscina_energia_solar_usada_hoje
- sensor.piscina_energia_importada_hoje
- sensor.piscina_poupanca_hoje
```

**Implementação:** Usar `utility_meter` com condição.

---

#### C) **Dashboard Card Automático**
```yaml
# Gerar card mushroom/custom para dashboard
- Excedente disponível
- Estado bomba
- Tempo filtragem hoje
- Próxima ação esperada
```

---

### 🔮 Nível 2: Médio

#### D) **Previsão Solar (Solcast)**
```yaml
solar_forecast: sensor.solcast_forecast_remaining_today

# Lógica:
if forecast > battery_needed + filtration_needed:
    # Pode ser mais agressivo (import_limit mais alto)
else:
    # Ser conservador (priorizar bateria)
```
**Benefício:** Decisões baseadas no futuro, não só presente.

---

#### E) **Coordenação com Outros Aparelhos**
```yaml
# Sistema de prioridades:
priority:
  1: Bateria (até 80%)
  2: Bomba piscina
  3: Aquecimento piscina
  4: Carro elétrico
  5: Ar condicionado

# Lógica:
available_excess = total_export - sum(higher_priority_needs)
if available_excess >= pump_power:
    turn_on()
```
**Benefício:** Não desperdiça excedente, coordena tudo.

---

#### F) **Aprendizagem de Padrões**
```yaml
# Aprender padrões diários:
- Hora típica de início de excedente
- Hora típica de fim de excedente
- Dias com melhor produção (histórico)
- Correlação clima/produção

# Usar para pré-aquecer decisões
if approaching_typical_excess_time:
    reduce_delay_on  # Resposta mais rápida
```

---

### 🔮 Nível 3: Avançado

#### G) **Integração com Tarifas Dinâmicas**
```yaml
# Se tiver tarifa indexada (OMIE):
current_price: sensor.omie_price

# Ajustar import_limit dinamicamente:
if current_price < offpeak_price:
    import_limit = pump_power  # Pode importar tudo!
elif current_price > 2 * offpeak_price:
    import_limit = 0  # Só com excedente puro
```
**Benefício:** Otimização económica real-time.

---

#### H) **Previsão Meteorológica**
```yaml
# Integrar com weather:
weather_forecast: weather.home

# Ajustar comportamento:
if forecast == "cloudy":
    start_margin = 0  # Aproveitar qualquer excedente
    delay_on = 10s    # Resposta rápida
elif forecast == "sunny":
    start_margin = 200  # Pode ser selectivo
    delay_on = 60s      # Mais calmo
```

---

#### I) **Machine Learning Local**
```yaml
# Usar pyscript ou AppDaemon para ML:
- Prever produção solar das próximas 2h
- Prever consumo da casa
- Otimizar scheduling da bomba

# Treinar com:
- Histórico de produção
- Histórico de consumo
- Hora do dia
- Dia da semana
- Época do ano
```

---

## 🎯 PRIORIZAÇÃO RECOMENDADA

### Implementar Agora (Fácil, Alto Impacto)
1. ✅ **Já feito:** Blueprint base com todas as melhorias básicas

### Implementar Esta Semana
2. 📊 **Estatísticas:** Adicionar utility_meters para tracking
3. 📱 **Notificações:** Alertas básicos de falha

### Implementar Este Mês
4. ☀️ **Solcast:** Integrar previsão solar
5. 🎛️ **Dashboard:** Card de monitorização

### Implementar Próximos 3 Meses
6. 🔗 **Coordenação:** Sistema multi-aparelho
7. 💶 **Tarifas:** Integração OMIE (se aplicável)

### Futuro
8. 🧠 **ML:** Aprendizagem de padrões
9. 🌤️ **Meteorologia:** Previsão avançada

---

## 📋 ROADMAP DETALHADO

### v1.0 (Atual) ✅
- [x] Blueprint funcional
- [x] Delays configuráveis
- [x] Tempo mínimo ON
- [x] Margem arranque
- [x] Consumo real opcional
- [x] Horários configuráveis
- [x] Override manual
- [x] Integração filtragem
- [x] Logs diagnóstico
- [x] 3 níveis fallback

### v1.1 (Próxima)
- [ ] Notificações de erro
- [ ] Notificação filtragem insuficiente
- [ ] Detecção anomalias consumo
- [ ] Contador estatísticas

### v1.2
- [ ] Integração Solcast
- [ ] Dashboard card
- [ ] Previsão próximas horas

### v2.0
- [ ] Coordenação multi-aparelho
- [ ] Sistema prioridades
- [ ] Fila de espera automática

### v2.1
- [ ] Tarifas dinâmicas OMIE
- [ ] Otimização económica avançada
- [ ] Relatórios mensais

### v3.0
- [ ] Machine learning
- [ ] Previsão consumo
- [ ] Scheduling otimizado

---

## 🔧 CÓDIGO EXEMPLO: Estatísticas

### utility_meter para Energia Solar Usada
```yaml
# configuration.yaml

utility_meter:
  piscina_energia_solar_diaria:
    source: sensor.bomba_piscina_energy
    name: "Piscina - Energia Solar Diária"
    cycle: daily
    # Só conta quando há excedente
    
sensor:
  - platform: template
    sensors:
      piscina_energia_quando_solar:
        friendly_name: "Energia Piscina (quando solar)"
        unit_of_measurement: "kWh"
        device_class: energy
        state: >-
          {% if is_state('binary_sensor.piscina_excedente_fv_bomba', 'on') %}
            {{ states('sensor.bomba_piscina_energy') }}
          {% else %}
            {{ states('sensor.piscina_energia_quando_solar') }}
          {% endif %}
```

### Contador de Tempo Filtragem Solar
```yaml
# history_stats sensor
sensor:
  - platform: history_stats
    name: "Piscina - Tempo Filtragem Solar Hoje"
    entity_id: switch.bomba_piscina_switch_0
    state: "on"
    type: time
    start: "{{ today_at('00:00') }}"
    end: "{{ now() }}"
```

---

## 🔧 CÓDIGO EXEMPLO: Notificações

### Alerta Bomba Sem Consumo
```yaml
automation:
  - alias: "🏊 Alerta: Bomba sem consumo"
    trigger:
      - platform: state
        entity_id: switch.bomba_piscina_switch_0
        to: "on"
        for: "00:02:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.bomba_piscina_power
        below: 100
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Bomba Piscina"
          message: >-
            Bomba ligada há 2 minutos mas consumo só 
            {{ states('sensor.bomba_piscina_power') }}W!
            Verificar se está a funcionar.
```

### Alerta Filtragem Insuficiente
```yaml
automation:
  - alias: "🏊 Alerta: Filtragem insuficiente"
    trigger:
      - platform: time
        at: "20:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.piscina_tempo_filtragem_solar_hoje
        below: 2  # Menos de 2 horas
    action:
      - service: notify.mobile_app
        data:
          title: "🏊 Filtragem Baixa"
          message: >-
            Hoje a piscina só filtrou 
            {{ states('sensor.piscina_tempo_filtragem_solar_hoje') }} horas.
            Considere filtragem noturna.
```

---

## 📊 CÓDIGO EXEMPLO: Dashboard Card

### Mushroom Card para Piscina Solar
```yaml
type: custom:mushroom-template-card
primary: Bomba Piscina
secondary: >-
  {% if is_state('switch.bomba_piscina_switch_0', 'on') %}
    ON • {{ states('sensor.bomba_piscina_power') }}W
  {% else %}
    OFF • Excedente: {{ states('binary_sensor.piscina_excedente_fv_bomba') }}
  {% endif %}
icon: mdi:pool
icon_color: >-
  {% if is_state('switch.bomba_piscina_switch_0', 'on') %}
    blue
  {% elif is_state('binary_sensor.piscina_excedente_fv_bomba', 'on') %}
    green
  {% else %}
    grey
  {% endif %}
entity: switch.bomba_piscina_switch_0
tap_action:
  action: toggle
hold_action:
  action: more-info
```

---

## 🎉 CONCLUSÃO

### O Blueprint Já Inclui:
- ✅ Todas as funcionalidades do binary_sensor original
- ✅ Melhorias de configurabilidade (delays, margens, tempos)
- ✅ Proteções adicionais (tempo mínimo, override)
- ✅ Diagnóstico integrado (logs)
- ✅ Tudo-em-um (sem automação separada)

### Próximos Passos Recomendados:
1. **Testar** blueprint por 1 semana
2. **Adicionar** estatísticas (utility_meter)
3. **Adicionar** notificações básicas
4. **Integrar** Solcast quando estável
5. **Considerar** coordenação multi-aparelho

---

**Queres que implemente alguma destas melhorias agora?** 😊

---

*Documento de sugestões*  
*Criado: 1 Fevereiro 2026*  
*Baseado em: binary_sensor.piscina_excedente_fv_bomba*
