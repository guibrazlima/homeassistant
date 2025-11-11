# 📚 Documentação - Home Assistant

> **Índice central** de toda a documentação do sistema Home Assistant

---

## 🎯 Navegação Rápida

### 📋 Por Categoria

| Categoria | Documentos | Descrição |
|-----------|------------|-----------|
| **📜 Histórico** | [Reorganização](historico/REORGANIZACAO.md) | Histórico completo de reorganizações |
| **🔍 Análises** | [Packages](analises/PACKAGES.md), [Erros](analises/ERROS_LOGS.md), [Melhorias](analises/MELHORIAS_TECNICAS.md), [Raiz](analises/ORGANIZACAO_RAIZ.md) | Análises técnicas detalhadas |
| **🚀 Melhorias** | [Fase 2](analises/MELHORIAS_APLICADAS_FASE2.md) | Melhorias aplicadas (logs, inputs) |
| **🔒 Segurança** | [Segurança](SECURITY.md) | Guia de segurança e boas práticas |

### 🚀 Por Objetivo

**Quero aprender sobre o sistema:**
- Começar por: [README.md principal](../README.md)
- Depois: [Histórico de Reorganização](historico/REORGANIZACAO.md)

**Quero entender os packages:**
- Ver: [Análise de Packages](analises/PACKAGES.md)
- Ver: [packages/README.md](../packages/README.md)

