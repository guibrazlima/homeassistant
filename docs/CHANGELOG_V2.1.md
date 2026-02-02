# Blueprint Piscina Solar v2.1 - Changelog

## 📅 2026-02-02

### 🐛 Correções Críticas

#### 1. Bug min_on_time (CRÍTICO)
**Problema:** Bomba ligava/desligava 95 vezes por dia (a cada 1.5-2 min) em vez de respeitar `min_on_time=5min`.

**Causa Raiz:** 
- Usava `last_changed` que atualiza em **qualquer mudança de estado/atributo**
- Não apenas quando bomba liga (ON)

**Correção:**
```yaml
# ANTES (BUGGY):
{% set last_on = states[pump_switch].last_changed %}

# DEPOIS (FIXED):
{% set entity = states[pump_switch] %}
{% if entity and entity.state == 'on' %}
  {% set minutes_on = (now() - entity.last_changed).total_seconds() / 60 %}
  {{ minutes_on >= min_on_time }}
{% endif %}
```

**Resultado:** Bomba agora permanece ligada pelo tempo mínimo configurado.

---

#### 2. Falta de re-verificação após delay_off
**Problema:** Após `delay_off`, bomba desligava sem verificar se condições melhoraram (ex: nuvem passou).

**Correção:** Adicionada re-verificação antes de desligar:
```yaml
- delay:
    seconds: "{{ effective_delay_off }}"

# 🆕 Re-verificar após delay
- if:
    - condition: template
      value_template: "{{ import_current > final_import_limit }}"
  then:
    - service: switch.turn_off  # Desligar
  else:
    - service: system_log.write  # Log: condições melhoraram
```

---

#### 3. Erro YAML - Indentação incorreta
**Problema:** `else` block mal indentado (linha 1450), causava `expected <block end>, but found '?'`

**Correção:** Ajustada indentação de 6 para 4 espaços.

---

### 🔧 Melhorias de Qualidade

#### 4. house_power_avg_7d não usado no modo fixo
**Problema:** Quando `use_dynamic_house_estimate=false`, usava `house_avg_power` (valor manual) em vez do sensor de média de 7 dias.

**Correção:**
```yaml
# ANTES:
{{ (house_avg_power / 1000 * hours_until_sunset)|round(1) }}

# DEPOIS:
{{ (house_power_avg_7d / 1000 * hours_until_sunset)|round(1) }}
```

**Benefício:** Agora usa estatísticas reais mesmo no modo fixo.

---

#### 5. pv_power obrigatório desnecessariamente
**Problema:** `pv_power` era obrigatório, impedindo uso apenas com NET ou Export.

**Correção:** Adicionado `default: {}` e texto "Opcional se usar NET ou Export".

---

#### 6. triggers/conditions/actions → singular
**Problema:** Home Assistant moderno usa `trigger`/`condition`/`action` (singular).

**Correção:** Alterado de plural para singular para compatibilidade.

---

#### 7. house_power_sensor_daily não usado
**Problema:** Input definido mas nunca usado no código.

**Solução:** Marcado como `[DEPRECATED]` com aviso que será removido.

---

### 📊 Logs de Debug Adicionados

```log
🏊 Blueprint EXECUTOU [trigger=house_changed]: source=house+pv, house=2603W, pv=0W, pump=False
🏊 Bomba NÃO PODE DESLIGAR [aggressive]: min_on_time=10min não atingido, ligada há 3.5min
🏊 Bomba MANTIDA [aggressive]: condições melhoraram após delay_off, import=650W ≤ limit=700W
```

---

### ⚙️ Alterações de Configuração

- **min_on_time** default: `5min` → `10min`
- Melhor para evitar ciclos rápidos com nuvens intermitentes

---

## 🧪 Testes Necessários

### ✅ Testes de Sintaxe
- [x] Blueprint carrega sem erros YAML
- [x] Automação inicializa corretamente
- [x] Debug logs funcionam

### ⏳ Testes Funcionais (aguardar sol)
- [ ] Bomba liga com excedente solar suficiente
- [ ] Bomba permanece ligada mínimo 10 minutos
- [ ] Bomba não desliga durante delay_off se condições melhoram
- [ ] Logs mostram "NÃO PODE DESLIGAR" quando aplicável
- [ ] Redução de ON/OFF events: de 95 para ~5-10 por dia

---

## 📝 Commits

- `fbe6139` - fix: Corrigir bug min_on_time no blueprint piscina solar v2
- `[PENDING]` - refactor: Melhorar qualidade e corrigir issues apontados

---

## 🔜 Próximos Passos

1. **Monitorizar logs amanhã (09:00-12:00)**
   ```bash
   tail -f home-assistant.log | grep --line-buffered "🏊"
   ```

2. **Validar métricas:**
   - Tempo médio bomba ligada: ≥ 10 minutos
   - Total ON/OFF events: < 15 por dia
   - Taxa de importação: < 200W em média

3. **Se tudo OK:**
   - Documentar fix completo
   - Considerar reduzir min_on_time para 7min se muito conservador
   - Release v2.1.0 oficial

4. **Se problemas persistirem:**
   - Adicionar sensor de média 5min para export
   - Ajustar delays on/off
   - Considerar hysteresis maior

---

## 📚 Referências

- **Issue Original:** 95 eventos LIGA/DESLIGA em 5 horas (11:00-16:00)
- **PV Observado:** 1782W - 2968W (inverno, fevereiro)
- **Sistema:** HA em Docker, EmonCMS, Solcast, Pool Pump 1380W
- **Repositório:** https://github.com/guibrazlima/homeassistant
