# 🗂️ Análise de Organização - Diretoria Raiz

**Data:** 11 de novembro de 2025  
**Total de ficheiros:** 40 ficheiros na raiz

---

## 📊 Resumo Executivo

| Categoria | Quantidade | Estado | Ação Necessária |
|-----------|------------|--------|-----------------|
| **Documentação** | 3 | 🟢 Bom | Remover 1 backup |
| **Configuração HA** | 17 | 🟡 Pode melhorar | Modularizar 9 ficheiros |
| **Scripts** | 2 | 🟡 Pode melhorar | Mover para scripts/ |
| **Backups** | 3 | 🔴 Problema | Mover para backups/ |
| **Exemplos** | 3 | 🟡 Pode melhorar | Mover para docs/examples/ |
| **Dados JSON** | 4 | 🟡 Pode melhorar | Criar pasta solcast/ |
| **Logs** | 3 | 🔴 Crítico | Log de 129 MB! |
| **Outros** | 5 | 🟡 Revisar | Vários precisam atenção |

**Score Geral:** 🟡 **Razoável** (precisa melhorias)

---

## 🔍 Análise Detalhada

### 1. ✅ Documentação (BOM)

| Ficheiro | Tamanho | Estado | Recomendação |
|----------|---------|--------|--------------|
| `README.md` | 8.2 KB | ✅ Excelente | Manter (recém corrigido) |
| `SECURITY.md` | 4.9 KB | ✅ Necessário | Manter na raiz |
| `README.md.backup` | 39.9 KB | ⚠️ Temporário | **Remover** (já não é necessário) |

**Ação:** Remover README.md.backup

---

### 2. ⚠️ Configuração Home Assistant (PRECISA ORGANIZAÇÃO)

#### ✅ Essenciais (manter na raiz)

```yaml
# Estes DEVEM ficar na raiz
configuration.yaml      # Ficheiro principal
secrets.yaml           # Credenciais (gitignored)
customize.yaml         # Customizações
frontend.yaml          # Configuração frontend
ingress.yaml          # Configuração de ingress
groups.yaml           # Grupos de entidades
scripts.yaml          # Scripts (4.0 KB - ok na raiz)
```

#### ⚠️ Podem ser modularizados em packages/

**Sensores e dispositivos:**
```yaml
binary_sensor.yaml     # 837 bytes  → packages/sensors/binary.yaml
cover.yaml            # 721 bytes  → packages/covers.yaml
switches.yaml         # 633 bytes  → packages/switches.yaml
thermal_comfort.yaml  # 987 bytes  → packages/thermal_comfort.yaml (JÁ existe em packages!)
```

**⚠️ PROBLEMA IDENTIFICADO:** `thermal_comfort.yaml` existe na raiz E em packages!
- Raiz: 987 bytes
- Verificar se há duplicação

**Energia solar:**
```yaml
pv_excess_control.yaml # 13.2 KB → packages/pv_excess_control.yaml
```

**Inputs (podem ser consolidados):**
```yaml
input_boolean.yaml    # 635 bytes
input_datetime.yaml   # 94 bytes
input_number.yaml     # 2.6 KB
input_select.yaml     # 123 bytes

# Opções:
# 1. Criar packages/inputs_common.yaml (consolidar todos)
# 2. Mover para packages relevantes (cada input com seu package)
```

#### ⚠️ Ficheiros vazios

```yaml
scenes.yaml           # 0 bytes - VAZIO!
known_devices.yaml    # 0 bytes - VAZIO! (também gitignored)
```

**Ação:** Remover ficheiros vazios ou adicionar comentário explicativo

---

### 3. ⚠️ Scripts/Utilitários (MOVER)

| Ficheiro | Tamanho | Propósito | Recomendação |
|----------|---------|-----------|--------------|
| `migrate_fase2.py` | 10.6 KB | Script de migração Fase 2 | Mover para `scripts/migration/` |
| `reorganizar_automacoes.py` | 5.0 KB | Script de reorganização | Mover para `scripts/migration/` |

