# 📚 Automações do Home Assistant

## 📁 Estrutura Reorganizada

Este diretório contém todas as automações organizadas por categoria.

### 🗂️ Categorias

#### 🏊 Piscina (piscina/)
- **piscina_filtragem.yaml** - Controlo de filtragem e horários
- **piscina_temperatura.yaml** - Monitorização de temperatura (A CRIAR)
- **piscina_cobertura.yaml** - Controlo da cobertura (A CRIAR)

#### 🚗 Veículo Elétrico (veiculo_eletrico/)
- **ev_depois_piscina.yaml** - Carregamento após bomba da piscina
- **ev_carregamento.yaml** - Controlo geral de carregamento (A CRIAR)

#### 🚪 Portões e Portarias (portoes_portarias/)
- **portao_botoes.yaml** - Controlo via botões
- **portao_principal.yaml** - Automações principais (A CRIAR)

#### 💡 Iluminação (iluminacao/)
- A CRIAR

#### 🌡️ Clima (clima/)
- A CRIAR

#### ☀️ Energia Solar (energia_solar/)
- A CRIAR

#### 🔐 Segurança (seguranca/)
- A CRIAR

#### ⚙️ Sistema (sistema/)
- **watchdogs.yaml** - Monitorização (A CRIAR)
- **utilidades.yaml** - Utilitários gerais (A CRIAR)

### 📝 Ficheiros Antigos (Manter como referência)
- `automations.yaml` - Ficheiro principal antigo
- `automations_root.yaml` - Ficheiro secundário antigo

---

## 🔄 Estado da Migração

**Fase Atual:** Estrutura reorganizada - Migração de conteúdo em fase 2

### ✅ FASE 1 CONCLUÍDA
- [x] Estrutura de diretórios criada (8 categorias)
- [x] Backup completo criado (backup_reorganizacao_20251111_202231.tar.gz)
- [x] Branch criado (feature/reorganize-automations)
- [x] Ficheiros movidos para nova estrutura:
  - ✅ `piscina/piscina_filtragem.yaml` (11 automações)
  - ✅ `veiculo_eletrico/ev_depois_piscina.yaml` (3 automações)
  - ✅ `portoes_portarias/portao_botoes.yaml` (2 automações exemplo)
  - ✅ `sistema/todas_automacoes_migradas.yaml` (53 automações)
  - ✅ `sistema/automacoes_root_migradas.yaml` (10 automações)
- [x] README.md criado com documentação
- [x] configuration.yaml já configurado (usa !include_dir_merge_list)

**Total:** 79 automações organizadas em estrutura modular

### 🔄 FASE 2 - PRÓXIMOS PASSOS
- [ ] Dividir `sistema/todas_automacoes_migradas.yaml` por categorias
- [ ] Adicionar IDs descritivos a todas as automações
- [ ] Adicionar descrições completas
- [ ] Adicionar mode e max_exceeded
- [ ] Adicionar condições de segurança
- [ ] Validação e testes

---

## 📊 Convenções

### IDs
```yaml
categoria_componente_acao
```
Exemplo: `piscina_bomba_ligar_manha`

### Aliases
```yaml
emoji Categoria - Descrição
```
Exemplo: `🏊 Piscina - Iniciar Filtragem`

### Ficheiros
```yaml
categoria_funcionalidade.yaml
```
Exemplo: `piscina_filtragem.yaml`

---

**Última atualização:** 2025-11-11
