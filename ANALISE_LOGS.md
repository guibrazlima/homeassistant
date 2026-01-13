# 🔍 Análise de Logs - Home Assistant

**Data:** 2026-01-13 15:30  
**Branch:** reorganizacao-homeassistant  
**Período analisado:** Últimas 1000 linhas de log

---

## 📊 Resumo de Problemas Encontrados

### 🔴 Problemas CRÍTICOS (necessitam correção)

#### 1. Automação Inexistente: `automation.new_automation_3`
**Severidade:** 🔴 Alta  
**Frequência:** Múltiplas vezes por minuto  
**Impacto:** Automações que dependem dela não funcionam corretamente

**Localização:**
- `automations/piscina/piscina_geral.yaml` (linhas 193, 214, 226, 232, 276)
- `automations/sistema/outros.yaml` (linhas 125, 151, 160)
- `automations/veiculo_eletrico/ev_carregamento.yaml` (linha 190)

**Causa:**
A automação "Bomba Piscina Dia" usa um blueprint PVExcessControl com `automation_id: automation.new_automation_3`, mas o ID real da automação é `automation.bomba_piscina_dia`.

**Solução:**
```yaml
# ANTES (ERRADO):
automation_id: automation.new_automation_3

# DEPOIS (CORRETO):
automation_id: automation.bomba_piscina_dia
```

---

#### 2. Sensores Coopernico Não Encontrados
**Severidade:** 🟡 Média  
**Frequência:** A cada 5 minutos  
**Impacto:** Dados de preços de energia não disponíveis

**Entidades afetadas:**
- `sensor.coopernico_prices`
- `sensor.coopernico_injection`

**Possíveis causas:**
- Integração Coopernico desativada ou com erro de configuração
- API da Coopernico offline ou com problemas de autenticação
- Sensores foram renomeados mas referências antigas permanecem

**Ações recomendadas:**
1. Verificar configuração da integração Coopernico
2. Procurar referências a estes sensores e atualizar ou remover
3. Considerar desabilitar forced_update se sensores não existem

---

#### 3. Câmera Inexistente: `camera.eira_hd_stream`
**Severidade:** 🟡 Média  
**Frequência:** A cada 5 minutos  
**Impacto:** Automações de análise de imagem podem falhar

**Possíveis causas:**
- Câmera offline ou desligada
- Nome da câmera mudou
- Câmera foi removida mas automações ainda referenciam

**Ações recomendadas:**
1. Verificar se câmera existe: Developer Tools → States → procurar "eira"
2. Corrigir referências se nome mudou
3. Desabilitar automações se câmera foi removida

---

### 🟡 Problemas de PERFORMANCE

#### 4. AdGuard Home - Lentidão nos Sensores
**Severidade:** 🟡 Média  
**Frequência:** Regular  
**Impacto:** Updates demoram >10 segundos

**Sensores afetados:**
- `sensor.adguard_home_consultas_de_dns_bloqueadas`
- `sensor.adguard_home_racio_de_consultas_dns_bloqueadas`
- `sensor.adguard_home_controlo_parental_bloqueado`
- `sensor.adguard_home_pesquisa_segura_bloqueada`
- `sensor.adguard_home_velocidade_media_de_processamento`

**Causa provável:**
- API do AdGuard Home lenta
- Intervalo de scan muito agressivo
- Rede com latência alta

**Soluções:**
1. Aumentar `scan_interval` da integração AdGuard
2. Verificar conectividade com servidor AdGuard
3. Considerar desabilitar sensores menos críticos

---

### 🔵 Problemas MENORES (não críticos)

#### 5. Câmera Tapo Não Alcançável
**Severidade:** 🔵 Baixa  
**Frequência:** Ocasional  
**Impacto:** Stream de vídeo indisponível temporariamente

**Dispositivo:** `192.168.1.106` (Tapo Camera)

**Causa:** Host não alcançável na rede

**Ações:**
- Verificar se dispositivo está online
- Verificar configuração de rede
- Normal se câmera for móvel/temporária

---

#### 6. Shelly "Luz Churrasco" - Erro de Dados
**Severidade:** 🔵 Baixa  
**Frequência:** Ocasional  
**Impacto:** Dados do dispositivo temporariamente indisponíveis

**Ações:**
- Verificar conectividade Wi-Fi do Shelly
- Atualizar firmware se disponível
- Normal se dispositivo for exterior (pode ter interferências)

---

#### 7. Stream de Câmera Terminado
**Severidade:** 🔵 Baixa  
**Frequência:** Ocasional  
**Dispositivo:** `camera.sala_hd_stream`

**Causa:** Stream de vídeo encerrado (normal)

**Ação:** Nenhuma - comportamento normal quando stream para

---

## 🛠️ Plano de Ação Prioritário

### 1️⃣ URGENTE - Corrigir automation.new_automation_3
```bash
# Substituir em todos os ficheiros:
find automations/ -name "*.yaml" -exec sed -i 's/automation\.new_automation_3/automation.bomba_piscina_dia/g' {} \;
```

### 2️⃣ IMPORTANTE - Resolver sensores Coopernico
- Verificar Developer Tools → Integrations
- Procurar "Coopernico" e verificar status
- Remover referências se integração não existe mais

### 3️⃣ RECOMENDADO - Otimizar AdGuard Home
- Aumentar scan_interval para 300s (5 min)
- Desabilitar sensores não utilizados

### 4️⃣ OPCIONAL - Verificar câmeras
- Confirmar status de camera.eira_hd_stream
- Verificar conectividade da Tapo (192.168.1.106)

---

## 📈 Estatísticas

**Total de problemas identificados:** 7  
**Críticos:** 1 (automation.new_automation_3)  
**Importantes:** 2 (sensores Coopernico, câmera)  
**Performance:** 1 (AdGuard Home)  
**Menores:** 3 (Tapo, Shelly, stream)

---

## ✅ Próximos Passos

1. **Corrigir referências** de `automation.new_automation_3` → `automation.bomba_piscina_dia`
2. **Verificar integrações** inexistentes (Coopernico)
3. **Testar** após correções
4. **Commit** das correções no branch `reorganizacao-homeassistant`

---

**📝 Nota:** Análise baseada nos logs das últimas ~2 horas de funcionamento.
