# 🌤️ METEOROLOGIA NA BLUEPRINT PISCINA SOLAR

**Data:** 2026-02-02  
**Versão Blueprint:** v2.0  
**Status Integração:** ⚠️ **NÃO INTEGRADO** (sensor criado mas blueprint não usa)

---

## 🎯 CONCEITO: Como a Meteorologia Afeta o Sistema

### **Objetivo:**
Ajustar automaticamente os **delays** (tempos de espera) da blueprint baseado na **previsão meteorológica**, tornando o sistema:

- **Mais agressivo** ☀️ em dias ensolarados (solar estável e previsível)
- **Mais conservador** ☁️ em dias nublados (solar instável)  
- **Muito conservador** 🌧️ em dias de chuva (solar muito imprevisível)

### **Por Que é Importante:**

| Condição | Comportamento Solar | Problema Sem Ajuste | Solução com Ajuste |
|----------|---------------------|---------------------|-------------------|
| ☀️ **Ensolarado** | Produção estável e previsível | Delays desnecessariamente longos | Delays **-20%** → Mais rápido ligar |
| ⛅ **Parcial** | Produção normal | - | Sem alteração (1.0×) |
| ☁️ **Nublado** | Produção instável | Liga/desliga muito rápido | Delays **+20%** → Mais cauteloso |
| 🌧️ **Chuva** | Produção muito instável | Oscilações constantes | Delays **+100%** → Muito conservador |

---

## 📊 MULTIPLICADORES DE DELAY

| Condição Meteorológica | Estados Weather | Multiplicador | Efeito | Exemplo |
|------------------------|-----------------|---------------|--------|---------|
| ☀️ **Ensolarado** | `sunny`, `clear` | **0.8×** | Delays -20% | 300s → 240s |
| ⛅ **Parcialmente Nublado** | `partlycloudy` | **1.0×** | Sem alteração | 300s → 300s |
| ☁️ **Nublado** | `cloudy` | **1.2×** | Delays +20% | 300s → 360s |
| 🌧️ **Chuva** | `rainy`, `pouring` | **2.0×** | Delays duplicados | 300s → 600s |

---

## 🔧 CONFIGURAÇÃO ATUAL

### **1. Sensor de Ajuste Meteorológico** ✅ CRIADO

**Localização:** `sensors/piscina_weather_adjustment.yaml`

```yaml
- platform: template
  sensors:
    piscina_weather_delay_multiplier:
      friendly_name: "Multiplicador Delay Meteorologia"
      unique_id: piscina_weather_delay_multiplier
      unit_of_measurement: "×"
      
      # Lógica de decisão
      value_template: >
        {% if is_state('input_boolean.piscina_use_weather_forecast', 'off') %}
          1.0  # Ajuste desativado
        {% else %}
          {% set condition = states('weather.home') %}
          {% if condition in ['sunny', 'clear'] %}
            0.8  # Ensolarado: -20%
          {% elif condition in ['partlycloudy'] %}
            1.0  # Parcial: sem ajuste
          {% elif condition in ['cloudy'] %}
            1.2  # Nublado: +20%
          {% elif condition in ['rainy', 'pouring'] %}
            2.0  # Chuva: +100%
          {% else %}
            1.0  # Desconhecido: sem ajuste
          {% endif %}
        {% endif %}
```

**Atributos Disponíveis:**
- `weather_condition`: Estado atual (ex: "sunny", "cloudy")
- `adjustment_enabled`: true/false
- `recommendation`: Mensagem explicativa

---

### **2. Toggle de Ativação** ✅ CRIADO

**Localização:** `packages/piscina_solar_optimization.yaml`

```yaml
input_boolean:
  piscina_use_weather_forecast:
    name: "🌤️ Ajustar por Meteorologia"
    icon: mdi:weather-partly-cloudy
    initial: true  # ✅ Ativo por padrão
```

**Controlo:**
- Dashboard > Otimizações > Toggle "Ajustar por Meteorologia"
- Quando OFF: multiplicador sempre 1.0 (sem ajuste)
- Quando ON: multiplicador dinâmico baseado em weather.home

---

### **3. Entidade Weather** ⚠️ VERIFICAR

**Entidade usada:** `weather.home`

**IMPORTANTE:** Confirmar se esta entidade existe:

```bash
# Listar entidades weather
grep "weather\." .storage/core.entity_registry | cut -d'"' -f4
```

Se `weather.home` não existir, editar `sensors/piscina_weather_adjustment.yaml` e trocar para a entidade correta.

