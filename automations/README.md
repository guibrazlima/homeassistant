# 📚 Automações do Home Assistant

## 📁 Estrutura Reorganizada

Este diretório contém todas as automações organizadas por categoria.

### 🗂️ Categorias

#### 🏊 Piscina (piscina/) - 14 automações
- **piscina_filtragem.yaml** (1) - Controlo de filtragem (migrado da Fase 2)
- **piscina_geral.yaml** (12) - Automações gerais da piscina
- **piscina_cobertura.yaml** (1) - Estado da cobertura (LLM Vision)

#### 🚗 Veículo Elétrico (veiculo_eletrico/) - 10 automações
- **ev_depois_piscina.yaml** (3) - Carregamento após bomba da piscina
- **ev_carregamento.yaml** (7) - Smart charging, SOC, wallbox

#### 🚪 Portões e Portarias (portoes_portarias/) - 8 automações
- **portao_botoes.yaml** (2) - Controlo via botões exemplo
- **portao_principal.yaml** (6) - Callbacks, luzes, notificações

#### 💡 Iluminação (iluminacao/) - 1 automação
- **luzes_exterior.yaml** (1) - Luz exterior automática

#### 🌡️ Clima (clima/) - 3 automações
- **aquecimento_arrefecimento.yaml** (2) - Backups, callbacks
- **ventilacao.yaml** (1) - Ventilador cave solar

#### ☀️ Energia Solar (energia_solar/) - 1 automação
- **paineis_solares.yaml** (1) - Otimização bomba piscina solar

#### ⚙️ Sistema (sistema/) - 31 automações
- **monitorizacao.yaml** (1) - SpeedTests
- **outros.yaml** (30) - Várias automações diversas (a categorizar)

**TOTAL ATIVO:** 68 automações organizadas

### 📝 Ficheiros Antigos (Manter como referência)
- `automations.yaml` - Ficheiro principal antigo
- `automations_root.yaml` - Ficheiro secundário antigo

---

## 🔄 Estado da Migração

**Fase Atual:** Fase 2 CONCLUÍDA! ✅

### ✅ FASE 1 CONCLUÍDA
- [x] Estrutura de diretórios criada (8 categorias)
- [x] Backup completo criado
- [x] Branch criado (feature/reorganize-automations)
- [x] Ficheiros base organizados
- [x] README.md e documentação criada

### ✅ FASE 2 CONCLUÍDA
- [x] Script Python de migração automática criado
- [x] 63 automações categorizadas automaticamente
- [x] 11 ficheiros novos criados
- [x] IDs descritivos gerados (de numéricos para texto)
- [x] Descrições automáticas adicionadas
- [x] Mode e max_exceeded configurados
- [x] Headers informativos em cada ficheiro

**Automações processadas:** 68 ativas (de 79 originais)

### 🔄 FASE 3 - PRÓXIMA
- [ ] Mover 30 automações de `sistema/outros.yaml` para categorias corretas
- [ ] Melhorar descrições automáticas com descrições personalizadas
- [ ] Adicionar condições de segurança
- [ ] Validação YAML completa
- [ ] Testar carregamento no Home Assistant

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
