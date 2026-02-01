# 🏊 Piscina - Controlo Solar Inteligente

## Blueprint Português para Home Assistant

Blueprint otimizado para maximizar o autoconsumo solar na filtragem da piscina.

---

## ✨ Funcionalidades

### 🧠 Lógica Inteligente
- **Previsão de importação** - Liga ANTES de precisar importar
- **Hysteresis dual** - Critérios diferentes para ligar vs manter
- **3 níveis de fallback** - Usa sensores alternativos automaticamente

### 💶 Otimização Económica
- **Break-even automático** - Calcula importação que ainda compensa
- **Integração tarifas** - Considera preço vazio vs fora-vazio
- **Máximo autoconsumo** - Prioriza uso do excedente solar

### 🛡️ Proteções
- **Delays configuráveis** - Evita oscilações rápidas
- **Tempo mínimo ligada** - Protege motor de ciclos curtos
- **Override manual** - Respeita controlo manual
- **Fallback sensores** - Sistema não para se sensor falhar

### ⏰ Gestão Horária
- **Horários solares** - Só funciona com sol
- **Offsets configuráveis** - Ajusta a janela de operação
- **Integração filtragem** - Para quando atingir tempo diário

### 🔍 Diagnóstico
- **Logs detalhados** - Debug fácil
- **Atributos ricos** - Sabe porquê decidiu
- **Notificações** - Alerta em erros

---

## 📦 Instalação

### 1. Copiar Blueprint
```bash
# Já está em:
/config/blueprints/automation/piscina_solar/piscina_solar_control.yaml
```

### 2. Recarregar Blueprints
- **Settings** → **Automations & Scenes** → **Blueprints** → **Reload**

### 3. Criar Automação
- **Settings** → **Automations & Scenes** → **Create Automation** → **Use Blueprint**
- Selecionar: **🏊 Piscina - Controlo Solar Inteligente (PT)**

---

## ⚙️ Configuração

### Sensores Obrigatórios

| Sensor | Descrição | Exemplo |
|--------|-----------|---------|
| **☀️ Produção Solar** | PV instantâneo (W) | `sensor.emoncms_solar` |
| **🔌 Switch Bomba** | Controlo ON/OFF | `switch.bomba_piscina_switch_0` |

### Sensores Recomendados (escolher 1 grupo)

**Grupo A (Preferencial - Mais Preciso):**
| Sensor | Descrição | Exemplo |
|--------|-----------|---------|
| **🏠 Consumo Casa** | Sem bomba (W) | `sensor.emoncms_use_no_pool_pump` |

**Grupo B (Alternativa):**
| Sensor | Descrição | Exemplo |
|--------|-----------|---------|
| **📊 NET Power** | Import/Export (W) | `sensor.emoncms_import_export` |

**Grupo C (Fallback):**
| Sensor | Descrição | Exemplo |
|--------|-----------|---------|
| **📤 Exportação** | Sempre positivo (W) | `sensor.emoncms_export_power_positive` |

### Parâmetros Recomendados

```yaml
# Bomba típica 1.5CV
pump_nominal_power: 800-1200W

# Thresholds conservadores
import_limit: 500-700W
start_margin: 100-200W

# Delays anti-oscilação
delay_on: 30s
delay_off: 60s
min_on_time: 5-10min

# Horários
sun_offset_start: 30min (após nascer)
sun_offset_end: 30min (antes pôr)
```

---

## 🔄 Comparação com Versão Anterior

### Binary Sensor (Original)
```yaml
# O que tinha:
✅ Lógica preditiva
✅ Hysteresis inteligente  
✅ 3 fallbacks
✅ Break-even económico
❌ Delays hardcoded (20s/30s)
❌ Sem tempo mínimo ON
❌ Sem override manual
❌ Sem horários configuráveis
❌ Precisava automação separada
```

### Blueprint (Melhorado)
```yaml
# O que ganhou:
✅ Tudo do original
✅ Delays configuráveis (UI)
✅ Tempo mínimo ON (protege motor)
✅ Override manual integrado
✅ Horários configuráveis
✅ Automação completa (tudo-em-um)
✅ Integração timer filtragem
✅ Logs de diagnóstico opcionais
✅ Notificações de erro
✅ Sensor consumo real (opcional)
✅ Margem extra para arranque
```

---

## 📊 Lógica de Decisão

### Fluxograma

