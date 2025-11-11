# 🏠 Home Assistant - Sistema de Automação Residencial

> **Sistema Home Assistant** com automações inteligentes, controlo de energia solar, 
> gestão de piscina e climatização avançada.

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.1+-blue.svg)](https://www.home-assistant.io/)
[![Maintenance](https://img.shields.io/badge/Maintained-Yes-green.svg)](https://github.com/guibrazlima/homeassistant)

---

## 🚀 Início Rápido

### Componentes Principais

- **🤖 Automações:** 68+ automações organizadas em 13 categorias
- **📦 Packages:** 8 packages modulares (AQS, Piscina, Climatização)
- **🔌 Integrações:** 24+ integrações personalizadas
- **☀️ Energia Solar:** Controlo automático de excesso PV
- **🏊 Piscina:** Gestão completa (cloro, pH, cobertura)
- **🌡️ Climatização:** Sensores de conforto térmico

### Estrutura do Projeto

```
homeassistant/
├── automations/           # 13 ficheiros de automações categorizadas
├── packages/              # 8 packages modulares
├── custom_components/     # Integrações personalizadas
├── docs/                  # 📚 Documentação consolidada
│   ├── historico/         # Histórico de reorganizações
│   ├── analises/          # Análises técnicas
│   └── SECURITY.md        # Guia de segurança
├── scripts/               # Scripts de automação
└── configuration.yaml     # Configuração principal
```

---

## 📚 Documentação

### 📖 Guias Principais

| Documento | Descrição |
|-----------|-----------|
| [📋 Histórico de Reorganização](docs/historico/REORGANIZACAO.md) | Completo histórico de todas as reorganizações |
| [📦 Análise de Packages](docs/analises/PACKAGES.md) | Análise técnica detalhada de todos os packages |
| [🔍 Análise de Erros](docs/analises/ERROS_LOGS.md) | Diagnóstico de erros e soluções |
| [🚀 Melhorias Técnicas](docs/analises/MELHORIAS_TECNICAS.md) | Guia completo de boas práticas |
| [🔒 Segurança](docs/SECURITY.md) | Guia de segurança e ficheiros sensíveis |

### 🎯 Documentação por Categoria

#### Automações
- Ver: [`automations/README.md`](automations/README.md)
- 13 ficheiros categorizados
- 100% IDs únicos
- Descrições completas

#### Packages
- Ver: [`packages/README.md`](packages/README.md)
- 8 packages modulares
- Dependências documentadas
- Error handling implementado

---

## ��️ Arquitetura

### Componentes do Sistema

```
┌─────────────────────────────────────────────┐
│         Home Assistant Core                 │
├─────────────────────────────────────────────┤
│  Automações (13 ficheiros)                  │
│  Packages (8 módulos)                       │
│  Custom Components (24+)                    │
└─────────────────────────────────────────────┘
         │              │              │
    ┌────┴────┐    ┌───┴───┐    ┌────┴────┐
    │ MariaDB │    │InfluxDB│    │ Telegram│
    └─────────┘    └────────┘    └─────────┘
```

### Integrações Principais

- **☀️ Solar:** PV Excess Control, Solcast
- **📷 Câmaras:** Tapo Control, ONVIF
- **🌡️ Sensores:** Thermal Comfort, Sensor avançados
- **🔌 Dispositivos:** TP-Link Deco, dispositivos Zigbee/WiFi
- **🤖 IA:** LLM Vision para análise de imagens

---

## 💡 Funcionalidades Destacadas

### 🌞 Gestão de Energia Solar
- Controlo automático de excesso de produção solar
- Otimização de autoconsumo
- Integração com previsões Solcast

### 🏊 Automação de Piscina
- **Clorador de sal:** Controlo automático de produção de cloro
- **pH:** Monitorização e alertas
- **Cobertura:** Deteção automática via IA (LLM Vision)
- **TPO:** Cálculo de tempo ótimo de cloração

### 🌡️ Conforto Térmico
- Sensores de conforto para 4 divisões
- Cálculos de ponto de orvalho
- Alertas de humidade ideal

### 💧 Água Quente Sanitária (AQS)
- Estimador térmico para bomba de calor HP90
- Cálculo de perdas térmicas
- Otimização de aquecimento

---

## 🔧 Instalação e Configuração

### Pré-requisitos

- Home Assistant 2023.1 ou superior
- MariaDB (para recorder)
- Python 3.11+

### Configuração Inicial

1. **Clonar repositório:**
   ```bash
   git clone https://github.com/guibrazlima/homeassistant.git
   cd homeassistant
   ```

2. **Configurar secrets:**
   ```bash
   cp secrets.yaml.example secrets.yaml
   # Editar secrets.yaml com as suas credenciais
   ```

3. **Validar configuração:**
   ```bash
   hass --script check_config
   ```

4. **Reiniciar Home Assistant**

### ⚠️ Ficheiros Sensíveis

> **IMPORTANTE:** Este repositório contém configurações públicas. 
> Ficheiros sensíveis como `secrets.yaml`, bases de dados e tokens 
> **NÃO** estão incluídos.

Os seguintes ficheiros **NÃO** estão no repositório e devem ser criados manualmente:

- `secrets.yaml` (credenciais)
- `*.db*` (bases de dados)
- `known_devices.yaml` (dispositivos)
- `home-assistant.log*` (logs)

Ver [SECURITY.md](docs/SECURITY.md) para detalhes completos.

---

## 📊 Estatísticas

| Categoria | Quantidade | Estado |
|-----------|------------|--------|
| **Automações** | 68+ | ✅ 100% válidas |
| **Packages** | 8 | ✅ 100% documentados |
| **Integrações** | 24+ | ✅ Funcionais |
| **Sensores** | 100+ | ✅ Monitorizados |
| **Documentação** | 2800+ linhas | ✅ Consolidada |

### Qualidade do Código

- ✅ **100%** YAML válido
- ✅ **100%** Unique IDs nos sensores
- ✅ **100%** Error handling em automações críticas
- ✅ **95%** Documentação completa
- ✅ **Nomenclatura padronizada:** `categoria_descricao.yaml`

---

## 🚀 Melhorias Recentes

### Novembro 2025

#### ✨ Reorganização Completa
- ✅ 68 automações reorganizadas em 13 ficheiros categorizados
- ✅ 8 packages otimizados e documentados
- ✅ Documentação consolidada em `docs/`
- ✅ Eliminação de duplicações
- ✅ Padronização de nomenclatura

#### 🔧 Melhorias Técnicas
- ✅ Unique IDs em 100% dos sensores
- ✅ Timeout e error handling em automações LLM Vision
- ✅ Criação de `aqs_common.yaml` para inputs partilhados
- ✅ README.md para automações e packages

Ver [REORGANIZACAO.md](docs/historico/REORGANIZACAO.md) para histórico completo.

---

## 🤝 Contribuir

### Como Contribuir

1. Fork o repositório
2. Criar branch: `git checkout -b feature/nova-funcionalidade`
3. Validar YAML: `hass --script check_config`
4. Commit: `git commit -m "Adicionar nova funcionalidade"`
5. Push: `git push origin feature/nova-funcionalidade`
6. Abrir Pull Request

### Boas Práticas

- ✅ Sempre adicionar `unique_id` a sensores
- ✅ Usar nomenclatura: `categoria_descricao.yaml`
- ✅ Documentar dependências em cabeçalhos
- ✅ Adicionar timeout em services externos
- ✅ Nunca commitar `secrets.yaml`

Ver [MELHORIAS_TECNICAS.md](docs/analises/MELHORIAS_TECNICAS.md) para guia completo.

---

## 📞 Suporte

### Documentação

- 📚 [Documentação Home Assistant](https://www.home-assistant.io/docs/)
- 🔧 [Guia de Troubleshooting](docs/analises/ERROS_LOGS.md)
- 💡 [Boas Práticas](docs/analises/MELHORIAS_TECNICAS.md)

### Issues

- 🐛 Reportar bugs via [GitHub Issues](https://github.com/guibrazlima/homeassistant/issues)
- 💬 Discussões na comunidade Home Assistant

---

## 📜 Licença

Este projeto está sob licença MIT. Ver `LICENSE` para detalhes.

---

## 🙏 Agradecimentos

- [Home Assistant](https://www.home-assistant.io/) - Plataforma incrível
- [PV Excess Control](https://github.com/InventoCasa/ha-advanced-blueprints) - Blueprint de energia solar
- [LLM Vision](https://github.com/valentinfrlch/ha-llmvision) - Integração de IA para visão computacional
- Comunidade Home Assistant Portugal 🇵🇹

---

**Última atualização:** 11 de novembro de 2025  
**Versão:** 2.0.0  
**Manutenção:** Ativa ✅
