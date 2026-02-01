# 🔍 Investigação: Automação `bomba_piscina_dia`

## 📋 Resumo Executivo

✅ **ENCONTRADA!** A automação `bomba_piscina_dia` existia e foi recuperada com sucesso do histórico Git.

---

## 🕵️ O Que Foi Descoberto

### 📍 Localização Original
- **Commit:** `f0cd1c2` - "✨ Fase 2: Categorização automática e melhorias"
- **Data:** ~Janeiro 2026
- **Status Atual:** ❌ Removida do sistema

### 🎯 Função Original
Automação que controlava a **bomba da piscina durante o dia** baseando-se no **excedente de energia solar fotovoltaica** usando o blueprint **PVExcessControl**.

### ⚙️ Tecnologia
- **Blueprint:** `PVExcessControl/pv_excess_control.yaml`
- **Repositório:** [github.com/panhans/HomeAssistant](https://github.com/panhans/HomeAssistant)
- **Estado Blueprint:** ✅ Ainda instalado no sistema

---

## 📊 Configuração da Automação

```yaml
id: bomba_piscina_dia
alias: 🏊🏻Bomba Piscina Dia
use_blueprint:
  path: PVExcessControl/pv_excess_control.yaml
  input:
    automation_id: automation.bomba_piscina_dia
    grid_voltage: 230
    pv_power: sensor.emoncms_solar
    export_power: sensor.emoncms_export_power_positive
    load_power: sensor.emoncms_use
    actual_power: sensor.bomba_piscina_switch_0_power
    power_toggle_margin: 10
    appliance_switch: switch.bomba_piscina_switch_0
    inverter_limit: 0
```

### 🔌 Sensores Utilizados

| Sensor | Função |
|--------|--------|
| `sensor.emoncms_solar` | Produção solar total |
| `sensor.emoncms_export_power_positive` | Energia exportada para rede |
| `sensor.emoncms_use` | Consumo total da casa |
| `sensor.bomba_piscina_switch_0_power` | Potência da bomba |

### 🎛️ Switch Controlado
- `switch.bomba_piscina_switch_0` - Bomba principal da piscina

---

## ⚠️ Problema Atual

### 🔴 Automações que Referenciam `bomba_piscina_dia`

**1. `automation.ligardesligar_automacao_piscina` (Prioridade EV/Piscina)**
- Linhas: 583, 604, 616, 622
- Tenta ligar/desligar automação inexistente
- **Impacto:** Erros nos logs, coordenação EV/Piscina falha

**2. `automation.hidrojet`**
- Linhas: 1635, 1661, 1670
- Tenta desligar automação antes de ativar hidrojet
- **Impacto:** Conflito não gerido entre bomba e hidrojet

---

## 🔄 Substituições Atuais

Após remoção da `bomba_piscina_dia`, o sistema usa **3 automações alternativas**:

### 1️⃣ `automation.automacao_bomba_piscina`
**Tipo:** Manual com thresholds fixos  
**Triggers:**
- < -750W → Liga bomba
- > +750W → Desliga bomba

**Vantagens:**
- ✅ Simples e direto
- ✅ Sem dependências

**Desvantagens:**
- ❌ Menos inteligente
- ❌ Thresholds fixos

### 2️⃣ `automation.piscina_arranque_com_excedente_fv`
**Tipo:** Baseado em sensor binário  
**Trigger:**
- `binary_sensor.piscina_excedente_fv_bomba` ON por 2min

**Função:** Sistema principal de arranque FV

### 3️⃣ `automation.piscina_watchdog_arranque_fv_2min_v2`
**Tipo:** Watchdog/Backup  
**Trigger:**
- Time pattern a cada 2 minutos

**Função:** Failsafe que garante arranque se #2 falhar

---

## 💡 Soluções Possíveis

### 🟢 Opção A: Restaurar Blueprint (Recomendado)

**Vantagens:**
- ✅ Controlo mais sofisticado
- ✅ Funcionalidades avançadas (estatísticas, fine-tuning)
- ✅ Consolida 3 automações numa só
- ✅ Blueprint já instalado

**Passos:**
1. Verificar sensores `emoncms_*` ativos
2. Adicionar automação do backup ao `automations.yaml`
3. Desativar `automation.automacao_bomba_piscina`
4. Manter watchdog como backup
5. Atualizar referências em `ligardesligar_automacao_piscina` e `hidrojet`

**Ficheiro de Backup:**
- 📄 `/data/homeassistant/docs/BACKUP_AUTOMACAO_BOMBA_PISCINA_DIA.yaml`

---

### 🟡 Opção B: Remover Referências

**Vantagens:**
- ✅ Rápido e simples
- ✅ Sistema atual funciona

**Desvantagens:**
- ❌ Perde coordenação EV/Piscina
- ❌ Hidrojet sem proteção

**Passos:**
1. Remover linhas que referenciam `automation.bomba_piscina_dia`
2. Substituir por lógica alternativa ou remover funcionalidade

---

### 🔵 Opção C: Criar Nova Automação Simples

**Criar `bomba_piscina_dia` manualmente:**

```yaml
- id: bomba_piscina_dia
  alias: 🏊🏻 Piscina - Bomba Dia (Manual)
  description: Controlo manual da bomba durante o dia
  triggers:
    - minutes: /5
      trigger: time_pattern
  conditions:
    - condition: sun
      after: sunrise
      after_offset: '00:15:00'
      before: sunset
      before_offset: '-00:15:00'
    - condition: numeric_state
      entity_id: input_number.piscina_filtracao_min_restantes
      above: 0
    - condition: state
      entity_id: input_boolean.piscina_override_manual
      state: 'off'
  actions:
    - if:
      - condition: numeric_state
        entity_id: sensor.potencia_emonpi_import_export_media_5_minutos
        below: -750
      then:
        - service: switch.turn_on
          target:
            entity_id: switch.bomba_piscina_switch_0
      else:
        - if:
          - condition: numeric_state
            entity_id: sensor.potencia_emonpi_import_export_media_5_minutos
            above: 750
          then:
            - service: switch.turn_off
              target:
                entity_id: switch.bomba_piscina_switch_0
  mode: single
```

**Vantagens:**
- ✅ Resolve referências
- ✅ Código simples e claro
- ✅ Sem dependências externas

**Desvantagens:**
- ❌ Menos funcionalidades que blueprint
- ❌ Redundante com automações existentes

---

## 📊 Comparação das Soluções

| Critério | Opção A<br/>(Blueprint) | Opção B<br/>(Remover) | Opção C<br/>(Manual) |
|----------|------------------------|-----------------------|---------------------|
| **Complexidade** | 🟡 Média | 🟢 Baixa | 🟡 Média |
| **Funcionalidades** | ⭐⭐⭐⭐⭐ | ⭐☆☆☆☆ | ⭐⭐⭐☆☆ |
| **Manutenibilidade** | 🟢 Alta | 🔴 Baixa | 🟢 Alta |
| **Risco** | 🟡 Médio | 🟢 Baixo | 🟢 Baixo |
| **Tempo Impl.** | 30-60 min | 10 min | 20-30 min |
| **Recomendado?** | ✅ **SIM** | ❌ Não | 🤔 Se necessário |

---

## 🎯 Recomendação Final

### ✅ OPÇÃO A - Restaurar Blueprint

**Razões:**
1. 🤖 Blueprint já instalado e testado
2. 📊 Funcionalidades avançadas úteis
3. 🔧 Consolida lógica duplicada
4. 🛡️ Resolve problemas de coordenação
5. 📈 Melhor controlo energético

**Próximos Passos:**
1. ✅ Verificar sensores emoncms (seguinte)
2. ✅ Restaurar automação
3. ✅ Testar funcionamento
4. ✅ Desativar redundâncias
5. ✅ Atualizar documentação

---

## 📁 Ficheiros Criados

1. **📄 BACKUP_AUTOMACAO_BOMBA_PISCINA_DIA.yaml**
   - Automação completa recuperada
   - Documentação detalhada
   - Instruções de restauração

2. **📄 INVESTIGACAO_BOMBA_PISCINA_DIA.md** (este ficheiro)
   - Análise completa
   - Comparação de soluções
   - Recomendações

---

## 🔗 Links Úteis

- 📦 [PVExcessControl Blueprint](https://github.com/panhans/HomeAssistant)
- 📚 [Documentação Piscina](AUTOMACOES_PISCINA.md)
- 🔧 [Histórico Git](commit:f0cd1c2)

---

## ✅ Checklist de Verificação

Antes de restaurar, verificar:

- [ ] Blueprint `PVExcessControl` instalado
- [ ] Sensor `sensor.emoncms_solar` ativo
- [ ] Sensor `sensor.emoncms_export_power_positive` ativo
- [ ] Sensor `sensor.emoncms_use` ativo
- [ ] Sensor `sensor.bomba_piscina_switch_0_power` ativo
- [ ] Switch `switch.bomba_piscina_switch_0` funcional
- [ ] Fazer backup de `automations.yaml`
- [ ] Testar em horário não crítico

---

**📅 Criado:** 31 Janeiro 2026  
**✍️ Autor:** Análise Git + Recovery Assistant  
**🏷️ Tags:** `recovery` `piscina` `blueprint` `solar` `automation`
