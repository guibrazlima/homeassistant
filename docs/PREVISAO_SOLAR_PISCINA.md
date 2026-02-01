# ☀️ PREVISÃO SOLAR NO CONTROLO DA PISCINA

## Para Que Serve e Como Usar

---

## 📊 Sensores Solcast Disponíveis

Com a integração Solcast instalada, tens acesso a:

| Sensor | Descrição | Unidade | Uso |
|--------|-----------|---------|-----|
| `sensor.solcast_pv_forecast_forecast_remaining_today` | Energia restante hoje | kWh | ⭐ Principal |
| `sensor.solcast_pv_forecast_forecast_today` | Previsão total hoje | kWh | Referência |
| `sensor.solcast_pv_forecast_forecast_tomorrow` | Previsão amanhã | kWh | Planeamento |
| `sensor.solcast_pv_forecast_power_now` | Potência esperada agora | W | Real-time |
| `sensor.solcast_pv_forecast_power_now_30m` | Potência em 30min | W | Antecipar |
| `sensor.solcast_pv_forecast_power_now_1hr` | Potência em 1 hora | W | Antecipar |
| `sensor.solcast_pv_forecast_peak_forecast_today` | Pico esperado hoje | W | Dimensionar |
| `sensor.solcast_pv_forecast_peak_time_today` | Hora do pico | Hora | Agendar |

---

## 🎯 CASOS DE USO PARA A PISCINA

### 1️⃣ **Decisão Mais Agressiva com Sol Garantido**

**Problema:** Sistema conservador não liga a bomba quando há pouco excedente, mas vai haver muito sol depois.

**Solução com Forecast:**
```python
# Lógica atual (sem forecast):
if export_available >= pump_power:
    turn_on()  # Só liga quando JÁ há excedente

# Lógica melhorada (com forecast):
if forecast_remaining >= filtration_needed + buffer:
    # Há sol suficiente garantido para o dia
    # Posso ser mais agressivo
    import_limit = import_limit * 1.5  # Aceita mais importação
    start_margin = 0  # Liga mais cedo
```

**Exemplo Prático:**
```
Situação: 09:00, nuvens passageiras
- Export atual: 300W (abaixo dos 800W da bomba)
- Forecast restante: 25 kWh (sol forte esperado)
- Filtragem necessária: 5 kWh (~6 horas)

SEM Forecast: Espera... espera... talvez ligue às 11:00
COM Forecast: "Tenho 25 kWh garantidos, preciso 5 → Posso ligar JÁ!"
```

---

### 2️⃣ **Filtragem Noturna de Backup**

**Problema:** Dia nublado → bomba não correu → água suja amanhã.

**Solução:**
```yaml
# Às 20:00, verificar:
if filtration_today < minimum_required:
    if forecast_tomorrow < threshold:  # Amanhã também mau
        schedule_night_filtration()  # Filtrar esta noite
    else:
        # Amanhã há sol, pode esperar
        skip_night_filtration()
```

**Exemplo Prático:**
```
Situação: 20:00, bomba correu só 2 horas (mínimo: 6h)
- Forecast amanhã: 8 kWh (dia nublado previsto)

DECISÃO: Agendar filtragem noturna para compensar!
         Usar tarifa vazio (mais barato)
```

---

### 3️⃣ **Otimização com Bateria Doméstica**

**Problema:** Se tiver bateria, preciso garantir que carrega antes do fim do dia.

**Solução:**
```python
battery_capacity = 10  # kWh
battery_current = 60   # %
battery_target = 80    # % ao fim do dia
battery_needed = battery_capacity * (battery_target - battery_current) / 100
# = 10 * (80-60) / 100 = 2 kWh

forecast_remaining = 15  # kWh

available_for_pool = forecast_remaining - battery_needed - house_consumption
# = 15 - 2 - 5 = 8 kWh → Pode filtrar à vontade!
```

---

### 4️⃣ **Antecipação de Nuvens (30min/1h)**

**Problema:** Nuvem grande a chegar → bomba vai desligar → pode ligar noutro aparelho antes.

