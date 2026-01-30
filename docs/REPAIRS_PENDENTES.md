# 🔧 Repairs Pendentes - Home Assistant

**Data da análise**: 30 de Janeiro de 2026  
**Branch**: `consolidacao-automations-gui`  
**Commit atual**: `7847063`

---

## 📊 Resumo Executivo

| Categoria | Quantidade | Prioridade | Estado |
|-----------|-----------|------------|--------|
| **Automações quebradas** | 2 | 🔴 **CRÍTICA** | Requer ação |
| **Templates com erros** | 3-4 | 🟠 **ALTA** | Requer correção |
| **Switch template deprecated** | 1 | ✅ **RESOLVIDO** | Migrado |
| **HACS deprecated** | 2 | 🟡 **MÉDIA** | Informativo |
| **Dispositivos offline** | 8+ | 🟢 **BAIXA** | Normal |
| **Custom integrations warnings** | 25 | 🟢 **BAIXA** | Informativo |
| **MQTT object_id deprecated** | 40 | 🟡 **MÉDIA** | Deadline: Abril 2026 |

---

## 🔴 PRIORIDADE CRÍTICA

### 1. Pyscript Desativado (2 automações quebradas)

**Status**: ❌ **BLOQUEADOR**  
**Impacto**: 2 automações falhando constantemente  
**Erro**:
```
Action pyscript.pv_excess_control not found
```

**Automações afetadas**:
1. ✅ `ventilador_cave_solar` - "Ventilador Cave Solar" (em `automations.yaml`)
2. ❌ `bomba_piscina_dia` - "🏊🏻Bomba Piscina Dia" (em `_archive/automations_piscina/piscina_geral.yaml`)

**Causa raiz**:
- Pyscript está **instalado** (`custom_components/pyscript/`)
- Pyscript está **configurado** (entry_id: `138a18459753faf674f9ce919c100f9b`)
- Pyscript está **DESATIVADO pelo utilizador** (`"disabled_by": "user"`)
- Script existe: `/config/pyscript/pv_excess_control.py`

**Solução**:
```
1. GUI → Settings → Devices & Services
2. Procurar "Pyscript"
3. Clicar em "ENABLE" / "ATIVAR"
4. Reiniciar Home Assistant
5. Verificar logs: docker logs homeassistant | grep pyscript
```

**Ou via CLI**:
```bash
# Editar manualmente o config_entries
docker exec homeassistant python3 << 'EOF'
import json
with open('/config/.storage/core.config_entries', 'r') as f:
    data = json.load(f)
for entry in data['data']['entries']:
    if entry['domain'] == 'pyscript':
        entry['disabled_by'] = None
        print(f"✅ Pyscript habilitado: {entry['entry_id']}")
with open('/config/.storage/core.config_entries', 'w') as f:
    json.dump(data, f, indent=2)
EOF

# Reiniciar HA
docker restart homeassistant
```

**Atenção**:
- A automação `bomba_piscina_dia` está em `_archive/` mas ainda **ativa no sistema**
- Considerar:
  - ✅ Consolidar para `automations.yaml` (se ainda necessária)
  - ⚠️ Desativar/remover (se obsoleta)

---

## 🟠 PRIORIDADE ALTA

### 2. ✅ Switch Template Deprecated - RESOLVIDO

**Status**: ✅ **MIGRADO**  
**Deadline evitado**: HA Core 2026.6 (Junho 2026)  
**Commit**: `7847063`

**Problema original**:
```
Legacy switch template deprecation
Switch: evse_admin_rules_inverted
Location: switches.yaml
```

**Solução implementada**:
```yaml
# ANTES (switches.yaml - DEPRECATED):
- platform: template
  switches:
    evse_admin_rules_inverted:
      unique_id: evse_admin_rules
      value_template: "{{ is_state('switch.wallbox_charging_rules_enabled', 'off') }}"
      turn_on:
        service: switch.turn_off
        ...

# DEPOIS (templates/evse_switch.yaml - MODERN):
- switch:
  - unique_id: evse_admin_rules
    name: evse_admin_rules
    state: "{{ is_state('switch.wallbox_charging_rules_enabled', 'off') }}"
    turn_on:
      - action: switch.turn_off
        ...
```

