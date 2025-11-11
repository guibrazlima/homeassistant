# 📦 Análise da Pasta Packages

**Data:** 11 de novembro de 2025  
**Configuração:** `configuration.yaml` → `packages: !include_dir_named packages`

---

## ✅ Estado Atual

### Validação YAML
- ✅ **7 ficheiros válidos** (0 erros de sintaxe)
- ⚠️ **1 ficheiro obsoleto** (`solar_hp90_from_fs.yaml_old`)

### Estrutura de Ficheiros

| Ficheiro | Tamanho | Categoria | Componentes |
|----------|---------|-----------|-------------|
| `aqs_perdas.yaml` | 6.7 KB | AQS/Energia | sensor, binary_sensor, template, input_number |
| `climate_comfort.yaml` | 51 KB | Clima/Conforto | template (muitos sensores) |
| `clorador_sal.yaml` | 5.2 KB | Piscina | input_boolean, input_number, automation, template |
| `cobertura_piscina.yaml` | 4.2 KB | Piscina | template, automation (LLM Vision) |
| `hp90_thermal_estimator_v2.yaml` | 16 KB | Solar/AQS | input_number, template |
| `piscina_cloro_tpo_por_cobertura.yaml` | 4.5 KB | Piscina | input_boolean, input_number, automation, template, sensor |
| `piscina_ph.yaml` | 8.4 KB | Piscina | input_number, input_text, template, sensor, automation |

**Total:** 96 KB de configurações em packages

---

## 🎯 Configuração no `configuration.yaml`

```yaml
homeassistant:
  packages: !include_dir_named packages  # ✅ CORRETO
```

**Status:** ✅ Configurado corretamente com `!include_dir_named`

**Como funciona:**
- Cada ficheiro YAML na pasta `packages/` é carregado como um "pacote"
- Permite agrupar entidades relacionadas (sensors, automations, inputs, etc.)
- Sobrepõe-se às configurações globais se houver conflito

---

## ⚠️ Problemas Identificados

### 1. **Ficheiro Obsoleto**
```
packages/solar_hp90_from_fs.yaml_old
```
**Problema:** Ficheiro com extensão `_old` que não é carregado mas polui o diretório  
**Solução:** Mover para pasta `backups/` ou eliminar

### 2. **climate_comfort.yaml é MUITO GRANDE (51 KB)**
**Problema:** Contém 1128 linhas com sensores repetitivos para múltiplas divisões  
**Impacto:**
- Difícil de manter
- Muita duplicação de código
- Lento para carregar

**Exemplo de duplicação:**
```yaml
# Sala Inferior - 8 sensores
- name: "Sala Inferior - Ponto de orvalho"
- name: "Sala Inferior - Humidade absoluta"
- name: "Sala Inferior - Margem de condensação"
- name: "Sala Inferior - Comfort score"
# ... mais 4 sensores

# Cave - mesmos 8 sensores (código duplicado!)
- name: "Cave - Ponto de orvalho"
- name: "Cave - Humidade absoluta"
# ...
```

### 3. **Falta de Documentação Consistente**
- ✅ `aqs_perdas.yaml`: Tem cabeçalho explicativo
- ✅ `clorador_sal.yaml`: Tem comentários descritivos
- ⚠️ `climate_comfort.yaml`: Sem cabeçalho
- ⚠️ `cobertura_piscina.yaml`: Sem cabeçalho
- ⚠️ `piscina_cloro_tpo_por_cobertura.yaml`: Sem cabeçalho

### 4. **Dependências LLM Vision Não Documentadas**
**Ficheiros que usam LLM Vision:**
- `clorador_sal.yaml` → Deteção de LED "sal baixo"
- `cobertura_piscina.yaml` → Estado da cobertura
- `piscina_ph.yaml` → OCR do valor de pH

**Problemas:**
- Não há documentação sobre o provider ID (`01K5S60RJSW6MFMB543KEDHE23`)
- Não está claro quais câmaras são necessárias
- Falta configuração de fallback se LLM Vision falhar

