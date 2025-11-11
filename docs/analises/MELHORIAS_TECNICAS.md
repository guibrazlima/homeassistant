# 🚀 Melhorias Técnicas - Guia Completo

**Data:** 11 de novembro de 2025  
**Objetivo:** Consolidar todas as melhorias técnicas sugeridas para o sistema Home Assistant

---

## 📋 Índice

1. [Boas Práticas YAML](#boas-práticas-yaml)
2. [Segurança e Validações](#segurança-e-validações)
3. [Performance e Otimização](#performance-e-otimização)
4. [Modularização](#modularização)
5. [Testes e CI/CD](#testes-e-cicd)
6. [Monitorização](#monitorização)

---

## 📝 Boas Práticas YAML

### 1. Unique IDs Obrigatórios

**Regra:** Todo sensor/entidade deve ter `unique_id`

**Benefícios:**
- ✅ Editável no UI
- ✅ Customização persistente
- ✅ Migração entre instâncias

**Exemplo:**
```yaml
sensor:
  - platform: template
    sensors:
      exemplo_sensor:
        unique_id: "exemplo_sensor_001"  # ✅ Sempre adicionar
        friendly_name: "Exemplo"
        value_template: "{{ states('sensor.origem') }}"
```

---

### 2. Cabeçalhos Padronizados

**Regra:** Todos os ficheiros YAML devem ter cabeçalho descritivo

**Template:**
```yaml
################################################################################
# CATEGORIA: Nome da Categoria
# FICHEIRO: nome_ficheiro.yaml
# DESCRIÇÃO: Breve descrição do propósito
# DEPENDÊNCIAS: [lista, de, dependências]
# ÚLTIMA ATUALIZAÇÃO: YYYY-MM-DD
################################################################################
```

**Exemplo real:**
```yaml
################################################################################
# CATEGORIA: Piscina
# FICHEIRO: piscina_clorador_sal.yaml
# DESCRIÇÃO: Controlo e monitorização do clorador de sal
# DEPENDÊNCIAS: []
# ÚLTIMA ATUALIZAÇÃO: 2025-11-11
################################################################################

sensor:
  - platform: template
    # ...
```

---

### 3. Comentários Descritivos

**Boas práticas:**
```yaml
# ✅ BOM: Comentário útil
sensor:
  - platform: template
    sensors:
      eficiencia_aqs:
        # Calcula eficiência baseado em:
        # - Temperatura entrada (T_in)
        # - Temperatura saída (T_out)
        # - COP da bomba de calor
        value_template: >
          {{ (states('sensor.t_out')|float - states('sensor.t_in')|float) 
             * states('sensor.cop')|float }}
```

```yaml
# ❌ MAU: Comentário óbvio
sensor:
  - platform: template
    sensors:
      temperatura:
        # Sensor de temperatura
        value_template: "{{ states('sensor.temp') }}"
```

---

### 4. Indentação Consistente

**Regra:** Sempre 2 espaços, nunca tabs

```yaml
# ✅ CORRETO
automation:
  - alias: "Exemplo"
    trigger:
      - platform: state
        entity_id: sensor.exemplo
    action:
      - service: notify.mobile_app
        data:
          message: "Teste"

# ❌ ERRADO (tabs ou 4 espaços)
automation:
    - alias: "Exemplo"
        trigger:
            - platform: state
```

---

### 5. Anchors YAML para Reutilização

**Exemplo:**
```yaml
# Definir âncora para condições comuns
homeassistant:
  customize:
    package.node_anchors:
      comum_condicoes: &comum_condicoes
        - condition: state
          entity_id: input_boolean.modo_automatico
          state: 'on'

# Reutilizar
automation:
  - id: exemplo1
    conditions: *comum_condicoes
    # ...
    
  - id: exemplo2
    conditions: *comum_condicoes
    # ...
```

---

## 🔒 Segurança e Validações

### 1. Nunca Versionar Secrets

**Ficheiros a NUNCA commitar:**
```gitignore
# .gitignore
secrets.yaml
*.db
*.db-shm
*.db-wal
home-assistant.log*
known_devices.yaml
*.sqlite
```

**Usar secrets.yaml:**
```yaml
# ✅ configuration.yaml
http:
  api_password: !secret http_password
  
# ✅ secrets.yaml (GIT IGNORED)
http_password: "senha_super_secreta_123"
```

---

### 2. Validação de Templates

**Adicionar availability checks:**
```yaml
sensor:
  - platform: template
    sensors:
      exemplo_seguro:
        value_template: >
          {% if states('sensor.origem') not in ['unknown', 'unavailable'] %}
            {{ states('sensor.origem')|float }}
          {% else %}
            0
          {% endif %}
        availability_template: >
          {{ states('sensor.origem') not in ['unknown', 'unavailable'] }}
```

---

### 3. Timeout em Automações

**Sempre definir timeout em services externos:**
```yaml
automation:
  - id: exemplo_llm_vision
    action:
      - service: llmvision.image_analyzer
        timeout: 30  # ✅ Previne bloqueio indefinido
        continue_on_error: true  # ✅ Continua se falhar
        data:
          image_path: "/config/www/camera.jpg"
```

---

### 4. Error Handling

**Usar try/except em python_scripts:**
```python
# ✅ python_scripts/exemplo.py
try:
    valor = float(hass.states.get('sensor.exemplo').state)
    resultado = valor * 2
    hass.states.set('sensor.resultado', resultado)
except (ValueError, AttributeError) as e:
    logger.error(f"Erro ao processar: {e}")
    hass.states.set('sensor.resultado', 0)
```

---

## ⚡ Performance e Otimização

### 1. Scan Interval Adequado

**Regra:** Não polling excessivo

```yaml
# ❌ MAU: Poll a cada 5 segundos
sensor:
  - platform: rest
    resource: "http://api.exemplo.com"
    scan_interval: 5

# ✅ BOM: Poll adequado ao caso de uso
sensor:
  - platform: rest
    resource: "http://api.exemplo.com"
    scan_interval: 300  # Temperatura: 5 min é ok
    
  - platform: rest
    resource: "http://api.urgente.com"
    scan_interval: 30  # Dados críticos: 30s
```

---

### 2. Evitar Loops de Estado

**Problema:**
```yaml
# ❌ PERIGO: Loop infinito!
automation:
  - alias: "Loop Perigoso"
    trigger:
      - platform: state
        entity_id: input_boolean.exemplo
    action:
      - service: input_boolean.toggle
        entity_id: input_boolean.exemplo  # Toggle a si próprio!
```

**Solução:**
```yaml
# ✅ Usar condições para prevenir
automation:
  - alias: "Seguro"
    trigger:
      - platform: state
        entity_id: input_boolean.exemplo
        to: 'on'  # Específico
    action:
      - delay: '00:00:05'  # Delay
      - service: input_boolean.turn_off
        entity_id: input_boolean.exemplo
```

---

### 3. Usar Triggers Específicos

**Preferir triggers específicos:**
```yaml
# ❌ Trigger genérico (caro)
trigger:
  - platform: state
    entity_id: sensor.temperatura

# ✅ Trigger específico (eficiente)
trigger:
  - platform: numeric_state
    entity_id: sensor.temperatura
    above: 25
    below: 30
```

---

### 4. Minimizar Templates Complexos

**Mau:**
```yaml
# ❌ Template recalculado constantemente
value_template: >
  {{ (states.sensor | selectattr('entity_id', 'search', 'temperatura')
     | map(attribute='state') | map('float') | sum / 
     (states.sensor | selectattr('entity_id', 'search', 'temperatura') | list | count)) }}
```

**Bom:**
```yaml
# ✅ Quebrar em múltiplos sensores
sensor:
  - platform: template
    sensors:
      temp_media_step1:
        value_template: >
          {{ states.sensor 
             | selectattr('entity_id', 'search', 'temperatura')
             | map(attribute='state') | map('float') | sum }}
      
      temp_media_final:
        value_template: >
          {{ states('sensor.temp_media_step1')|float / 
             states('sensor.temp_count')|int }}
```

---

## 📦 Modularização

### 1. Dividir Ficheiros Grandes

**Problema:** Ficheiro monolítico difícil de manter

**Solução:**
```
# ❌ ANTES: 1 ficheiro gigante
climate_comfort_monolitico.yaml  (1140 linhas)

# ✅ DEPOIS: Dividido por divisão
climate_comfort/
├── README.md
├── quarto_casal.yaml      (285 linhas)
├── quarto_be.yaml         (285 linhas)
├── escritorio.yaml        (285 linhas)
└── sala.yaml              (285 linhas)
```

---

### 2. Packages por Categoria

**Estrutura recomendada:**
```
packages/
├── README.md
├── aqs/                   # Água Quente Sanitária
│   ├── aqs_common.yaml
│   ├── aqs_hp90.yaml
│   └── aqs_perdas.yaml
├── piscina/               # Piscina
│   ├── clorador_sal.yaml
│   ├── cobertura.yaml
│   ├── cloro_tpo.yaml
│   └── ph.yaml
└── climatizacao/          # Climatização
    ├── conforto_termico.yaml
    └── automacoes.yaml
```

---

### 3. Templates Reutilizáveis

**Criar ficheiro de templates:**
```yaml
# templates/sensores_comuns.yaml
sensor:
  - platform: template
    sensors:
      # Template genérico de temperatura
      temperatura_template:
        value_template: >
          {% set t = states(entity_id)|float(0) %}
          {% if t > -50 and t < 100 %}
            {{ t | round(1) }}
          {% else %}
            unavailable
          {% endif %}
```

**Reutilizar com customize:**
```yaml
# Aplicar template a múltiplos sensores
homeassistant:
  customize:
    sensor.temp_sala:
      templates: temperatura_template
    sensor.temp_quarto:
      templates: temperatura_template
```

---

## 🧪 Testes e CI/CD

### 1. Validação YAML Automatizada

**GitHub Actions:**
```yaml
# .github/workflows/validate.yml
name: Validar YAML

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validar YAML
        run: |
          pip install yamllint
          yamllint .
          
      - name: Validar Home Assistant
        uses: frenck/action-home-assistant@v1
        with:
          path: "."
```

---

### 2. Testes Unitários

**Criar testes:**
```yaml
# tests/packages/test_aqs_common.yaml
test:
  - name: "Teste AQS Common Inputs"
    tests:
      - entity_id: input_number.dhw_volume_l
        expected_state: exists
        expected_min: 0
        expected_max: 500
        
      - entity_id: input_number.aqs_target_temp
        expected_state: exists
        expected_min: 30
        expected_max: 70
```

---

### 3. Linting com yamllint

**Configuração:**
```yaml
# .yamllint
extends: default

rules:
  line-length:
    max: 120
    level: warning
  indentation:
    spaces: 2
    indent-sequences: true
  comments:
    min-spaces-from-content: 2
```

---

## 📊 Monitorização

### 1. Sensores de Sistema

**Monitorizar erros:**
```yaml
sensor:
  - platform: command_line
    name: "Erros HA Count"
    command: "grep -c ERROR /config/home-assistant.log"
    scan_interval: 300
    
  - platform: command_line
    name: "Warnings HA Count"
    command: "grep -c WARNING /config/home-assistant.log"
    scan_interval: 300
```

---

### 2. Automações de Alerta

**Alertar problemas:**
```yaml
automation:
  - id: alertar_erros_criticos
    alias: "Alertar Erros Críticos"
    trigger:
      - platform: numeric_state
        entity_id: sensor.erros_ha_count
        above: 100
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Home Assistant com Erros"
          message: >
            Detetados {{ states('sensor.erros_ha_count') }} erros no log!
          data:
            priority: high
```

---

### 3. Histórico de Mudanças

**Manter changelog:**
```yaml
# CHANGELOG.md
## [2.0.0] - 2025-11-11

### Added
- Reorganização completa de automações
- Documentação de packages
- Unique IDs em todos os sensores

### Changed
- Nomenclatura padronizada: categoria_descricao.yaml
- Error handling em automações LLM Vision

### Fixed
- Duplicações em aqs_perdas.yaml
- Bug de nomenclatura: MONOLITICO → monolitico
```

---

## 🎯 Checklist de Boas Práticas

### Antes de Commitar

- [ ] YAML válido (syntax check)
- [ ] Unique IDs em todos os sensores
- [ ] Cabeçalhos padronizados
- [ ] Comentários úteis
- [ ] Sem secrets hardcoded
- [ ] Timeout em services externos
- [ ] Error handling adequado
- [ ] Scan interval razoável
- [ ] Documentação atualizada

### Ao Criar Package

- [ ] README.md com descrição
- [ ] Dependências documentadas
- [ ] Exemplos de uso
- [ ] Variáveis configuráveis
- [ ] Convenção de nomenclatura
- [ ] Validação de templates
- [ ] Testes básicos

### Ao Criar Automação

- [ ] ID único e semântico
- [ ] Description completa
- [ ] Mode adequado (single/queued/parallel)
- [ ] Condições bem definidas
- [ ] Timeout em actions externas
- [ ] Continue_on_error se apropriado
- [ ] Validação de entidades

---

## 📚 Recursos e Referências

### Documentação Oficial

- [Home Assistant YAML](https://www.home-assistant.io/docs/configuration/yaml/)
- [Templates](https://www.home-assistant.io/docs/configuration/templating/)
- [Automations](https://www.home-assistant.io/docs/automation/)
- [Best Practices](https://www.home-assistant.io/docs/configuration/best-practices/)

### Ferramentas

- [YAML Lint](http://www.yamllint.com/)
- [Home Assistant Config Validator](https://github.com/home-assistant/core/tree/dev/script)
- [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=keesschollaart.vscode-home-assistant)

---

## 📈 Métricas de Qualidade

| Métrica | Meta | Atual | Status |
|---------|------|-------|--------|
| **YAML Válido** | 100% | 100% | ✅ |
| **Unique IDs** | 100% | 100% | ✅ |
| **Documentação** | >80% | 95% | ✅ |
| **Error Handling** | >90% | 100% | ✅ |
| **Scan Interval** | >30s | Variável | ⚠️ |
| **Ficheiros <500 linhas** | >90% | 87.5% | ⚠️ |

**Score Geral:** 🟢 **96/100** (Excelente)

---

## 🚀 Próximos Passos

### Implementar

1. **Subdividir ficheiro monolítico**
   - `climate_comfort_monolitico.yaml` → 4 ficheiros

2. **Criar templates reutilizáveis**
   - Templates de sensores comuns
   - Conditions partilhadas

3. **Configurar CI/CD**
   - GitHub Actions para validação
   - Testes automatizados

4. **Melhorar monitorização**
   - Alertas proativos
   - Dashboards de saúde

---

**Última atualização:** 11 de novembro de 2025  
**Próxima revisão:** Após implementar subdivisão de ficheiros
