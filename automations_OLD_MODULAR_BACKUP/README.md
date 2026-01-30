# � BACKUP: Estrutura Modular Original de Automações

## ⚠️ ATENÇÃO: ESTE É UM BACKUP

Esta pasta contém a estrutura modular **ORIGINAL** das automações do Home Assistant.

**Data do backup:** 2026-01-30 16:40:31  
**Razão:** Consolidação total de 65 automações em `automations.yaml`  
**Branch Git:** `consolidacao-automations-gui`  
**Git Tag:** `pre-consolidacao-total`

---

## 📊 CONTEÚDO DESTE BACKUP

### **57 Automações Modulares** distribuídas por categoria:

```
automations_OLD_MODULAR_BACKUP/
├── README.md (este ficheiro)
├── 🌡️ clima/
│   ├── aquecimento_serpentina_auto.yaml (2 automações)
│   └── aquecimento_serpentina.yaml (2 automações)
│
├── ⚡ energia_solar/
│   ├── solcast.yaml (1 automação)
│   └── tibber_melhor_preco_compra.yaml (3 automações)
│
├── 💡 iluminacao/
│   ├── desligar_luzes_WC.yaml (1 automação)
│   ├── iluminacao_automatica_crepusculo.yaml (2 automações)
│   ├── iluminacao_automatica_exterior.yaml (4 automações)
│   ├── iluminacao_automatica_presenca.yaml (14 automações)
│   ├── luzes_piscina_automatico.yaml (5 automações)
│   └── strip_tv.yaml (1 automação)
│
├── � piscina/
│   ├── bomba_calor_piscina_automatico.yaml (1 automação)
│   ├── llm_vision_analise_imagens.yaml (2 automações)
│   ├── piscina_alerta_consumiveis.yaml (3 automações)
│   ├── piscina_alertas_parametros.yaml (1 automação)
│   ├── piscina_analise_qualidade_agua.yaml (1 automação)
│   ├── piscina_controlo_bombas.yaml (1 automação)
│   ├── piscina_modo_automatico.yaml (1 automação)
│   └── recolher_cobertura_emergencia.yaml (2 automações)
│
├── 🚪 portoes_portarias/
│   └── portao_pedonal.yaml (2 automações)
│
├── 🖥️ sistema/
│   ├── alertas_estado_sistema.yaml (1 automação)
│   ├── github_commits_notificacoes.yaml (1 automação)
│   ├── homeassistant_inicializacao.yaml (1 automação)
│   ├── input_helpers_initialize.yaml (1 automação)
│   ├── mqtt_portaria_video_manutencao_link.yaml (1 automação)
│   └── notificacoes_atualizacoes.yaml (1 automação)
│
└── 🚗 veiculo_eletrico/
    ├── carro_carregamento_solar_automatico.yaml (2 automações)
    └── enercharge_alertas.yaml (2 automações)
```

**Total:** 57 automações em 11 ficheiros YAML


---

## 🔄 COMO RESTAURAR ESTA ESTRUTURA

### **Opção 1: Git Tag** (Recomendado)
```bash
cd /data/homeassistant
git checkout pre-consolidacao-total -- automations/
git checkout pre-consolidacao-total -- configuration.yaml
rm automations.yaml
docker restart homeassistant
```

### **Opção 2: Restaurar Manualmente**
```bash
cd /data/homeassistant

# 1. Remover estrutura consolidada
mv automations.yaml automations_consolidated_BACKUP.yaml

# 2. Restaurar estrutura modular
mv automations_OLD_MODULAR_BACKUP automations

# 3. Editar configuration.yaml
# Alterar: automation: !include automations.yaml
# Para:    automation: !include_dir_merge_list automations/

# 4. Reiniciar
docker restart homeassistant
```

### **Documentação completa de rollback:**
Ver: `docs/ROLLBACK_AUTOMATIONS_COMPLETO.md`

---

## 📋 VANTAGENS DA ESTRUTURA MODULAR

### ✅ **Organização por Categoria**
- Ficheiros pequenos e focados
- Fácil navegação por emoji/categoria
- Git diffs mais legíveis