### 5. **Duplicação de input_number.dhw_volume_l**
**Encontrado em:**
- `aqs_perdas.yaml` (linha 8-14)
- `hp90_thermal_estimator_v2.yaml` (linha 33-39)

**Problema:** Definição duplicada pode causar conflito  
**Solução:** Manter apenas num ficheiro ou criar `aqs_common.yaml`

### 6. **Falta de IDs nas Automações de Alguns Packages**
**Com IDs:** ✅
- `clorador_sal.yaml`: `piscina_llmvision_sal_baixo`
- `cobertura_piscina.yaml`: `piscina_llmvision_cobertura`, etc.
- `piscina_cloro_tpo_por_cobertura.yaml`: IDs presentes
- `piscina_ph.yaml`: `piscina_ph_ocr`

**Status:** ✅ Todas as automações têm IDs

### 7. **Automações Sem Descrições Detalhadas**
Algumas automações têm `description:` mas são muito genéricas ou incompletas.

### 8. **Sensores statistics Sem unique_id**
Em `piscina_ph.yaml`:
```yaml
sensor:
  - platform: statistics
    name: "pH — Mín 24h"
    # ❌ Falta unique_id
```

**Problema:** Sensores sem `unique_id` não podem ser configurados no UI

---

## 💡 Sugestões de Melhorias

### 🔥 **PRIORIDADE ALTA**

#### 1. **Reorganizar climate_comfort.yaml**
**Problema:** 51 KB, 1128 linhas, muito código duplicado

**Solução A: Usar Macros Jinja2** (não suportado nativamente no HA)

**Solução B: Criar Package por Divisão**
```
packages/
├── clima/
│   ├── sala_inferior.yaml
│   ├── cave.yaml
│   ├── quarto_principal.yaml
│   └── ...
```

**Solução C: Usar Custom Component**
Considerar usar `thermal_comfort` (já está no `configuration.yaml`!)

**Verificar:**
```yaml
# Em configuration.yaml já existe:
thermal_comfort: !include thermal_comfort.yaml
```

**Ação recomendada:**
1. Verificar se `thermal_comfort.yaml` já faz o que `climate_comfort.yaml` tenta fazer
2. Se sim, migrar entidades e eliminar duplicação
3. Se não, subdividir `climate_comfort.yaml` por divisão

#### 2. **Eliminar Duplicação de dhw_volume_l**
**Opção A:** Criar `packages/aqs_common.yaml`
```yaml
# packages/aqs_common.yaml
input_number:
  dhw_volume_l:
    name: "AQS — Volume (L)"
    min: 50
    max: 1000
    step: 10
    unit_of_measurement: "L"
    initial: 500
    icon: mdi:water-boiler
```

**Opção B:** Manter só em `aqs_perdas.yaml` e remover de `hp90_thermal_estimator_v2.yaml`

#### 3. **Adicionar Cabeçalhos a Todos os Packages**
**Template sugerido:**
```yaml
#############################################
# 📦 Package: [Nome do Package]
# 🎯 Objetivo: [Descrição breve]
# 📂 Localização: /config/packages/[nome].yaml
# 🔗 Dependências: [listar integrações necessárias]
# 📅 Última atualização: [data]
#############################################
```

**Exemplo:**
```yaml
#############################################
# 📦 Package: Cobertura da Piscina
# 🎯 Objetivo: Detetar estado da cobertura via LLM Vision
# 📂 Localização: /config/packages/cobertura_piscina.yaml
# 🔗 Dependências:
#    - LLM Vision (provider: 01K5S60RJSW6MFMB543KEDHE23)
#    - Câmara: camera.eira_piscina_hd_stream
#    - Bomba: switch.bomba_piscina_switch_0
# 📅 Última atualização: 2025-11-11
#############################################
```

#### 4. **Adicionar unique_id a Todos os Sensores statistics**
```yaml
sensor:
  - platform: statistics
    name: "pH — Mín 24h"
    unique_id: ph_piscina_min_24h  # ✅ ADICIONAR
    entity_id: sensor.piscina_ph
    state_characteristic: value_min
    max_age:
      hours: 24
```

