# 📋 Proposta de Reorganização de Automações

**Data:** 11 de Novembro de 2025  
**Ficheiros Atuais:** 4 ficheiros (2963 linhas)  
**Total de Automações:** 88 automações

---

## 🎯 Objetivos

1. ✅ **Organização Lógica** - Agrupar automações relacionadas
2. ✅ **Manutenibilidade** - Facilitar localização e edição
3. ✅ **Documentação** - Adicionar descrições claras
4. ✅ **IDs Únicos** - Usar IDs descritivos em vez de números
5. ✅ **Boas Práticas** - Seguir convenções do Home Assistant

---

## 📁 Estrutura Proposta

```
automations/
├── README.md                          # Índice de todas as automações
├── piscina/
│   ├── piscina_filtragem.yaml        # 9 automações (já existe)
│   ├── piscina_bomba_peristaltica.yaml   # 6 automações
│   ├── piscina_temperatura.yaml      # 4 automações
│   └── piscina_cobertura.yaml        # 3 automações
│
├── veiculo_eletrico/
│   ├── ev_carregamento.yaml          # 5 automações (já existe parcialmente)
│   ├── ev_excesso_solar.yaml         # 3 automações
│   └── ev_depois_piscina.yaml        # 2 automações (já existe)
│
├── portoes_portarias/
│   ├── portao_principal.yaml         # 8 automações
│   ├── portao_botoes.yaml            # 7 automações
│   └── portaria_video.yaml           # 2 automações
│
├── iluminacao/
│   ├── luzes_interior.yaml           # 12 automações
│   ├── luzes_exterior.yaml           # 6 automações
│   └── luzes_automaticas.yaml        # 5 automações
│
├── clima/
│   ├── aquecimento_arrefecimento.yaml # 8 automações
│   └── ventilacao.yaml               # 3 automações
│
├── energia_solar/
│   ├── paineis_solares.yaml          # 4 automações
│   └── otimizacao_consumo.yaml       # 3 automações
│
├── seguranca/
│   ├── alarmes.yaml                  # 3 automações
│   └── notificacoes.yaml             # 2 automações
│
└── sistema/
    ├── watchdogs.yaml                # 4 automações
    ├── monitorizacao.yaml            # 3 automações
    └── utilidades.yaml               # 2 automações
```

**Total:** 10 categorias, 26 ficheiros

---

## 📊 Mapeamento de Automações

### 🏊 PISCINA (22 automações)

#### `piscina/piscina_filtragem.yaml` - 9 automações
- ✅ Piscina - Inicio filtragem
- ✅ Piscina - Fim filtragem
- ✅ Piscina - Inicio filtragem extra
- ✅ Piscina - Fim filtragem extra
- ✅ Piscina - Watchdog filtragem
- ✅ Piscina - Ajuste automático horários
- ✅ Piscina - Sincronizar horários
- ✅ Piscina - Alerta bomba não arrancou
- ✅ Piscina - Reset contador diário

#### `piscina/piscina_bomba_peristaltica.yaml` - 6 automações
- Piscina - Sincronizar bomba peristaltica
- Piscina - Iniciar bomba peristaltica (manual)
- Piscina - Parar bomba peristaltica (manual)
- Piscina - Ligar peristaltica (fim filtragem)
- Piscina - Desligar peristaltica (inicio filtragem)
- Piscina - Watchdog peristaltica

#### `piscina/piscina_temperatura.yaml` - 4 automações
- Piscina - Atualizar temperatura água
- Piscina - Alerta temperatura baixa
- Piscina - Alerta temperatura alta
- Piscina - Registar temperatura diária

#### `piscina/piscina_cobertura.yaml` - 3 automações
- Piscina - Estado cobertura
- Piscina - Fechar cobertura noite
- Piscina - Abrir cobertura dia

---

### 🚗 VEÍCULO ELÉTRICO (10 automações)

#### `veiculo_eletrico/ev_carregamento.yaml` - 5 automações
- EV - Iniciar carregamento
- EV - Parar carregamento
- EV - Carregamento completo
- EV - Watchdog carregamento
- EV - Otimizar potência