**Solução:**
```python
power_now = 2500W
power_in_30min = 800W  # Nuvem a chegar!

if power_in_30min < pump_power:
    # Aumentar delay_off para não desligar
    # OU avisar sistema de coordenação
    prepare_for_drop()
```

---

### 5️⃣ **Scheduling Inteligente**

**Problema:** Quando é a melhor hora para correr a bomba?

**Solução:**
```python
# Analisar forecast horário:
peak_power = 3500W  # às 13:00
peak_time = "13:00"

# Se bomba precisa 800W:
# Melhor janela = peak_time ± 2h = 11:00-15:00

# Agendar automações adicionais (aquecimento, etc)
# para horas de pico quando há mais margem
```

---

### 6️⃣ **Decisão de Ligar Imediatamente vs Esperar**

**Cenário A:** Sol fraco agora, forte depois
```
09:00 - PV: 500W, Forecast restante: 20 kWh
→ ESPERAR (vai haver muito mais)
```

**Cenário B:** Sol forte agora, nuvens depois
```
09:00 - PV: 2000W, Forecast restante: 5 kWh (já é quase tudo)
→ LIGAR JÁ! (aproveitar enquanto há)
```

---

## 🔧 COMO FUNCIONA NO BLUEPRINT

### Parâmetros Adicionados:

```yaml
# Sensores de Previsão
forecast_remaining:
  name: "☀️ Previsão Solar Restante Hoje"
  description: >
    Sensor com kWh previstos para o resto do dia.
    Exemplo: sensor.solcast_pv_forecast_forecast_remaining_today
  
forecast_tomorrow:
  name: "🌅 Previsão Solar Amanhã"
  description: >
    Sensor com kWh previstos para amanhã.
    Usado para decidir filtragem noturna.
  
power_forecast_1h:
  name: "⏰ Previsão Potência 1h"
  description: >
    Potência esperada daqui a 1 hora.
    Ajuda a antecipar quedas/subidas.

# Configurações de Forecast
min_daily_filtration_kwh:
  name: "⚡ Energia Mínima Filtragem Diária (kWh)"
  description: >
    Energia mínima que a bomba deve consumir por dia.
    Típico: 5-8 kWh (6-10 horas × 800W)
  default: 6

forecast_confidence_factor:
  name: "📊 Factor Confiança Previsão (%)"
  description: >
    Quanto confiar na previsão. 80% = conservador.
    100% = confia totalmente na previsão.
  default: 85

enable_night_backup:
  name: "🌙 Ativar Filtragem Noturna Backup"
  description: >
    Se filtragem solar insuficiente E amanhã mau,
    agenda filtragem noturna automática.
  default: false
```

### Lógica Melhorada:

```python
# ═══════════════════════════════════════════════════
# VARIÁVEIS DE FORECAST
# ═══════════════════════════════════════════════════

forecast_remaining_kwh = states(forecast_remaining)|float(0)
forecast_tomorrow_kwh = states(forecast_tomorrow)|float(0)
power_forecast_1h = states(power_forecast_1h)|float(0)

# Ajustar por factor de confiança
adjusted_forecast = forecast_remaining_kwh * (forecast_confidence_factor / 100)

# Energia necessária para filtragem restante
filtration_done_today = states(filtration_energy_sensor)|float(0)
filtration_needed = max(min_daily_filtration_kwh - filtration_done_today, 0)

# ═══════════════════════════════════════════════════
# 🆕 ESTIMATIVA DINÂMICA CONSUMO DA CASA
# ═══════════════════════════════════════════════════

# Horas restantes até pôr do sol
hours_until_sunset = max((sunset - now()).total_seconds() / 3600, 0)

# Consumo atual da casa (sem bomba)
house_power_now = states(house_power_no_pump)|float(600)  # W

# Opção 1: Usar consumo atual × horas restantes (dinâmico)
house_consumption_estimate = (house_power_now / 1000) * hours_until_sunset * 1.2  # kWh

# Opção 2: Usar valor médio configurado (fixo)
# house_consumption_estimate = (house_avg_power / 1000) * hours_until_sunset  # kWh

# Energia disponível para piscina (com margem de segurança)
available_for_pool = adjusted_forecast - house_consumption_estimate - battery_needed

# ═══════════════════════════════════════════════════
# DECISÕES BASEADAS EM FORECAST
# ═══════════════════════════════════════════════════

# Modo de operação baseado em forecast
if available_for_pool >= filtration_needed * 1.5:
    # MODO RELAXADO: Muito sol garantido
    mode = "aggressive"
    effective_import_limit = import_limit * 1.5
    effective_start_margin = 0
    effective_delay_on = delay_on * 0.5
    
elif available_for_pool >= filtration_needed:
    # MODO NORMAL: Sol suficiente
    mode = "normal"
    effective_import_limit = import_limit
    effective_start_margin = start_margin
    effective_delay_on = delay_on
    
elif available_for_pool >= filtration_needed * 0.5:
    # MODO CONSERVADOR: Sol escasso
    mode = "conservative"
    effective_import_limit = import_limit * 0.7
    effective_start_margin = start_margin * 2
    effective_delay_on = delay_on * 1.5
    
else:
    # MODO EMERGÊNCIA: Muito pouco sol
    mode = "emergency"
    # Aceitar mais importação para garantir mínimo
    effective_import_limit = import_limit * 2
    effective_start_margin = 0

# ═══════════════════════════════════════════════════
# ANTECIPAÇÃO (POWER IN 1H)
# ═══════════════════════════════════════════════════

# Se potência vai cair muito, preparar
power_drop_expected = (pv_w - power_forecast_1h) / pv_w if pv_w > 0 else 0

if power_drop_expected > 0.5:  # Queda > 50%
    # Nuvem grande a chegar
    if pump_is_on:
        # Aumentar delay_off para não desligar cedo demais
        effective_delay_off = delay_off * 2
    else:
        # Não vale a pena ligar agora
        should_wait = true
```

---

## 📊 DIAGRAMA DE DECISÃO COM FORECAST

```
                         ┌────────────────────┐
                         │ Atualização Sensor │
                         └─────────┬──────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ Calcular Forecast Disponível │
                    │ = remaining × confidence     │
                    │ - house_estimate             │
                    └──────────────┬──────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
    ┌─────────▼─────────┐ ┌───────▼────────┐ ┌────────▼────────┐
    │  available >=     │ │ available >=   │ │ available <     │
    │  needed × 1.5     │ │ needed         │ │ needed × 0.5    │
    └─────────┬─────────┘ └───────┬────────┘ └────────┬────────┘
              │                   │                    │
    ┌─────────▼─────────┐ ┌───────▼────────┐ ┌────────▼────────┐
    │ MODO AGRESSIVO    │ │ MODO NORMAL    │ │ MODO EMERGÊNCIA │
    │ - Menos delays    │ │ - Padrão       │ │ - Aceita import │
    │ - Menos margem    │ │                │ │ - Prioridade    │
    │ - Liga mais cedo  │ │                │ │ - Força ligação │
    └─────────┬─────────┘ └───────┬────────┘ └────────┬────────┘
              │                   │                    │
              └───────────────────┴────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Verificar Power Forecast  │
                    │ (potência em 30min/1h)    │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Queda > 50% prevista?     │
                    └─────────────┬─────────────┘
                           │             │
                          YES           NO
                           │             │
              ┌────────────▼──┐    ┌─────▼────────────┐
              │ Bomba ON?     │    │ Continuar normal │
              │ → ↑ delay_off │    └──────────────────┘
              │               │
              │ Bomba OFF?    │
              │ → Esperar     │
              └───────────────┘
```

---

## 🌙 FILTRAGEM NOTURNA DE BACKUP

### Lógica:

```python
# Às 20:00 (ou sunset + 1h):

filtration_today = states(filtration_sensor)|float(0)  # kWh
minimum_required = min_daily_filtration_kwh  # 6 kWh

if filtration_today < minimum_required:
    # Não filtrou suficiente
    deficit = minimum_required - filtration_today
    
    forecast_tomorrow = states(forecast_tomorrow)|float(0)
    
    if forecast_tomorrow < good_day_threshold:  # < 15 kWh
        # Amanhã também vai ser fraco
        # Agendar filtragem noturna
        
        hours_needed = deficit / pump_power_kw
        # Ex: 3 kWh deficit / 0.8 kW = 3.75 horas
        
        start_time = "02:00"  # Tarifa vazio
        end_time = start_time + hours_needed
        
        schedule_night_run(start_time, end_time)
        notify("Filtragem noturna agendada: 02:00-05:45")
    else:
        # Amanhã há sol, compensar amanhã
        notify("Filtração insuficiente hoje, mas amanhã há sol")
```

### Automação de Backup:

```yaml
automation:
  - alias: "🏊 Piscina - Backup Filtragem Noturna"
    trigger:
      - platform: time
        at: "20:30:00"
    condition:
      - condition: template
        value_template: >-
          {% set done = states('sensor.piscina_filtragem_energia_hoje')|float(0) %}
          {% set needed = 6 %}
          {% set tomorrow = states('sensor.solcast_pv_forecast_forecast_tomorrow')|float(0) %}
          {{ done < needed and tomorrow < 15 }}
    action:
      - service: input_datetime.set_datetime
        target:
          entity_id: input_datetime.piscina_noite_inicio
        data:
          time: "02:00:00"
      - service: input_datetime.set_datetime
        target:
          entity_id: input_datetime.piscina_noite_fim
        data:
          time: >-
            {% set deficit = 6 - states('sensor.piscina_filtragem_energia_hoje')|float(0) %}
            {% set hours = (deficit / 0.8)|round(1) %}
            {{ (today_at('02:00') + timedelta(hours=hours)).strftime('%H:%M:%S') }}
      - service: notify.mobile_app
        data:
          title: "🏊 Filtragem Noturna"
          message: >-
            Dia fraco de sol ({{ states('sensor.piscina_filtragem_energia_hoje')|round(1) }} kWh).
            Amanhã também previsto fraco.
            Agendada filtragem noturna: 02:00-{{ ... }}
```

---

## 📈 BENEFÍCIOS RESUMIDOS

| Sem Forecast | Com Forecast |
|--------------|--------------|
| Reage ao presente | Planeia com futuro |
| Conservador sempre | Adapta agressividade |
| Pode perder excedente | Maximiza uso |
| Noite surpresa | Noite planeada |
| Oscilações em nuvens | Antecipa quedas |
| Filtragem aleatória | Filtragem garantida |

---

## 📊 MÉTRICAS ESPERADAS

### Sem Forecast:
- Dias com filtragem < 6h: **15-20%**
- Energia importada desnecessária: **5-10%**
- Filtragens noturnas surpresa: **5-10%**

### Com Forecast:
- Dias com filtragem < 6h: **< 5%** (com backup)
- Energia importada desnecessária: **< 3%**
- Filtragens noturnas surpresa: **0%** (sempre planeadas)

---

## 🎯 RESUMO

### A previsão solar serve para:

1. 🚀 **Ser mais agressivo** quando há sol garantido
2. 🛡️ **Ser conservador** quando sol é escasso
3. 🌙 **Planear backup noturno** se necessário
4. ⏰ **Antecipar quedas** de produção
5. 🔋 **Coordenar com bateria** (se existir)
6. 📊 **Otimizar scheduling** de múltiplos aparelhos

### Sensores principais a usar:

```yaml
# Obrigatório:
sensor.solcast_pv_forecast_forecast_remaining_today

# Recomendado:
sensor.solcast_pv_forecast_forecast_tomorrow
sensor.solcast_pv_forecast_power_now_1hr

# Opcional:
sensor.solcast_pv_forecast_peak_forecast_today
sensor.solcast_pv_forecast_peak_time_today
```

---

*Documentação: Previsão Solar para Piscina*  
*Versão: 1.0*  
*Data: 1 Fevereiro 2026*
