# 🌡️ Thermal Comfort - Conforto Térmico

Monitorização de temperatura, humidade e conforto térmico em todas as divisões da casa.

## 📊 Estrutura

```
thermal_comfort/
├── README.md (este ficheiro)
├── exterior.yaml      # Áreas exteriores (Eira)
├── utilidade.yaml     # Cave, garagem, arrumos
├── comum.yaml         # Salas, cozinha, corredores
├── quartos.yaml       # Quartos (suite, crianças)
└── groups.yaml        # Agrupamentos para UI
```

## 🎯 Divisões Monitorizadas

| Categoria | Divisão | Sensores Criados |
|-----------|---------|------------------|
| **Exterior** | Eira | Temperatura, Humidade, Ponto Orvalho, Heat Index |
| **Utilidade** | Cave | Temperatura, Humidade, Ponto Orvalho (anti-bolor) |
| **Comum** | Sala Superior | Temperatura, Humidade, Conforto Térmico |
| **Quartos** | Suite Principal | Temperatura, Humidade, Qualidade do Sono |
| **Quartos** | Quarto Miúdos | Temperatura, Humidade, Conforto Infantil |

## 📈 Sensores Derivados

Para cada divisão, o thermal_comfort cria automaticamente:

- **Absolute Humidity** - Humidade absoluta (g/m³)
- **Heat Index** - Índice de calor percebido
- **Dew Point** - Ponto de orvalho (condensação)
- **Thermal Perception** - Percepção térmica (frio/confortável/quente)
- **Frost Risk** - Risco de geada (exterior)
- **Simmer Index** - Índice de desconforto por calor

## ✅ Valores Ideais de Conforto

### Quartos (Sono)
- **Temperatura:** 18-22°C (ideal: 19°C)
- **Humidade:** 40-60% (ideal: 50%)
- **Nota:** Crianças preferem temperaturas ligeiramente mais altas

### Salas (Estar)
- **Temperatura:** 20-24°C (ideal: 21°C)
- **Humidade:** 40-60% (ideal: 50%)

### Cave (Anti-Bolor)
- **Humidade:** <70% (prevenir bolor)
- **Ponto Orvalho:** Monitorizar para prevenir condensação

### Exterior
- **Heat Index:** >32°C = desconforto
- **Frost Risk:** <0°C = risco de geada

## 🔔 Automações Recomendadas

1. **Alerta Humidade Alta**
   - Se humidade cave > 70% → notificar (risco bolor)

2. **Alerta Temperatura Quartos**
   - Se temperatura quarto crianças < 18°C → notificar
   - Se temperatura > 24°C → sugerir ventilação

3. **Sugestão Ventilação**
   - Se heat_index > 28°C → sugerir abrir janelas/ligar AC

4. **Qualidade do Sono**
   - Monitorizar conforto térmico durante a noite
   - Dashboard com histórico de condições ideais

## 🔧 Manutenção

### Adicionar Nova Divisão

1. Identificar categoria (exterior/utilidade/comum/quartos)
2. Editar ficheiro YAML correspondente
3. Adicionar sensor com unique_id único
4. Testar: `hass --script check_config`
5. Reiniciar Home Assistant
6. Adicionar ao group.yaml se necessário

### Exemplo Template
```yaml
- name: Nome da Divisão
  temperature_sensor: sensor.divisao_temperature
  humidity_sensor: sensor.divisao_humidity
  unique_id: thermal_comfort_divisao_nome
  # Comentário sobre especificidades desta divisão
```

## 📚 Referências

- **Custom Component:** https://github.com/dolezsa/thermal_comfort
- **Documentação HA:** https://www.home-assistant.io/integrations/sensor/
- **Análise Completa:** `/docs/analises/THERMAL_COMFORT_ANALISE.md`

## ⚠️ Notas

- O componente `thermal_comfort` precisa estar instalado em `custom_components/`
- Se houver erros de importação, verificar compatibilidade com versão HA
- Alternativa: usar template sensors (ver análise completa)

---

**Última Atualização:** 12 de novembro de 2025  
**Versão:** 1.0 - Estrutura modularizada
