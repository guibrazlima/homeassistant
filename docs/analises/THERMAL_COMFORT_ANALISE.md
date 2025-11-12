# 🌡️ Análise - Thermal Comfort (Conforto Térmico)

**Data:** 12 de novembro de 2025  
**Ficheiro Original:** `thermal_comfort.yaml`  
**Estado:** Monolítico (todas divisões num ficheiro)

---

## 📊 Análise do Ficheiro Atual

### Estrutura Atual

```yaml
thermal_comfort.yaml (987 bytes)
├─ custom_icons: true (configuração global)
└─ sensor: (5 divisões monitorizadas)
   ├─ Outside Eira (exterior)
   ├─ Cave (cave)
   ├─ Sala Superior (sala)
   ├─ Suite Principal (quarto principal)
   └─ Quarto Miudos (quarto crianças)
```

### 🔍 Análise Detalhada

| Divisão | Sensor Temperatura | Sensor Humidade | Unique ID | Categoria |
|---------|-------------------|-----------------|-----------|-----------|
| **Outside Eira** | bthome_sensor_6a2b_temperature | bthome_sensor_6a2b_humidity | 2f842c63...677514 | Exterior |
| **Cave** | bthome_sensor_25e6_temperature | bthome_sensor_25e6_humidity | 11adccb5...c27c | Cave |
| **Sala Superior** | sala_superior_temperature | sala_superior_humidity | 2f842c63...673456 | Comum |
| **Suite Principal** | meu_quarto_temperature | meu_quarto_humidity | 2f842c63...673456 | Privado |
| **Quarto Miudos** | quarto_miudos_temperature | quarto_miudos_humidity | 2f842c63...553453 | Privado |

### ⚠️ Problemas Identificados

1. **🔴 Monolítico**
   - Todas as divisões num único ficheiro
   - Dificulta manutenção e adição de novas divisões
   - Sem organização por tipo de espaço

2. **🟡 Sensores BThome vs Outros**
   - Exterior e Cave usam sensores BThome (sensor.bthome_sensor_*)
   - Outras divisões usam sensores diretos (sensor.sala_superior_*)
   - Inconsistência na nomenclatura

3. **🟡 Unique IDs**
   - Alguns IDs parecem duplicados/similares
   - Suite Principal tem ID igual a Sala Superior (provável erro)

4. **🟡 Nomes em Português**
   - "Outside Eira" mistura inglês/português
   - "Quarto Miudos" sem acento ("Miúdos")

5. **🔴 Componente com Erro**
   - Custom component `thermal_comfort` está com erro de importação
   - Precisa atualização ou alternativa

---

## 🎯 Proposta de Melhoria

### 1️⃣ Estrutura Modular por Categoria

```
packages/
├─ thermal_comfort_exterior.yaml    (áreas exteriores)
├─ thermal_comfort_comum.yaml       (áreas comuns)
├─ thermal_comfort_quartos.yaml     (quartos/privados)
└─ thermal_comfort_utilidade.yaml   (cave, garagem, etc)
```

### 2️⃣ Organização Proposta

#### 📁 `packages/thermal_comfort_exterior.yaml`
```yaml
# Conforto Térmico - Áreas Exteriores
# Monitorização de temperatura e humidade em espaços exteriores

thermal_comfort:
  - custom_icons: true
    sensor:
      - name: Eira Exterior
        temperature_sensor: sensor.bthome_sensor_6a2b_temperature
        humidity_sensor: sensor.bthome_sensor_6a2b_humidity
        unique_id: thermal_comfort_eira_exterior
        # Sensores derivados:
        # - sensor.eira_exterior_absolute_humidity
        # - sensor.eira_exterior_heat_index
        # - sensor.eira_exterior_dew_point
        # - sensor.eira_exterior_thermal_perception
```

#### 📁 `packages/thermal_comfort_utilidade.yaml`
```yaml
# Conforto Térmico - Áreas de Utilidade
# Cave, garagem, arrumos, etc.

thermal_comfort:
  - custom_icons: true
    sensor:
      - name: Cave
        temperature_sensor: sensor.bthome_sensor_25e6_temperature
        humidity_sensor: sensor.bthome_sensor_25e6_humidity
        unique_id: thermal_comfort_cave
        # Importante para monitorizar humidade e prevenir bolor
```

#### 📁 `packages/thermal_comfort_comum.yaml`
```yaml
# Conforto Térmico - Áreas Comuns
# Salas, cozinha, corredores, etc.

thermal_comfort:
  - custom_icons: true
    sensor:
      - name: Sala Superior
        temperature_sensor: sensor.sala_superior_temperature
        humidity_sensor: sensor.sala_superior_humidity
        unique_id: thermal_comfort_sala_superior
```

#### 📁 `packages/thermal_comfort_quartos.yaml`
```yaml
# Conforto Térmico - Quartos
# Monitorização de conforto nos quartos (importante para qualidade do sono)

thermal_comfort:
  - custom_icons: true
    sensor:
      - name: Suite Principal
        temperature_sensor: sensor.suite_principal_temperature
        humidity_sensor: sensor.suite_principal_humidity
        unique_id: thermal_comfort_suite_principal
        # Conforto ideal: 18-22°C, 40-60% humidade

      - name: Quarto Miúdos
        temperature_sensor: sensor.quarto_miudos_temperature
        humidity_sensor: sensor.quarto_miudos_humidity
        unique_id: thermal_comfort_quarto_miudos
        # Importante: crianças são mais sensíveis a temperatura
```

---

## 📋 Recomendações de Melhoria

### 🔴 Prioridade Alta