**Quero entender as automações:**
- Ver: [automations/README.md](../automations/README.md)
- Ver: [Histórico](historico/REORGANIZACAO.md#reorganização-de-automações)

**Tenho um erro para resolver:**
- Ver: [Análise de Erros e Logs](analises/ERROS_LOGS.md)
- Executar: Scripts de diagnóstico incluídos

**Quero contribuir/melhorar:**
- Ver: [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md)
- Ver: [Segurança](SECURITY.md)

---

## 📖 Documentos Principais

### 1. 📜 Histórico

#### [Reorganização Completa](historico/REORGANIZACAO.md)
**Conteúdo:**
- Reorganização de 68 automações
- Reorganização de 8 packages
- Planos A, B e C executados
- Validações e resultados
- Commits e branches

**Quando consultar:**
- Entender o que foi feito
- Ver antes/depois
- Verificar validações

---

### 2. 🔍 Análises Técnicas

#### [Análise de Packages](analises/PACKAGES.md)
**Conteúdo:**
- Análise de todos os 8 packages
- Dependências entre packages
- Problemas identificados e resolvidos
- Recomendações de melhoria
- Métricas de qualidade

**Quando consultar:**
- Criar novo package
- Modificar package existente
- Entender dependências
- Verificar convenções

#### [Análise de Erros e Logs](analises/ERROS_LOGS.md)
**Conteúdo:**
- Análise de erros do home-assistant.log
- Categorização de erros (câmaras, rede, etc.)
- Soluções priorizadas
- Scripts de diagnóstico
- Recomendações de monitorização

**Quando consultar:**
- Há erros nos logs
- Câmaras não respondem
- Entidades em falta
- Problemas de performance

#### [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md)
**Conteúdo:**
- Boas práticas YAML
- Segurança e validações
- Performance e otimização
- Modularização
- Testes e CI/CD
- Monitorização

**Quando consultar:**
- Criar nova automação
- Criar novo package
- Otimizar código
- Implementar CI/CD
- Melhorar qualidade

---

### 3. 🔒 Segurança

#### [Guia de Segurança](SECURITY.md)
**Conteúdo:**
- Ficheiros sensíveis (NUNCA versionar)
- Uso correto de secrets.yaml
- Configuração de .gitignore
- Boas práticas de segurança

**Quando consultar:**
- Antes de fazer commit
- Configurar novo repositório
- Partilhar código
- Adicionar credenciais

---

## 📊 Estatísticas da Documentação

| Documento | Linhas | Tamanho | Última Atualização |
|-----------|--------|---------|-------------------|
| **REORGANIZACAO.md** | 450+ | ~15 KB | 2025-11-11 |
| **PACKAGES.md** | 550+ | ~18 KB | 2025-11-11 |
| **ERROS_LOGS.md** | 600+ | ~20 KB | 2025-11-11 |
| **MELHORIAS_TECNICAS.md** | 700+ | ~23 KB | 2025-11-11 |
| **SECURITY.md** | 150+ | ~5 KB | 2025-11-11 |
| **automations/README.md** | 200+ | ~7 KB | 2025-11-11 |
| **packages/README.md** | 187 | ~6 KB | 2025-11-11 |

**Total:** ~2800 linhas de documentação consolidada! 📚

---

## 🗺️ Mapa da Documentação

```
docs/
├── README.md                          # ← Você está aqui
├── SECURITY.md                        # Guia de segurança
│
├── historico/                         # Histórico de mudanças
│   └── REORGANIZACAO.md               # Reorganização completa
│
└── analises/                          # Análises técnicas
    ├── PACKAGES.md                    # Análise de packages
    ├── ERROS_LOGS.md                  # Análise de erros
    └── MELHORIAS_TECNICAS.md          # Guia de melhorias

../automations/
└── README.md                          # Doc de automações

../packages/
└── README.md                          # Doc de packages
```

---

## 🔄 Fluxo de Trabalho

### Criar Nova Automação

1. ✅ Ler: [automations/README.md](../automations/README.md)
2. ✅ Consultar: [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md)
3. ✅ Adicionar em ficheiro correto de categoria
4. ✅ Validar YAML
5. ✅ Testar
6. ✅ Documentar no README

### Criar Novo Package

1. ✅ Ler: [packages/README.md](../packages/README.md)
2. ✅ Ver exemplos: [Análise de Packages](analises/PACKAGES.md)
3. ✅ Seguir convenção: `categoria_descricao.yaml`
4. ✅ Adicionar cabeçalho padronizado
5. ✅ Documentar dependências
6. ✅ Atualizar packages/README.md

### Resolver Erro

1. ✅ Verificar: [Análise de Erros](analises/ERROS_LOGS.md)
2. ✅ Executar: Scripts de diagnóstico
3. ✅ Aplicar: Solução recomendada
4. ✅ Validar: Erro resolvido
5. ✅ Documentar: Se novo tipo de erro

### Contribuir

1. ✅ Ler: [SECURITY.md](SECURITY.md)
2. ✅ Seguir: [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md)
3. ✅ Validar: YAML e testes
4. ✅ Documentar: Mudanças
5. ✅ Criar: Pull Request

---

## 🎓 Recursos de Aprendizagem

### Para Iniciantes

1. **Começar aqui:**
   - [README.md principal](../README.md) - Visão geral do sistema
   - [automations/README.md](../automations/README.md) - Entender automações
   - [packages/README.md](../packages/README.md) - Entender packages

2. **Depois explorar:**
   - [Histórico de Reorganização](historico/REORGANIZACAO.md)
   - [Análise de Packages](analises/PACKAGES.md)

### Para Utilizadores Avançados

1. **Otimização:**
   - [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md)
   - [Análise de Packages](analises/PACKAGES.md) → Recomendações

2. **Troubleshooting:**
   - [Análise de Erros](analises/ERROS_LOGS.md)
   - Scripts de diagnóstico incluídos

### Para Contribuidores

1. **Essencial:**
   - [SECURITY.md](SECURITY.md) - Evitar commits perigosos
   - [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md) - Boas práticas

2. **Recomendado:**
   - [Análise de Packages](analises/PACKAGES.md) - Padrões
   - Checklist de Boas Práticas

---

## 🔍 Procurar Informação

### Por Palavra-chave

| Procuro | Ver Documento |
|---------|---------------|
| **unique_id** | [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md) |
| **timeout** | [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md), [Packages](analises/PACKAGES.md) |
| **error handling** | [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md), [Packages](analises/PACKAGES.md) |
| **dependências** | [Packages](analises/PACKAGES.md) |
| **nomenclatura** | [Packages](analises/PACKAGES.md), [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md) |
| **secrets.yaml** | [SECURITY.md](SECURITY.md) |
| **validação** | [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md) |
| **erros câmaras** | [Erros e Logs](analises/ERROS_LOGS.md) |
| **performance** | [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md), [Erros](analises/ERROS_LOGS.md) |

### Por Componente

| Componente | Ver Documento |
|------------|---------------|
| **Automações** | [automations/README.md](../automations/README.md), [Reorganização](historico/REORGANIZACAO.md) |
| **Packages** | [packages/README.md](../packages/README.md), [Análise](analises/PACKAGES.md) |
| **AQS** | [Packages](analises/PACKAGES.md) → aqs_* |
| **Piscina** | [Packages](analises/PACKAGES.md) → piscina_* |
| **Climatização** | [Packages](analises/PACKAGES.md) → climate_comfort |
| **LLM Vision** | [Packages](analises/PACKAGES.md) → piscina_cobertura |
| **Câmaras** | [Erros e Logs](analises/ERROS_LOGS.md) |

---

## ✅ Checklist de Consulta

### Antes de Modificar Código

- [ ] Li a documentação relevante?
- [ ] Entendo as dependências?
- [ ] Sei as convenções a seguir?
- [ ] Tenho backup?

### Antes de Commitar

- [ ] Li [SECURITY.md](SECURITY.md)?
- [ ] Validei YAML?
- [ ] Atualizei documentação?
- [ ] Testei mudanças?

### Ao Encontrar Erro

- [ ] Consultei [Erros e Logs](analises/ERROS_LOGS.md)?
- [ ] Executei scripts de diagnóstico?
- [ ] Documentei solução se nova?

---

## 🆘 Ajuda Rápida

### Problemas Comuns

**"Erro ao carregar package"**
→ Ver: [Análise de Packages](analises/PACKAGES.md) → Problemas Identificados

**"Câmara não responde"**
→ Ver: [Erros e Logs](analises/ERROS_LOGS.md) → Câmaras Tapo/ONVIF

**"Entidade não encontrada"**
→ Ver: [Erros e Logs](analises/ERROS_LOGS.md) → Entidades em Falta

**"Como criar package?"**
→ Ver: [Análise de Packages](analises/PACKAGES.md) → Exemplos

**"Boas práticas YAML?"**
→ Ver: [Melhorias Técnicas](analises/MELHORIAS_TECNICAS.md)

**"O que nunca commitar?"**
→ Ver: [SECURITY.md](SECURITY.md)

---

## 📞 Suporte Adicional

- 🏠 [Home Assistant Docs](https://www.home-assistant.io/docs/)
- 💬 [Community Forum](https://community.home-assistant.io/)
- 🇵🇹 [Comunidade PT](https://www.facebook.com/groups/homeassistantportugal)

---

**Última atualização:** 11 de novembro de 2025  
**Documentos:** 7 principais + 2 READMEs  
**Total:** ~2800 linhas consolidadas