**Alterações**:
- ✅ Criado `templates/evse_switch.yaml` (sintaxe moderna)
- ✅ Removido legacy config de `switches.yaml`
- ✅ Mantida funcionalidade (lógica invertida preservada)
- ✅ Documentação adicionada em ambos os ficheiros

**Próximo passo**: Reiniciar HA ou recarregar template entities via GUI

---

### 3. Template Errors - Sensor OMIE

**Status**: ⚠️ **Erro recorrente**  
**Impacto**: Sensores de energia com valores incorretos  
**Erro**:
```
Template variable error: 'None' has no attribute 'items'
when rendering state_attr('sensor.omie_spot_price_pt', 'today_hours').items()
```

**Sensores afetados**:
1. `sensor.template_coopernico_excedente_indexado`
2. Outros sensores relacionados com `sensor.omie_spot_price_pt`

**Causa**:
- `sensor.omie_spot_price_pt` retorna `None` ou não tem o atributo `today_hours`/`tomorrow_hours`
- Templates não têm validação/default para quando o atributo não existe

**Solução**:
```yaml
# ANTES (erro):
{% for h, PM in state_attr('sensor.omie_spot_price_pt', 'today_hours').items() -%}

# DEPOIS (corrigido):
{% set today_hours = state_attr('sensor.omie_spot_price_pt', 'today_hours') %}
{% if today_hours is not none %}
  {% for h, PM in today_hours.items() -%}
  {# ... código ... #}
  {% endfor %}
{% endif %}
```

**Ficheiros a verificar**:
- `sensors/` ou `templates/` com referência a `omie_spot_price_pt`
- Procurar por: `state_attr.*today_hours.*items()`

### 3. Template Error - Float Conversion

**Status**: ⚠️ **Erro recorrente**  
**Erro**:
```
ValueError: could not convert string to float: 'unavailable'
Template: {{ states('sensor.template_coopernico_spot_price_bihorario') | float / 1000 }}
```

**Sensor afetado**:
- `sensor.coopernico_spot_price_bihorario_kwh`

**Solução**:
```yaml
# ANTES (erro):
{{ states('sensor.template_coopernico_spot_price_bihorario') | float / 1000 }}

# DEPOIS (corrigido):
{{ states('sensor.template_coopernico_spot_price_bihorario') | float(default=0) / 1000 }}
```

---

## 🟡 PRIORIDADE MÉDIA

### 4. HACS - Repositórios Deprecated

**Status**: ℹ️ **Informativo**  
**Impacto**: Cartões podem parar de funcionar no futuro  

**Repositórios removidos**:
1. **`custom-cards/bar-card`**
   - Razão: "Repository is no longer maintained"
   - Ação: Procurar alternativa ou fazer fork
   
2. **`custom-cards/dual-gauge-card`**
   - Razão: "Repository has been abandoned"
   - Ação: Procurar alternativa ou fazer fork

**Alternativas sugeridas**:
- Para `bar-card`: Usar `apexcharts-card` ou `mini-graph-card`
- Para `dual-gauge-card`: Usar `gauge-card` nativo ou criar custom card

---

### 5. MQTT - Object ID Deprecated (40 sensores)

**Status**: ⏰ **Deadline: Abril 2026 (HA Core 2026.4)**  
**Detalhes completos**: Ver `docs/REPAIRS_CORRIGIDOS.md` (secção MQTT)

**Sensores afetados**: 40 sensores Borgmatic (mclima, emonpi, openwrt, firegui)

---

## 🟢 PRIORIDADE BAIXA

### 6. Dispositivos Offline (Normal)

**Dispositivos com erro de conexão** (temporário/esperado):
- Câmaras Tapo: `192.168.1.146`, `192.168.1.106` (offline)
- Shelly Plug S: `shellyplug-s-51D430` (offline)
- Botões BTHome/Shelly (vários)
- Xiaomi Wireless Mini Switch (bateria null)

