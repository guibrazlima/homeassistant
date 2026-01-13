# 📋 PLANO DE SUBDIVISÃO: climate_comfort_monolitico.yaml

## 🎯 Objetivo
Subdividir `climate_comfort_monolitico.yaml` (1.139 linhas) em ficheiros modulares por divisão.

## 📊 Situação Atual
- **Ficheiro único:** `packages/climate_comfort_monolitico.yaml`
- **Tamanho:** 1.139 linhas, ~51 KB
- **Divisões:** 5 (Sala Inferior, Cave, Cozinha, Quarto Luisa, Quarto)
- **Sensores por divisão:** 8-9 sensores

## 🏗️ Estrutura Proposta

```
packages/clima/
  ├── README.md                   # Documentação da estrutura
  ├── sala_inferior.yaml          # 9 sensores (~230 linhas)
  ├── cave.yaml                   # 9 sensores (~230 linhas)
  ├── cozinha.yaml                # 9 sensores (~230 linhas)
  ├── quarto_luisa.yaml           # 9 sensores (~230 linhas)
  └── quarto.yaml                 # 9 sensores (~230 linhas)
```

## 📝 Mapeamento de Sensores

### Sala Inferior
**Sensores BTHome:** `sensor.bthome_sensor_4ee3_{temperature,humidity}`
**Sensores calculados:**
- Ponto de orvalho
- Humidade absoluta
- Margem de condensação
- Comfort score
- Heat Index
- Humidex
- WBGT (sombra)
- Enthalpia

### Cave
**Sensores BTHome:** `sensor.bthome_sensor_25e6_{temperature,humidity}`
(mesmos 8 sensores calculados)

### Cozinha
**Sensores BTHome:** `sensor.bthome_sensor_508c_{temperature,humidity}`
(mesmos 8 sensores calculados)

### Quarto Luisa
**Sensores BTHome:** `sensor.bthome_sensor_abf1_{temperature,humidity}`
(mesmos 8 sensores calculados)

### Quarto
**Sensores BTHome:** `sensor.bthome_sensor_0b29_{temperature,humidity}`
(mesmos 8 sensores calculados)

## 🔧 Passos de Implementação

### **Passo 1: Preparação** (FEITO ✅)
- [x] Analisar estrutura atual
- [x] Identificar divisões e sensores
- [x] Criar plano de migração
- [x] Documentar em `docs/ANALISE_CLIMATE_COMFORT.md`

### **Passo 2: Backup** (PENDENTE)
```bash
# Criar backup do ficheiro original
cp packages/climate_comfort_monolitico.yaml \
   packages/climate_comfort_monolitico.yaml.BACKUP_2026-01-13
```

### **Passo 3: Criar Estrutura** (PENDENTE)
```bash
# Criar diretório
mkdir -p packages/clima/

# Criar ficheiros vazios
touch packages/clima/{sala_inferior,cave,cozinha,quarto_luisa,quarto}.yaml
touch packages/clima/README.md
```

### **Passo 4: Extrair Conteúdo** (PENDENTE)
Para cada divisão:
1. Extrair linhas correspondentes do monolítico
2. Criar cabeçalho com metadata
3. Adicionar sensores extraídos
4. Validar sintaxe YAML

**Exemplo (Sala Inferior):**
```yaml
#############################################
# 📦 Package: Clima - Sala Inferior
# 🎯 Objetivo: Sensores de conforto térmico da Sala Inferior
# 📂 Localização: /config/packages/clima/sala_inferior.yaml
# 🔗 Dependências:
#    - sensor.bthome_sensor_4ee3_temperature
#    - sensor.bthome_sensor_4ee3_humidity
# 📅 Migrado de: climate_comfort_monolitico.yaml (2026-01-13)
#############################################

template:
  - sensor:
      - name: "Sala Inferior - Ponto de orvalho"
        unique_id: sala_inferior_ponto_de_orvalho
        # ... (conteúdo extraído)
```

### **Passo 5: Atualizar configuration.yaml** (PENDENTE)
```yaml
# ANTES:
homeassistant:
  packages:
    climate_comfort: !include packages/climate_comfort_monolitico.yaml

# DEPOIS:
homeassistant:
  packages:
    clima: !include_dir_merge_named packages/clima/
```

