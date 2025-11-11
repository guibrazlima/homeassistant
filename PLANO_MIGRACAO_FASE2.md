# 📋 Plano de Migração - Fase 2

## 🎯 Objetivo
Dividir os ficheiros migrados por categoria e adicionar melhorias

## 📊 Inventário Atual

### Ficheiros Migrados (a dividir)
1. **sistema/todas_automacoes_migradas.yaml** (53 automações)
2. **sistema/automacoes_root_migradas.yaml** (10 automações)

### Ficheiros Já Organizados
1. **piscina/piscina_filtragem.yaml** (11 automações) ✅
2. **veiculo_eletrico/ev_depois_piscina.yaml** (3 automações) ✅
3. **portoes_portarias/portao_botoes.yaml** (2 automações exemplo) ✅

**Total:** 79 automações

---

## 🔍 Categorização Necessária

### Das 63 automações a categorizar:

#### 🚪 Portões e Portarias (~15 automações)
- Callback to open gate from action
- Garage light on when gate opens/closes
- Botões diversos (Shelly, Sala, etc.)
→ **Destino:** `portoes_portarias/portao_principal.yaml`

#### 🚗 Veículo Elétrico (~7 automações)
- Notificação para ligar carro ao carregador
- Controlo wallbox cFos
- Excesso solar
→ **Destino:** `veiculo_eletrico/ev_carregamento.yaml`

#### 💡 Iluminação (~12 automações)
- Luzes sala, quarto, garagem
- Luzes exteriores
- Automações por movimento
→ **Destino:** `iluminacao/luzes_interior.yaml` e `luzes_exterior.yaml`

#### 🏊 Piscina (~8 automações adicionais)
- Watchdogs
- Temperatura
- Cobertura
→ **Destino:** `piscina/piscina_geral.yaml`

#### 🌡️ Clima (~6 automações)
- AC sala, quarto
- Aquecimento
→ **Destino:** `clima/aquecimento_arrefecimento.yaml`

#### ☀️ Energia Solar (~4 automações)
- Watchdog FV
- Produção solar
→ **Destino:** `energia_solar/paineis_solares.yaml`

#### ⚙️ Sistema (~8 automações)
- SpeedTests
- Watchdogs gerais
- Monitorização
→ **Destino:** `sistema/watchdogs.yaml` e `sistema/monitorizacao.yaml`

#### 🔐 Segurança (~3 automações)
- Alarmes
- Notificações
→ **Destino:** `seguranca/alarmes.yaml`

---

## 📝 Metodologia de Migração

### Para cada automação:

1. **Identificar categoria** (ver alias/descrição)
2. **Criar/atualizar ficheiro destino**
3. **Adicionar/melhorar:**
   ```yaml
   - id: categoria_componente_acao  # ID descritivo
     alias: emoji Categoria - Descrição
     description: |
       Descrição completa...
     mode: single
     max_exceeded: warning
     trigger: [...]
     condition: [...]
     action: [...]
   ```

### Ordem de Prioridade:

1. ✅ **CRÍTICAS** (já organizadas)
   - Piscina filtragem
   - EV depois piscina

2. 🔄 **IMPORTANTES** (fazer a seguir)
   - Portões (segurança)
   - Iluminação (uso diário)
   - Veículo Elétrico (energia)

3. ⏳ **NORMAIS**
   - Clima
   - Sistema
   - Solar

4. ⭕ **SECUNDÁRIAS**
   - Segurança
   - Outras

---

## 🛠️ Ferramentas

### Opção 1: Manual (preciso)
- Abrir ficheiros migrados
- Copiar automação por automação
- Colar em ficheiro correto
- Adicionar melhorias

### Opção 2: Script Python (rápido)
```python
# Ler YAML
# Categorizar por alias/descrição
# Gerar IDs descritivos
# Escrever em ficheiros por categoria
```

### Opção 3: Híbrido (recomendado)
- Script para categorização automática
- Revisão manual para melhorias
- Commit incremental por categoria

---

## ✅ Checklist por Categoria

### 🚪 Portões
- [ ] Criar portao_principal.yaml
- [ ] Migrar automações de portão
- [ ] Adicionar IDs descritivos
- [ ] Adicionar descrições
- [ ] Testar sintaxe
- [ ] Commit

### 💡 Iluminação
- [ ] Criar luzes_interior.yaml
- [ ] Criar luzes_exterior.yaml
- [ ] Migrar automações
- [ ] Melhorias
- [ ] Testar
- [ ] Commit

### 🚗 EV
- [ ] Criar ev_carregamento.yaml
- [ ] Migrar automações
- [ ] Melhorias
- [ ] Testar
- [ ] Commit

### 🏊 Piscina
- [ ] Criar piscina_geral.yaml
- [ ] Migrar automações restantes
- [ ] Melhorias
- [ ] Testar
- [ ] Commit

### 🌡️ Clima, ☀️ Solar, 🔐 Segurança, ⚙️ Sistema
- [ ] Criar ficheiros
- [ ] Migrar
- [ ] Melhorias
- [ ] Testar
- [ ] Commit

---

## 🎯 Meta

**Objetivo:** Ter todas as 79 automações organizadas, documentadas e testadas

**Timeline Estimado:**
- Fase 2A (categorização): 30 min
- Fase 2B (IDs e descrições): 45 min  
- Fase 2C (melhorias): 30 min
- Fase 2D (testes): 15 min

**Total:** ~2 horas de trabalho focado

---

## 🚀 Próximo Passo

**Aguardando decisão:**
- 🤖 Automatizar tudo com script?
- ✋ Fazer manualmente categoria por categoria?
- 🔀 Híbrido (script + revisão manual)?

**Recomendação:** Híbrido - script para velocidade, revisão para qualidade