### ⚙️ **PRIORIDADE MÉDIA**

#### 5. **Documentar Dependências LLM Vision**
Criar ficheiro `packages/README.md`:
```markdown
# Packages - Dependências

## LLM Vision
- Provider ID: `01K5S60RJSW6MFMB543KEDHE23`
- Modelo: `gpt-4o-mini`
- Usado em:
  - `clorador_sal.yaml` → camera.cave_hd_stream
  - `cobertura_piscina.yaml` → camera.eira_piscina_hd_stream
  - `piscina_ph.yaml` → camera.cave_hd_stream

## Câmaras Necessárias
- camera.cave_hd_stream (pH, sal)
- camera.eira_piscina_hd_stream (cobertura)
```

#### 6. **Adicionar Fallbacks para LLM Vision**
**Problema:** Se LLM Vision falhar, as automações podem ficar em estado indefinido

**Solução:** Adicionar timeouts e estados de fallback
```yaml
action:
  - service: llmvision.data_analyzer
    timeout: 30  # ✅ ADICIONAR timeout
    continue_on_error: true  # ✅ ADICIONAR
    # ...
  
  # ✅ ADICIONAR fallback
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ llmresp is not defined }}"
        sequence:
          - service: notify.telegram
            data:
              message: "⚠️ LLM Vision falhou - usando estado anterior"
```

#### 7. **Consolidar Packages de Piscina**
**Situação atual:**
```
packages/
├── clorador_sal.yaml
├── cobertura_piscina.yaml
├── piscina_cloro_tpo_por_cobertura.yaml
├── piscina_ph.yaml
```

**Opção A:** Manter separado (atual) ✅ RECOMENDADO
- Vantagem: Modular, fácil de desativar individualmente
- Desvantagem: 4 ficheiros relacionados

**Opção B:** Consolidar em subpasta
```
packages/piscina/
├── clorador_sal.yaml
├── cobertura.yaml
├── cloro_tpo.yaml
├── ph.yaml
```

**Nota:** Requer alteração no `configuration.yaml`:
```yaml
homeassistant:
  packages: !include_dir_named packages
  # ❌ Não suporta subpastas automaticamente
```

**Conclusão:** Manter estrutura atual

#### 8. **Adicionar Mode às Automações**
Algumas automações não têm `mode:` definido.

**Estado atual:**
- ✅ `clorador_sal.yaml`: `mode: restart`
- ✅ `cobertura_piscina.yaml`: `mode: restart`
- ✅ `piscina_cloro_tpo_por_cobertura.yaml`: `mode: single`, `mode: restart`
- ✅ `piscina_ph.yaml`: `mode: restart`

**Conclusão:** ✅ Todas têm `mode` definido

### 🎨 **PRIORIDADE BAIXA**

#### 9. **Padronizar Nomes de Entidades**
**Inconsistências encontradas:**
- `sensor.aqs_perda_c_h` vs `sensor.hp90_energia_termica_dia_kwh`
- `input_boolean.piscina_sal_baixo` vs `binary_sensor.piscina_clorador_comando_on`

**Sugestão:** Adoptar convenção consistente:
```
<domínio>.<categoria>_<componente>_<métrica>
sensor.aqs_perda_c_h ✅
sensor.piscina_ph_min_24h ✅
binary_sensor.piscina_cobertura_fechada ✅
```

#### 10. **Otimizar climate_comfort.yaml com Loops**
Se decidir manter num só ficheiro, considerar otimizar com variáveis:

**Antes (duplicado):**
```yaml
- name: "Sala Inferior - Ponto de orvalho"
  # ... código ...
- name: "Cave - Ponto de orvalho"
  # ... mesmo código ...
```

**Depois (otimizado - requer template avançado):**
Não é trivial em YAML, mas pode-se usar `customize:` para centralizar fórmulas.

---

## 🏗️ Estrutura Proposta Final

### Reorganização Sugerida