**Ação:** Criar `scripts/migration/` e mover scripts de utilidade

---

### 4. 🔴 Backups (PROBLEMA - NA RAIZ!)

| Ficheiro | Tamanho | Data | Recomendação |
|----------|---------|------|--------------|
| `backup_packages_20251111_222034.tar.gz` | 14.5 KB | 2025-11-11 | Mover para `backups/` |
| `backup_reorganizacao_20251111_202210.tar.gz` | 1.2 KB | 2025-11-11 | Mover para `backups/` |
| `backup_reorganizacao_20251111_202231.tar.gz` | 50.7 KB | 2025-11-11 | Mover para `backups/` |

**⚠️ PROBLEMA:** Backups na raiz poluem o diretório principal!

**Ação:** Mover todos para a pasta `backups/` existente

---

### 5. ⚠️ Exemplos/Rascunhos (ORGANIZAR)

| Ficheiro | Tamanho | Propósito | Recomendação |
|----------|---------|-----------|--------------|
| `EXEMPLO_PORTAO_BOTOES.yaml` | 4.7 KB | Exemplo de automação | `docs/examples/` |
| `PREVIEW_ESTRUTURA.txt` | 4.3 KB | Preview de estrutura | `docs/` ou remover |
| `delete_from_database.txt` | 89 bytes | Script SQL? | Verificar e organizar |

**Ação:** Criar `docs/examples/` para exemplos de código

---

### 6. ⚠️ Dados JSON Solcast (MOVER)

| Ficheiro | Tamanho | Tipo | Recomendação |
|----------|---------|------|--------------|
| `solcast.json` | 2.8 MB | Dados | Mover para `solcast/` ou `.storage/` |
| `solcast-undampened.json` | 146.2 KB | Dados | Mover para `solcast/` |
| `solcast-usage.json` | 85 bytes | Dados | Mover para `solcast/` |
| `solcast-sites.json` | 346 bytes | Dados | Mover para `solcast/` |
| `solcast-sites.json.example` | 276 bytes | Exemplo | ✅ Manter na raiz |

**Problema:** 3 MB de dados JSON na raiz!

**Ação:** Criar pasta `solcast/` para dados temporários

---

### 7. 🔴 Logs e Outros (CRÍTICO)

| Ficheiro | Tamanho | Problema | Recomendação |
|----------|---------|----------|--------------|
| `home-assistant.log` | **129.3 MB** | 🔴 MUITO GRANDE! | Rotação de logs |
| `home-assistant.log.1` | 1.6 MB | Normal (rotacionado) | ✅ OK (gitignored) |
| `home-assistant.log.fault` | 0 bytes | Vazio | Remover ou ignorar |
| `latest` | 89.4 KB | ??? | Investigar conteúdo |
| `index.html` | 18.3 KB | HTML | Mover para `www/` |

#### 🔴 PROBLEMA CRÍTICO: Log de 129 MB!

**Causa provável:** Rotação de logs não está funcionando corretamente

**Verificação do .gitignore:**
```gitignore
# Log files
home-assistant.log
home-assistant.log.*
```

✅ Logs estão protegidos no .gitignore

**Soluções:**

1. **Imediata:** Limpar log manualmente
   ```bash
   > home-assistant.log  # Esvaziar ficheiro
   # OU
   rm home-assistant.log && touch home-assistant.log
   ```

2. **Permanente:** Configurar rotação de logs no `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       # ... seus logs
   
   recorder:
     purge_keep_days: 7  # Já configurado
   
   # Adicionar se não existir:
   # Rotação automática de logs
   # Via logrotate do sistema ou configuração HA
   ```

---

## 🎯 Plano de Reorganização

### Prioridade ALTA (Fazer AGORA)

#### 1. 🔴 Limpar log gigante
```bash
# Opção 1: Esvaziar (preserva ficheiro)
> home-assistant.log

# Opção 2: Arquivar e criar novo
mv home-assistant.log home-assistant.log.archive
gzip home-assistant.log.archive
mv home-assistant.log.archive.gz backups/
touch home-assistant.log
```