```
                    ┌─────────────────┐
                    │  Sensor Update  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Horário Solar?  │──NO──► EXIT
                    └────────┬────────┘
                            YES
                             │
                    ┌────────▼────────┐
                    │ Override OFF?   │──NO──► EXIT
                    └────────┬────────┘
                            YES
                             │
                    ┌────────▼────────┐
                    │ Filtragem OK?   │──NO──► EXIT
                    └────────┬────────┘
                            YES
                             │
              ┌──────────────┴──────────────┐
              │                              │
     ┌────────▼────────┐            ┌───────▼────────┐
     │   Bomba OFF?    │            │   Bomba ON?    │
     └────────┬────────┘            └───────┬────────┘
              │                              │
     ┌────────▼────────┐            ┌───────▼────────┐
     │ import_previsto │            │ import_atual   │
     │ <= limit-margin │            │ <= limit       │
     └────────┬────────┘            └───────┬────────┘
              │                              │
         ┌────┴────┐                    ┌────┴────┐
        YES       NO                   YES       NO
         │         │                    │         │
    ┌────▼────┐   EXIT            ┌────▼────┐    │
    │ Wait    │                   │ MANTÉM  │    │
    │ delay_on│                   │   ON    │    │
    └────┬────┘                   └─────────┘    │
         │                                       │
    ┌────▼────┐                        ┌────────▼────────┐
    │ Ainda   │                        │ Tempo min ON?   │
    │ OK?     │                        └────────┬────────┘
    └────┬────┘                                YES
         │                                       │
        YES                               ┌──────▼──────┐
         │                                │ Wait        │
    ┌────▼────┐                           │ delay_off   │
    │  LIGA   │                           └──────┬──────┘
    └─────────┘                                  │
                                          ┌──────▼──────┐
                                          │ Ainda >lim? │
                                          └──────┬──────┘
                                                YES
                                                 │
                                          ┌──────▼──────┐
                                          │   DESLIGA   │
                                          └─────────────┘
```

### Fórmulas

#### Importação Prevista (Bomba OFF)
```python
# Grupo A (house+pv):
import_previsto = max(house + pump - pv, 0)

# Grupo B (net):
import_previsto = max(net + pump, 0)

# Grupo C (export):
import_previsto = max(pump - export, 0)
```

#### Importação Atual (Bomba ON)
```python
# Grupo A (house+pv):
import_atual = max(house + pump - pv, 0)  # house já não inclui bomba

# Grupo B (net):
import_atual = max(net, 0)  # net já inclui bomba
```

#### Break-Even Económico
```python
# Importação que ainda compensa vs ligar à noite
break_even = pump * (preco_fv - preco_vazio) / preco_fv

# Exemplo: bomba 800W, preços 0.1537/0.0929
break_even = 800 * (0.1537 - 0.0929) / 0.1537
           = 800 * 0.0608 / 0.1537
           = 316W

# Significa: Se importar até 316W, ainda compensa vs noite!
```

---

## 🎯 Exemplos de Configuração

### Conservador (Máximo Autoconsumo)
```yaml
import_limit: 300W
start_margin: 200W
delay_on: 60s
delay_off: 120s
min_on_time: 10min
use_economic_optimization: false
```

### Balanceado (Recomendado)
```yaml
import_limit: 700W
start_margin: 100W
delay_on: 30s
delay_off: 60s
min_on_time: 5min
use_economic_optimization: true
```

### Agressivo (Máxima Filtragem)
```yaml
import_limit: 1000W
start_margin: 0W
delay_on: 15s
delay_off: 30s
min_on_time: 3min
use_economic_optimization: true
```

---

## 🔧 Troubleshooting

### Bomba não liga
1. **Verificar sensores:** Developer Tools → States
2. **Verificar horário:** Está entre sunrise e sunset?
3. **Verificar override:** input_boolean está OFF?
4. **Verificar filtragem:** Tempo restante > 0?
5. **Ativar logs:** enable_debug_logs: true

### Bomba oscila muito
1. **Aumentar delays:** delay_on: 60s, delay_off: 120s
2. **Aumentar tempo mínimo:** min_on_time: 15min
3. **Aumentar margem:** start_margin: 300W
4. **Verificar sensores:** Valores estáveis?

### Logs para diagnóstico
```bash
# Ver logs do blueprint
grep "Piscina Solar" /config/home-assistant.log
```

---

## 📋 Migração do Binary Sensor

### Manter Ambos (Recomendado inicialmente)
1. Criar automação com blueprint
2. Desativar automações antigas
3. Manter binary_sensor para comparação
4. Após 1 semana, se OK, remover binary_sensor

### Input Numbers Necessários
O blueprint não precisa dos input_numbers do binary_sensor antigo!
Tudo é configurado diretamente no blueprint.

**Pode remover (opcional):**
- `input_number.piscina_potencia_bomba_w` → Configurado no blueprint
- `input_number.piscina_import_max_w` → Configurado no blueprint
- `input_number.piscina_buffer_w` → Não usado

**Manter (se usar):**
- `input_number.piscina_filtracao_min_restantes` → Integrado no blueprint
- `input_boolean.piscina_override_manual` → Integrado no blueprint

---

## 📈 Roadmap / Melhorias Futuras

### v1.1 (Planeado)
- [ ] Integração com previsão Solcast
- [ ] Coordenação com outros aparelhos (EV)
- [ ] Dashboard card automático

### v1.2 (Futuro)
- [ ] Machine learning para prever padrões
- [ ] Otimização baseada em previsão meteorológica
- [ ] Integração com tarifas dinâmicas

---

## 🙏 Créditos

- **Código Original:** guibrazlima (binary_sensor.piscina_excedente_fv_bomba)
- **Blueprint:** AI Assistant
- **Inspiração:** PVExcessControl (InventoCasa)

---

## 📄 Licença

MIT License - Uso livre com atribuição.

---

*Criado: 1 Fevereiro 2026*  
*Versão: 1.0.0*  
*Compatibilidade: Home Assistant 2024.1+*
