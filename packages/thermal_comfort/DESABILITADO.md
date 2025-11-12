# ⚠️ NOTA: Thermal Comfort Desabilitado Temporariamente

**Data:** 12 de novembro de 2025  
**Status:** ⏸️ Estrutura criada mas desabilitada

---

## 🔴 Problema

O custom component `thermal_comfort` está **incompatível** com a versão atual do Home Assistant:

```
Component thermal_comfort cannot import name 'ConfigValidationError' 
from 'homeassistant.exceptions'
```

---

## ✅ Solução Temporária

A estrutura modular foi criada mas os ficheiros foram **desabilitados** (extensão `.disabled`):

```
packages/thermal_comfort/
├─ exterior.yaml.disabled
├─ utilidade.yaml.disabled
├─ comum.yaml.disabled
├─ quartos.yaml.disabled
└─ groups.yaml (mantido para futura ativação)
```

---

## 🔧 Para Ativar No Futuro

### Opção 1: Atualizar Componente

1. Verificar versão compatível do thermal_comfort
2. Atualizar custom component em `custom_components/thermal_comfort/`
3. Renomear ficheiros `.disabled` para `.yaml`
4. Validar e reiniciar HA

```bash
cd /data/homeassistant/packages/thermal_comfort
for f in *.yaml.disabled; do mv "$f" "${f%.disabled}"; done
hass --script check_config
```

### Opção 2: Usar Template Sensors

Implementar os cálculos manualmente com templates (ver análise completa).

---

## 📚 Documentação Disponível

- **Análise Completa:** `docs/analises/THERMAL_COMFORT_ANALISE.md`
- **Guia de Uso:** `packages/thermal_comfort/README.md`
- **Backup Original:** `backups/old_configs/thermal_comfort.yaml.backup`

---

## 🎯 Estrutura Pronta

Quando o componente for atualizado, basta ativar os ficheiros:

✅ 4 ficheiros modulares por categoria  
✅ 5 divisões organizadas  
✅ Unique IDs corrigidos  
✅ Nomenclatura padronizada  
✅ Documentação completa  
✅ Grupos para dashboards  

**Total:** ~30 sensores prontos para ativar!
