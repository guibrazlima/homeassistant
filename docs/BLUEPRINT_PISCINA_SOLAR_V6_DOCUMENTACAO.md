# 🏊 Blueprint Piscina Solar v6 — Documentação Completa

> **Versão:** 6.0 | **Última revisão:** 2026-02-13  
> **Autor:** guibrazlima (original) + AI Assistant (blueprint v6 híbrido)  
> **Resultado auditoria:** ✅ Blueprint validado — 0 erros de lógica, 0 erros YAML

---

## 📋 Índice

1. [Visão Geral](#1-visão-geral)
2. [Arquitetura do Sistema](#2-arquitetura-do-sistema)
3. [Ficheiros do Sistema](#3-ficheiros-do-sistema)
4. [Blueprint v6 — Referência Completa](#4-blueprint-v6--referência-completa)
   - [4.1 Inputs (44 parâmetros)](#41-inputs-44-parâmetros)
   - [4.2 Variáveis Computadas (68)](#42-variáveis-computadas-68)
   - [4.3 Triggers (10)](#43-triggers-10)
   - [4.4 Actions (8 choices + default)](#44-actions-8-choices--default)
5. [Sensores de Suporte](#5-sensores-de-suporte)
6. [Package de Planeamento Solar](#6-package-de-planeamento-solar)
7. [Fluxo de Decisão Completo](#7-fluxo-de-decisão-completo)
8. [Fórmulas Matemáticas](#8-fórmulas-matemáticas)
9. [Proteção Anti-Cycling](#9-proteção-anti-cycling)
10. [Resolução de Problemas](#10-resolução-de-problemas)
11. [Auditoria e Bugs Corrigidos](#11-auditoria-e-bugs-corrigidos)

---

## 1. Visão Geral

O sistema controla automaticamente a bomba da piscina combinando dois modos operacionais:

| Modo | Período | Lógica | Objetivo |
|------|---------|--------|----------|
| ☀️ **Solar (Dia)** | Nascer+30min → Pôr-30min | Excedente fotovoltaico em tempo real | Autoconsumo gratuito |
| 🌙 **Coopernico (Noite)** | 22:00 → 08:00 | Janela mais barata (preços dinâmicos 15min) | Complementar filtração ao menor custo |

### Princípio Fundamental

A previsão Solcast **não liga a bomba diretamente**. Funciona como **porteiro**:
- **Previsão boa** → Abre a porta para o controlo solar diurno
- **Previsão má** → Fecha a porta → Filtração transferida para a noite Coopernico
- **Decisão real** → Baseada em excedente solar medido em tempo real

---

## 2. Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA 4: PLANEAMENTO                        │
│  Solcast (07:00) → Análise Janelas → Flag prefer_night          │
│  Package: piscina_solar_optimization.yaml                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │ input_boolean.piscina_prefer_night_filtering
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA 3: AJUSTE METEO                       │
│  Condição tempo + Instabilidade solar → Multiplicador delays    │
│  Sensor: piscina_weather_delay_multiplier                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │ delay_multiplier (0.8× a 3.0×)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA 2: DADOS POTÊNCIA                     │
│  Hierarquia 6 níveis (NET 5min → Export inst.) + Smoothing      │
│  Sensores: solar_smoothed.yaml (statistics)                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │ current_net_power (W)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA 1: BLUEPRINT v6                        │
│  10 Triggers → 68 Variáveis → 8 Actions → switch.turn_on/off   │
│  Ficheiro: piscina_solar_control_v6.yaml                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Ficheiros do Sistema

| Ficheiro | Localização | Função |
|----------|-------------|--------|
| `piscina_solar_control_v6.yaml` | `blueprints/automation/piscina_solar/` | Blueprint principal (1530 linhas) |
| `piscina_solar_forecast_windows.yaml` | `sensors/` | Análise Solcast + previsão meteo |
| `piscina_weather_adjustment.yaml` | `sensors/` | Multiplicador de delay meteo/instabilidade |
| `solar_smoothed.yaml` | `sensors/` | Médias móveis 5min + indicador estabilidade |
| `piscina_solar_optimization.yaml` | `packages/` | Helpers + automações planeamento |
| `Excendente_break_even.yaml` | `templates/` | Sensores break-even económico (dashboard) |
| `piscina.yaml` | `templates/` | Tempo filtração, temperatura, duração |
| `piscina_filtragem.yaml` | `templates/` | Cálculo horas recomendadas |

---

## 4. Blueprint v6 — Referência Completa

### 4.1 Inputs (44 parâmetros)

#### Secção 1: Configuração Essencial

| Input | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `pump_switch` | `switch` | *(obrigatório)* | Switch da bomba (ex: `switch.bomba_piscina_switch_0`) |
| `pump_nominal_power` | number | `1380` W | Potência nominal da bomba |
| `pump_actual_power` | `sensor` | `{}` (opcional) | Consumo real em tempo real |

#### Secção 2: Modo Híbrido

| Input | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `hybrid_mode_enabled` | boolean | `true` | Ativa Solar (dia) + Coopernico (noite) |

#### Secção 3: Coopernico (Noite)

| Input | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `use_coopernico_optimization` | boolean | `false` | Calcular janela mais barata |
| `coopernico_price_sensor` | `sensor` | `{}` | Sensor preços Coopernico (prices attr) |
| `cheapest_window_helper` | `input_datetime` | `.piscina_hora_agendada_mais_barata` | Guarda hora calculada |
| `coopernico_end_helper` | `input_datetime` | `.piscina_fim_janela_coopernico` | Guarda hora fim janela |
| `night_session_active_helper` | `input_boolean` | `.piscina_sessao_noturna_ativa` | Lock de sessão noturna |
| `calculation_info_helper` | `input_text` | `.piscina_ultima_janela_calculada` | Info último cálculo |
| `calculation_time` | time | `19:00:00` | Hora do cálculo diário |

#### Secção 4: Sensores de Potência (Hierarquia 6 Níveis)

| Nível | Input | Tipo | Cálculo NET |
|-------|-------|------|-------------|
| 1 ⭐ | `net_power_5min` | sensor | Direto (mais estável) |
| 2 | `house_power_no_pump_5min` + `pv_power_5min` | 2× sensor | `house - pv` |
| 3 | `export_power_5min` | sensor | `0 - export` |
| 4 | `net_power` | sensor | Direto (instantâneo) |
| 5 | `house_power_no_pump` + `pv_power` | 2× sensor | `house - pv` |
| 6 | `export_power` | sensor | `0 - export` |

> **Convenção:** NET negativo = exportação (excedente solar) = bom para ligar

#### Secção 5: Filtração Dinâmica

| Input | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `use_dynamic_filtration_time` | boolean | `true` | Usa temperatura para calcular horas |
| `dynamic_filtration_hours_sensor` | `sensor` | `{}` | Sensor horas recomendadas |
| `min_daily_filtration_kwh` | number | `11` kWh | Energia fixa (se dinâmico OFF) |
| `filtration_energy_today` | `sensor` | `{}` | Energia já consumida hoje |
| `ignore_filtration_limit` | boolean | `false` | Permitir sobre-filtragem com excedente |
| `min_night_deficit_kwh` | number | `2` kWh | Mínimo para ativar noite |

#### Secção 6: Filtragem Noturna

| Input | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `enable_night_auto` | boolean | `false` | Ativar filtração noturna automática |
| `night_start_time` | time | `22:00:00` | Início vazio (fallback) |
| `night_end_time` | time | `08:00:00` | Fim vazio (failsafe) |

#### Secção 7: Otimização Económica (Dia)

| Input | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `use_economic_optimization` | boolean | `true` | Calcular break-even dia vs noite |
| `price_peak` | number | `0.1537` €/kWh | Preço fora-vazio (fallback) |
| `price_offpeak` | number | `0.0929` €/kWh | Preço vazio (fallback) |
| `import_limit` | number | `700` W | Limite importação dia |
| `start_margin` | number | `100` W | Margem extra para arranque |
| `import_limit_strategy` | select | `maior` | Estratégia: maior/menor/fixo/break_even |

#### Secção 8: Delays e Timings

| Input | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `delay_on` | number | `30` s | Delay antes de ligar |
| `delay_off` | number | `60` s | Delay antes de desligar |
| `min_on_time` | number | `10` min | Tempo mínimo ligada |
| `min_off_time` | number | `5` min | Cooldown após desligar (anti-cycling) |
| `delay_multiplier_sensor` | `sensor` | `{}` | Multiplicador meteo (ex: 1.5×) |

#### Secção 9: Horários Solares

| Input | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `sun_offset_start` | number | `30` min | Offset após nascer do sol |
| `sun_offset_end` | number | `-30` min | Offset antes do pôr do sol |

#### Secção 10: Controlo e Debug

| Input | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `override_manual` | `input_boolean` | `{}` | Override modo manual |
| `enable_debug_logs` | boolean | `false` | Logs detalhados no logbook |
| `dry_run_mode` | boolean | `false` | Testar sem controlar bomba |

---

### 4.2 Variáveis Computadas (68)

#### Estado da Bomba
| Variável | Valor | Descrição |
|----------|-------|-----------|
| `pump_is_on` | `true/false` | Estado atual do switch |
| `pump_current_power` | W | Consumo real ou nominal |

#### Cálculo de Défice
| Variável | Valor | Descrição |
|----------|-------|-----------|
| `target_kwh` | kWh | Meta diária (dinâmica ou fixa) |
| `energy_consumed` | kWh | Energia já consumida hoje |
| `deficit_kwh` | kWh | `max(target - consumed, 0)` |
| `deficit_hours` | h | `deficit_kwh / (pump_power / 1000)` |

#### Hierarquia de Sensores
| Variável | Valor | Descrição |
|----------|-------|-----------|
| `sensor_level` | 1-6 | Nível de sensor ativo |
| `current_net_power` | W | Potência NET atual |
| `import_predicted` | W | `current_net + pump_current_power` |

#### Break-Even Económico
| Variável | Valor | Descrição |
|----------|-------|-----------|
| `price_current_day` | €/kWh | Preço diurno real (Coopernico) ou fallback |
| `price_cheapest_night` | €/kWh | Média preços vazio noturnos |
| `break_even_import_w` | W | Importação máxima onde custo dia = custo noite |
| `final_import_limit` | W | Limite final (baseado na estratégia) |

#### Delays Dinâmicos
| Variável | Valor | Descrição |
|----------|-------|-----------|
| `delay_multiplier` | 0.8×–3.0× | Do sensor meteo (ou 1.0) |
| `final_delay_on` | s | `delay_on × delay_multiplier` |
| `final_delay_off` | s | `delay_off × delay_multiplier` |

#### Condições de Ligação (Dia)
| Variável | Condição | Descrição |
|----------|----------|-----------|
| `can_turn_on` | `import_predicted ≤ limit - margin` | Excedente suficiente para ligar |
| `can_keep_on` | `import_predicted ≤ limit` | Excedente suficiente para manter |
| `has_deficit` | `deficit_kwh > 0.1 ou ignore_limit` | Ainda falta filtrar |
| `min_time_elapsed` | `tempo_ligada ≥ min_on_time` | Tempo mínimo ON respeitado |
| `min_off_time_elapsed` | `tempo_desligada ≥ min_off_time × multiplier` | Cooldown anti-cycling |
| `forecast_allows_solar` | `prefer_night = OFF ou planning = OFF` | Previsão permite solar |

#### Coopernico
| Variável | Valor | Descrição |
|----------|-------|-----------|
| `cheapest_result` | dict | `{start_time, avg_price, total_cost, duration_hours, found}` |
| `current_mode` | `day/night` | Baseado na hora atual vs night_start/night_end |

---

### 4.3 Triggers (10)

| # | ID | Platform | Quando Dispara | Usado Em |
|---|-----|----------|---------------|----------|
| 1 | `daily_calculation` | time | `calculation_time` (19h) | ACTION 1 |
| 2 | `cheapest_scheduled_time` | time | Hora calculada mais barata | ACTION 2 |
| 3 | `coopernico_window_end` | time | Fim da janela Coopernico | ACTION 3.5 |
| 4 | `night_fallback_start` | time | `night_start_time` (22h) | ACTION 3 |
| 5 | `night_end` | time | `night_end_time` (08h) | ACTION 4 |
| 6 | `sunrise` | sun | Nascer + offset (30min) | ACTION 5 |
| 7 | `sunset` | sun | Pôr do sol + offset (-30min) | ACTION 6 |
| 8 | `power_change_5min` | state | Sensor NET 5min muda | ACTION 7 |
| 9 | `power_change_inst` | state | Sensor NET instantâneo muda | ACTION 7 |
| 10 | `pump_state_change` | state | Estado bomba muda | Default (debug) |

> **Nota:** O trigger `pump_state_change` não tem choice próprio — serve para debug via default action (regista estado no logbook quando debug está ativo).

---

### 4.4 Actions (8 Choices + Default)

#### ACTION 1: Cálculo Coopernico (19h)
- **Trigger:** `daily_calculation`
- **Condição:** `hybrid_mode AND use_coopernico`
- **Ação:** Sliding window nos preços noturnos → guarda hora mais barata no helper
- **Output:** `input_datetime.piscina_hora_agendada_mais_barata` + `input_text.piscina_ultima_janela_calculada`

#### ACTION 2: Ligar na Hora Agendada (Noite)
- **Trigger:** `cheapest_scheduled_time`
- **Condição:** `hybrid_mode AND use_coopernico AND enable_night_auto AND deficit ≥ min_deficit AND session OFF`
- **Ação:** Ativa session lock → Liga bomba → Calcula e guarda hora de fim

#### ACTION 3: Fallback Horário Fixo (Noite)
- **Trigger:** `night_fallback_start`
- **Condição:** `(NOT use_coopernico OR NOT hybrid_mode) AND enable_night_auto AND deficit ≥ min_deficit AND session OFF`
- **Ação:** Liga bomba no horário fixo (22h) como fallback

#### ACTION 3.5: Fim Janela Coopernico (Auto-Stop)
- **Trigger:** `coopernico_window_end`
- **Condição:** `session ON`
- **Ação:** Reset session lock → Desliga bomba

#### ACTION 4: Fim Período Noturno (Failsafe)
- **Trigger:** `night_end`
- **Ação:** Reset session → Desliga bomba (se ainda ligada)

#### ACTION 5: Nascer do Sol
- **Trigger:** `sunrise`
- **Ação:** Reset session noturna → Modo DIA ativo

#### ACTION 6: Pôr do Sol
- **Trigger:** `sunset`
- **Ação:** Desliga bomba (se ligada de dia) → Modo NOITE pronto

#### ACTION 7: Controlo Solar Diurno ⭐ (Motor Principal)
- **Triggers:** `power_change_5min` OR `power_change_inst`
- **Pré-condições:** `current_mode == 'day' AND session OFF`
- **Sub-choice LIGAR:** 5 condições + delay + re-verificação live
- **Sub-choice DESLIGAR:** 3 condições + delay + re-verificação live

##### LIGAR BOMBA — 5 Condições Simultâneas

```
1. ❓ pump_is_on == false           → Bomba está OFF?
2. ❓ has_deficit == true            → Falta filtrar?
3. ❓ can_turn_on == true            → Excedente suficiente?
4. ❓ min_off_time_elapsed == true   → Cooldown respeitado?
5. ❓ forecast_allows_solar == true  → Previsão permite?
        ↓ TODAS verdadeiras
   ⏱️ Delay ON (ex: 30s × 1.5 = 45s)
        ↓
   🔄 Re-leitura live dos sensores
        ↓ Ainda verdadeiras?
   ✅ switch.turn_on
```

##### DESLIGAR BOMBA — 3 Condições Simultâneas

```
1. ❓ pump_is_on == true             → Bomba está ON?
2. ❓ NOT can_keep_on OR NOT has_deficit → Sem excedente OU meta cumprida?
3. ❓ min_time_elapsed == true       → Tempo mínimo ON respeitado?
        ↓ TODAS verdadeiras
   ⏱️ Delay OFF (ex: 60s × 1.5 = 90s)
        ↓
   🔄 Re-leitura live dos sensores
        ↓ Ainda verdadeiras?
   ✅ switch.turn_off
```

#### DEFAULT (Debug)
- **Trigger:** Qualquer trigger não tratado (inclui `pump_state_change`)
- **Ação:** Log no logbook com estado atual (se debug ON)

---

## 5. Sensores de Suporte

### 5.1 `sensor.piscina_solar_forecast_analysis`
**Ficheiro:** `sensors/piscina_solar_forecast_windows.yaml`

Analisa o atributo `detailedHourly` do Solcast para identificar janelas contínuas de excedente solar.

| Atributo | Exemplo | Descrição |
|----------|---------|-----------|
| `viable_windows` | 2 | Nº janelas ≥30min |
| `best_window_minutes` | 180 | Maior janela contínua (min) |
| `viable_hours` | 5 | Total horas com FV ≥ threshold |
| `viable_solar_kwh` | 8.2 | Energia solar viável total |
| `recommendation_code` | `solar_diurno` | Código para automação |
| `forecast_total_kwh` | 9.92 | Previsão total do dia |
| `forecast_this_hour_w` | 78 | Potência esta hora (W) |
| `forecast_next_hour_w` | 0 | Potência próxima hora (W) |
| `peak_forecast_w` | 2485 | Pico previsto (W) |
| `pump_threshold_w` | 1656 | Threshold usado (1380W × 1.2) |

**Códigos de recomendação:**
| Código | Condição | Significado |
|--------|----------|-------------|
| `solar_diurno` | best_window ≥ 180min | Dia bom → prioridade solar |
| `misto` | best_window ≥ 60min | Dia razoável → solar + noite |
| `pouco_solar` | best_window ≥ 30min | Pouco sol → tentar mas complementar |
| `noite_coopernico` | best_window < 30min | Sem sol viável → noite Coopernico |

**Conversão de unidades Solcast:**
- `detailedHourly.pv_estimate` → **kWh** por hora → `× 1000 = W médios`
- `forecast_this_hour` → **Wh** por hora → `= W médios` (sem conversão)
- `peak_forecast_today` → **W** → direto (sem conversão)
- `forecast_today` → **kWh** total do dia

### 5.2 `sensor.piscina_weather_delay_multiplier`
**Ficheiro:** `sensors/piscina_weather_adjustment.yaml`

Combina condição meteo + instabilidade solar para ajustar delays.

| Factor | Fonte | Escala |
|--------|-------|--------|
| Meteo | `sensor.realtime_condition` | ☀️ 0.8× → 🌧️ 2.0× |
| Instabilidade | `sensor.solar_stability_indicator` | <10%: 1.0× → >60%: 3.0× |
| **Final** | `MAX(meteo, instabilidade)` | **0.8× — 3.0×** |

### 5.3 `sensor.solar_stability_indicator`
**Ficheiro:** `sensors/solar_smoothed.yaml`

Mede variação percentual entre produção solar instantânea e média 5min.

| Classificação | Variação | Recomendação |
|--------------|----------|--------------|
| Muito Estável | < 5% | ✅ Condições ótimas |
| Estável | 5-15% | ✅ Condições boas |
| Instável | 15-30% | ⚠️ Aguardar estabilização |
| Muito Instável | > 30% | 🔴 Evitar decisões |

### 5.4 Sensores de Média Móvel (5min)
**Ficheiro:** `sensors/solar_smoothed.yaml`

| Sensor | Fonte | Função |
|--------|-------|--------|
| `sensor.solar_power_5min_smooth` | `sensor.emoncms_solar` | Produção FV suavizada |
| `sensor.house_power_5min_smooth` | `sensor.emoncms_..._use_no_pool_pump` | Consumo casa suavizado |
| `sensor.import_export_5min_smooth` | `sensor.emoncms_import_export` | NET suavizado |
| `sensor.export_power_5min_smooth` | `sensor.emoncms_export_power_positive` | Exportação suavizada |

---

## 6. Package de Planeamento Solar

**Ficheiro:** `packages/piscina_solar_optimization.yaml`

### Helpers Criados

| Entity | Tipo | Função |
|--------|------|--------|
| `input_boolean.piscina_forecast_planning_enabled` | toggle | Ativa/desativa planeamento |
| `input_boolean.piscina_prefer_night_filtering` | flag | Flag: dia sem solar → filtrar à noite |
| `input_boolean.piscina_use_weather_forecast` | toggle | Ativa/desativa ajuste meteo |
| `input_boolean.piscina_night_session_done` | flag | Sessão noturna completa |
| `input_number.piscina_weekend_consumption_factor` | slider | Fator fim-de-semana |
| `input_select.piscina_notification_level` | dropdown | Nível de notificações |

### Automações de Planeamento

| Automação | Hora | Função |
|-----------|------|--------|
| `piscina_forecast_morning_planning` | 07:00 | Análise Solcast → define flag noite |
| `piscina_forecast_midday_recheck` | 12:00 | Re-avaliação → corrige se condições mudaram |
| `piscina_forecast_daily_reset` | sunrise-1h | Reset flag noite para novo dia |

### Utility Meter

```yaml
bomba_piscina_switch_0_energy:
  source: sensor.bomba_piscina_total_energy
  cycle: daily
```

---

## 7. Fluxo de Decisão Completo

### Dia Bom Solar (Exemplo Real)

```
06:30  🌅 Reset: piscina_prefer_night_filtering → OFF
07:00  🔮 Planeamento: Solcast mostra 5h viáveis, janela 180min
       → recommendation_code = "solar_diurno"
       → prefer_night_filtering = OFF ✅

09:30  📊 NET_5min muda para -800W (excedente solar crescente)
       → Trigger power_change_5min
       → ACTION 7 avalia:
         ✅ pump_is_on = false
         ✅ has_deficit = true (deficit 4.2 kWh)
         ✅ can_turn_on: import_predicted = -800+0 = -800 ≤ 600 ✅
         ✅ min_off_time_elapsed (>5min desde último OFF)
         ✅ forecast_allows_solar (prefer_night = OFF)
       → Delay ON: 30s × 0.8 (sunny) = 24s
       → Re-verifica live: NET=-780W → live_can_turn_on ✅
       → 🔌 switch.turn_on

14:00  ☁️ Nuvem: NET_5min muda para +400W (importação)
       → ACTION 7 avalia DESLIGAR:
         ✅ pump_is_on = true
         ✅ can_keep_on: predicted = 400+1380 = 1780 > 700 → NOT can_keep_on ✅
         ✅ min_time_elapsed (>10min ON)
       → Delay OFF: 60s × 1.0 = 60s
       → Re-verifica: NET=+500W → still NOT can_keep_on ✅
       → 🔌 switch.turn_off

17:30  🌇 Pôr do sol: ACTION 6 → Desliga se ainda ON → Modo NOITE pronto
```

### Dia Sem Solar (Exemplo Real)

```
06:30  🌅 Reset: prefer_night_filtering → OFF
07:00  🔮 Planeamento: Solcast mostra 0h viáveis, janela 0min
       → recommendation_code = "noite_coopernico"
       → prefer_night_filtering = ON 🔴

10:30  📊 NET_5min muda para -500W (momento fugaz de sol)
       → ACTION 7 avalia LIGAR:
         ✅ pump_is_on = false
         ✅ has_deficit = true
         ✅ can_turn_on = true
         ✅ min_off_time_elapsed = true
         🔴 forecast_allows_solar = FALSE (prefer_night = ON)
       → BLOQUEADO na condição 5 → NÃO LIGA
       → ✅ Evitou cycling inútil

19:00  💰 Cálculo Coopernico: janela mais barata = 03:15
       → input_datetime.piscina_hora_agendada_mais_barata = 03:15

03:15  🌙 Trigger cheapest_scheduled_time:
       → deficit = 6.2 kWh ≥ 2.0 kWh mínimo ✅
       → session OFF ✅
       → Liga bomba + session ON
       → Calcula fim: 03:15 + 4.5h = 07:45

07:45  ⏱️ Trigger coopernico_window_end:
       → Desliga bomba + session OFF
```

---

## 8. Fórmulas Matemáticas

### Break-Even Importação (Blueprint)

$$\text{break\_even\_import\_W} = \frac{P_{\text{noite}} \times P_{\text{bomba}}}{P_{\text{dia}}}$$

**Exemplo:** $\frac{0.0929 \times 1380}{0.1537} = 834\text{W}$

**Significado:** Se importar até 834W enquanto a bomba funciona de dia, o custo é ≤ ao custo de correr a bomba toda à noite.

### Break-Even Solar (Template)

$$\text{solar\_minimo\_W} = \frac{P_{\text{bomba}} \times (P_{\text{dia}} - P_{\text{noite}})}{P_{\text{dia}}}$$

**Exemplo:** $\frac{1380 \times (0.1537 - 0.0929)}{0.1537} = 546\text{W}$

**Relação:** $\text{break\_even\_import} + \text{solar\_minimo} = P_{\text{bomba}}$
→ $834 + 546 = 1380\text{W}$ ✅

### Threshold Previsão Solar

$$\text{pump\_threshold} = P_{\text{bomba}} \times \text{safety\_margin} = 1380 \times 1.2 = 1656\text{W}$$

### Delay Dinâmico

$$\text{final\_delay} = \text{delay\_base} \times \text{MAX}(\text{meteo\_mult}, \text{instab\_mult})$$

### Cooldown Anti-Cycling

$$\text{min\_off\_seconds} = \text{min\_off\_time} \times 60 \times \text{delay\_multiplier}$$

---

## 9. Proteção Anti-Cycling

O sistema tem **3 camadas** de proteção contra cycling excessivo:

| Camada | Mecanismo | Protege Contra |
|--------|-----------|----------------|
| **1. Previsão Solcast** | `forecast_allows_solar = FALSE` em dias nublados | Liga/desliga constante em dias sem sol viável |
| **2. Delay + Re-verificação** | Espera N×multiplier segundos, re-lê sensores | Picos momentâneos de sol/nuvens |
| **3. min_off_time** | Cooldown obrigatório após desligar (× multiplier) | Religar imediato após desligar |

### Tabela de Cenários

| Cenário | Meteo Mult | Delay ON | Delay OFF | Cooldown |
|---------|-----------|----------|-----------|----------|
| ☀️ Céu limpo | 0.8× | 24s | 48s | 4min |
| 🌤️ Parcialmente nublado | 1.0× | 30s | 60s | 5min |
| ☁️ Nublado | 1.5× | 45s | 90s | 7.5min |
| 🌧️ Chuva | 2.0× | 60s | 120s | 10min |
| ⛈️ Muito instável (>60% var) | 3.0× | 90s | 180s | 15min |

---

## 10. Resolução de Problemas

### A bomba não liga de dia apesar de ter excedente

1. **Verificar `forecast_allows_solar`:**
   - Se `input_boolean.piscina_prefer_night_filtering` está ON → previsão bloqueou
   - Solução: desligar manualmente ou esperar reset ao nascer do sol

2. **Verificar `has_deficit`:**
   - Se `sensor.bomba_piscina_energy_today` já atingiu a meta → não liga mais
   - Solução: ativar `ignore_filtration_limit = true`

3. **Verificar `min_off_time_elapsed`:**
   - Se desligou há pouco tempo → está em cooldown
   - Ver `states.switch.bomba_piscina_switch_0.last_changed`

4. **Verificar `can_turn_on`:**
   - `import_predicted` deve ser ≤ `final_import_limit - start_margin`
   - Se excedente é marginal → não passa o teste

### A bomba não desliga quando deveria

1. **Verificar `min_time_elapsed`:**
   - Deve ter passado `min_on_time` (10min default) desde que ligou

2. **Verificar re-verificação live:**
   - Após o delay, os valores podem ter mudado novamente para favorável
   - O delay protege contra oscilações → a condição não se manteve

### Erros no cálculo Coopernico

1. **Preços não disponíveis:**
   - Verificar `sensor.coopernico_base_bi_horario_ciclo_diario_all_prices`
   - Atributo `prices` deve ter lista de dicts com `datetime` e `price_w_vat`

2. **Janela calculada muito cedo/tarde:**
   - Verificar `input_text.piscina_ultima_janela_calculada` para ver detalhes
   - Aumentar/diminuir `min_night_deficit_kwh`

### Debug — Como ativar logs detalhados

1. Na automação criada pelo blueprint, ativar `enable_debug_logs = true`
2. Ver logs em: **Ferramentas de Desenvolvimento → Logbook** → filtrar por `Piscina v6`
3. Cada ação regista: trigger, modo, estado bomba, NET, défice, sensor level

---

## 11. Auditoria e Bugs Corrigidos

### Auditoria 2026-02-13

#### Resultado Geral
- ✅ **YAML válido** (1530 linhas, parser OK)
- ✅ **44 inputs** — todos definidos e referenciados
- ✅ **68 variáveis** — todas as críticas definidas
- ✅ **10 triggers** — 9 usados em choices, 1 (`pump_state_change`) rota para default/debug
- ✅ **8 choices + 1 default** — lógica consistente
- ✅ **Fórmulas break-even** — matematicamente corretas (blueprint e template são complementares)
- ✅ **Todos os sensores existem** no Home Assistant e retornam valores válidos

#### Sensores Verificados (estado atual)

| Sensor | Estado | Validação |
|--------|--------|-----------|
| `sensor.realtime_condition` | `partlycloudy` | ✅ Existe (integração meteo) |
| `sensor.solar_stability_indicator` | `0%` | ✅ Definido em `solar_smoothed.yaml` |
| `sensor.piscina_weather_delay_multiplier` | `1.0×` | ✅ Definido em `piscina_weather_adjustment.yaml` |
| `sensor.piscina_solar_forecast_analysis` | `Dia misto (2h viáveis)` | ✅ Definido em `piscina_solar_forecast_windows.yaml` |
| `sensor.solcast_pv_forecast_forecast_today` | `9.92 kWh` | ✅ Custom component `solcast_solar` |
| `sensor.solcast_pv_forecast_peak_forecast_today` | `2485 W` | ✅ Unidade: W (não kW) |
| `sensor.solcast_pv_forecast_forecast_this_hour` | `78 Wh` | ✅ Unidade: Wh |
| `sensor.import_export_5min_smooth` | `2200 W` | ✅ Statistics sensor |
| `sensor.coopernico_base_bi_horario_ciclo_diario_all_prices` | `188` | ✅ Integração Coopernico |
| `input_boolean.piscina_prefer_night_filtering` | `off` | ✅ Definido no package |
| `input_boolean.piscina_forecast_planning_enabled` | `on` | ✅ Definido no package |

#### Bugs Corrigidos Nesta Auditoria

| # | Ficheiro | Bug | Correção |
|---|---------|-----|----------|
| 1 | `sensors/piscina_solar_forecast_windows.yaml` | `peak_forecast_w` multiplicava por 1000 mas Solcast já retorna em W | Removido `* 1000` |
| 2 | `sensors/piscina_solar_forecast_windows.yaml` | `forecast_this_hour_w` multiplicava por 1000 mas Solcast retorna em Wh (= W médio) | Removido `* 1000` |
| 3 | `sensors/piscina_solar_forecast_windows.yaml` | `forecast_next_hour_w` mesmo problema | Removido `* 1000` |
| 4 | `sensors/piscina_solar_forecast_windows.yaml` | `peak_w` no sensor afternoon multiplicava por 1000 | Removido `* 1000` |
| 5 | `packages/piscina_solar_optimization.yaml` | `peak_w` no planeamento matinal multiplicava por 1000 | Removido `* 1000` |

> **Nota:** A conversão `pv_estimate × 1000` no `detailedHourly` está **CORRETA** porque esse campo é em kWh (ex: 2.289 kWh → 2289 W médios nessa hora).

#### Observações

- **Trigger `pump_state_change`:** Definido mas sem choice próprio. Isto é intencional — serve para registar mudanças de estado no logbook via default action quando debug está ativo. Não é um bug.
- **`mode: single` + `max_exceeded: silent`:** Correto. Previne execuções paralelas e não gera avisos quando múltiplos triggers chegam durante uma execução.
- **Fórmula break-even no blueprint vs template:** São complementares ($834W + 546W = 1380W$). O blueprint calcula o **limite de importação**, o template calcula o **solar mínimo necessário**.
