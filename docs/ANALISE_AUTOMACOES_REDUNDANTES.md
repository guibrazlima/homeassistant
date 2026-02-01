# 🔍 ANÁLISE: Automações Redundantes da Piscina

## 🎯 Objetivo
Identificar automações que fazem a mesma coisa e podem entrar em conflito após restauração da `bomba_piscina_dia`.

---

## 📊 Automações Encontradas que Controlam a Bomba Baseado em Energia Solar

### 1️⃣ **`bomba_piscina_dia`** ✅ (RESTAURADA)
**ID:** `bomba_piscina_dia`  
**Alias:** 🏊🏻 Piscina - Bomba Piscina Dia  
**Tipo:** Blueprint (PVExcessControl)  
**Linhas:** 670-687

#### Funcionamento:
- ✅ **Controlo inteligente** via blueprint PVExcessControl
- ✅ **Sensores:**
  - `sensor.emoncms_solar` (produção solar)
  - `sensor.emoncms_export_power_positive` (exportação)
  - `sensor.emoncms_use` (consumo casa)
  - `sensor.bomba_piscina_switch_0_power` (consumo bomba)
- ✅ **Lógica:** Liga/desliga baseado em excedente disponível
- ✅ **Margem:** 10W (power_toggle_margin)
- ✅ **Switch:** `switch.bomba_piscina_switch_0`

#### Vantagens:
- ✅ Algoritmo adaptativo do blueprint
- ✅ Estatísticas e histórico integrados
- ✅ Fine-tuning de parâmetros
- ✅ Previsão de comportamento
- ✅ Evita oscilações com margem configurável

---

### 2️⃣ **`automacao_bomba_piscina`** ⚠️ (REDUNDANTE)
**ID:** `automacao_bomba_piscina`  
**Alias:** 🏊🏻 Piscina - Automação Bomba Piscina  
**Tipo:** Manual (triggers simples)  
**Linhas:** 689-750

#### Funcionamento:
- ⚠️ **Controlo básico** com thresholds fixos
- ⚠️ **Sensor:**
  - `sensor.potencia_emonpi_import_export_media_5_minutos` (importação/exportação média 5min)
- ⚠️ **Lógica:**
  - Liga se < -750W (exportação > 750W)
  - Desliga se > 750W (importação > 750W)
- ⚠️ **Switches:** Liga/desliga 2 dispositivos (device IDs)
- ⚠️ **Condição:** Apenas entre sunrise/sunset

#### Problemas:
- ❌ Thresholds fixos (não adaptativos)
- ❌ Pode oscilar muito (margem muito grande: 1500W total)
- ❌ Usa device IDs em vez de entity IDs (menos legível)
- ❌ Não considera consumo da bomba
- ❌ Sensor de média 5min (resposta mais lenta)

#### Conflito com `bomba_piscina_dia`:
- ⚠️ **AMBAS ligam/desligam o mesmo switch**
- ⚠️ **Critérios diferentes** → podem competir
- ⚠️ **Oscilações possíveis** se ambas ativas

---

### 3️⃣ **`piscina_-_arranque_com_excedente_fv`** ⚠️ (PARCIALMENTE REDUNDANTE)
**ID:** `piscina_-_arranque_com_excedente_fv`  
**Alias:** 🏊🏻 Piscina - Arranque com excedente FV  
**Tipo:** Manual (trigger por binary_sensor)  
**Linhas:** 789-813

#### Funcionamento:
- ⚠️ **Trigger:** `binary_sensor.piscina_excedente_fv_bomba` = ON por 2min
- ⚠️ **Condições:**
  - Tempo de filtragem restante > 0
  - Entre sunrise e sunset (±15min)
- ⚠️ **Ação:** Liga `switch.bomba_piscina` E `switch.bomba_piscina_switch_0`
- ⚠️ **Mode:** single