### **Passo 6: Validar** (PENDENTE)
```bash
# Validar configuração
docker exec homeassistant python -m homeassistant --script check_config -c /config

# Verificar se todos os sensores foram criados
docker exec homeassistant ha core states | grep -E "(sala_inferior|cave|cozinha|quarto)"
```

### **Passo 7: Testar** (PENDENTE)
1. Reiniciar Home Assistant
2. Verificar se todos os 58 sensores estão disponíveis
3. Comparar valores com versão anterior (se possível)
4. Verificar dashboards/automações que usam estes sensores

### **Passo 8: Desativar Monolítico** (PENDENTE)
```yaml
# configuration.yaml - comentar o monolítico
homeassistant:
  packages:
    # climate_comfort: !include packages/climate_comfort_monolitico.yaml  # MIGRADO para clima/
    clima: !include_dir_merge_named packages/clima/
```

### **Passo 9: Commit** (PENDENTE)
```bash
git add packages/clima/
git add configuration.yaml
git commit -m "♻️ Refactor: Subdividir climate_comfort_monolitico em packages/clima/

- Dividir 1.139 linhas em 5 ficheiros modulares (~230 linhas cada)
- Melhora manutenibilidade por divisão
- Mantém todos os 58 sensores de conforto térmico
- Ficheiro original mantido como .BACKUP_2026-01-13

Divisões:
  - Sala Inferior (9 sensores)
  - Cave (9 sensores)
  - Cozinha (9 sensores)
  - Quarto Luisa (9 sensores)
  - Quarto (9 sensores)

Testado: ✅ check_config passou
Risco: MÉDIO - Validar valores após restart"
```

## ⚠️ RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **Erro de extração** | Média | Alto | Usar script automatizado, validar sintaxe |
| **Sensores não criados** | Baixa | Alto | Validar com `check_config` antes de restart |
| **Dashboards quebrados** | Baixa | Médio | IDs/nomes mantidos iguais |
| **Automações quebradas** | Baixa | Médio | IDs/nomes mantidos iguais |
| **Valores diferentes** | Muito Baixa | Baixo | Fórmulas mantidas idênticas |

## 🎁 Benefícios

✅ **Manutenção:** Editar sensores por divisão  
✅ **Clareza:** Ficheiros de ~230 linhas vs 1.139  
✅ **Git:** Diffs mais limpos, menos conflitos  
✅ **Performance:** Nenhum impacto (mesmo número de sensores)  
✅ **Escalabilidade:** Fácil adicionar novas divisões  

## 📚 Alternativa: Custom Component

**⚠️ IMPORTANTE:** Antes de implementar a subdivisão manual, considerar:

### Avaliar `thermal_comfort` custom component
- **Já instalado:** `custom_components/thermal_comfort/`
- **Documentação:** https://github.com/dolezsa/thermal_comfort
- **Potencial:** Reduzir 58 sensores para ~15-20 (component calcula automaticamente)

### Teste Recomendado
1. Configurar component para uma divisão (ex: Cave)
2. Comparar valores com sensores atuais
3. Se 80%+ das métricas estiverem corretas:
   - Migrar para component ✅
   - Manter apenas sensores custom (Comfort Score, Margem Condensação)
4. Se <80% corretas:
   - Proceder com subdivisão manual (este plano)

## 🚀 Status Atual

- [x] **Análise completa** - Estrutura documentada
- [x] **Plano criado** - Este ficheiro
- [ ] **Decisão:** Subdivisão manual OU custom component?
- [ ] **Implementação:** Aguarda decisão
- [ ] **Validação:** Após implementação
- [ ] **Commit:** Após validação

## 📅 Timeline Estimado

| Fase | Tempo | Status |
|------|-------|--------|
| Análise | 30 min | ✅ FEITO |
| Decisão (manual vs component) | 15 min | ⏳ PENDENTE |
| Implementação manual | 45 min | ⏳ PENDENTE |
| Validação + Testes | 30 min | ⏳ PENDENTE |
| **TOTAL** | **2 horas** | ⏳ PENDENTE |

---

**Última atualização:** 2026-01-13  
**Decisão necessária:** Subdivisão manual OU migração para custom component?
