# ======================================================================
# 📚 SCRIPTS - README
# ======================================================================
# Estrutura de Scripts Modularizados
# Migrado em: 2026-01-13
# ======================================================================

## 📁 Estrutura

```
scripts/
  ├── piscina.yaml        - Scripts de controlo da piscina (3 scripts)
  └── README.md           - Este ficheiro
```

## 📋 Scripts Disponíveis

### 🏊 Piscina (piscina.yaml)

| Script | Alias | Descrição |
|--------|-------|-----------|
| `alternar_modo_automacao_piscina` | Alternar Entre Modo Piscina Manual e Automático | Alterna entre controlo manual/automático |
| `piscina_manual_start` | Piscina - Manual (arrancar com tempo) | Inicia bomba com duração (1-600 min) |
| `piscina_manual_stop` | Piscina - Manual (parar) | Para bomba e cancela timer |

## 🔄 Migração

**Origem:** `scripts.yaml` (root) - 114 linhas monolítico  
**Destino:** `scripts/` directory - modular por categoria

**Status:**
- ✅ Piscina (3 scripts) → `scripts/piscina.yaml`
- ⏳ Clima (a adicionar quando necessário)
- ⏳ Energia (a adicionar quando necessário)
- ⏳ Portões (a adicionar quando necessário)

## 📝 Como Adicionar Novos Scripts

1. **Criar ficheiro por categoria:**
   ```bash
   touch scripts/clima.yaml
   ```

2. **Adicionar scripts no formato:**
   ```yaml
   nome_script:
     alias: "Nome Amigável"
     description: "Descrição detalhada"
     mode: restart  # opcional
     fields:        # opcional
       parametro:
         description: "..."
     sequence:
       - service: ...
   ```

3. **Não é necessário alterar `configuration.yaml`** - já usa:
   ```yaml
   script: !include_dir_merge_named scripts/
   ```

## 🎯 Boas Práticas

- ✅ Um ficheiro por categoria funcional
- ✅ Cabeçalho com descrição e metadata
- ✅ Comentários explicativos em lógica complexa
- ✅ Campo `description` em todos os scripts
- ✅ Validação de parâmetros (min/max)
- ✅ Mode (`restart`, `single`, `parallel`) quando necessário

## 🔍 Validação

```bash
# Validar configuração
docker exec homeassistant ha core check

# Recarregar scripts sem restart
docker exec homeassistant ha core reload scripts
```

## 📚 Documentação Oficial

- [Scripts Documentation](https://www.home-assistant.io/integrations/script/)
- [Script Syntax](https://www.home-assistant.io/docs/scripts/)