#### Problemas:
- ❌ **Apenas LIGA**, não desliga automaticamente
- ❌ Depende de binary_sensor externo (`piscina_excedente_fv_bomba`)
- ❌ Delay de 2min (menos responsivo)
- ❌ Liga 2 switches (duplicação?)

#### Conflito com `bomba_piscina_dia`:
- ⚠️ **Função complementar** (só liga, não desliga)
- ⚠️ **Pode funcionar em conjunto** SE o binary_sensor for bem configurado
- ⚠️ **Risco baixo** de conflito direto

---

### 4️⃣ **`piscina_-_watchdog_arranque_fv_2min_v2`** ⚠️ (WATCHDOG - PODE SER ÚTIL)
**ID:** `piscina_-_watchdog_arranque_fv_2min_v2`  
**Alias:** 🏊🏻 Piscina - Watchdog arranque FV (*/2min) v2  
**Tipo:** Watchdog (time_pattern)  
**Linhas:** 841-869

#### Funcionamento:
- 🔄 **Trigger:** A cada 2 minutos (time_pattern)
- 🔄 **Condições:**
  - Override manual = OFF
  - Bomba = OFF
  - Tempo de filtragem restante > 0
  - `binary_sensor.piscina_excedente_fv_bomba` = ON
  - Entre sunrise e sunset (±15min)
- 🔄 **Ação:** Liga `switch.bomba_piscina_switch_0`

#### Função:
- ✅ **Backup/recovery** se bomba não arrancar por falha
- ✅ **Não desliga** → complementar
- ✅ **Verifica estado** a cada 2min

#### Conflito com `bomba_piscina_dia`:
- ✅ **Pode ser complementar** (safety net)
- ⚠️ **Pode forçar ligação** quando blueprint decidiu desligar
- ⚠️ **Depende do mesmo binary_sensor** que automação #3

---

## 🚨 Resumo de Conflitos

### ❌ CONFLITO DIRETO (Alta Prioridade)
**`automacao_bomba_piscina` vs `bomba_piscina_dia`**

| Aspecto | automacao_bomba_piscina | bomba_piscina_dia |
|---------|-------------------------|-------------------|
| Controlo | Liga/Desliga | Liga/Desliga |
| Switch | Mesmo (`bomba_piscina_switch_0`) | Mesmo |
| Lógica | Threshold fixo ±750W | Algoritmo adaptativo |
| Sensor | Média 5min | Real-time múltiplos |
| Intervalo | Sunrise-Sunset | Configurável |
| Qualidade | ⚠️ Básica | ✅ Avançada |

**Resultado:** PODEM COMPETIR - Um desliga, outro liga → oscilações

---

### ⚠️ CONFLITO INDIRETO (Média Prioridade)
**`piscina_-_arranque_com_excedente_fv` + `piscina_-_watchdog_arranque_fv_2min_v2`**

Estas 2 automações trabalham juntas baseadas no mesmo sensor:
- `binary_sensor.piscina_excedente_fv_bomba`

**Problemas:**
1. ❓ Não sabemos como este binary_sensor é calculado
2. ⚠️ Se basear-se nos mesmos dados → redundância total
3. ⚠️ Se basear-se em dados diferentes → conflito de critérios
4. ⚠️ Watchdog pode **forçar ligação** contra decisão do blueprint

---

## 🎯 Recomendações

### 🔴 Ação Imediata: Desativar `automacao_bomba_piscina`

**Razão:** Conflito direto com `bomba_piscina_dia`

**Como fazer:**
1. UI: Settings → Automations → "Automação Bomba Piscina" → Toggle OFF
2. OU editar `automations.yaml` e adicionar `initial_state: false`

**Código para desativar:**
```yaml
- id: automacao_bomba_piscina
  alias: "🏊🏻 Piscina - Automação Bomba Piscina"
  initial_state: false  # ← ADICIONAR ESTA LINHA
  description: ...
```

---

### 🟡 Ação Recomendada: Investigar Binary Sensor

**Verificar:** Como é calculado `binary_sensor.piscina_excedente_fv_bomba`