#### 2. 🔴 Mover backups
```bash
mv backup_*.tar.gz backups/
```

#### 3. ⚠️ Remover ficheiros desnecessários
```bash
rm README.md.backup        # Backup já não necessário
rm scenes.yaml            # Vazio
rm home-assistant.log.fault  # Vazio
```

### Prioridade MÉDIA (Esta Semana)

#### 4. Organizar scripts de migração
```bash
mkdir -p scripts/migration
mv migrate_fase2.py scripts/migration/
mv reorganizar_automacoes.py scripts/migration/
```

#### 5. Organizar dados Solcast
```bash
mkdir -p solcast
mv solcast*.json solcast/
# Manter solcast-sites.json.example na raiz
cp solcast/solcast-sites.json.example ./
```

#### 6. Organizar exemplos
```bash
mkdir -p docs/examples
mv EXEMPLO_PORTAO_BOTOES.yaml docs/examples/
mv PREVIEW_ESTRUTURA.txt docs/ # ou remover se desatualizado
```

#### 7. Investigar ficheiros desconhecidos
```bash
# Verificar conteúdo
file latest
head -20 latest

# Verificar index.html
file index.html
# Se for do lovelace, mover para www/
```

### Prioridade BAIXA (Quando Tiver Tempo)

#### 8. Modularizar configurações

**Verificar duplicação thermal_comfort.yaml:**
```bash
diff thermal_comfort.yaml packages/climate_comfort_monolitico.yaml
# Se duplicado, remover da raiz
```

**Consolidar inputs em package:**
```bash
# Criar packages/inputs_common.yaml com todos os inputs
# Remover input_*.yaml da raiz
```

**Mover configurações para packages:**
```bash
# Criar packages apropriados:
# - packages/covers.yaml (de cover.yaml)
# - packages/switches.yaml (de switches.yaml)
# - packages/sensors_binary.yaml (de binary_sensor.yaml)
# - packages/pv_excess_control.yaml (de pv_excess_control.yaml)
```

---

## 📋 Checklist de Ações

### Imediatas
- [ ] Limpar home-assistant.log (129 MB → 0)
- [ ] Mover 3 backups para backups/
- [ ] Remover README.md.backup
- [ ] Remover scenes.yaml (vazio)
- [ ] Remover home-assistant.log.fault (vazio)

### Curto Prazo
- [ ] Criar scripts/migration/
- [ ] Mover migrate_fase2.py
- [ ] Mover reorganizar_automacoes.py
- [ ] Criar solcast/
- [ ] Mover solcast*.json
- [ ] Criar docs/examples/
- [ ] Mover EXEMPLO_PORTAO_BOTOES.yaml
- [ ] Investigar ficheiro 'latest'
- [ ] Verificar index.html

### Médio Prazo
- [ ] Verificar duplicação thermal_comfort.yaml
- [ ] Consolidar inputs em package
- [ ] Modularizar configurações restantes
- [ ] Configurar rotação automática de logs

---

## 📊 Estrutura Recomendada Final

```
homeassistant/
├── configuration.yaml          ✅ Principal
├── secrets.yaml               ✅ Credenciais
├── customize.yaml             ✅ Customizações
├── frontend.yaml              ✅ Frontend
├── ingress.yaml              ✅ Ingress
├── groups.yaml               ✅ Grupos
├── scripts.yaml              ✅ Scripts
│
├── README.md                  ✅ Documentação
├── SECURITY.md               ✅ Segurança
├── secrets.yaml.example      ✅ Exemplo
├── solcast-sites.json.example ✅ Exemplo
│
├── automations/              ✅ Automações (já organizado)
├── packages/                 ✅ Packages modulares
├── scripts/                  
│   └── migration/            ⭐ NOVO - Scripts de migração
├── docs/
│   ├── examples/             ⭐ NOVO - Exemplos de código
│   ├── historico/
│   └── analises/
├── solcast/                  ⭐ NOVO - Dados Solcast
│   ├── solcast.json
│   ├── solcast-undampened.json
│   └── ...
├── backups/                  ✅ Backups (mover .tar.gz)
└── [outras pastas existentes]
```

