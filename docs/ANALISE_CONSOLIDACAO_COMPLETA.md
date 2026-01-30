# 🔄 ANÁLISE COMPLETA: Consolidação de Automações (ATUALIZADA)

## 📅 Data: 2026-01-30
## 🌿 Branch: `consolidacao-automations-gui`
## 🎯 Objetivo: Consolidar TODAS as automações para edição via GUI

---

## 📊 SITUAÇÃO ATUAL - ANÁLISE COMPLETA

### **Descoberta Importante!** ⚠️
As automações estão distribuídas em **2 locais**:

#### 1️⃣ **Pasta `automations/`** (Estrutura Modular)
```
automations/
  ├── clima/
  │   ├── aquecimento_arrefecimento.yaml  (11.5 KB)
  │   └── ventilacao.yaml                 (956 bytes)
  ├── piscina/
  │   ├── piscina_geral.yaml              (16.2 KB)
  │   ├── piscina_filtragem.yaml          (1.2 KB)
  │   └── piscina_cobertura.yaml          (1.6 KB)
  ├── energia_solar/
  │   └── paineis_solares.yaml            (2.2 KB)
  ├── portoes_portarias/
  │   ├── portao_principal.yaml           (5.6 KB)
  │   └── portao_botoes.yaml              (1.7 KB)
  ├── iluminacao/
  │   └── luzes_exterior.yaml             (774 bytes)
  └── sistema/
      ├── outros.yaml                     (31.8 KB)
      └── monitorizacao.yaml              (794 bytes)
```

**Total:** 57 automações

#### 2️⃣ **Pasta `packages/`** (Automações Integradas)
```
packages/
  ├── piscina_clorador_sal.yaml      (144 linhas)
  │   └── automation: 1 (piscina_llmvision_sal_baixo)
  ├── piscina_cloro_tpo.yaml         (176 linhas)
  │   └── automation: 2 (piscina_cloro_tpo_seconds, piscina_cloro_tpo_failsafe)
  ├── piscina_cobertura.yaml         (177 linhas)
  │   └── automation: 2 (piscina_llmvision_cobertura, piscina_cobertura_quando_bomba_para)
  └── piscina_ph.yaml                (170 linhas)
      └── automation: 3 (piscina_ph_ocr, piscina_ph_backup_on_change, piscina_ph_restore_on_start)
```

**Total:** 8 automações (todas relacionadas com piscina)

#### 3️⃣ **Pasta `templates/`**
**Total:** 0 automações (apenas template sensors)

---

## 📊 ESTATÍSTICAS GLOBAIS

