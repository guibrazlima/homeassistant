# 📦 Packages - Documentação e Dependências

## 📋 Índice de Packages

### AQS (Águas Quentes Sanitárias)
| Ficheiro | Descrição | Entidades |
|----------|-----------|-----------|
| `aqs_common.yaml` | Configurações partilhadas (volume, temp. alvo) | 2 input_number |
| `aqs_perdas.yaml` | Perdas térmicas do depósito Daikin 500L | 3 sensor, 4 binary_sensor, 10 template |
| `aqs_hp90_estimador_termico.yaml` | Estimador térmico tubos solares HP90 | 4 input_number, ~15 template |

### Piscina
| Ficheiro | Descrição | Entidades |
|----------|-----------|-----------|
| `piscina_clorador_sal.yaml` | Deteção sal baixo via LLM Vision | 2 input_boolean, 2 input_number, 1 binary_sensor, 1 automation |
| `piscina_cobertura.yaml` | Estado cobertura via LLM Vision | 1 binary_sensor, 2 automation |
| `piscina_cloro_tpo.yaml` | Ajuste tempo produção cloro por cobertura | 1 input_boolean, 3 input_number, 2 automation, 1 binary_sensor, 3 sensor |
| `piscina_ph.yaml` | Leitura pH via OCR (LLM Vision) | 2 input_number, 2 input_text, 1 template, 4 sensor stats, 1 automation |

### Clima
| Ficheiro | Descrição | Entidades |
|----------|-----------|-----------|
| `climate_comfort_MONOLITICO.yaml` | ⚠️ Sensores conforto térmico (4 divisões) | 32 template sensors |

> ⚠️ **NOTA:** `climate_comfort_MONOLITICO.yaml` (51 KB, 1140 linhas) contém código muito duplicado
> para 4 divisões (Sala Inferior, Cave, Cozinha, Quarto Luisa). Cada divisão tem 8 sensores idênticos.
> 
> **TODO:** Subdividir em `clima_sala_inferior.yaml`, `clima_cave.yaml`, `clima_cozinha.yaml`, 
> `clima_quarto_luisa.yaml` OU verificar se `thermal_comfort.yaml` (já incluído em configuration.yaml) 
> pode substituir esta funcionalidade.

---

## 🔗 Dependências Externas

### LLM Vision
**Custom Component:** [valentinfrlch/ha-llmvision](https://github.com/valentinfrlch/ha-llmvision)

**Provider ID:** `01K5S60RJSW6MFMB543KEDHE23`  
**Modelo:** `gpt-4o-mini`

**Usado em:**
- `piscina_clorador_sal.yaml` → `camera.cave_hd_stream` (detetar LED "sal baixo")
- `piscina_cobertura.yaml` → `camera.eira_piscina_hd_stream` (estado cobertura)
- `piscina_ph.yaml` → `camera.cave_hd_stream` (OCR do valor pH)

**Configuração:**
```yaml
# LLM Vision deve estar instalado e configurado
# Ver: https://github.com/valentinfrlch/ha-llmvision
```

### Câmaras Necessárias
```yaml
camera.cave_hd_stream           # pH, sal baixo
camera.eira_piscina_hd_stream   # Cobertura piscina
```

### Sensores BTHome
```yaml
# Sala Inferior
sensor.bthome_sensor_4ee3_temperature
sensor.bthome_sensor_4ee3_humidity

# Cave
sensor.bthome_sensor_25e6_temperature
sensor.bthome_sensor_25e6_humidity

# Cozinha (verificar entity_id exato)
sensor.bthome_sensor_XXXX_temperature
sensor.bthome_sensor_XXXX_humidity

# Quarto Luisa (verificar entity_id exato)
sensor.bthome_sensor_YYYY_temperature
sensor.bthome_sensor_YYYY_humidity
```

### Forecast.Solar
**Usado por:** `aqs_hp90_estimador_termico.yaml`

**Configuração da instância:**
- Potência: 1000 Wp
- Inclinação: 20°
- Azimute: 174°

**Sensores necessários:**
```yaml
sensor.power_production_now_tubos_hp90
sensor.energy_production_today_tubos_hp90
```

### HPSU (Daikin)
**Usado por:** `aqs_perdas.yaml`

**Sensores necessários:**
```yaml
sensor.hpsu_can_hot_water_temperature
sensor.hpsu_can_outside_temperature
sensor.hpsu_can_mode_of_operating
select.hpsu_can_target_hot_water_temperature
```

---

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| **Total de packages** | 8 ficheiros |
| **Tamanho total** | ~96 KB |
| **Maior ficheiro** | climate_comfort_MONOLITICO.yaml (51 KB) |
| **Integrações usadas** | 5 (LLM Vision, BTHome, Forecast.Solar, HPSU, Câmaras) |
| **Automações** | 6 automações |
| **Template sensors** | ~60 sensores |
| **Input helpers** | ~15 inputs |

---

## 🔧 Manutenção

### Adicionar Novo Package
1. Criar ficheiro em `packages/nome_package.yaml`
2. Adicionar cabeçalho seguindo o template:
```yaml
#############################################
# 📦 Package: [Nome]
# 🎯 Objetivo: [Descrição]
# 📂 Localização: /config/packages/[nome].yaml
# 🔗 Dependências: [listar]
# 📅 Última atualização: [data]
#############################################
```
3. Reiniciar Home Assistant
4. Verificar logs para erros
5. Atualizar este README.md

### Validar Packages
```bash
cd /data/homeassistant/packages
python3 << 'EOF'
import yaml
from pathlib import Path

for f in Path('.').glob('*.yaml'):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            yaml.safe_load(file)
        print(f"✅ {f.name}")
    except Exception as e:
        print(f"❌ {f.name}: {e}")
EOF
```

---

## 🚨 Problemas Conhecidos

### 1. climate_comfort_MONOLITICO.yaml muito grande
- **Impacto:** Difícil de manter, muito código duplicado
- **Solução proposta:** Subdividir por divisão OU usar `thermal_comfort` integration
- **Status:** ⏳ Pendente

### 2. Dependência forte de LLM Vision
- **Impacto:** Se LLM Vision falhar, 3 automações param
- **Solução proposta:** Adicionar fallbacks e timeouts
- **Status:** ⏳ Pendente (ver Plano B)

### 3. IDs hardcoded de sensores BTHome
- **Impacto:** Se trocar sensor, precisa alterar múltiplos ficheiros
- **Solução proposta:** Usar variáveis ou input_text para entity_ids
- **Status:** ⏳ Futuro

---

## 📅 Histórico de Alterações

### 2025-11-11 - Reorganização Plano A
- ✅ Criado `aqs_common.yaml` para eliminar duplicações
- ✅ Removida duplicação de `dhw_volume_l` e `aqs_target_temp`
- ✅ Adicionados cabeçalhos a todos os packages
- ✅ Adicionados `unique_id` aos sensores statistics
- ✅ Movido `solar_hp90_from_fs.yaml_old` para backups/
- ✅ Renomeado `climate_comfort.yaml` → `climate_comfort_MONOLITICO.yaml`

---

**Última atualização:** 2025-11-11 22:25