**Ação**: ✅ Nenhuma (comportamento normal para dispositivos offline)

---

### 7. Custom Integrations Warnings

**Status**: ℹ️ **Informativo** (25 warnings)  
**Mensagem**: "This component might cause stability problems"

**Integrações instaladas**:
- ✅ Todas funcionais (ver lista em `REPAIRS_CORRIGIDOS.md`)

**Ação**: ✅ Nenhuma (avisos padrão para custom components)

---

## 📋 Checklist de Ações

### ✅ Concluído
- [x] **Corrigir timeout errors** (2 automações) - Commit `b545d56`
- [x] **Corrigir Automatic Backups** (auto_backup → backup.create) - Commit `e68a3bb`
- [x] **Migrar switch template** (evse_admin_rules) - Commit `7847063`

### Imediato (Esta Sessão)
- [ ] **Ativar Pyscript** via GUI ou CLI
- [ ] **Desativar ou consolidar** `bomba_piscina_dia` do `_archive/`
- [ ] **Reiniciar HA** e verificar se automações carregam
- [ ] **Validar** logs após reinício

### Curto Prazo (Esta Semana)
- [ ] **Corrigir templates** OMIE (adicionar validação `is not none`)
- [ ] **Corrigir template** float conversion (adicionar `default=0`)
- [ ] **Localizar ficheiros** dos sensores template afetados
- [ ] **Testar** sensores após correção

### Médio Prazo (Este Mês)
- [ ] **Avaliar** uso de `bar-card` e `dual-gauge-card`
- [ ] **Procurar alternativas** ou fazer fork
- [ ] **Migrar** para novas cards se necessário

### Longo Prazo (Antes Abril 2026)
- [ ] **Migrar** 40 sensores MQTT object_id
- [ ] Ver plano detalhado em `REPAIRS_CORRIGIDOS.md`

---

## 🔍 Comandos de Diagnóstico

### Verificar Pyscript
```bash
# Status da integração
docker exec homeassistant cat /config/.storage/core.config_entries | grep -A10 pyscript

# Logs do pyscript
docker logs homeassistant 2>&1 | grep -i pyscript | tail -20

# Verificar scripts instalados
ls -la /data/homeassistant/pyscript/
```

### Verificar Automações Quebradas
```bash
# Erros recentes de automações
docker logs homeassistant 2>&1 | grep "Service not found\|Action.*not found" | tail -20

# Automações em _archive ainda ativas
docker logs homeassistant 2>&1 | grep "bomba_piscina_dia" | head -5
```

### Verificar Template Errors
```bash
# Erros de template
docker logs homeassistant 2>&1 | grep "Template.*error\|TemplateError" | tail -30

# Sensor OMIE específico
docker logs homeassistant 2>&1 | grep "omie_spot_price" | tail -20
```

---

## 📊 Progresso Total

**Repairs corrigidos** (todas as sessões): 4
- ✅ Telegram Bot YAML deprecated
- ✅ Automation timeout errors (2 automações) - `b545d56`
- ✅ Automatic Backups unknown action - `e68a3bb`
- ✅ Switch template deprecated (evse_admin_rules) - `7847063`

**Repairs pendentes** (esta análise): 6
- 🔴 Pyscript desativado (CRÍTICO)
- 🟠 Template OMIE errors (3-4 sensores)
- 🟡 HACS deprecated (2 cards)
- 🟡 MQTT object_id (40 sensores, deadline Abril 2026)
- 🟢 Dispositivos offline (normal)
- 🟢 Custom integration warnings (informativo)

---

## 📝 Notas Finais

1. **Pyscript é a prioridade #1** - Está a causar erros constantes (cada 5 minutos)
2. **Templates OMIE** devem ser corrigidos logo após Pyscript
3. **MQTT migration** pode aguardar (ainda faltam 2 meses até deadline)
4. **HACS cards** são informativas - podem continuar a funcionar por enquanto

---

**Última atualização**: 30 Janeiro 2026, 17:35 UTC  
**Analisado por**: GitHub Copilot Agent  
**Comandos executados**: 15+ (grep, docker logs, config_entries analysis)