1. **Corrigir Unique IDs Duplicados**
   ```yaml
   # ANTES (duplicado):
   unique_id: 2f842c63-051a-4c49-9da2-4f04ee673456  # Sala Superior
   unique_id: 2f842c63-051a-4c49-9da2-4f05fe673456 # Suite (similar)
   
   # DEPOIS (únicos e descritivos):
   unique_id: thermal_comfort_sala_superior
   unique_id: thermal_comfort_suite_principal
   unique_id: thermal_comfort_quarto_miudos
   ```

2. **Atualizar Componente thermal_comfort**
   - Verificar versão compatível com HA atual
   - Ou implementar alternativa com template sensors

3. **Subdividir em Packages**
   - 4 ficheiros modulares por categoria
   - Facilita manutenção e expansão

### 🟡 Prioridade Média

4. **Padronizar Nomenclatura**
   ```yaml
   # ANTES:
   name: Outside Eira        # Inglês + Português
   name: Quarto Miudos       # Sem acento
   
   # DEPOIS (português correto):
   name: Eira Exterior
   name: Quarto Miúdos
   ```

5. **Adicionar Documentação em Comentários**
   - Explicar sensores derivados criados
   - Valores ideais de conforto por divisão
   - Alertas/automações relacionadas

6. **Verificar Sensores Base**
   ```yaml
   # Confirmar que estes sensores existem:
   sensor.meu_quarto_temperature     → sensor.suite_principal_temperature?
   sensor.quarto_miudos_temperature  → confirmar existe
   sensor.sala_superior_temperature  → confirmar existe
   ```

### 🟢 Prioridade Baixa

7. **Criar Grupos por Categoria**
   ```yaml
   # Em groups.yaml ou package
   group:
     thermal_comfort_exterior:
       name: Conforto Térmico - Exterior
       entities:
         - sensor.eira_exterior_temperature
         - sensor.eira_exterior_humidity
         - sensor.eira_exterior_heat_index
   ```

8. **Adicionar Alertas de Conforto**
   ```yaml
   # Exemplo de automação
   - Alertar se humidade > 70% (risco de bolor)
   - Alertar se temperatura quarto crianças < 18°C
   - Sugerir ventilação se heat_index elevado
   ```

---

## 🎨 Alternativa: Template Sensors (Sem Custom Component)

Se o componente `thermal_comfort` continuar com erros, pode-se recriar com templates:

```yaml
# packages/thermal_comfort_templates.yaml
template:
  - sensor:
      # Ponto de Orvalho (Dew Point)
      - name: "Sala Superior - Ponto de Orvalho"
        unique_id: sala_superior_dew_point
        unit_of_measurement: "°C"
        state: >
          {% set T = states('sensor.sala_superior_temperature') | float %}
          {% set RH = states('sensor.sala_superior_humidity') | float %}
          {% set a = 17.27 %}
          {% set b = 237.7 %}
          {% set alpha = ((a * T) / (b + T)) + log(RH/100.0) %}
          {{ ((b * alpha) / (a - alpha)) | round(1) }}
        
      # Índice de Calor (Heat Index)
      - name: "Sala Superior - Índice de Calor"
        unique_id: sala_superior_heat_index
        unit_of_measurement: "°C"
        state: >
          {% set T = states('sensor.sala_superior_temperature') | float %}
          {% set RH = states('sensor.sala_superior_humidity') | float %}
          {% if T < 27 %}
            {{ T }}
          {% else %}
            {# Fórmula simplificada do Heat Index #}
            {% set HI = -8.78 + 1.61*T + 2.34*RH - 0.14*T*RH %}
            {{ HI | round(1) }}
          {% endif %}
```

---

## 📊 Estrutura Final Recomendada

```
/data/homeassistant/
├─ thermal_comfort.yaml (MANTER como fallback, comentado)
│
└─ packages/
   ├─ thermal_comfort/
   │  ├─ README.md (documentação)
   │  ├─ exterior.yaml (1 divisão)
   │  ├─ utilidade.yaml (1 divisão - cave)
   │  ├─ comum.yaml (1 divisão - salas)
   │  ├─ quartos.yaml (2 divisões)
   │  └─ groups.yaml (agrupamentos)
   │
   └─ (outros packages...)
```

---

## ✅ Checklist de Implementação

- [ ] 1. Criar diretório `packages/thermal_comfort/`
- [ ] 2. Criar 4 ficheiros modulares (exterior, utilidade, comum, quartos)
- [ ] 3. Corrigir unique IDs (usar formato descritivo)
- [ ] 4. Padronizar nomes (português correto)
- [ ] 5. Verificar sensores base existem
- [ ] 6. Adicionar documentação em comentários
- [ ] 7. Criar groups.yaml para agrupamentos
- [ ] 8. Testar configuração (hass check_config)
- [ ] 9. Comentar thermal_comfort.yaml original (backup)
- [ ] 10. Atualizar configuration.yaml se necessário
- [ ] 11. Validar no HA (reiniciar e verificar sensores)
- [ ] 12. Documentar em docs/analises/

---

## 🔗 Referências

- **Custom Component:** https://github.com/dolezsa/thermal_comfort
- **Fórmulas:** Dew Point, Heat Index, Absolute Humidity
- **Valores Ideais de Conforto:**
  - Temperatura: 18-22°C (quartos), 20-24°C (salas)
  - Humidade: 40-60% (ideal), <70% (prevenir bolor)

---

## 💡 Benefícios da Modularização

1. **Organização** - Ficheiros pequenos e específicos
2. **Manutenção** - Fácil encontrar e editar divisão específica
3. **Escalabilidade** - Adicionar novas divisões sem tocar nas existentes
4. **Documentação** - Comentários específicos por categoria
5. **Testes** - Validar e testar por categoria
6. **Performance** - HA carrega packages em paralelo
7. **Reutilização** - Template comum para novas divisões

---

**Status:** 📝 Análise concluída - Pronto para implementação