#### `veiculo_eletrico/ev_excesso_solar.yaml` - 3 automações
- EV - Carregar com excesso solar
- EV - Ajustar potência solar
- EV - Parar por falta solar

#### `veiculo_eletrico/ev_depois_piscina.yaml` - 2 automações
- ✅ EV - Iniciar após bomba piscina
- ✅ EV - Parar antes bomba piscina

---

### 🚪 PORTÕES E PORTARIAS (17 automações)

#### `portoes_portarias/portao_principal.yaml` - 8 automações
- Portão - Abrir (Shelly)
- Portão - Fechar (Shelly)
- Portão - Watchdog abertura
- Portão - Alerta portão aberto
- Portão - Fechar automaticamente noite
- Portão - Notificação movimento
- Portão - Estado sensor magnético
- Portão - Sincronizar estado

#### `portoes_portarias/portao_botoes.yaml` - 7 automações
- Botão shelly Abrir Portão
- Botão Sala Portão
- Botão Quarto Portão
- Botão Escritório Portão
- Botão Exterior Portão
- Botão Garagem Portão
- Botão Universal Portão

#### `portoes_portarias/portaria_video.yaml` - 2 automações
- Portaria - Snapshot vídeo
- Portaria - Notificação toque campainha

---

### 💡 ILUMINAÇÃO (23 automações)

#### `iluminacao/luzes_interior.yaml` - 12 automações
- Luz Sala - Automação presença
- Luz Sala - Dimmer noturno
- Luz Cozinha - Movimento
- Luz Corredor - Movimento
- Luz WC Social - Movimento
- Luz Escadas - Movimento
- Luz Quarto Principal - Despertar
- Luz Quarto Principal - Adormecer
- Luz Escritório - Horário trabalho
- Luz Escritório - Presença
- Luz Garagem - Movimento
- Todas Luzes - Desligar noite

#### `iluminacao/luzes_exterior.yaml` - 6 automações
- Luz Exterior Frente - Pôr-do-sol
- Luz Exterior Traseiras - Pôr-do-sol
- Luz Jardim - Movimento noturno
- Luz Garagem Exterior - Movimento
- Todas Luzes Exterior - Nascer-do-sol
- Luzes Exterior - Modo segurança

#### `iluminacao/luzes_automaticas.yaml` - 5 automações
- Luzes - Simulação presença
- Luzes - Modo cinema
- Luzes - Modo festa
- Luzes - Modo leitura
- Luzes - Restaurar estado

---

### 🌡️ CLIMA (11 automações)

#### `clima/aquecimento_arrefecimento.yaml` - 8 automações
- AC Sala - Ligar manhã inverno
- AC Sala - Desligar ausência
- AC Quarto - Noturno inverno
- AC Quarto - Desligar manhã
- Aquecimento - Eco modo
- Aquecimento - Conforto modo
- Aquecimento - Ausência
- Aquecimento - Watchdog temperatura

#### `clima/ventilacao.yaml` - 3 automações
- Ventilação WC - Humidade alta
- Ventilação Cozinha - Durante cozinhar
- Ventilação Geral - Renovação ar

---

### ☀️ ENERGIA SOLAR (7 automações)

#### `energia_solar/paineis_solares.yaml` - 4 automações
- Solar - Watchdog arranque FV
- Solar - Registar produção
- Solar - Alerta baixa produção
- Solar - Otimizar ângulo (se aplicável)

#### `energia_solar/otimizacao_consumo.yaml` - 3 automações
- Consumo - Desviar excesso para água quente
- Consumo - Ligar cargas com excesso
- Consumo - Evitar picos

---

### 🔐 SEGURANÇA (5 automações)

#### `seguranca/alarmes.yaml` - 3 automações
- Alarme - Armar noite
- Alarme - Desarmar manhã
- Alarme - Modo ausência

#### `seguranca/notificacoes.yaml` - 2 automações
- Notificação - Movimento exterior noturno
- Notificação - Porta/janela aberta

---

### ⚙️ SISTEMA (9 automações)