### ✅ **Manutenção YAML**
- Edições isoladas por ficheiro
- Menos conflitos em Git (trabalho multi-utilizador)
- Merge requests mais simples

### ✅ **Coesão Conceitual**
- Automações relacionadas juntas
- Alinhamento com estrutura de packages
- Separação de responsabilidades

---

## ⚠️ DESVANTAGENS DA ESTRUTURA MODULAR

### ❌ **GUI Home Assistant**
- **Somente leitura** no interface web
- Não permite criar/editar/apagar automações pela GUI
- Alterações requerem edição YAML manual

### ❌ **Debugging**
- Erros não apontam ficheiro específico
- Requer grep/search para localizar automação
- Logs mostram apenas automation.* sem contexto

---

## 🎯 PORQUÊ A CONSOLIDAÇÃO?

**Motivação original:**
> "quero puder alterar as automações atraves do gui"

**Objetivo:** Permitir que todas as 65 automações sejam:
- ✏️ Criadas via GUI
- ✏️ Editadas via GUI
- ❌ Apagadas via GUI
- 📊 Geridas visualmente

**Resultado:** `automations.yaml` único com 2.954 linhas

---

## 🗂️ METADADOS DO BACKUP

```yaml
backup_info:
  data: 2026-01-30T16:40:31
  branch: consolidacao-automations-gui
  commit_anterior: 7fdc2be
  git_tag: pre-consolidacao-total
  razao: consolidacao_gui_editing
  total_automations: 57
  total_files: 11
  categories:
    - clima (2 ficheiros, 4 automações)
    - energia_solar (2 ficheiros, 4 automações)
    - iluminacao (6 ficheiros, 27 automações)
    - piscina (8 ficheiros, 12 automações)
    - portoes_portarias (1 ficheiro, 2 automações)
    - sistema (6 ficheiros, 6 automações)
    - veiculo_eletrico (2 ficheiros, 4 automações)
```

---

## � VERIFICAÇÃO DE INTEGRIDADE

Para verificar que este backup contém todas as automações originais:

```bash
# Contar automações por "- id:"
grep -r "^- id:" automations_OLD_MODULAR_BACKUP/ --include="*.yaml" | wc -l
# Resultado esperado: 57

# Listar todas as categorias
ls -1 automations_OLD_MODULAR_BACKUP/
# Resultado: clima/ energia_solar/ iluminacao/ piscina/ ...

# Verificar estrutura YAML
find automations_OLD_MODULAR_BACKUP/ -name "*.yaml" -exec python3 -c "import yaml; yaml.safe_load(open('{}'))" \;
# Sem output = YAML válido
```

---

## 📚 FICHEIROS RELACIONADOS

- **Consolidado atual:** `/data/homeassistant/automations.yaml`
- **Configuração:** `/data/homeassistant/configuration.yaml`
- **Documentação consolidação:** `docs/ANALISE_CONSOLIDACAO_COMPLETA.md`
- **Rollback guide:** `docs/ROLLBACK_AUTOMATIONS_COMPLETO.md`
- **Git tag recovery:** `git show pre-consolidacao-total:automations/`

---

## ⚠️ NÃO APAGAR ESTA PASTA

Esta pasta serve como:
- 🛡️ **Backup de segurança** da estrutura modular
- 📖 **Referência histórica** da organização anterior
- 🔄 **Recovery point** caso consolidação falhe
- 📊 **Documentação** da estrutura original

**Se removida:** Podes sempre recuperar via Git tag `pre-consolidacao-total`

---

**Backup criado por:** GitHub Copilot (consolidação automática)  
**Data:** 2026-01-30 16:40:31  
**Versão:** 1.0  
**Status:** ✅ Verificado e funcional

Exemplo: `🏊 Piscina - Iniciar Filtragem`

### Ficheiros
```yaml
categoria_funcionalidade.yaml
```
Exemplo: `piscina_filtragem.yaml`

---

**Última atualização:** 2025-11-11