---

## ❌ PROBLEMA: BLUEPRINT NÃO INTEGRADA

### **Status Atual:**

✅ Sensor criado e funcional  
✅ Toggle criado e funcional  
❌ **Blueprint NÃO usa o sensor** (ainda!)

### **Onde Deveria Estar:**

A blueprint calcula delays em duas variáveis:

**`effective_delay_on`** (linha ~1013):
```yaml
effective_delay_on: >-
  {% if operation_mode == 'aggressive' %}
    {{ (delay_on * 0.5)|int }}
  {% elif operation_mode == 'conservative' %}
    {{ (delay_on * 1.5)|int }}
  {% elif operation_mode == 'emergency' %}
    {{ 10 }}
  {% else %}
    {{ delay_on }}
  {% endif %}
```

**`effective_delay_off`** (linha ~1032):
```yaml
effective_delay_off: >-
  {% if power_drop_expected > 50 %}
    {{ delay_off * 2 }}
  {% elif power_drop_expected > 30 %}
    {{ (delay_off * 1.5)|int }}
  {% else %}
    {{ delay_off }}
  {% endif %}
```

---

## ✅ SOLUÇÃO: INTEGRAR METEOROLOGIA NA BLUEPRINT

### **Opção 1: Input Opcional (RECOMENDADO)**

Adicionar novo input à blueprint para o sensor de meteorologia:

```yaml
# Na secção de inputs (linha ~50)
weather_multiplier:
  name: "🌤️ Sensor Multiplicador Meteorologia"
  description: "Sensor que ajusta delays baseado em previsão tempo (opcional)"
  default: {}
  selector:
    entity:
      domain: sensor
      filter:
        - device_class: null
```

Depois alterar cálculos de delay:

```yaml
# Variável helper (linha ~900)
weather_multiplier: >-
  {% if weather_multiplier is defined and weather_multiplier != None %}
    {{ states(weather_multiplier)|float(1.0) }}
  {% else %}
    1.0
  {% endif %}

# Aplicar em effective_delay_on (linha ~1013)
effective_delay_on: >-
  {% set base_delay = delay_on %}
  {% if operation_mode == 'aggressive' %}
    {% set base_delay = (base_delay * 0.5)|int %}
  {% elif operation_mode == 'conservative' %}
    {% set base_delay = (base_delay * 1.5)|int %}
  {% elif operation_mode == 'emergency' %}
    {% set base_delay = 10 %}
  {% endif %}
  {{ (base_delay * weather_multiplier)|int }}

# Aplicar em effective_delay_off (linha ~1032)
effective_delay_off: >-
  {% set base_delay = delay_off %}
  {% if power_drop_expected > 50 %}
    {% set base_delay = base_delay * 2 %}
  {% elif power_drop_expected > 30 %}
    {% set base_delay = (base_delay * 1.5)|int %}
  {% endif %}
  {{ (base_delay * weather_multiplier)|int }}
```

---

### **Opção 2: Hard-Coded (Mais Simples, Menos Flexível)**

Adicionar diretamente na blueprint sem input:

```yaml
# Variável helper (linha ~900)
weather_multiplier: >-
  {% set weather_entity = 'sensor.piscina_weather_delay_multiplier' %}
  {% if states(weather_entity) not in ['unknown', 'unavailable'] %}
    {{ states(weather_entity)|float(1.0) }}
  {% else %}
    1.0
  {% endif %}

# Aplicar nos mesmos locais da Opção 1
```

**Vantagem:** Não precisa configurar input  
**Desvantagem:** Sensor fixo, sem flexibilidade

---

## 🧪 COMO TESTAR (Após Integração)

### **Teste 1: Verificar Multiplicador**

```yaml
# Ferramentas Dev > Estados
sensor.piscina_weather_delay_multiplier

# Deve mostrar:
State: 0.8 (se ensolarado)
State: 1.0 (se parcial/desconhecido)
State: 1.2 (se nublado)
State: 2.0 (se chuva)
```

### **Teste 2: Simular Condições**

```yaml
# Ferramentas Dev > Serviços
service: weather.set_weather
data:
  entity_id: weather.home
  weather_condition: rainy

# Aguardar 30s e verificar:
sensor.piscina_weather_delay_multiplier
# Deve mudar para 2.0
```

### **Teste 3: Validar Delays Reais**

```bash
# Monitorizar logs da blueprint
tail -f home-assistant.log | grep "🏊.*delay"

# Com sol (multiplier 0.8):
# delay_on = 300s × 0.8 = 240s

# Com chuva (multiplier 2.0):
# delay_on = 300s × 2.0 = 600s
```

