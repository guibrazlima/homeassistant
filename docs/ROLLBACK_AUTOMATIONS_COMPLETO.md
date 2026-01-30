# 🔄 ROLLBACK: Como Reverter a Consolidação de Automações

## 📅 Data da Consolidação: 2026-01-30
## 🌿 Branch: `consolidacao-automations-gui`
## 📊 Alteração: 65 automações (automations/ + packages/) → automations.yaml

---

## ⚠️ QUANDO USAR ESTE ROLLBACK

Se após a consolidação encontrares problemas como:
- ❌ Automações não funcionam corretamente
- ❌ GUI não responde como esperado
- ❌ Preferências por estrutura modular original
- ❌ Problemas com dependências de packages

---

## 🎯 3 MÉTODOS DE ROLLBACK

### **Método 1: Git Tag (RÁPIDO E SEGURO)** ✅ Recomendado

```bash
cd /data/homeassistant

# 1. Verificar tag
git tag -l "pre-consolidacao-total"

# 2. Restaurar ficheiros do tag
git checkout pre-consolidacao-total -- automations/
git checkout pre-consolidacao-total -- packages/
git checkout pre-consolidacao-total -- configuration.yaml

# 3. Confirmar alterações
git status

# 4. Remover automations.yaml consolidado
rm automations.yaml

# 5. Reiniciar Home Assistant
docker restart homeassistant

# 6. (Opcional) Criar commit do rollback
git add .
git commit -m "🔄 Rollback: Restaurar estrutura modular de automações"
```

**Tempo:** ~3 minutos  
**Risco:** Nenhum  
**Resultado:** Volta exatamente ao estado antes da consolidação

---

### **Método 2: Backup Manual (SEM GIT)**

```bash
cd /data/homeassistant

# 1. Parar Home Assistant
docker stop homeassistant

# 2. Remover estrutura consolidada
mv automations.yaml automations_consolidated_BACKUP.yaml

# 3. Restaurar da pasta de backup
mv automations_OLD_MODULAR_BACKUP automations

# 4. Restaurar packages (se necessário)
for f in packages/piscina_*.yaml.before_automation_removal; do
  original="${f%.before_automation_removal}"
  cp "$f" "$original"
done

# 5. Restaurar configuration.yaml
# Editar manualmente ou usar backup:
# automation: !include_dir_merge_list automations/

# 6. Reiniciar
docker start homeassistant
```

**Tempo:** ~5 minutos  
**Risco:** Baixo (requer edição manual configuration.yaml)

---

### **Método 3: Git Revert (Desfazer Commit)**

```bash
cd /data/homeassistant

# 1. Ver histórico
git log --oneline | head -10

# 2. Identificar commit da consolidação
# Procurar por: "♻️ Consolidação TOTAL: 65 automações"

# 3. Reverter commit
git revert <COMMIT_HASH>

# 4. Reiniciar Home Assistant
docker restart homeassistant
```

**Tempo:** ~2 minutos  
**Risco:** Nenhum (Git cria novo commit revertendo)  
**Vantagem:** Mantém histórico completo

---

## 📦 RESTAURAR AUTOMAÇÕES NOS PACKAGES

Se quiseres voltar a ter automações dentro dos packages (não recomendado para GUI):

```bash
cd /data/homeassistant

# Restaurar cada package individualmente
for f in packages/piscina_*.yaml.before_automation_removal; do
  original="${f%.before_automation_removal}"
  echo "Restaurando $original..."
  cp "$f" "$original"
  echo "  ✓ Restaurado"
done

# Verificar
grep "^automation:" packages/piscina_*.yaml
# Deve mostrar blocos automation em cada package
```

---

## ✅ VALIDAÇÃO PÓS-ROLLBACK

Após qualquer método de rollback:

```bash
# 1. Verificar estrutura restaurada
ls -la automations/
# Deve mostrar pastas: clima/, piscina/, sistema/, etc.

# 2. Verificar configuration.yaml
grep "automation:" configuration.yaml
# Deve mostrar: automation: !include_dir_merge_list automations/

# 3. Validar configuração
docker exec homeassistant python -m homeassistant --script check_config -c /config

# 4. Contar automações
echo "automations/: $(grep -r "^- id:" automations/ --include="*.yaml" | wc -l)"
echo "packages/: $(grep -c "^  - id:" packages/piscina_*.yaml | awk '{s+=$1} END {print s}')"

# 5. Restart e testar
docker restart homeassistant
```