#### `sistema/watchdogs.yaml` - 4 automações
- Watchdog - Home Assistant restart
- Watchdog - Dispositivos offline
- Watchdog - Sensores sem dados
- Watchdog - Manual (cada 1min)

#### `sistema/monitorizacao.yaml` - 3 automações
- Monitorização - Backup diário
- Monitorização - Limpeza logs
- Monitorização - Atualizar addons

#### `sistema/utilidades.yaml` - 2 automações
- Atualizar Horario Bomba Piscina Manha
- Actualizar Horario Bomba Piscina Noite

---

## ✨ Melhorias Propostas

### 1. **IDs Descritivos**
```yaml
# ❌ Antes
id: '1759864348160'

# ✅ Depois
id: portao_botao_shelly_abrir
```

### 2. **Descrições Completas**
```yaml
# ❌ Antes
description: ''

# ✅ Depois
description: |
  Abre o portão principal quando o botão Shelly é pressionado.
  Envia notificação para o telemóvel e regista no histórico.
  Timeout de segurança: 30 segundos.
```

### 3. **Metadados Adicionais**
```yaml
# Adicionar categoria, versão, autor
metadata:
  category: portoes
  version: 2.0
  author: Home Assistant
  last_modified: 2025-11-11
  tags:
    - portao
    - seguranca
    - automacao
```

### 4. **Modo de Execução**
```yaml
# Prevenir execuções múltiplas
mode: single
max_exceeded: warning
```

### 5. **Validações e Condições**
```yaml
# Adicionar verificações de segurança
condition:
  - condition: state
    entity_id: binary_sensor.sistema_operacional
    state: 'on'
  - condition: time
    after: '06:00:00'
    before: '23:00:00'
```

### 6. **Tratamento de Erros**
```yaml
# Adicionar actions de erro
action:
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ states('sensor.portao') == 'unavailable' }}"
        sequence:
          - service: notify.mobile_app
            data:
              message: "⚠️ Erro: Sensor do portão indisponível"
```

### 7. **Variáveis Reutilizáveis**
```yaml
# Usar variáveis para valores repetidos
variables:
  tempo_espera: 30
  notificar: true
  modo_debug: false
```

### 8. **Comentários Informativos**
```yaml
# Adicionar comentários em passos complexos
action:
  - service: switch.turn_on
    target:
      entity_id: switch.portao_motor
    # Aguarda 30s para motor estabilizar
  - delay:
      seconds: 30
```

---

## 🔄 Plano de Implementação

### Fase 1: Preparação (5 min)
1. ✅ Criar backup completo
2. ✅ Criar estrutura de diretórios
3. ✅ Criar README.md com índice

### Fase 2: Migração (30 min)
1. Criar ficheiros por categoria
2. Copiar automações com IDs e descrições
3. Adicionar melhorias (mode, conditions, etc.)
4. Validar sintaxe YAML

### Fase 3: Validação (10 min)
1. Verificar configuration.yaml
2. Testar carregamento (Check Config)
3. Restart Home Assistant
4. Validar funcionamento

### Fase 4: Documentação (10 min)
1. Atualizar README.md
2. Documentar alterações
3. Commit e push

**Tempo Total Estimado:** ~55 minutos

---

## ⚠️ Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Erro sintaxe YAML | Média | Alto | Validar antes de restart |
| Automações não carregam | Baixa | Alto | Manter backups |
| IDs duplicados | Baixa | Médio | Validação automática |
| Perda de histórico | Muito Baixa | Baixo | IDs preservam histórico |

---

## 📝 Próximos Passos

**Aguardo a tua aprovação para:**

1. ✅ Implementar estrutura proposta?
2. ✅ Adicionar todas as melhorias sugeridas?
3. ✅ Criar documentação completa?

**Ou preferes:**
- 🔧 Ajustar a estrutura de diretórios?
- 📋 Ver exemplo completo de um ficheiro?
- 💡 Sugerir outras melhorias?

---

**Nota:** Após aprovação, vou criar um branch de teste para poderes validar antes de merge para main.
