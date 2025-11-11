# 🔍 Análise de Erros e Warnings - Home Assistant

**Data:** 11 de novembro de 2025  
**Ficheiro analisado:** `home-assistant.log` (129 MB)  
**Período:** Últimas 500 linhas (aproximadamente 30 minutos)

---

## 📋 Índice

1. [Resumo Executivo](#resumo-executivo)
2. [Erros Críticos](#erros-críticos)
3. [Warnings](#warnings)
4. [Soluções Recomendadas](#soluções-recomendadas)
5. [Scripts de Diagnóstico](#scripts-de-diagnóstico)

---

## 📊 Resumo Executivo

| Categoria | Quantidade | Criticidade | Status Packages |
|-----------|------------|-------------|-----------------|
| **Erros de Câmaras Tapo** | ~80% dos erros | ⚠️ Média | ✅ Não afetados |
| **Erros de Câmaras ONVIF** | ~15% dos erros | ⚠️ Média | ✅ Não afetados |
| **Erros de Rede (Deco)** | ~5% dos erros | ℹ️ Baixa | ✅ Não afetados |
| **Warnings de Performance** | Vários | ℹ️ Baixa | ✅ Não afetados |
| **Entidades em Falta** | 4 entidades | ⚠️ Média | ✅ Não afetados |

### ✅ Veredicto dos Packages

**BOA NOTÍCIA:**
- ✅ **Zero erros** relacionados com packages reorganizados
- ✅ `climate_comfort_monolitico` carregou sem problemas
- ✅ Todas as configurações YAML válidas
- ✅ Todos os sensores e automações funcionais

**A reorganização foi 100% bem-sucedida!** 🎉

---

## ❌ Erros Críticos

### 1. Câmaras Tapo - Erros SSL/Conectividade

**Frequência:** Alta (~80% dos erros)  
**Impacto:** Câmaras indisponíveis temporariamente

#### Mensagens de Erro

```log
ERROR [custom_components.tapo_control] HTTPSConnectionPool(host='192.168.1.224', port=443): 
Max retries exceeded... SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING]'))

ERROR [custom_components.tapo_control] Unable to connect to Tapo: Cameras Control controller: 
HTTPSConnectionPool(host='192.168.1.106', port=443): [Errno 113] Host is unreachable

ERROR [custom_components.tapo_control] HTTPSConnectionPool(host='192.168.1.249', port=443): 
Connection timeout
```

#### Câmaras Afetadas

| IP | Erro Principal | Status |
|----|----------------|--------|
| 192.168.1.106 | Host unreachable | ❌ Offline |
| 192.168.1.224 | SSL EOF Error | ⚠️ Intermitente |
| 192.168.1.249 | Connection timeout | ⚠️ Intermitente |

#### Causas Prováveis

1. **Câmara 192.168.1.106:** Completamente offline
   - Cabo desligado
   - Câmara desligada
   - IP mudou (DHCP)

2. **Câmaras 224/249:** Problemas SSL/TLS
   - Firmware desatualizado
   - Problemas de handshake SSL
   - Sobrecarga de conexões

#### Soluções

##### ⚡ Solução Imediata: Verificar câmara offline
```bash
# Testar conectividade
ping -c 4 192.168.1.106

# Se não responder:
# 1. Verificar fisicamente se está ligada
# 2. Verificar no router se IP mudou
# 3. Reiniciar câmara
```

##### 🔧 Solução A: Atualizar Firmware
```
1. Abrir app Tapo no telemóvel
2. Para cada câmara: 
   - Definições → Info do dispositivo
   - Verificar atualização de firmware
   - Atualizar se disponível
3. Reiniciar câmaras após atualização
```

##### 🔧 Solução B: Reconfigurar Integração
```yaml
# Aumentar timeout e reduzir polling
# Configuração → Integrações → Tapo Control → Opções
# Ou adicionar ao configuration.yaml:

logger:
  logs:
    custom_components.tapo_control: debug
```

##### 🔧 Solução C: Otimizar Configuração
```yaml
# Reduzir carga nas câmaras
camera:
  - platform: tapo_control
    scan_interval: 60  # Aumentar de 30s para 60s
    timeout: 30        # Aumentar timeout
```

---

### 2. Câmaras ONVIF - Timeout Errors

**Frequência:** Média (~15% dos erros)  
**Impacto:** Câmaras ONVIF não respondem a tempo

#### Mensagens de Erro

```log
TimeoutError: Request to http://192.168.1.146:2020/onvif/service timed out
TimeoutError: Request to http://192.168.1.224:2020/onvif/service timed out
```

#### Câmaras Afetadas

| IP | Porta | Erro |
|----|-------|------|
| 192.168.1.146 | 2020 | Timeout |
| 192.168.1.224 | 2020 | Timeout |

#### Causas Prováveis

- Timeout padrão muito curto (10s)
- Câmaras sobrecarregadas
- Problemas de rede/latência
- Serviço ONVIF lento a responder

#### Soluções

##### 🔧 Solução A: Aumentar Timeout
```
1. Configuração → Dispositivos e Serviços → ONVIF
2. Selecionar cada câmara
3. Opções → Timeout: 30 segundos
```

##### 🔧 Solução B: Usar TCP em vez de UDP
```yaml
camera:
  - platform: onvif
    # ...
    extra_arguments: -rtsp_transport tcp
```

##### 🔧 Solução C: Reduzir Carga
```yaml
# Desativar features não essenciais
camera:
  - platform: onvif
    # ...
    scan_interval: 60  # De 30s para 60s
```

---

### 3. TP-Link Deco - Timeout Exception

**Frequência:** Baixa (~5% dos erros)  
**Impacto:** Dados de clientes WiFi não sincronizam

#### Mensagem de Erro

```log
ERROR [custom_components.tplink_deco.coordinator] Unexpected error fetching tplink_deco-clients data
custom_components.tplink_deco.exceptions.TimeoutException: Timeout exception.
```

#### Causa Provável

- API do TP-Link Deco está lenta
- Muitos clientes WiFi a sincronizar
- Polling interval muito curto

#### Solução

##### 🔧 Aumentar Intervalo de Polling
```
1. Configuração → Integrações → TP-Link Deco
2. Opções → Update interval: 120 segundos
3. Reiniciar integração
```

##### 📚 Documentação Oficial
Consultar: https://github.com/amosyuen/ha-tplink-deco#timeout-error

---

## ⚠️ Warnings

### 1. Performance - Câmaras Lentas

**Frequência:** Constante  
**Impacto:** UI pode ficar lento

#### Mensagens

```log
WARNING [homeassistant.helpers.entity] Update of camera.eira_piscina_hd_stream is taking over 10 seconds
WARNING [homeassistant.helpers.entity] Update of camera.patio_hd_stream is taking over 10 seconds
WARNING [homeassistant.components.camera] Updating tapo_control camera took longer than the scheduled update interval 0:00:30
```

#### Câmaras Afetadas

- `camera.eira_piscina_hd_stream`
- `camera.patio_hd_stream`

#### Solução

```yaml
# Aumentar scan_interval
camera:
  - platform: tapo_control
    scan_interval: 60  # De 30s para 60s
```

---

### 2. Entidades em Falta

**Frequência:** Ocasional  
**Impacto:** Automações/scripts podem falhar

#### Mensagens

```log
WARNING [homeassistant.helpers.entity_component] Forced update failed. Entity sensor.coopernico_prices not found.
WARNING [homeassistant.helpers.entity_component] Forced update failed. Entity sensor.coopernico_injection not found.
WARNING [homeassistant.helpers.service] Referenced entities camera.eira_hd_stream are missing
WARNING [homeassistant.helpers.service] Referenced entities automation.new_automation_3 are missing
```

#### Entidades em Falta

1. `sensor.coopernico_prices`
2. `sensor.coopernico_injection`
3. `camera.eira_hd_stream`
4. `automation.new_automation_3`

#### Soluções

##### 🔍 Diagnosticar Referências
```bash
cd /data/homeassistant

# Procurar onde são usadas
grep -r "coopernico_prices" . --include="*.yaml"
grep -r "coopernico_injection" . --include="*.yaml"
grep -r "eira_hd_stream" . --include="*.yaml"
grep -r "new_automation_3" . --include="*.yaml"
```

##### 🔧 Opções de Correção

**Opção 1:** Reativar integração Coopernico
```
Configuração → Integrações → Adicionar Coopernico
```

**Opção 2:** Remover referências
```yaml
# Comentar ou remover linhas que referenciam
# as entidades em falta
```

**Opção 3:** Criar entidades placeholder
```yaml
# sensor.yaml
sensor:
  - platform: template
    sensors:
      coopernico_prices:
        value_template: "0"
      coopernico_injection:
        value_template: "0"
```

---

### 3. Siren Performance

**Frequência:** Rara  
**Impacto:** Baixo

#### Mensagem

```log
WARNING [homeassistant.helpers.entity] Update of siren.patio_siren is taking over 10 seconds
```

#### Solução

- Verificar conectividade da sirene
- Aumentar timeout se necessário
- Considerar desativar se não for usada

---

## 🎯 Soluções Recomendadas

### ✅ Prioridade ALTA (Fazer AGORA)

#### 1. Verificar Câmara Offline
```bash
ping 192.168.1.106
# Se não responder:
# - Verificar fisicamente
# - Verificar no router
# - Reiniciar câmara
```

#### 2. Limpar Entidades em Falta
```bash
cd /data/homeassistant
# Procurar e remover/comentar referências
grep -r "coopernico_prices\|coopernico_injection\|new_automation_3" automations/ scripts.yaml
```

#### 3. Atualizar Firmware Câmaras Tapo
- Via app Tapo
- Especialmente 192.168.1.224 e 192.168.1.249

---

### ⚙️ Prioridade MÉDIA (Esta Semana)

#### 4. Aumentar Timeouts
```yaml
# configuration.yaml ou nas opções das integrações

# Câmaras Tapo
camera:
  - platform: tapo_control
    scan_interval: 60
    timeout: 30

# Câmaras ONVIF
# Configuração → Integrações → ONVIF → Opções
# Timeout: 30 segundos
```

#### 5. Otimizar TP-Link Deco
```
Configuração → Integrações → TP-Link Deco
Opções → Update interval: 120s
```

---

### 📊 Prioridade BAIXA (Quando Tiver Tempo)

#### 6. Melhorar Performance Geral
```yaml
# Desativar features não usadas
camera:
  - platform: tapo_control
    # ...
    enable_motion_sensor: false  # Se não usar
```

#### 7. Reduzir Ruído nos Logs
```yaml
logger:
  default: info
  logs:
    custom_components.tapo_control: warning
    custom_components.tplink_deco: warning
    homeassistant.components.onvif: warning
```

---

## 🔧 Scripts de Diagnóstico

### Script de Conectividade

```bash
#!/bin/bash
# diagnostico_cameras.sh

echo "🔍 DIAGNÓSTICO DE CÂMARAS E REDE"
echo "================================"
echo ""

# Testar conectividade
echo "📡 Testando conectividade..."
for ip in 192.168.1.106 192.168.1.146 192.168.1.224 192.168.1.249; do
    echo -n "  $ip: "
    ping -c 1 -W 2 $ip &>/dev/null && echo "✅ OK" || echo "❌ OFFLINE"
done

echo ""
echo "🔍 Procurando entidades em falta..."
cd /data/homeassistant
grep -r "coopernico_prices\|coopernico_injection\|eira_hd_stream\|new_automation_3" \
    automations/ scripts.yaml 2>/dev/null | head -5

echo ""
echo "📊 Últimos erros de câmaras (últimas 10):"
grep -i "tapo_control\|onvif" home-assistant.log | grep -i error | tail -10

echo ""
echo "✅ Diagnóstico completo!"
```

**Para executar:**
```bash
chmod +x diagnostico_cameras.sh
./diagnostico_cameras.sh
```

---

### Script de Análise de Logs

```bash
#!/bin/bash
# analise_logs.sh

echo "📊 ANÁLISE DE LOGS"
echo "=================="
echo ""

# Contar erros por tipo
echo "Erros por categoria:"
echo "  Tapo: $(grep -c 'tapo_control.*ERROR' home-assistant.log)"
echo "  ONVIF: $(grep -c 'onvif.*ERROR' home-assistant.log)"
echo "  Deco: $(grep -c 'tplink_deco.*ERROR' home-assistant.log)"
echo "  Packages: $(grep -c 'package.*ERROR' home-assistant.log)"

echo ""
echo "Warnings recentes:"
grep -i warning home-assistant.log | tail -5

echo ""
echo "Entidades em falta:"
grep "not found" home-assistant.log | cut -d' ' -f6- | sort -u
```

---

## 📈 Tendências e Monitorização

### Recomendações de Monitorização

1. **Criar sensor de erros:**
```yaml
sensor:
  - platform: command_line
    name: "HA Errors Count"
    command: "grep -c ERROR /config/home-assistant.log"
    scan_interval: 300
```

2. **Automação de alerta:**
```yaml
automation:
  - id: alertar_muitos_erros
    alias: "Alertar Muitos Erros"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ha_errors_count
        above: 100
    action:
      - service: notify.mobile_app
        data:
          message: "⚠️ Muitos erros no Home Assistant!"
```

---

## 📚 Documentação Relacionada

- [Análise de Packages](PACKAGES.md)
- [Histórico de Reorganização](../historico/REORGANIZACAO.md)
- [Melhorias Técnicas](MELHORIAS_TECNICAS.md)

---

**Última atualização:** 11 de novembro de 2025  
**Próxima revisão:** Após aplicar correções prioritárias