| Local | Automações | Linhas | Tamanho |
|-------|------------|--------|---------|
| **automations/** | 57 | ~2.445 | ~73 KB |
| **packages/** | 8 | ~667 | ~20 KB |
| **templates/** | 0 | - | - |
| **TOTAL** | **65** | **~3.112** | **~93 KB** |

---

## ⚠️ PROBLEMA IDENTIFICADO (Atualizado)

### **Automações em `automations/`**
```yaml
automation: !include_dir_merge_list automations/
```
❌ **GUI NÃO FUNCIONA** - Somente leitura

### **Automações em `packages/`**
```yaml
homeassistant:
  packages:
    piscina_clorador_sal: !include packages/piscina_clorador_sal.yaml
    # ... outros packages
```

**Estrutura dos packages:**
```yaml
# piscina_clorador_sal.yaml
input_boolean:
  piscina_sal_baixo_raw:
    # ...

input_number:
  piscina_sal_baixo_off_streak:
    # ...

template:
  - binary_sensor:
      # ...

automation:  # ← Automação integrada no package
  - id: piscina_llmvision_sal_baixo
    alias: Piscina — Sal baixo (LLM Vision, amostragem+debounce)
    # ...
```

❌ **GUI NÃO FUNCIONA** - Automações em packages são somente leitura

---

## 🎯 OBJETIVO ATUALIZADO

**Consolidar TODAS as 65 automações** de 3 fontes:
1. ✅ `automations/` (57 automações)
2. ✅ `packages/` (8 automações)
3. ✅ `templates/` (0 automações)

**Para:**
```yaml
automation: !include automations.yaml
```

**Resultado:**
- ✅ GUI 100% funcional (editar/criar/apagar)
- ✅ Todas as 65 automações num único ficheiro
- ✅ Packages mantêm os outros componentes (input_boolean, sensors, etc.)

---

## 🔍 ANÁLISE DETALHADA DAS AUTOMAÇÕES EM PACKAGES

### **Características Especiais**

Estas 8 automações são **tightly coupled** com:
- `input_boolean` (estados internos)
- `input_number` (contadores, thresholds)
- `template sensors` (binary_sensor)

**Exemplo:** `piscina_clorador_sal.yaml`
```yaml
# Componentes interdependentes:
input_boolean:
  piscina_sal_baixo_raw:      # ← Usado pela automação
  piscina_sal_baixo:          # ← Usado pela automação

input_number:
  piscina_sal_baixo_off_streak:    # ← Usado pela automação
  piscina_sal_baixo_off_debounce:  # ← Usado pela automação

template:
  - binary_sensor:
      - name: "Piscina — Sal baixo (via LLM Vision)"
        state: "{{ is_state('input_boolean.piscina_sal_baixo', 'on') }}"  # ← Depende do input_boolean

automation:
  - id: piscina_llmvision_sal_baixo
    # Usa TODOS os componentes acima
```

### **Dependências dos 4 Packages**

| Package | Input Boolean | Input Number | Template Sensors | Automações |
|---------|---------------|--------------|------------------|------------|
| **piscina_clorador_sal** | 2 | 2 | 1 | 1 |
| **piscina_cloro_tpo** | 1 | 3 | 0 | 2 |
| **piscina_cobertura** | 0 | 0 | 0 | 2 |
| **piscina_ph** | 0 | 2 | 1 | 3 |

---

## 🎯 ESTRATÉGIAS DISPONÍVEIS

### **Opção A: Consolidação Total (RECOMENDADO)**

**O que fazer:**
1. Extrair as 8 automações dos packages
2. Merge com as 57 de `automations/`
3. Criar `automations.yaml` único com 65 automações
4. **Manter packages sem o bloco `automation:`** (só input_boolean, sensors, etc.)

**Vantagens:**
✅ **GUI 100% funcional** para todas as 65 automações  
✅ **Packages limpos** - Apenas configuração de entidades  
✅ **Separação de responsabilidades** - Automações num local, configuração noutro  
✅ **Padrão HA** - Automações geridas pelo GUI  

**Desvantagens:**
⚠️ **Perda de cohesão** - Automações separadas das entidades que usam  
⚠️ **Ficheiro grande** - 3.112 linhas num único ficheiro  
⚠️ **Manutenção** - Mais difícil encontrar automação relacionada com package  

---

### **Opção B: Consolidação Parcial (HÍBRIDO)**

**O que fazer:**
1. Consolidar apenas `automations/` (57) → `automations.yaml`
2. **Manter automações nos packages** (8) - Aceitar que não são editáveis no GUI
3. Documentar claramente quais automações estão em packages

**Vantagens:**
✅ **Cohesão mantida** - Automações complexas ficam com suas entidades  
✅ **GUI funcional para 88%** - 57 de 65 editáveis  
✅ **Menos disruptivo** - Packages não são alterados  

**Desvantagens:**
❌ **GUI parcialmente funcional** - 8 automações somente leitura  
❌ **Confusão** - Automações em 2 locais diferentes  
❌ **Inconsistência** - Algumas editáveis, outras não  

---

### **Opção C: Manter Estrutura Atual**

**O que fazer:**
- Nada. Aceitar que GUI não funciona.

❌ **NÃO RECOMENDADO** - Não atinge o objetivo.

---

## ✅ RECOMENDAÇÃO FINAL

### **Opção A: Consolidação Total**

**Porque:**
1. ✅ Atinge objetivo (GUI 100% funcional)
2. ✅ Consistência (todas as automações num local)
3. ✅ Facilita gestão no GUI
4. ✅ Separação clara: Packages = Config, Automations = Lógica

**Trade-off aceite:**
- Automações dos packages ficam fisicamente separadas das suas entidades
- **Solução:** Documentar com comentários e nomes claros

**Exemplo:**
```yaml
# automations.yaml

# ======================================================================
# 🏊 PISCINA - CLORADOR SAL (LLM Vision)
# ======================================================================
# 📦 Package relacionado: piscina_clorador_sal.yaml
# 🔗 Dependências:
#    - input_boolean.piscina_sal_baixo_raw
#    - input_boolean.piscina_sal_baixo
#    - input_number.piscina_sal_baixo_off_streak
#    - input_number.piscina_sal_baixo_off_debounce
# ======================================================================

- id: piscina_llmvision_sal_baixo
  alias: Piscina — Sal baixo (LLM Vision, amostragem+debounce)
  # ...
```

---

## 🛠️ PLANO DE IMPLEMENTAÇÃO ATUALIZADO

### **Fase 1: Preparação e Backup** (5 min)

```bash
# 1.1 Validar configuração atual
docker exec homeassistant ha core check

# 1.2 Contar automações
echo "Automations folder:"
grep -r "^- id:" /data/homeassistant/automations --include="*.yaml" | wc -l

echo "Packages:"
grep -c "^  - id:" /data/homeassistant/packages/piscina_*.yaml

# 1.3 Backups múltiplos
cp -r /data/homeassistant/automations /data/homeassistant/automations_modular_backup_$(date +%Y%m%d_%H%M%S)
cp -r /data/homeassistant/packages /data/homeassistant/packages_backup_$(date +%Y%m%d_%H%M%S)

# 1.4 Git commit
git add automations/ packages/
git commit -m "💾 Backup: Estrutura antes de consolidação (automations + packages)"

# 1.5 Git tag (recovery point)
git tag -a "pre-consolidacao-total" -m "Ponto de restauro antes de consolidar 65 automações"
```

---

### **Fase 2: Extração de Automações dos Packages** (10 min)

```bash
cd /data/homeassistant

# Criar ficheiro temporário para automações dos packages
cat > automations_from_packages.yaml << 'EOF'
# ======================================================================
# 🏊 PISCINA - AUTOMAÇÕES DOS PACKAGES (8 automações)
# ======================================================================
# Extraídas de: packages/piscina_*.yaml
# Data: $(date +%Y-%m-%d)
# ======================================================================

EOF

# Extrair bloco automation de cada package
for package in packages/piscina_clorador_sal.yaml \
               packages/piscina_cloro_tpo.yaml \
               packages/piscina_cobertura.yaml \
               packages/piscina_ph.yaml; do
  
  echo "# ----------------------------------------------------------------------" >> automations_from_packages.yaml
  echo "# Fonte: $(basename $package)" >> automations_from_packages.yaml
  echo "# ----------------------------------------------------------------------" >> automations_from_packages.yaml
  echo "" >> automations_from_packages.yaml
  
  # Extrair apenas o bloco automation (indentação correta)
  awk '/^automation:/,/^[a-z]/ {
    if (/^automation:/) next;
    if (/^[a-z]/ && !/^  /) exit;
    sub(/^  /, "");
    print
  }' "$package" >> automations_from_packages.yaml
  
  echo "" >> automations_from_packages.yaml
done
```

---

### **Fase 3: Consolidação Total** (15 min)

```bash
cd /data/homeassistant

# 3.1 Criar automations.yaml com cabeçalho
cat > automations.yaml << 'EOF'
# ======================================================================
# 🤖 AUTOMAÇÕES DO HOME ASSISTANT (CONSOLIDADAS)
# ======================================================================
# Ficheiro único para permitir edição via GUI
# Migrado de: automations/ (57) + packages/ (8)
# Data: $(date +%Y-%m-%d)
# Total: 65 automações
#
# 📝 ORGANIZAÇÃO:
#   🏊 Piscina - Geral (12)
#   🏊 Piscina - Packages (8) ← Extraídas de packages/piscina_*.yaml
#   🚪 Portões e Portarias (8)
#   🌡️ Clima (3)
#   💡 Iluminação (1)
#   ☀️ Energia Solar (1)
#   ⚙️ Sistema (31)
#
# ⚠️ AUTOMAÇÕES DE PACKAGES:
#   As 8 automações extraídas de packages/ mantêm dependências:
#   - input_boolean.piscina_*
#   - input_number.piscina_*
#   - binary_sensor.piscina_*
#   
#   📦 Packages mantidos (sem automation:):
#   - piscina_clorador_sal.yaml
#   - piscina_cloro_tpo.yaml
#   - piscina_cobertura.yaml
#   - piscina_ph.yaml
#
# 🔄 ROLLBACK:
#   Git tag: pre-consolidacao-total
#   Backup: automations_modular_backup_*, packages_backup_*
#   Ver: docs/ROLLBACK_AUTOMATIONS_COMPLETO.md
# ======================================================================

EOF

# 3.2 Função helper para adicionar categoria
add_category() {
  echo "" >> automations.yaml
  echo "# ======================================================================" >> automations.yaml
  echo "# $1" >> automations.yaml
  echo "# ======================================================================" >> automations.yaml
  echo "" >> automations.yaml
}

# 3.3 Adicionar automações dos PACKAGES primeiro
add_category "🏊 PISCINA - PACKAGES (8 automações)"
echo "# 📦 Extraídas de packages/ - Mantêm dependências com input_boolean, input_number, etc." >> automations.yaml
echo "# 🔗 Packages relacionados (sem automation:):" >> automations.yaml
echo "#    - piscina_clorador_sal.yaml (input_boolean × 2, input_number × 2)" >> automations.yaml
echo "#    - piscina_cloro_tpo.yaml (input_boolean × 1, input_number × 3)" >> automations.yaml
echo "#    - piscina_cobertura.yaml" >> automations.yaml
echo "#    - piscina_ph.yaml (input_number × 2, template × 1)" >> automations.yaml
echo "" >> automations.yaml
cat automations_from_packages.yaml >> automations.yaml

# 3.4 Adicionar automações de automations/
add_category "🏊 PISCINA - GERAL (12 automações)"
cat automations/piscina/piscina_geral.yaml >> automations.yaml

add_category "🏊 PISCINA - FILTRAGEM (1 automação)"
cat automations/piscina/piscina_filtragem.yaml >> automations.yaml

add_category "🏊 PISCINA - COBERTURA (1 automação - automations/)"
echo "# ⚠️ Diferente de piscina_cobertura em packages (LLM Vision)" >> automations.yaml
cat automations/piscina/piscina_cobertura.yaml >> automations.yaml

add_category "🚪 PORTÕES E PORTARIAS (8 automações)"
cat automations/portoes_portarias/portao_principal.yaml >> automations.yaml
cat automations/portoes_portarias/portao_botoes.yaml >> automations.yaml

add_category "🌡️ CLIMA (3 automações)"
cat automations/clima/aquecimento_arrefecimento.yaml >> automations.yaml
cat automations/clima/ventilacao.yaml >> automations.yaml

add_category "💡 ILUMINAÇÃO (1 automação)"
cat automations/iluminacao/luzes_exterior.yaml >> automations.yaml

add_category "☀️ ENERGIA SOLAR (1 automação)"
cat automations/energia_solar/paineis_solares.yaml >> automations.yaml

add_category "⚙️ SISTEMA (31 automações)"
cat automations/sistema/monitorizacao.yaml >> automations.yaml
cat automations/sistema/outros.yaml >> automations.yaml

# 3.5 Remover ficheiro temporário
rm automations_from_packages.yaml
```

---

### **Fase 4: Limpar Packages (Remover blocos `automation:`)** (5 min)

Para cada package, remover APENAS o bloco `automation:`, manter todo o resto.

**⚠️ IMPORTANTE:** Vou criar scripts para fazer isto de forma segura.

```bash
cd /data/homeassistant

# Backup adicional antes de modificar packages
for f in packages/piscina_*.yaml; do
  cp "$f" "$f.before_automation_removal"
done

# Remover blocos automation de cada package
# (Manter input_boolean, input_number, template, binary_sensor, sensor, etc.)

python3 << 'PYTHON_SCRIPT'
import yaml
import sys

packages = [
    'packages/piscina_clorador_sal.yaml',
    'packages/piscina_cloro_tpo.yaml',
    'packages/piscina_cobertura.yaml',
    'packages/piscina_ph.yaml'
]

for pkg_path in packages:
    print(f"Processando {pkg_path}...")
    
    with open(pkg_path, 'r') as f:
        content = f.read()
    
    # Parse YAML
    data = yaml.safe_load(content)
    
    # Remover chave 'automation' se existir
    if 'automation' in data:
        del data['automation']
        print(f"  ✓ Removido bloco 'automation'")
    
    # Guardar de volta (sem automation)
    with open(pkg_path, 'w') as f:
        # Manter comentários do cabeçalho
        lines = content.split('\n')
        for line in lines:
            if line.startswith('#'):
                f.write(line + '\n')
            else:
                break
        
        f.write('\n')
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"  ✓ Guardado sem 'automation'")

print("\n✅ Todos os packages limpos!")
PYTHON_SCRIPT
```

---

### **Fase 5: Atualizar configuration.yaml** (2 min)

```yaml
# ANTES:
automation: !include_dir_merge_list automations/

# DEPOIS:
automation: !include automations.yaml
```

---

### **Fase 6: Validar e Testar** (10 min)

```bash
# 6.1 Validar YAML
docker exec homeassistant python -c "
import yaml
with open('/config/automations.yaml') as f:
    data = yaml.safe_load(f)
    print(f'✅ YAML válido: {len(data)} automações')
"

# 6.2 Validar configuração completa
docker exec homeassistant ha core check

# 6.3 Contar automações no ficheiro
grep "^- id:" /data/homeassistant/automations.yaml | wc -l
# Deve dar 65

# 6.4 Reload automations (SEM restart)
docker exec homeassistant ha core reload automations

# 6.5 Verificar automações carregadas
docker exec homeassistant ha core states | grep "automation\." | wc -l
# Deve dar 65
```

---

### **Fase 7: Testar GUI** (5 min)

1. Abrir: `Configurações → Automações e Cenas`
2. Verificar que existem **65 automações**
3. Tentar **editar** uma automação de `automations/` (ex: Bomba Piscina Noite)
4. Tentar **editar** uma automação de `packages/` (ex: Piscina — Sal baixo)
5. Tentar **criar** uma nova automação simples
6. Tentar **apagar** a automação de teste
7. ✅ Se tudo funcionar → Sucesso!

---

### **Fase 8: Limpeza e Documentação** (10 min)

```bash
# 8.1 Renomear pastas antigas (não apagar ainda!)
mv /data/homeassistant/automations /data/homeassistant/automations_OLD_MODULAR_BACKUP

# 8.2 Adicionar comentário nos packages
for f in packages/piscina_clorador_sal.yaml \
         packages/piscina_cloro_tpo.yaml \
         packages/piscina_cobertura.yaml \
         packages/piscina_ph.yaml; do
  
  # Adicionar nota no topo
  sed -i '1i\
# ⚠️ NOTA: As automações deste package foram movidas para automations.yaml\
#    para permitir edição via GUI. Este ficheiro contém apenas:\
#    - input_boolean, input_number, template sensors, etc.\
#    Ver: automations.yaml (procurar por "# Fonte: '$(basename $f)'")\
' "$f"
done
```

---

### **Fase 9: Commit Git** (3 min)

```bash
cd /data/homeassistant

git add automations.yaml
git add configuration.yaml
git add packages/piscina_*.yaml
git rm -r automations/

git commit -m "♻️ Consolidação TOTAL: 65 automações num único ficheiro

## 🎯 Objetivo
Permitir edição completa via GUI (Configurações → Automações)

## 📊 Origem das Automações
- automations/ (estrutura modular): 57 automações
- packages/ (blocos automation:): 8 automações
- **TOTAL: 65 automações**

## 🔄 Alterações

### automations.yaml (NOVO)
- ✅ Criado ficheiro único com 65 automações (~3.112 linhas)
- ✅ Organizado por categorias com comentários delimitadores
- ✅ Automações de packages documentadas com dependências

### packages/piscina_*.yaml (MODIFICADOS)
- ✅ Removido bloco \`automation:\` de 4 packages
- ✅ Mantidos: input_boolean, input_number, template sensors
- ✅ Adicionado comentário explicativo no topo

### configuration.yaml
- ✅ Alterado: \`automation: !include automations.yaml\`

## 📦 Packages Afetados
1. piscina_clorador_sal.yaml (1 automação extraída)
2. piscina_cloro_tpo.yaml (2 automações extraídas)
3. piscina_cobertura.yaml (2 automações extraídas)
4. piscina_ph.yaml (3 automações extraídas)

## 💾 Backups
- Git tag: pre-consolidacao-total
- Pasta: automations_OLD_MODULAR_BACKUP/
- Pasta: packages_backup_*/
- Ficheiros: *.before_automation_removal