**Ficheiros onde procurar:**
- `binary_sensor.yaml`
- `sensors/` (qualquer ficheiro)
- `templates/` (templates)
- `configuration.yaml` (secção template)

**Se for baseado nos mesmos dados:**
- ⚠️ Considerar desativar automações #3 e #4
- ✅ Blueprint já faz esse trabalho melhor

**Se for baseado em dados diferentes (ex: previsão meteorológica):**
- ✅ Manter como complemento
- ⚠️ Mas ajustar para não conflitar

---

### 🟢 Ação Opcional: Criar Grupo de Controlo

**Objetivo:** Garantir que apenas 1 sistema controla a bomba de cada vez

**Solução A - Input Select:**
```yaml
input_select:
  piscina_controlo_modo:
    name: Modo de Controlo da Bomba
    options:
      - "Blueprint (Automático)"
      - "Manual (Básico)"
      - "Excedente FV (Sensor)"
      - "Desativado"
    initial: "Blueprint (Automático)"
```

Depois adicionar condição em cada automação:
```yaml
conditions:
  - condition: state
    entity_id: input_select.piscina_controlo_modo
    state: "Blueprint (Automático)"  # ou o nome apropriado
```

---

## 📋 Checklist de Ações

### Imediato (Antes de Reload)
- [ ] **Verificar** binary_sensor.piscina_excedente_fv_bomba (onde é definido?)
- [ ] **Decidir** se desativa `automacao_bomba_piscina` ANTES do reload
- [ ] **Backup** do estado atual (já feito automaticamente pelo Git)

### Após Reload
- [ ] **Desativar** `automacao_bomba_piscina` via UI ou YAML
- [ ] **Observar** comportamento durante 2-3 dias solares
- [ ] **Monitorizar** logs para conflitos

### Esta Semana
- [ ] **Analisar** necessidade das automações #3 e #4
- [ ] **Decidir** se mantém watchdog como safety net
- [ ] **Documentar** decisão final

### Próximo Mês
- [ ] **Avaliar** se blueprint suficiente sozinho
- [ ] **Considerar** remover automações redundantes permanentemente
- [ ] **Atualizar** documentação AUTOMACOES_PISCINA.md

---

## 🔍 Investigação Necessária: Binary Sensor

### Procurar Definição:
```bash
# No terminal
cd /data/homeassistant
grep -r "piscina_excedente_fv_bomba" --include="*.yaml" .
```

### Analisar:
1. **Se for template simples** com threshold → redundante
2. **Se incluir lógica avançada** (previsão, ML) → pode ser útil
3. **Se for external sensor** (integração) → investigar fonte

---

## 📊 Comparação de Performance (estimada)

| Característica | Blueprint | automacao_bomba | arranque_fv + watchdog |
|----------------|-----------|-----------------|------------------------|
| **Responsividade** | ⚡ Alta | 🐌 Baixa (5min) | 🐌 Média (2min) |
| **Estabilidade** | ✅ Excelente | ⚠️ Pode oscilar | ⚠️ Média |
| **Inteligência** | 🧠 Adaptativa | 🤖 Fixa | 🤖 Fixa/Sensor |
| **Manutenção** | ✅ Fácil | ⚠️ Manual | ⚠️ Múltiplos ficheiros |
| **Estatísticas** | ✅ Integradas | ❌ Nenhuma | ❌ Nenhuma |
| **Configuração** | ✅ UI inputs | ⚠️ Hardcoded | ⚠️ Sensor externo |

---

## 🎯 Decisão Sugerida

### Cenário A: Blueprint Sozinho (Recomendado) ⭐
**Desativar:**
- ❌ `automacao_bomba_piscina`
- ❌ `piscina_-_arranque_com_excedente_fv` (se sensor redundante)
- ❌ `piscina_-_watchdog_arranque_fv_2min_v2` (se sensor redundante)

**Vantagens:**
- ✅ Sistema limpo e simples
- ✅ Sem conflitos
- ✅ Controlo profissional
- ✅ Fácil de diagnosticar

