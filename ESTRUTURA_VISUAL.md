# 📐 Estrutura Visual da Reorganização

```
📁 /data/homeassistant/
│
├── 📄 configuration.yaml
│   └── automation: !include_dir_merge_list automations/
│
└── 📁 automations/
    │
    ├── 📄 README.md ................................. Índice completo (88 automações)
    │
    ├── 🏊 piscina/ .................................. 22 automações
    │   ├── piscina_filtragem.yaml .................. 9 automações ✅
    │   ├── piscina_bomba_peristaltica.yaml ......... 6 automações
    │   ├── piscina_temperatura.yaml ................ 4 automações
    │   └── piscina_cobertura.yaml .................. 3 automações
    │
    ├── 🚗 veiculo_eletrico/ ......................... 10 automações
    │   ├── ev_carregamento.yaml .................... 5 automações
    │   ├── ev_excesso_solar.yaml ................... 3 automações
    │   └── ev_depois_piscina.yaml .................. 2 automações ✅
    │
    ├── 🚪 portoes_portarias/ ........................ 17 automações
    │   ├── portao_principal.yaml ................... 8 automações
    │   ├── portao_botoes.yaml ...................... 7 automações
    │   └── portaria_video.yaml ..................... 2 automações
    │
    ├── 💡 iluminacao/ ............................... 23 automações
    │   ├── luzes_interior.yaml ..................... 12 automações
    │   ├── luzes_exterior.yaml ..................... 6 automações
    │   └── luzes_automaticas.yaml .................. 5 automações
    │
    ├── 🌡️ clima/ .................................... 11 automações
    │   ├── aquecimento_arrefecimento.yaml .......... 8 automações
    │   └── ventilacao.yaml ......................... 3 automações
    │
    ├── ☀️ energia_solar/ ............................ 7 automações
    │   ├── paineis_solares.yaml .................... 4 automações
    │   └── otimizacao_consumo.yaml ................. 3 automações
    │
    ├── 🔐 seguranca/ ................................ 5 automações
    │   ├── alarmes.yaml ............................ 3 automações
    │   └── notificacoes.yaml ....................... 2 automações
    │
    └── ⚙️ sistema/ .................................. 9 automações
        ├── watchdogs.yaml .......................... 4 automações
        ├── monitorizacao.yaml ...................... 3 automações
        └── utilidades.yaml ......................... 2 automações
```

---

## 📊 Estatísticas

| Categoria | Ficheiros | Automações | % Total |
|-----------|-----------|------------|---------|
| 💡 Iluminação | 3 | 23 | 26.1% |
| 🏊 Piscina | 4 | 22 | 25.0% |
| 🚪 Portões | 3 | 17 | 19.3% |
| 🌡️ Clima | 2 | 11 | 12.5% |
| 🚗 EV | 3 | 10 | 11.4% |
| ⚙️ Sistema | 3 | 9 | 10.2% |
| ☀️ Solar | 2 | 7 | 8.0% |
| 🔐 Segurança | 2 | 5 | 5.7% |
| **TOTAL** | **26** | **88** | **100%** |

---

## 🔄 Comparação: Antes vs Depois

### ANTES ❌
```
automations/
├── automations.yaml ............... 2403 linhas (misturado)
├── automations_root.yaml .......... 208 linhas (misturado)
├── piscina_filtragem.yaml ......... 270 linhas
└── ev_depois_bomba_piscina.yaml ... 82 linhas
```
- ❌ Difícil encontrar automações
- ❌ Ficheiros muito grandes
- ❌ Sem organização lógica
- ❌ Sem descrições
- ❌ IDs numéricos

### DEPOIS ✅
```
automations/
├── piscina/
│   ├── piscina_filtragem.yaml
│   ├── piscina_bomba_peristaltica.yaml
│   ├── piscina_temperatura.yaml
│   └── piscina_cobertura.yaml
├── veiculo_eletrico/
│   ├── ev_carregamento.yaml
│   ├── ev_excesso_solar.yaml
│   └── ev_depois_piscina.yaml
└── [...]
```
- ✅ Organização lógica por categoria
- ✅ Ficheiros pequenos e focados
- ✅ Fácil manutenção
- ✅ Descrições completas
- ✅ IDs descritivos

---

## 🎨 Convenções de Nomenclatura

### Ficheiros
```
categoria_funcionalidade.yaml
```
Exemplos:
- `piscina_filtragem.yaml`
- `portao_botoes.yaml`
- `luzes_interior.yaml`

### IDs
```
categoria_componente_acao
```
Exemplos:
- `piscina_bomba_ligar_manha`
- `portao_botao_shelly_abrir`
- `luz_sala_movimento_detectado`

### Aliases
```
emoji Categoria - Descrição Curta
```
Exemplos:
- `🏊 Piscina - Iniciar Filtragem`
- `🚪 Portão - Botão Shelly`
- `💡 Luz Sala - Movimento`

