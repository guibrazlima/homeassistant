#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# SCRIPT DE VALIDAÇÃO - OTIMIZAÇÕES PISCINA SOLAR
# ═══════════════════════════════════════════════════════════════════
#
# Verifica se todas as otimizações estão funcionando corretamente
#
# Uso: ./scripts/validate_piscina_optimizations.sh
#
# ═══════════════════════════════════════════════════════════════════

# NÃO usar set -e para continuar em caso de erro
set +e

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🏊 VALIDAÇÃO: OTIMIZAÇÕES PISCINA SOLAR v2.1                ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Contador
PASS=0
FAIL=0
WARN=0

# ───────────────────────────────────────────────────────────────────
# TESTE 1: Ficheiros Existem
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[1/10]${NC} Verificando ficheiros criados..."

FILES=(
    "sensors/solar_smoothed.yaml"
    "sensors/house_consumption_weekday.yaml"
    "sensors/piscina_weather_adjustment.yaml"
    "packages/piscina_solar_optimization.yaml"
    "automations/piscina_solar_notifications.yaml"
    "lovelace/piscina_solar_dashboard.yaml"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
        ((PASS++))
    else
        echo -e "  ${RED}✗${NC} $file ${RED}(FALTA!)${NC}"
        ((FAIL++))
    fi
done
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTE 2: Configuration.yaml tem packages
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[2/10]${NC} Verificando configuration.yaml..."

if grep -q "packages:" configuration.yaml; then
    echo -e "  ${GREEN}✓${NC} Packages configurado"
    ((PASS++))
else
    echo -e "  ${YELLOW}⚠${NC} Packages não encontrado (pode estar OK se via UI)"
    ((WARN++))
fi
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTE 3: Sensores Registados
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[3/10]${NC} Verificando sensores registados..."

SENSORS=(
    "sensor.solar_power_5min_smooth"
    "sensor.house_power_5min_smooth"
    "sensor.solar_stability_indicator"
    "sensor.house_consumption_weekday_factor"
    "sensor.piscina_weather_delay_multiplier"
)

for sensor in "${SENSORS[@]}"; do
    if grep -q "$sensor" .storage/core.entity_registry 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $sensor"
        ((PASS++))
    else
        echo -e "  ${YELLOW}⚠${NC} $sensor ${YELLOW}(aguardar restart)${NC}"
        ((WARN++))
    fi
done
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTE 4: Input Helpers
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[4/10]${NC} Verificando input helpers..."

INPUTS=(
    "input_number.piscina_weekend_consumption_factor"
    "input_boolean.piscina_use_weather_forecast"
    "input_select.piscina_notification_level"
)

for input in "${INPUTS[@]}"; do
    if grep -q "$input" .storage/core.entity_registry 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $input"
        ((PASS++))
    else
        echo -e "  ${YELLOW}⚠${NC} $input ${YELLOW}(aguardar restart)${NC}"
        ((WARN++))
    fi
done
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTE 5: Automações Carregadas
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[5/10]${NC} Verificando automações..."

AUTOMATIONS=(
    "automation.piscina_solar_alert_high_import"
    "automation.piscina_solar_alert_low_time"
    "automation.piscina_solar_info_high_excess"
    "automation.piscina_solar_info_unstable"
)

for auto in "${AUTOMATIONS[@]}"; do
    if grep -q "$auto" .storage/core.entity_registry 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $auto"
        ((PASS++))
    else
        echo -e "  ${YELLOW}⚠${NC} $auto ${YELLOW}(aguardar restart)${NC}"
        ((WARN++))
    fi
done
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTE 6: Logs Sem Erros Críticos
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[6/10]${NC} Verificando logs recentes..."

ERRORS=$(tail -100 home-assistant.log | grep -i "error" | grep -i "solar_smoothed\|weekday\|weather_adjustment\|piscina_solar_optimization" | wc -l)

if [ "$ERRORS" -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} Sem erros nos novos componentes"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} $ERRORS erros encontrados!"
    tail -100 home-assistant.log | grep -i "error" | grep -i "solar_smoothed\|weekday\|weather_adjustment\|piscina_solar_optimization" | head -3
    ((FAIL++))
fi
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTE 7: Sensores com Dados (se HA rodando)
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[7/10]${NC} Verificando se sensores têm dados..."

if docker ps | grep -q homeassistant; then
    # Aguardar 5s
    sleep 5
    
    # Verificar sensor solar_power_5min_smooth
    STATE=$(curl -s http://localhost:8123/api/states/sensor.solar_power_5min_smooth 2>/dev/null | grep -o '"state":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$STATE" ] && [ "$STATE" != "unknown" ] && [ "$STATE" != "unavailable" ]; then
        echo -e "  ${GREEN}✓${NC} Sensores com dados (${STATE}W)"
        ((PASS++))
    else
        echo -e "  ${YELLOW}⚠${NC} Sensores ainda sem dados (aguardar 5-10min)"
        ((WARN++))
    fi
else
    echo -e "  ${YELLOW}⚠${NC} HA não está rodando, não é possível verificar"
    ((WARN++))
fi
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTE 8: Dashboard Acessível
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[8/10]${NC} Verificando dashboard..."

if [ -f "lovelace/piscina_solar_dashboard.yaml" ]; then
    SIZE=$(wc -l < lovelace/piscina_solar_dashboard.yaml)
    if [ "$SIZE" -gt 100 ]; then
        echo -e "  ${GREEN}✓${NC} Dashboard criado ($SIZE linhas)"
        ((PASS++))
    else
        echo -e "  ${RED}✗${NC} Dashboard muito pequeno?"
        ((FAIL++))
    fi
else
    echo -e "  ${RED}✗${NC} Dashboard não encontrado"
    ((FAIL++))
fi
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTE 9: Integrações HACS (opcional)
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[9/10]${NC} Verificando integrações HACS..."

HACS_INTEGRATIONS=(
    "www/community/lovelace-mushroom"
    "www/community/apexcharts-card"
    "www/community/button-card"
    "www/community/power-flow-card-plus"
    "www/community/mini-graph-card"
)

HACS_FOUND=0
for integration in "${HACS_INTEGRATIONS[@]}"; do
    if [ -d "$integration" ]; then
        ((HACS_FOUND++))
    fi
done

if [ "$HACS_FOUND" -eq 5 ]; then
    echo -e "  ${GREEN}✓${NC} Todas as integrações HACS instaladas (5/5)"
    ((PASS++))
elif [ "$HACS_FOUND" -gt 0 ]; then
    echo -e "  ${YELLOW}⚠${NC} Algumas integrações HACS faltam ($HACS_FOUND/5)"
    ((WARN++))
else
    echo -e "  ${YELLOW}⚠${NC} Integrações HACS não encontradas (dashboard pode não funcionar)"
    ((WARN++))
fi
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTE 10: Git Status
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}[10/10]${NC} Verificando git status..."

if git status | grep -q "nothing to commit"; then
    echo -e "  ${GREEN}✓${NC} Tudo commitado"
    ((PASS++))
else
    echo -e "  ${YELLOW}⚠${NC} Há alterações pendentes"
    ((WARN++))
fi
echo ""

# ───────────────────────────────────────────────────────────────────
# RESUMO
# ───────────────────────────────────────────────────────────────────
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  📊 RESUMO DA VALIDAÇÃO                                       ║${NC}"
echo -e "${BLUE}╠═══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║  ${GREEN}✓ PASS:    $PASS${NC}                                                   ${BLUE}║${NC}"
echo -e "${BLUE}║  ${RED}✗ FAIL:    $FAIL${NC}                                                   ${BLUE}║${NC}"
echo -e "${BLUE}║  ${YELLOW}⚠ WARNING: $WARN${NC}                                                   ${BLUE}║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Status final
if [ "$FAIL" -eq 0 ] && [ "$WARN" -le 5 ]; then
    echo -e "${GREEN}✅ VALIDAÇÃO PASSOU!${NC}"
    echo -e "Sistema pronto para uso. Aguardar 5-10min para sensores terem dados."
    exit 0
elif [ "$FAIL" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  VALIDAÇÃO PASSOU COM AVISOS${NC}"
    echo -e "Sistema provavelmente OK, mas verificar warnings acima."
    exit 0
else
    echo -e "${RED}❌ VALIDAÇÃO FALHOU!${NC}"
    echo -e "Corrigir erros acima antes de continuar."
    exit 1
fi