---

## 🎯 Resultados Esperados

### Antes
```
40 ficheiros na raiz
├── 17 configurações (algumas moduláveis)
├── 3 backups (não deveriam estar aqui)
├── 3 ficheiros vazios
├── 1 log de 129 MB!
└── Vários ficheiros desorganizados
```

### Depois
```
~12 ficheiros essenciais na raiz
├── 7 configurações principais
├── 2 documentação
├── 2 exemplos (.example)
├── 1 log limpo e rotacionado
└── Tudo organizado em pastas apropriadas
```

**Redução:** -70% ficheiros na raiz! ✅

---

## 🔧 Script de Reorganização Automática

```bash
#!/bin/bash
# reorganizar_raiz.sh

echo "🗂️  REORGANIZAÇÃO DA RAIZ"
echo "========================"

# 1. Limpar log
echo "📋 Limpando log gigante..."
> home-assistant.log
echo "   ✅ home-assistant.log limpo"

# 2. Mover backups
echo "📦 Movendo backups..."
mv backup_*.tar.gz backups/ 2>/dev/null
echo "   ✅ Backups movidos"

# 3. Remover ficheiros desnecessários
echo "🗑️  Removendo ficheiros desnecessários..."
rm -f README.md.backup scenes.yaml home-assistant.log.fault
echo "   ✅ Ficheiros removidos"

# 4. Criar estruturas
echo "📁 Criando estruturas..."
mkdir -p scripts/migration
mkdir -p solcast
mkdir -p docs/examples

# 5. Mover scripts
echo "🐍 Movendo scripts..."
mv migrate_fase2.py scripts/migration/ 2>/dev/null
mv reorganizar_automacoes.py scripts/migration/ 2>/dev/null
echo "   ✅ Scripts movidos"

# 6. Mover dados Solcast
echo "☀️  Organizando Solcast..."
mv solcast.json solcast/ 2>/dev/null
mv solcast-undampened.json solcast/ 2>/dev/null
mv solcast-usage.json solcast/ 2>/dev/null
mv solcast-sites.json solcast/ 2>/dev/null
echo "   ✅ Dados Solcast organizados"

# 7. Mover exemplos
echo "📝 Movendo exemplos..."
mv EXEMPLO_PORTAO_BOTOES.yaml docs/examples/ 2>/dev/null
mv PREVIEW_ESTRUTURA.txt docs/ 2>/dev/null
echo "   ✅ Exemplos movidos"

echo ""
echo "✅ REORGANIZAÇÃO CONCLUÍDA!"
echo ""
echo "📊 Verificar:"
echo "   • scripts/migration/"
echo "   • solcast/"
echo "   • docs/examples/"
echo "   • backups/"
```

---

## ⚠️ Avisos Importantes

### Antes de Reorganizar

1. **Fazer backup completo:**
   ```bash
   tar -czf backup_raiz_$(date +%Y%m%d_%H%M%S).tar.gz *.yaml *.py *.json *.txt *.md
   mv backup_raiz_*.tar.gz backups/
   ```

2. **Verificar configuration.yaml:**
   - Se há includes absolutos que vão quebrar
   - Atualizar paths se necessário

3. **Testar configuração após cada mudança:**
   ```bash
   hass --script check_config
   ```

### Depois de Reorganizar

1. **Reiniciar Home Assistant**
2. **Verificar logs** para erros
3. **Confirmar que todas as entidades carregaram**
4. **Atualizar .gitignore** se necessário

---

## 📚 Documentação Relacionada

- [Histórico de Reorganização](../historico/REORGANIZACAO.md)
- [Análise de Packages](PACKAGES.md)
- [Melhorias Técnicas](MELHORIAS_TECNICAS.md)
- [Segurança](../SECURITY.md)

---

**Última atualização:** 11 de novembro de 2025  
**Próxima ação:** Executar reorganização prioritária
