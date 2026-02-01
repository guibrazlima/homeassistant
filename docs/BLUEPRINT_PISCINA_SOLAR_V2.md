# 🏊 Blueprint: Piscina - Controlo Solar Inteligente v2

<div align="center">

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue?style=for-the-badge&logo=home-assistant)
![Blueprint](https://img.shields.io/badge/Blueprint-v2.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Automação inteligente para bomba de piscina com excedente solar, previsão Solcast e tarifa bi-horária**

[Instalação](#-instalação) • [Configuração](#-configuração) • [Fórmulas](#-fórmulas-e-algoritmos) • [Sensores](#-sensores-necessários)

</div>

---

## 📋 Índice

- [Características](#-características)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Fórmulas e Algoritmos](#-fórmulas-e-algoritmos)
- [Sensores Necessários](#-sensores-necessários)
- [Modos de Operação](#-modos-de-operação)
- [Exemplos Práticos](#-exemplos-práticos)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Características

| Funcionalidade | Descrição |
|----------------|-----------|
| ☀️ **Excedente Solar** | Liga bomba apenas quando há produção solar suficiente |
| 📊 **Previsão Solcast** | Usa forecast para otimizar quando ligar |
| 🌡️ **Tempo Dinâmico** | Calcula horas de filtragem baseado na temperatura |
| 🌙 **Bi-Horário Noturno** | Completa filtragem em tarifa vazio (22:00-08:00) |
| 🏠 **Consumo Casa** | Considera consumo doméstico nas previsões |
| 🔋 **Bateria** | Suporte opcional para bateria doméstica |
| 📈 **4 Modos Adaptativos** | Normal, Económico, Agressivo, Emergência |

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BLUEPRINT PISCINA SOLAR v2                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              │
│  │   SENSORES  │───▶│  CÁLCULOS   │───▶│   DECISÃO   │              │
│  │   ENTRADA   │    │  INTERNOS   │    │   FINAL     │              │
│  └─────────────┘    └─────────────┘    └─────────────┘              │
│         │                  │                  │                      │
│         ▼                  ▼                  ▼                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              │
│  │ • PV Power  │    │ • Excedente │    │ • Ligar?    │              │
│  │ • Casa      │    │ • Previsão  │    │ • Desligar? │              │
│  │ • Rede      │    │ • Tempo     │    │ • Modo      │              │
│  │ • Bomba     │    │   Filtragem │    │   Noturno?  │              │
│  │ • Solcast   │    │ • Modo Op.  │    │             │              │
│  └─────────────┘    └─────────────┘    └─────────────┘              │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Instalação

### 1. Copiar Blueprint

```yaml
# Localização do ficheiro:
blueprints/automation/piscina_solar/piscina_solar_control_v2.yaml
```

### 2. Criar Sensores Auxiliares

Adiciona ao `configuration.yaml`:

```yaml
homeassistant:
  customize: !include customize.yaml
```

### 3. Reiniciar Home Assistant

```bash
docker restart homeassistant
```

---

## ⚙️ Configuração

### Inputs Obrigatórios

| Input | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `pump_switch` | switch | Entidade da bomba | `switch.bomba_piscina_switch_0` |
| `pv_power` | sensor | Produção FV atual (W) | `sensor.emoncms_solar` |
| `pump_nominal_power` | number | Potência bomba (W) | `1380` |

### Inputs Recomendados

| Input | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `house_power_no_pump` | sensor | Consumo casa sem bomba (W) | `sensor.emoncms_use_no_pool_pump` |
| `net_power` | sensor | Import/Export (W) | `sensor.emoncms_import_export` |
| `export_power` | sensor | Exportação positiva (W) | `sensor.emoncms_export_power_positive` |
| `filtration_remaining` | sensor | Tempo restante (HH:MM) | `sensor.pool_pump_remaining_time` |

### Inputs Solcast (Opcional)

| Input | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `forecast_remaining_today` | sensor | kWh restantes hoje | `sensor.solcast_pv_forecast_forecast_remaining_today` |
| `forecast_tomorrow` | sensor | kWh previstos amanhã | `sensor.solcast_pv_forecast_forecast_tomorrow` |
| `power_forecast_1h` | sensor | Potência próxima hora (W) | `sensor.solcast_pv_forecast_power_next_hour` |

---

## 📐 Fórmulas e Algoritmos

### 1️⃣ Excedente Solar Disponível

O cálculo do excedente considera múltiplas fontes de dados:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CÁLCULO DO EXCEDENTE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   MÉTODO PREFERENCIAL (house+pv):                                │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  export_available = PV_power - House_power              │   │
│   │                                                          │   │
│   │  Onde:                                                   │   │
│   │  • PV_power = sensor.emoncms_solar (W)                  │   │
│   │  • House_power = sensor.emoncms_use_no_pool_pump (W)    │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   MÉTODO ALTERNATIVO (net):                                      │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  export_available = -net_power  (se net < 0)            │   │
│   │                                                          │   │
│   │  net_power > 0 → Importação                             │   │
│   │  net_power < 0 → Exportação (excedente)                 │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   MÉTODO FALLBACK (export):                                      │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  export_available = export_power                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Fórmula Final:**

$$\text{Excedente} = \max(0, P_{PV} - P_{Casa})$$

---

### 2️⃣ Tempo Dinâmico de Filtragem 🌡️

O tempo de filtragem é calculado dinamicamente baseado na temperatura:

```
┌─────────────────────────────────────────────────────────────────┐
│              TEMPO DINÂMICO DE FILTRAGEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   SENSOR: sensor.piscina_tempo_de_filtracao_recomendado         │
│                                                                   │
│   FÓRMULA:                                                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                          │   │
│   │   horas_temp = 0.5 × MAX(T_água, T_ar) × fator_cobertura│   │
│   │                                                          │   │
│   │   horas_turnover = Volume_piscina / Caudal_bomba        │   │
│   │                                                          │   │
│   │   horas_final = MAX(horas_temp, horas_turnover)         │   │
│   │                                                          │   │
│   │   resultado = CLAMP(horas_final, 4, 24)                 │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   PARÂMETROS:                                                    │
│   • T_água: sensor.temperatura_piscina_filtrado (°C)            │
│   • T_ar: sensor.bthome_sensor_temperature (°C)                 │
│   • Volume: input_number.piscina_volume_m3 (m³)                 │
│   • Caudal: input_number.bomba_caudal_m3h (m³/h)               │
│   • fator_cobertura: 0.75 (fechada) ou 1.0 (aberta)            │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Fórmula Matemática:**

$$H_{filtragem} = \text{clamp}\left(\max\left(0.5 \times \max(T_{água}, T_{ar}) \times f_{cob}, \frac{V}{Q}\right), 4, 24\right)$$

**Onde:**
- $T_{água}$ = Temperatura da água (°C)
- $T_{ar}$ = Temperatura do ar (°C)
- $f_{cob}$ = Fator cobertura (0.75 se fechada, 1.0 se aberta)
- $V$ = Volume da piscina (m³)
- $Q$ = Caudal da bomba (m³/h)

#### Exemplos Práticos:

| T_água | T_ar | Cobertura | Volume | Caudal | **Horas Recomendadas** |
|--------|------|-----------|--------|--------|------------------------|
| 20°C | 22°C | Aberta | 66m³ | 12m³/h | **5.5h** (max=11, turnover=5.5) |
| 28°C | 30°C | Aberta | 66m³ | 12m³/h | **15h** (temp) |
| 28°C | 30°C | Fechada | 66m³ | 12m³/h | **11.25h** (15×0.75) |
| 15°C | 12°C | Aberta | 66m³ | 12m³/h | **5.5h** (turnover) |

---

### 3️⃣ Energia Necessária para Filtragem

```
┌─────────────────────────────────────────────────────────────────┐
│              ENERGIA NECESSÁRIA PARA FILTRAGEM                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   MODO DINÂMICO (use_dynamic_filtration_time = true):           │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                          │   │
│   │   target_hours = sensor.piscina_tempo_de_filtracao_     │   │
│   │                  recomendado                             │   │
│   │                                                          │   │
│   │   target_kwh = target_hours × (pump_power / 1000)       │   │
│   │                                                          │   │
│   │   needed_kwh = MAX(target_kwh - done_kwh, 0)            │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   MODO FIXO (use_dynamic_filtration_time = false):              │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                          │   │
│   │   needed_kwh = MAX(min_daily_filtration_kwh - done_kwh, │   │
│   │                    0)                                    │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Fórmula:**

$$E_{necessária} = \max\left(H_{alvo} \times \frac{P_{bomba}}{1000} - E_{feita}, 0\right)$$

**Exemplo com bomba de 1380W e 5h recomendadas:**

$$E_{alvo} = 5h \times 1.38kW = 6.9kWh$$

Se já filtrou 2kWh:

$$E_{restante} = 6.9 - 2 = 4.9kWh$$

---

### 4️⃣ Tempo Restante de Filtragem

```
┌─────────────────────────────────────────────────────────────────┐
│              TEMPO RESTANTE DE FILTRAGEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   SENSOR: sensor.pool_pump_remaining_time                        │
│                                                                   │
│   CÁLCULO:                                                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                          │   │
│   │   SE sensor dinâmico disponível:                        │   │
│   │     target_seconds = horas_recomendadas × 3600          │   │
│   │   SENÃO:                                                 │   │
│   │     target_seconds = input_number × 60                  │   │
│   │                                                          │   │
│   │   worked_seconds = horas_trabalhadas × 3600             │   │
│   │                                                          │   │
│   │   remaining = MAX(target_seconds - worked_seconds, 0)   │   │
│   │                                                          │   │
│   │   OUTPUT: "HH:MM" + atributo 'seconds'                  │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   ATRIBUTOS DO SENSOR:                                           │
│   • seconds: tempo restante em segundos                         │
│   • target_hours: horas alvo de filtragem                       │
│   • source: "dynamic (temperatura)" ou "manual (input_number)" │
│   • worked_hours: horas já trabalhadas hoje                     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 5️⃣ Previsão de Consumo da Casa

```
┌─────────────────────────────────────────────────────────────────┐
│              ESTIMATIVA CONSUMO CASA                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   PRIORIDADES (por ordem):                                       │
│                                                                   │
│   1️⃣ Sensor média 7 dias (sensor.casa_consumo_medio_7_dias)    │
│      ┌──────────────────────────────────────────────────────┐   │
│      │  house_consumption = avg_7d × hours_until_sunset     │   │
│      └──────────────────────────────────────────────────────┘   │
│                                                                   │
│   2️⃣ Consumo atual × tempo restante                             │
│      ┌──────────────────────────────────────────────────────┐   │
│      │  house_consumption = current_power × hours_sunset    │   │
│      └──────────────────────────────────────────────────────┘   │
│                                                                   │
│   3️⃣ Valor manual (house_avg_power input)                       │
│      ┌──────────────────────────────────────────────────────┐   │
│      │  house_consumption = manual_avg × hours_sunset       │   │
│      └──────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Fórmula:**

$$E_{casa} = P_{média} \times H_{até\_pôr\_do\_sol} / 1000$$

---

### 6️⃣ Decisão de Ligar/Desligar

```
┌─────────────────────────────────────────────────────────────────┐
│                    LÓGICA DE DECISÃO                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   CONDIÇÃO PARA LIGAR (should_start):                           │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                          │   │
│   │   export_available >= pump_power + start_margin         │   │
│   │                                                          │   │
│   │   OU                                                     │   │
│   │                                                          │   │
│   │   import_predicted <= final_import_limit                 │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   CONDIÇÃO PARA MANTER (should_stay_on):                        │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                          │   │
│   │   import_current <= effective_import_limit               │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   CONDIÇÃO FINAL:                                                │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                          │   │
│   │   should_turn_on = (pump_off AND should_start)          │   │
│   │                  OR (pump_on AND should_stay_on)        │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 7️⃣ Modos de Operação Adaptativos

```
┌─────────────────────────────────────────────────────────────────┐
│              MODOS DE OPERAÇÃO ADAPTATIVOS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   🟢 MODO NORMAL (previsão boa, sol suficiente)                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Condição: forecast_kwh >= filtration_kwh + house_kwh   │   │
│   │                                                          │   │
│   │  • import_limit: valor configurado (ex: 700W)           │   │
│   │  • start_margin: valor configurado (ex: 100W)           │   │
│   │  • delay_on: valor configurado (ex: 30s)                │   │
│   │  • delay_off: valor configurado (ex: 60s)               │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   🟡 MODO ECONÓMICO (previsão marginal)                         │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Condição: forecast >= 70% do necessário                │   │
│   │                                                          │   │
│   │  • import_limit: +200W (mais tolerante)                 │   │
│   │  • start_margin: -50W (liga mais fácil)                 │   │
│   │  • delay_on: valor original                             │   │
│   │  • delay_off: +30s (desliga mais devagar)               │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   🟠 MODO AGRESSIVO (previsão fraca)                            │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Condição: forecast >= 40% do necessário                │   │
│   │                                                          │   │
│   │  • import_limit: +500W (bastante tolerante)             │   │
│   │  • start_margin: 0W (liga assim que possível)           │   │
│   │  • delay_on: ÷2 (liga mais rápido)                      │   │
│   │  • delay_off: +60s (desliga muito devagar)              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   🔴 MODO EMERGÊNCIA (previsão muito fraca)                     │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Condição: forecast < 40% do necessário                 │   │
│   │                                                          │   │
│   │  • import_limit: ×2 (muito tolerante)                   │   │
│   │  • start_margin: 0W                                     │   │
│   │  • delay_on: ÷3 (liga muito rápido)                     │   │
│   │  • delay_off: valor original                            │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Fórmula de Seleção:**

$$\text{Modo} = \begin{cases} 
\text{normal} & \text{se } E_{forecast} \geq E_{pool} + E_{casa} \\
\text{economic} & \text{se } E_{forecast} \geq 0.7 \times (E_{pool} + E_{casa}) \\
\text{aggressive} & \text{se } E_{forecast} \geq 0.4 \times (E_{pool} + E_{casa}) \\
\text{emergency} & \text{caso contrário}
\end{cases}$$

---

### 8️⃣ Bi-Horário Noturno 🌙

```
┌─────────────────────────────────────────────────────────────────┐
│              FILTRAGEM NOTURNA BI-HORÁRIO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   PERÍODO: 22:00 - 08:00 (tarifa vazio)                         │
│                                                                   │
│   TARIFA:                                                        │
│   • Vazio (noite): €0.0929/kWh                                  │
│   • Fora-vazio (dia): €0.1537/kWh                               │
│   • Poupança: 40%                                                │
│                                                                   │
│   CONDIÇÕES PARA LIGAR À NOITE:                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                          │   │
│   │   1. enable_night_auto = true                           │   │
│   │   2. is_night_tariff = true (22:00-08:00)              │   │
│   │   3. manual_override_off = true                         │   │
│   │   4. filtration_remaining_minutes > 0                   │   │
│   │   5. filtration_remaining >= min_night_filtration       │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│   TRIGGERS NOTURNOS:                                             │
│   • 22:00:00 - Início tarifa vazio                              │
│   • Cada 15 minutos durante a noite                             │
│   • Mudança no sensor de tempo restante                         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Fórmula de Poupança:**

$$\text{Poupança} = E_{noite} \times (P_{dia} - P_{noite}) = E \times (0.1537 - 0.0929)$$

**Exemplo:** 5kWh à noite poupam:
$$5 \times 0.0608 = €0.30/dia = €9/mês$$

---

## 📊 Sensores Necessários

### Sensores de Energia (EmonCMS)

| Sensor | Descrição | Unidade | device_class |
|--------|-----------|---------|--------------|
| `sensor.emoncms_solar` | Produção FV atual | W | power |
| `sensor.emoncms_import_export` | Import/Export rede | W | power |
| `sensor.emoncms_export_power_positive` | Exportação (positivo) | W | power |
| `sensor.emoncms_192_168_1_250_use_no_pool_pump` | Consumo casa (sem bomba) | W | power |
| `sensor.emoncms_192_168_1_250_piscina_bomba_kwhd` | Energia bomba hoje | kWh | energy |

### Sensores de Bomba

| Sensor | Descrição | Unidade | device_class |
|--------|-----------|---------|--------------|
| `switch.bomba_piscina_switch_0` | Switch da bomba | - | switch |
| `sensor.bomba_piscina_switch_0_power` | Potência atual bomba | W | power |

### Sensores de Filtragem

| Sensor | Descrição | Unidade | Atributos |
|--------|-----------|---------|-----------|
| `sensor.pool_pump_remaining_time` | Tempo restante | HH:MM | seconds, target_hours, source |
| `sensor.piscina_tempo_de_filtracao_recomendado` | Horas recomendadas | h/dia | T_agua, T_ar, volume |
| `sensor.bomba_piscina_horas_ligada_diario` | Horas trabalhadas hoje | h | - |

### Sensores Solcast

| Sensor | Descrição | Unidade |
|--------|-----------|---------|
| `sensor.solcast_pv_forecast_forecast_remaining_today` | kWh restantes hoje | kWh |
| `sensor.solcast_pv_forecast_forecast_tomorrow` | Previsão amanhã | kWh |
| `sensor.solcast_pv_forecast_power_next_hour` | Potência próxima hora | W |

### Sensores Auxiliares

| Sensor | Descrição | Unidade |
|--------|-----------|---------|
| `sensor.casa_consumo_medio_7_dias` | Média consumo 7 dias | W |
| `sensor.temperatura_piscina_filtrado` | Temperatura água | °C |
| `input_boolean.piscina_override_manual` | Override manual | on/off |

---

## 🔧 Exemplo de Configuração Completa

```yaml
# automations.yaml
- id: piscina_solar_v2
  alias: "🏊 Piscina - Solar Inteligente v2"
  description: >
    Controlo inteligente da bomba da piscina com:
    - Excedente solar durante o dia
    - Previsão Solcast para otimização
    - Bi-horário noturno (22:00-08:00)
    - Tempo de filtragem dinâmico baseado em temperatura
  use_blueprint:
    path: piscina_solar/piscina_solar_control_v2.yaml
    input:
      # === SENSORES DE ENERGIA ===
      house_power_no_pump: sensor.emoncms_192_168_1_250_use_no_pool_pump
      pv_power: sensor.emoncms_solar
      net_power: sensor.emoncms_import_export
      export_power: sensor.emoncms_export_power_positive
      
      # === BOMBA ===
      pump_switch: switch.bomba_piscina_switch_0
      pump_actual_power: sensor.bomba_piscina_switch_0_power
      pump_nominal_power: 1380  # 6A × 230V
      
      # === THRESHOLDS ===
      import_limit: 700
      start_margin: 100
      delay_on: 30
      delay_off: 60
      min_on_time: 5
      
      # === FILTRAGEM ===
      filtration_remaining: sensor.pool_pump_remaining_time
      filtration_energy_today: sensor.emoncms_192_168_1_250_piscina_bomba_kwhd
      use_dynamic_filtration_time: true
      dynamic_filtration_hours_sensor: sensor.piscina_tempo_de_filtracao_recomendado
      min_daily_filtration_kwh: 8  # Fallback se dinâmico falhar
      
      # === SOLCAST ===
      forecast_remaining_today: sensor.solcast_pv_forecast_forecast_remaining_today
      forecast_tomorrow: sensor.solcast_pv_forecast_forecast_tomorrow
      power_forecast_1h: sensor.solcast_pv_forecast_power_next_hour
      forecast_confidence: 85
      
      # === CONSUMO CASA ===
      house_avg_power: 600
      house_power_avg_sensor: sensor.casa_consumo_medio_7_dias
      use_dynamic_house_estimate: true
      
      # === BI-HORÁRIO NOTURNO ===
      enable_night_auto: true
      night_start_time: '22:00:00'
      night_end_time: '08:00:00'
      min_night_filtration_minutes: 60
      price_peak: 0.1537
      price_offpeak: 0.0929
      
      # === OUTROS ===
      override_manual: input_boolean.piscina_override_manual
      sun_offset_start: 30
      sun_offset_end: 30
      use_economic_optimization: true
      enable_debug_logs: true
  mode: single
```

---

## 📈 Dashboard Exemplo

```yaml
# Cartão para Lovelace
type: entities
title: 🏊 Piscina - Bomba Solar
entities:
  - entity: switch.bomba_piscina_switch_0
    name: Bomba
  - entity: sensor.pool_pump_remaining_time
    name: Tempo Restante
  - entity: sensor.piscina_tempo_de_filtracao_recomendado
    name: Horas Recomendadas
  - entity: sensor.emoncms_192_168_1_250_piscina_bomba_kwhd
    name: Energia Hoje
  - entity: sensor.emoncms_solar
    name: Produção FV
  - entity: automation.piscina_solar_inteligente_v2
    name: Automação
```

---

## 🐛 Troubleshooting

### Bomba não liga com sol

1. Verificar `sensor.pool_pump_remaining_time` > 0
2. Verificar excedente: `PV - Casa > Bomba + Margem`
3. Verificar `input_boolean.piscina_override_manual` = off
4. Consultar logs: `enable_debug_logs: true`

### Tempo dinâmico não funciona

1. Verificar `sensor.piscina_tempo_de_filtracao_recomendado` disponível
2. Verificar sensores de temperatura válidos
3. Atributo `source` deve mostrar "dynamic (temperatura)"

### Bi-horário não liga à noite

1. Verificar `enable_night_auto: true`
2. Verificar horário: 22:00-08:00
3. Verificar `filtration_remaining_minutes > min_night_filtration_minutes`

---

## 📄 Licença

MIT License - Uso livre com atribuição.

---

<div align="center">

**Desenvolvido para Home Assistant** 🏠

[Reportar Bug](https://github.com/guibrazlima/homeassistant/issues) • [Sugerir Funcionalidade](https://github.com/guibrazlima/homeassistant/issues)

</div>