---

## 📋 README.md (Índice)

Cada categoria terá um README.md com índice:

```markdown
# 🏊 Automações da Piscina

## Ficheiros

1. **piscina_filtragem.yaml** (9 automações)
   - Controlo de filtragem diária
   - Ajustes automáticos de horário
   - Watchdogs e alertas

2. **piscina_bomba_peristaltica.yaml** (6 automações)
   - Sincronização com bomba principal
   - Controlo manual
   - Segurança

3. **piscina_temperatura.yaml** (4 automações)
   - Monitorização temperatura
   - Alertas
   - Registos históricos

4. **piscina_cobertura.yaml** (3 automações)
   - Controlo automático
   - Estado e posicionamento

## Entidades Principais

- `switch.bomba_piscina_principal`
- `switch.bomba_peristaltica`
- `sensor.temperatura_piscina`
- `cover.cobertura_piscina`

## Dependências

- Timers: `input_datetime.piscina_*`
- Booleans: `input_boolean.piscina_*`
- Scripts: `script.piscina_*`
```

---

## 🔗 Dependências Entre Automações

### Exemplo: Piscina + EV

```
┌─────────────────────┐
│  Piscina Filtragem  │
│  (7h-18h)           │
└──────────┬──────────┘
           │
           │ desliga às 18h
           ▼
┌─────────────────────┐
│  EV Carregamento    │
│  (18h-7h)           │
└─────────────────────┘
```

**Ficheiros afetados:**
- `piscina/piscina_filtragem.yaml`
- `veiculo_eletrico/ev_depois_piscina.yaml`

**Coordenação:**
```yaml
# Em piscina_filtragem.yaml
- id: piscina_fim_filtragem
  trigger:
    - platform: time
      at: input_datetime.piscina_fim
  action:
    - service: switch.turn_off
      target:
        entity_id: switch.bomba_piscina
    # Sinaliza que EV pode iniciar
    - service: input_boolean.turn_on
      target:
        entity_id: input_boolean.piscina_concluida

# Em ev_depois_piscina.yaml
- id: ev_iniciar_depois_piscina
  trigger:
    - platform: state
      entity_id: input_boolean.piscina_concluida
      to: 'on'
  action:
    - service: switch.turn_on
      target:
        entity_id: switch.cfos_wallbox
```

---

## 🎯 Roadmap de Implementação

### ✅ Fase 1: PREPARAÇÃO (5 min)
- [x] Criar backup completo
- [x] Documentar estrutura atual
- [x] Identificar categorias
- [x] Mapear 88 automações

### 🔄 Fase 2: CRIAÇÃO (15 min)
- [ ] Criar estrutura de diretórios
- [ ] Criar README.md principal
- [ ] Criar templates base
- [ ] Configurar git ignore

### 🔄 Fase 3: MIGRAÇÃO (30 min)
- [ ] Piscina (22 automações)
- [ ] Iluminação (23 automações)
- [ ] Portões (17 automações)
- [ ] Clima (11 automações)
- [ ] EV (10 automações)
- [ ] Sistema (9 automações)
- [ ] Solar (7 automações)
- [ ] Segurança (5 automações)

### 🔄 Fase 4: MELHORIAS (20 min)
- [ ] Adicionar IDs descritivos
- [ ] Adicionar descrições
- [ ] Adicionar mode/max_exceeded
- [ ] Adicionar condições segurança
- [ ] Adicionar tratamento erros

### 🔄 Fase 5: VALIDAÇÃO (10 min)
- [ ] Validar sintaxe YAML
- [ ] Check configuration
- [ ] Testar carregamento
- [ ] Verificar logs

### 🔄 Fase 6: DEPLOY (5 min)
- [ ] Commit alterações
- [ ] Push para GitHub
- [ ] Restart Home Assistant
- [ ] Monitorizar 24h

---

## 💾 Estratégia de Backup

### Antes de começar:
```bash
# Backup completo
tar -czf backup_before_reorganization_$(date +%Y%m%d_%H%M%S).tar.gz automations/

# Git commit
git add -A
git commit -m "📸 Snapshot antes de reorganização"
git tag -a v1.0-before-reorg -m "Estado antes da reorganização"
```

### Durante migração:
- Criar branch `feature/reorganize-automations`
- Commits incrementais por categoria
- Pull requests para review

### Rollback se necessário:
```bash
git checkout v1.0-before-reorg
# ou
git revert <commit>
```

---

**Pronto para começar?** 🚀

Responde com:
- ✅ "Sim, implementa tudo" - Vou criar tudo automaticamente
- 🔧 "Ajusta primeiro" - Vou esperar feedback
- 👀 "Mostra mais exemplos" - Vou criar mais ficheiros exemplo