```
packages/
├── README.md                              # ✨ NOVO - Documentação
├── aqs/
│   ├── aqs_common.yaml                    # ✨ NOVO - Inputs comuns
│   ├── aqs_perdas.yaml                    # Movido
│   └── hp90_thermal_estimator_v2.yaml     # Movido
├── piscina/
│   ├── clorador_sal.yaml                  # Movido
│   ├── cobertura.yaml                     # Renomeado
│   ├── cloro_tpo.yaml                     # Renomeado
│   └── ph.yaml                            # Renomeado
├── clima/
│   ├── sala_inferior.yaml                 # ✨ NOVO - Split de climate_comfort
│   ├── cave.yaml                          # ✨ NOVO
│   ├── quarto_principal.yaml              # ✨ NOVO
│   └── ...
└── backups/
    └── solar_hp90_from_fs.yaml_old        # Movido
```

**⚠️ ATENÇÃO:** Esta reorganização requer alteração no `configuration.yaml` porque `!include_dir_named` não suporta subpastas.

**Alternativa:** Manter estrutura flat mas com prefixos:
```
packages/
├── README.md                              # ✨ NOVO
├── aqs_common.yaml                        # ✨ NOVO
├── aqs_perdas.yaml                        # ✅ Mantém
├── aqs_hp90_thermal_estimator.yaml        # Renomeado (remover _v2)
├── clima_sala_inferior.yaml               # ✨ NOVO
├── clima_cave.yaml                        # ✨ NOVO
├── clima_quarto_principal.yaml            # ✨ NOVO
├── piscina_clorador_sal.yaml              # Renomeado
├── piscina_cobertura.yaml                 # Renomeado
├── piscina_cloro_tpo.yaml                 # Renomeado
└── piscina_ph.yaml                        # Renomeado
```

---

## 📋 Checklist de Ações Recomendadas

### Imediato (pode fazer agora)
- [ ] Mover `solar_hp90_from_fs.yaml_old` para `backups/`
- [ ] Adicionar cabeçalhos a todos os packages
- [ ] Adicionar `unique_id` aos sensores `statistics` em `piscina_ph.yaml`
- [ ] Verificar e eliminar duplicação de `dhw_volume_l`

### Curto Prazo (próxima semana)
- [ ] Criar `packages/README.md` documentando dependências
- [ ] Subdividir `climate_comfort.yaml` (51 KB → múltiplos ficheiros)
- [ ] Verificar se `thermal_comfort.yaml` pode substituir funcionalidades
- [ ] Adicionar fallbacks/timeouts às automações LLM Vision

### Médio Prazo (quando tiver tempo)
- [ ] Padronizar nomes de entidades
- [ ] Adicionar testes para automações críticas
- [ ] Considerar criar integration tests
- [ ] Documentar todos os sensores com `description:` nos atributos

---

## 🎯 Qualidade Geral

| Critério | Status | Nota |
|----------|--------|------|
| **Sintaxe YAML** | ✅ Válida | 10/10 |
| **Organização** | ⚠️ Boa mas melhorável | 7/10 |
| **Documentação** | ⚠️ Inconsistente | 5/10 |
| **Manutenibilidade** | ⚠️ Difícil (climate_comfort) | 6/10 |
| **Modularidade** | ✅ Boa (packages separados) | 8/10 |
| **IDs únicos** | ✅ Presentes | 9/10 |
| **Robustez** | ⚠️ Falta fallbacks | 6/10 |

**Média:** 7.3/10

---

## 🚀 Próximos Passos Sugeridos

**Escolha um dos planos:**

### Plano A: Mínimo (30 min)
1. Limpar ficheiro obsoleto
2. Adicionar cabeçalhos
3. Corrigir duplicação `dhw_volume_l`
4. Adicionar `unique_id` faltantes

### Plano B: Recomendado (2-3h)
1. Tudo do Plano A
2. Subdividir `climate_comfort.yaml`
3. Criar `README.md` com documentação
4. Adicionar fallbacks LLM Vision

### Plano C: Completo (1 dia)
1. Tudo do Plano B
2. Reorganizar com prefixos consistentes
3. Adicionar testes
4. Criar documentação completa

---

**Qual plano prefere implementar?** 🤔