**Desvantagens:**
- ⚠️ Depende só do blueprint (single point of failure)

---

### Cenário B: Blueprint + Watchdog (Conservador)
**Desativar:**
- ❌ `automacao_bomba_piscina`
- ❌ `piscina_-_arranque_com_excedente_fv`

**Manter:**
- ✅ `bomba_piscina_dia` (blueprint)
- ✅ `piscina_-_watchdog_arranque_fv_2min_v2` (safety net)

**Vantagens:**
- ✅ Blueprint como principal
- ✅ Watchdog como backup
- ✅ Redundância de segurança

**Desvantagens:**
- ⚠️ Watchdog pode interferir
- ⚠️ Mais complexo de diagnosticar

---

### Cenário C: Manter Tudo (Não Recomendado) ❌
**Problemas:**
- ❌ Conflitos inevitáveis
- ❌ Oscilações da bomba
- ❌ Difícil de diagnosticar
- ❌ Logs confusos
- ❌ Desgaste do equipamento

---

## 🔧 Código para Desativar Automações

Se decidir desativar `automacao_bomba_piscina`:

### Opção A - Via UI (Mais Simples):
1. Settings → Automations & Scenes
2. Procurar "Automação Bomba Piscina"
3. Clicar no toggle para **OFF**
4. Observar por 1 semana
5. Se tudo OK → eliminar definitivamente

### Opção B - Via YAML (Permanente):
Adicionar `initial_state: false` na linha 690:

```yaml
- id: automacao_bomba_piscina
  alias: "🏊🏻 Piscina - Automação Bomba Piscina"
  initial_state: false  # DESATIVADA - redundante com bomba_piscina_dia
  description: Automação ativada por valor numérico...
```

---

## 📄 Ficheiros de Referência

1. **ANALISE_AUTOMACOES_REDUNDANTES.md** (este ficheiro)
2. **RESTAURACAO_CONCLUIDA.md** - Status da restauração
3. **BACKUP_AUTOMACAO_BOMBA_PISCINA_DIA.yaml** - Código restaurado
4. **AUTOMACOES_PISCINA.md** - Documentação geral

---

## 📅 Timeline Sugerida

### Hoje (1 Fev 2026)
- ⏰ **Agora:** Investigar binary_sensor.piscina_excedente_fv_bomba
- ⏰ **Após investigação:** Decidir estratégia (A, B ou C)
- ⏰ **Antes de reload:** Desativar automação redundante

### Esta Semana
- 📅 **Dias 2-4:** Observar comportamento durante dias solares
- 📅 **Dia 5:** Avaliar resultados, ajustar se necessário
- 📅 **Dia 7:** Decisão final sobre outras automações

### Próximo Mês
- 📅 **Semana 2:** Análise de estatísticas do blueprint
- 📅 **Semana 4:** Limpeza definitiva (remover código morto)
- 📅 **Fim do mês:** Atualizar documentação final

---

## 🆘 Em Caso de Problemas

### Se bomba oscilar muito (liga/desliga rápido):
1. **Verificar** se ambas automações estão ativas
2. **Desativar** uma temporariamente
3. **Observar** comportamento
4. **Ajustar** power_toggle_margin do blueprint (aumentar para 20W ou 50W)

### Se bomba não ligar com sol:
1. **Verificar** sensores têm valores
2. **Verificar** thresholds do blueprint
3. **Verificar** condições adicionais (tempo restante, etc)
4. **Ativar** watchdog temporariamente como backup

### Se bomba não desligar ao importar:
1. **Verificar** sensor export_power funciona
2. **Verificar** lógica do blueprint
3. **Temporariamente** reativar `automacao_bomba_piscina` para forçar desligar

---

**Próxima ação:** Investigar `binary_sensor.piscina_excedente_fv_bomba` 🔍

---

*Análise gerada automaticamente*  
*Data: 1 Fevereiro 2026*  
*Versão: 1.0*