---

## 📈 IMPACTO ESPERADO

### **Sem Ajuste Meteorológico:**
```
Dia Ensolarado:
├─ Delay ON: 300s (desnecessariamente longo)
├─ Delay OFF: 180s
└─ Resultado: Perde oportunidades de ligar rápido

Dia Chuvoso:
├─ Delay ON: 300s (curto demais)
├─ Delay OFF: 180s (curto demais)
└─ Resultado: Liga/desliga muito rápido (oscilações)
```

### **Com Ajuste Meteorológico:**
```
Dia Ensolarado (0.8×):
├─ Delay ON: 240s (-20% mais rápido)
├─ Delay OFF: 144s (-20% mais rápido)
└─ Resultado: ✅ Aproveita melhor janelas de sol estável

Dia Chuvoso (2.0×):
├─ Delay ON: 600s (+100% mais conservador)
├─ Delay OFF: 360s (+100% mais conservador)
└─ Resultado: ✅ Evita oscilações em condições instáveis
```

### **Métricas Estimadas:**

| Métrica | Sem Ajuste | Com Ajuste | Melhoria |
|---------|------------|------------|----------|
| **ON/OFF por dia (sol)** | 8-12 | 6-10 | -20% |
| **ON/OFF por dia (chuva)** | 15-25 | 5-8 | -60% |
| **Aproveitamento solar** | 85% | 92% | +7% |
| **Oscilações em chuva** | Alta | Baixa | -50% |

---

## 🚀 PRÓXIMOS PASSOS

### **Passo 1: Verificar Entidade Weather** (AGORA)

```bash
docker exec homeassistant grep "weather\." /config/.storage/core.entity_registry | grep -o '"entity_id":"[^"]*"' | cut -d'"' -f4
```

Se `weather.home` não existir, editar:
```bash
nano sensors/piscina_weather_adjustment.yaml
# Trocar 'weather.home' pela entidade correta
```

### **Passo 2: Integrar na Blueprint** (OPCIONAL)

Escolher Opção 1 (input opcional) ou Opção 2 (hard-coded) acima.

Benefícios:
- ✅ Sistema adapta-se automaticamente ao clima
- ✅ Menos oscilações em dias instáveis
- ✅ Mais eficiente em dias ensolarados
- ✅ Totalmente configurável via toggle no dashboard

### **Passo 3: Validar Funcionamento** (Após Integração)

1. Dashboard > Otimizações > Ajuste Meteo: ON
2. Verificar sensor mostra multiplicador correto
3. Monitorizar logs para confirmar delays ajustados
4. Comparar eventos ON/OFF antes/depois

---

## 📝 NOTAS TÉCNICAS

### **Interação com Modos de Operação:**

A meteorologia **multiplica após** o modo de operação:

```
Delay Final = delay_base × modo_operação × weather_multiplier

Exemplo (Nublado + Conservative):
delay_on = 300s × 1.5 (conservative) × 1.2 (nublado)
delay_on = 300s × 1.8 = 540s
```

### **Prioridade de Ajustes:**

1. **Modo Operação** (aggressive/conservative/emergency)
2. **Antecipação de Queda** (power_drop_expected)
3. **🌤️ Meteorologia** (weather_multiplier)

### **Fallback Seguro:**

Se sensor indisponível ou weather.home não existe:
```yaml
weather_multiplier → 1.0 (sem ajuste)
```

Sistema continua funcional mesmo sem integração meteorológica.

---

## 📚 REFERÊNCIAS

**Ficheiros Relacionados:**
- `sensors/piscina_weather_adjustment.yaml` - Sensor multiplicador
- `packages/piscina_solar_optimization.yaml` - Toggle ativação
- `blueprints/automation/piscina_solar/piscina_solar_control_v2.yaml` - Blueprint (não integrado)
- `lovelace/piscina_solar_dashboard.yaml` - Visualização no dashboard

**Documentação:**
- `docs/OTIMIZACOES_RESUMO.md` - Resumo otimizações v2.1
- `docs/INSTALACAO_OTIMIZACOES.md` - Guia instalação
- `docs/PROXIMOS_PASSOS.md` - Checklist implementação

---

**Status:** ⚠️ Sensor criado mas **blueprint não integrada**  
**Próxima ação:** Verificar weather.home existe, depois (opcional) integrar na blueprint  
**Prioridade:** Média (sistema funciona sem, mas melhora significativa com)