---

## 🗂️ BACKUPS DISPONÍVEIS

### **Git Tag**
```bash
Tag: pre-consolidacao-total
Commit: 7fdc2be
Data: 2026-01-30 16:40:31
```

### **Backups Locais**
```bash
# Estrutura modular original
automations_modular_backup_20260130_164031/

# Packages antes da remoção de automation
packages_backup_20260130_164031/

# Packages com ficheiros .before_automation_removal
packages/piscina_*.yaml.before_automation_removal
```

### **Ficheiro Consolidado (se quiseres manter)**
```bash
# Após rollback, automations.yaml fica como:
automations_consolidated_BACKUP.yaml
```

---

## 🔍 TROUBLESHOOTING

### **Problema: automations/ já existe**
```bash
# Solução: Renomear primeiro
mv automations automations_temp
mv automations_OLD_MODULAR_BACKUP automations
```

### **Problema: Git mostra conflitos**
```bash
# Solução: Reset hard ao tag
git reset --hard pre-consolidacao-total
# ⚠️ ATENÇÃO: Perde alterações não commitadas
```

### **Problema: Automações não carregam após rollback**
```bash
# 1. Verificar configuration.yaml
cat configuration.yaml | grep automation

# 2. Deve ser:
automation: !include_dir_merge_list automations/

# 3. Se estiver errado, corrigir e reiniciar
docker restart homeassistant
```

### **Problema: GUI ainda mostra consolidado**
```bash
# Limpar cache do browser
# Ctrl+Shift+R (Firefox/Chrome)
# Ou limpar Application Storage no DevTools
```

---

## 📊 COMPARAÇÃO: Consolidado vs Modular

| Aspecto | Consolidado (atual) | Modular (após rollback) |
|---------|---------------------|-------------------------|
| **GUI edição** | ✅ 100% funcional | ❌ Somente leitura |
| **Estrutura** | 1 ficheiro (2.954 linhas) | 11+ ficheiros organizados |
| **Packages** | Automações separadas | Automações integradas |
| **Manutenção YAML** | Ficheiro grande | Ficheiros pequenos |
| **Git diffs** | Ficheiro único | Por ficheiro/categoria |

---

## 🎯 QUANDO NÃO FAZER ROLLBACK

**Mantém consolidado se:**
- ✅ GUI está funcional e útil
- ✅ Não tens problemas com automações
- ✅ Prefers editar via interface web
- ✅ Não editas YAML manualmente frequentemente

**Rollback se:**
- ❌ Preferes estrutura modular no Git
- ❌ Editas YAML manualmente sempre
- ❌ Queres automações nos packages (cohesão)
- ❌ Encontraste bugs após consolidação

---

## 📞 SUPORTE

**Documentação relacionada:**
- `docs/ANALISE_CONSOLIDACAO_COMPLETA.md` - Análise inicial
- `automations_OLD_MODULAR_BACKUP/README.md` - Estrutura original
- Git commit log - Histórico completo de alterações

**Git Tags:**
- `pre-consolidacao-total` - Antes da consolidação
- (futuro) `pos-consolidacao-validada` - Após validação

---

## ✅ CHECKLIST DE ROLLBACK

Antes de fazer rollback, confirma:

- [ ] Backup atual criado (se fizeste alterações em automations.yaml)
- [ ] Home Assistant pode ser parado (~5 min downtime)
- [ ] Sabes qual método de rollback usar
- [ ] Tens acesso aos backups/git tags
- [ ] Validaste que rollback resolve o problema

Durante rollback:

- [ ] Ficheiros restaurados corretamente
- [ ] configuration.yaml aponta para automations/
- [ ] check_config passou
- [ ] Automações contadas (57 + 8 = 65)

Após rollback:

- [ ] Home Assistant reiniciado
- [ ] Automações carregadas no GUI
- [ ] Testadas algumas automações críticas
- [ ] Commit do rollback criado (opcional)

---

**Criado em:** 2026-01-30  
**Última atualização:** 2026-01-30  
**Versão:** 1.0
