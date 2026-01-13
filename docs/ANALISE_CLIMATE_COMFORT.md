# 🔬 ANÁLISE: climate_comfort_monolitico.yaml

## 📊 Estatísticas

- **Tamanho:** 1.139 linhas, ~51 KB
- **Sensores totais:** 58 template sensors
- **Divisões:** 5 (Sala Inferior, Cave, Cozinha, Quarto Luisa, Quarto)
- **Sensores por divisão:** ~9-11 cada
- **Duplicação de código:** ~90% (mesma lógica replicada)

## 🏠 Breakdown por Divisão

| Divisão | Sensores | Input Temp | Input Humidity |
|---------|----------|------------|----------------|
| **Sala Inferior** | 9 | `sensor.bthome_sensor_4ee3_temperature` | `sensor.bthome_sensor_4ee3_humidity` |
| **Cave** | 9 | `sensor.bthome_sensor_9a9b_temperature` | `sensor.bthome_sensor_9a9b_humidity` |
| **Cozinha** | 9 | `sensor.bthome_sensor_2b45_temperature` | `sensor.bthome_sensor_2b45_humidity` |
| **Quarto Luisa** | 9 | `sensor.bthome_sensor_abf1_temperature` | `sensor.bthome_sensor_abf1_humidity` |
| **Quarto** | 9 | `sensor.bthome_sensor_0b29_temperature` | `sensor.bthome_sensor_0b29_humidity` |

## 📐 Métricas Calculadas (por divisão)

1. **Ponto de orvalho** (Dew Point) - Temperatura de saturação
2. **Humidade absoluta** - g/m³ de vapor de água
3. **Margem de condensação** - Diferença T atual vs ponto orvalho
4. **Comfort score** - 0-100% (T ideal 22°C, RH ideal 50%)
5. **Heat Index** - Sensação térmica (T+RH)
6. **Humidex** - Índice canadiano
7. **WBGT (sombra)** - Wet Bulb Globe Temperature
8. **Enthalpia** - Energia térmica total (kJ/kg)
9. *(algumas divisões têm sensores extra)*

## 🔄 Opções de Refatoração

### **Opção A: Usar Custom Component `thermal_comfort` (RECOMENDADO)**

✅ **Prós:**
- Custom component **já instalado** (`dolezsa/thermal_comfort`)
- Calcula automaticamente todas as métricas
- Menos código, mais robusto
- Atualizações e bugfixes automáticos
- Documentação: https://github.com/dolezsa/thermal_comfort

❌ **Contras:**
- Requer configuração via UI (Config Flow)
- Pode não ter todas as métricas custom (verificar)
- Migração requer recriar sensores

**Configuração típica:**
```yaml
# Via UI em: Configurações → Integrações → Adicionar → Thermal Comfort
# Ou via configuration.yaml (se suportar):
thermal_comfort:
  sala_inferior:
    temperature_sensor: sensor.bthome_sensor_4ee3_temperature
    humidity_sensor: sensor.bthome_sensor_4ee3_humidity
  cave:
    temperature_sensor: sensor.bthome_sensor_9a9b_temperature
    humidity_sensor: sensor.bthome_sensor_9a9b_humidity
  # ... outras divisões
```

### **Opção B: Subdividir em 5 ficheiros YAML (FALLBACK)**

Se o custom component não suportar todas as métricas, subdividir:

```
packages/clima/
  ├── README.md
  ├── sala_inferior.yaml    (9 sensores, ~230 linhas)
  ├── cave.yaml             (9 sensores, ~230 linhas)
  ├── cozinha.yaml          (9 sensores, ~230 linhas)
  ├── quarto_luisa.yaml     (9 sensores, ~230 linhas)
  └── quarto.yaml           (9 sensores, ~230 linhas)
```

✅ **Prós:**
- Mantém controlo total das fórmulas
- Fácil de manter por divisão
- Sensores custom adicionais

❌ **Contras:**
- Ainda duplica código (mesma lógica 5×)
- Manutenção de fórmulas em múltiplos locais

### **Opção C: Template Macro (AVANÇADO)**

Criar um macro Jinja2 reutilizável (requer Python/Jinja advanced):
- Mais complexo
- Não recomendado para este caso

## 🎯 RECOMENDAÇÃO

### **Fase 1: Investigar Custom Component** (10 min)

1. Verificar se `thermal_comfort` calcula todas as métricas necessárias:
   - Dew Point ✅ (provavelmente)
   - Absolute Humidity ✅
   - Heat Index ✅
   - Humidex ✅
   - WBGT ⚠️ (verificar)
   - Enthalpia ⚠️ (verificar)
   - Comfort Score ❌ (custom, provavelmente não)
   - Margem Condensação ❌ (custom, definitivamente não)

2. Testar numa divisão (ex: Cave)
   ```bash
   # Adicionar via UI: Configurações → Integrações → Thermal Comfort
   # Configurar com sensor da Cave
   # Comparar resultados com sensores atuais
   ```

3. **Se 80%+ das métricas estiverem cobertas:**
   - Migrar para o custom component
   - Manter apenas 2-3 sensores custom (Comfort Score, Margem Condensação)
   - **Redução: 58 sensores → ~15 sensores custom + 40 do component**

4. **Se <80% cobertas:**
   - Subdividir em 5 ficheiros YAML (Opção B)
   - **Redução: 1 ficheiro 1.139 linhas → 5 ficheiros ~230 linhas cada**

### **Fase 2: Implementar (dependendo do resultado)**

**Cenário A (Custom Component):**
```yaml
# packages/clima_comfort_config.yaml (novo)
# Se o component suportar YAML:

thermal_comfort:
  - unique_id: sala_inferior_comfort
    name: "Sala Inferior"
    temperature_sensor: sensor.bthome_sensor_4ee3_temperature
    humidity_sensor: sensor.bthome_sensor_4ee3_humidity
  # ... repetir para outras divisões

# Manter sensores custom:
template:
  - sensor:
      - name: "Sala Inferior - Comfort score"
        # ... custom logic
      - name: "Sala Inferior - Margem de condensação"
        # ... custom logic
```

**Cenário B (Subdivisão):**
- Criar `packages/clima/` directory
- Extrair cada divisão para seu ficheiro
- Atualizar `configuration.yaml` para incluir a pasta

## ⚠️ RISCOS

| Cenário | Risco | Mitigação |
|---------|-------|-----------|
| **Migrar para component** | MÉDIO | Testar numa divisão primeiro, comparar valores |
| **Subdividir YAML** | BAIXO | Copiar/colar, validar sintaxe |
| **Manter como está** | BAIXO | Funciona, mas difícil manter |

## 📝 PRÓXIMOS PASSOS

1. ✅ **Decisão:** Qual opção seguir? (A ou B)
2. ⏳ **Teste:** Se Opção A, testar component numa divisão
3. ⏳ **Implementação:** Migrar ou subdividir
4. ⏳ **Validação:** Comparar valores, verificar dashboards
5. ⏳ **Backup:** Manter `climate_comfort_monolitico.yaml.backup`
6. ⏳ **Commit:** Documentar alterações

## 🔗 Links Úteis

- **Custom Component:** https://github.com/dolezsa/thermal_comfort
- **HA Thermal Comfort Docs:** https://www.home-assistant.io/integrations/thermal_comfort (oficial?)
- **Template Sensors:** https://www.home-assistant.io/integrations/template/