## ✅ GUI Funcional
- Criar novas automações: ✅
- Editar automações existentes: ✅
- Apagar automações: ✅
- Duplicar automações: ✅

## 🔄 Rollback
Ver: docs/ROLLBACK_AUTOMATIONS_COMPLETO.md
Tag Git: pre-consolidacao-total

## ✅ Validação
- check_config: PASSOU
- 65 automações carregadas
- GUI testado e funcional

Risco: BAIXO - Backup triplo + Git tag + documentação completa"
```

---

## ⚠️ RISCOS E MITIGAÇÕES ATUALIZADOS

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **Erro ao extrair automation de packages** | Média | Alto | Script Python validado, backup completo |
| **Quebrar dependências packages** | Baixa | Alto | Manter input_boolean, input_number, templates |
| **Automações não carregam** | Baixa | Alto | Git tag + 3 backups antes de começar |
| **Ficheiro muito grande (3.112 linhas)** | Alta | Baixo | Normal, GUI aguenta |
| **Perda de cohesão packages** | Alta | Médio | Documentar com comentários no automations.yaml |

---

## 📊 COMPARAÇÃO: Antes vs Depois (Atualizado)

| Aspecto | Estrutura Atual | Ficheiro Único |
|---------|-----------------|----------------|
| **Edição GUI** | ❌ SOMENTE LEITURA | ✅ COMPLETA (65 automações) |
| **Automations folder** | 57 automações (11 ficheiros) | 0 (pasta backup) |
| **Packages automation** | 8 automações (4 ficheiros) | 0 (extraídas) |
| **automations.yaml** | ❌ Não existe | ✅ 65 automações |
| **Cohesão packages** | ✅ Alta (automation com config) | ⚠️ Baixa (separados) |
| **Organização** | ✅ Pastas + Packages | ⚠️ Comentários |
| **Manutenção** | ⚠️ Múltiplos locais | ✅ Um único local |
| **Git diffs** | ✅ Por ficheiro | ⚠️ Ficheiro único |
| **Padrão HA** | ❌ Custom | ✅ Default |
| **Reversibilidade** | ✅ Git tag | ✅ Git tag |

---

## 🎯 RECOMENDAÇÃO FINAL ATUALIZADA

### ✅ **SIM, consolidar todas as 65 automações**

**Porque:**
1. ✅ GUI passa a funcionar 100% (todas as 65)
2. ✅ Um único local de gestão
3. ✅ Padrão do Home Assistant
4. ✅ Backups completos garantidos (triplo)
5. ✅ Reversível via Git tag
6. ✅ Packages mantêm funcionalidade (entidades preservadas)

**Trade-off:**
- ⚠️ Perda de cohesão em 4 packages (automações separadas das entidades)
- ✅ **Mitigação:** Documentação clara com comentários

---

## 📝 DOCUMENTAÇÃO ADICIONAL A CRIAR

### 1. `docs/ROLLBACK_AUTOMATIONS_COMPLETO.md`
- Como reverter consolidação
- Como restaurar automações para packages
- Comandos Git específicos

### 2. `docs/AUTOMATIONS_STRUCTURE.md`
- Mapa de automações por categoria
- Dependências de automações de packages
- Guia de troubleshooting

### 3. `automations_OLD_MODULAR_BACKUP/README.md`
- Estrutura original preservada
- Instruções de restauro
- Data e motivo do backup

---

## 🚀 TEMPO ESTIMADO

| Fase | Descrição | Tempo |
|------|-----------|-------|
| **1** | Backup (Git + cópias) | 5 min |
| **2** | Extrair automações packages | 10 min |
| **3** | Consolidação total | 15 min |
| **4** | Limpar packages | 5 min |
| **5** | Atualizar configuration.yaml | 2 min |
| **6** | Validar e testar | 10 min |
| **7** | Testar GUI | 5 min |
| **8** | Limpeza e documentação | 10 min |
| **9** | Commit Git | 3 min |
| **TOTAL** | | **~65 minutos** |

---

## ✅ APROVAÇÃO NECESSÁRIA

**Antes de prosseguir, confirma:**

1. ✅ Entendo que 8 automações serão extraídas de packages
2. ✅ Entendo que packages ficarão sem bloco `automation:`
3. ✅ Entendo que ficheiro terá ~3.112 linhas
4. ✅ Aceito o trade-off de cohesão vs GUI funcional
5. ✅ Tenho backups suficientes (Git tag + cópias)

---

**Estás pronto para avançar?** 🚀

Responde:
- **"Sim, executar plano completo"** - Executo as 9 fases automaticamente
- **"Sim, fase a fase"** - Executo e espero aprovação em cada fase
- **"Mostrar exemplo"** - Mostro como ficará o automations.yaml
- **"Esclarecer X"** - Explico melhor algum ponto
