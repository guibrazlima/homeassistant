#!/usr/bin/env python3
"""
Script para reorganizar automações do Home Assistant
Lê ficheiros YAML e organiza por categoria
"""

import yaml
import os
from pathlib import Path
import re

# Diretório base
BASE_DIR = Path("/data/homeassistant/automations")

# Mapeamento de aliases para categorias e ficheiros
CATEGORIA_MAP = {
    # PISCINA
    r".*[Pp]iscina.*[Ff]iltr.*": ("piscina", "piscina_filtragem.yaml"),
    r".*[Pp]iscina.*[Pp]erist.*": ("piscina", "piscina_bomba_peristaltica.yaml"),
    r".*[Pp]iscina.*[Tt]emperat.*": ("piscina", "piscina_temperatura.yaml"),
    r".*[Pp]iscina.*[Cc]obertura.*": ("piscina", "piscina_cobertura.yaml"),
    r".*[Pp]iscina.*": ("piscina", "piscina_geral.yaml"),
    
    # VEÍCULO ELÉTRICO
    r".*EV.*": ("veiculo_eletrico", "ev_carregamento.yaml"),
    r".*[Cc]arrega.*wallbox.*": ("veiculo_eletrico", "ev_carregamento.yaml"),
    r".*[Cc]Fos.*": ("veiculo_eletrico", "ev_carregamento.yaml"),
    
    # PORTÕES
    r".*[Pp]ort[ãa]o.*[Bb]ot[ãa]o.*": ("portoes_portarias", "portao_botoes.yaml"),
    r".*[Bb]otão.*[Pp]ort[ãa]o.*": ("portoes_portarias", "portao_botoes.yaml"),
    r".*[Pp]ort[ãa]o.*": ("portoes_portarias", "portao_principal.yaml"),
    r".*[Pp]ortaria.*": ("portoes_portarias", "portaria_video.yaml"),
    
    # ILUMINAÇÃO
    r".*[Ll]uz.*[Ss]ala.*": ("iluminacao", "luzes_interior.yaml"),
    r".*[Ll]uz.*[Qq]uarto.*": ("iluminacao", "luzes_interior.yaml"),
    r".*[Ll]uz.*[Cc]ozinha.*": ("iluminacao", "luzes_interior.yaml"),
    r".*[Ll]uz.*[Ee]scrit.*": ("iluminacao", "luzes_interior.yaml"),
    r".*[Ll]uz.*[Ee]xterior.*": ("iluminacao", "luzes_exterior.yaml"),
    r".*[Ll]uz.*[Jj]ardim.*": ("iluminacao", "luzes_exterior.yaml"),
    
    # CLIMA
    r".*AC.*": ("clima", "aquecimento_arrefecimento.yaml"),
    r".*[Aa]quec.*": ("clima", "aquecimento_arrefecimento.yaml"),
    r".*[Vv]entil.*": ("clima", "ventilacao.yaml"),
    
    # ENERGIA SOLAR
    r".*[Ss]olar.*": ("energia_solar", "paineis_solares.yaml"),
    r".*FV.*": ("energia_solar", "paineis_solares.yaml"),
    r".*[Ee]xcesso.*": ("energia_solar", "otimizacao_consumo.yaml"),
    
    # SEGURANÇA
    r".*[Aa]larme.*": ("seguranca", "alarmes.yaml"),
    r".*[Ss]eguran.*": ("seguranca", "notificacoes.yaml"),
    
    # SISTEMA
    r".*[Ww]atchdog.*": ("sistema", "watchdogs.yaml"),
    r".*[Mm]onitor.*": ("sistema", "monitorizacao.yaml"),
    r".*[Hh]or[áa]rio.*[Bb]omba.*": ("sistema", "utilidades.yaml"),
}

def gerar_id_descritivo(alias, old_id):
    """Gera ID descritivo baseado no alias"""
    # Remove emojis e caracteres especiais
    texto = re.sub(r'[^\w\s-]', '', alias.lower())
    # Remove acentos
    texto = texto.replace('ã', 'a').replace('á', 'a').replace('é', 'e')
    texto = texto.replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    texto = texto.replace('ç', 'c')
    # Substitui espaços por underscore
    texto = re.sub(r'\s+', '_', texto.strip())
    # Limita tamanho
    texto = texto[:60]
    
    return texto

def categorizar_automacao(automacao):
    """Determina categoria e ficheiro baseado no alias"""
    alias = automacao.get('alias', '')
    
    for pattern, (categoria, ficheiro) in CATEGORIA_MAP.items():
        if re.match(pattern, alias, re.IGNORECASE):
            return categoria, ficheiro
    
    # Default
    return "sistema", "outros.yaml"

def processar_ficheiro(filepath):
    """Lê ficheiro YAML e retorna lista de automações"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
            if isinstance(content, list):
                return content
            else:
                return [content] if content else []
    except Exception as e:
        print(f"❌ Erro ao ler {filepath}: {e}")
        return []

def main():
    print("🚀 Iniciando reorganização de automações...")
    print(f"📁 Diretório base: {BASE_DIR}")
    
    # Ler ficheiros existentes
    ficheiros_antigos = [
        BASE_DIR / "automations.yaml",
        BASE_DIR / "automations_root.yaml",
    ]
    
    todas_automacoes = []
    for filepath in ficheiros_antigos:
        if filepath.exists():
            print(f"📖 Lendo {filepath.name}...")
            automacoes = processar_ficheiro(filepath)
            todas_automacoes.extend(automacoes)
            print(f"   ✓ {len(automacoes)} automações encontradas")
    
    print(f"\n📊 Total: {len(todas_automacoes)} automações")
    
    # Agrupar por categoria/ficheiro
    agrupadas = {}
    for auto in todas_automacoes:
        categoria, ficheiro = categorizar_automacao(auto)
        chave = f"{categoria}/{ficheiro}"
        
        if chave not in agrupadas:
            agrupadas[chave] = []
        
        agrupadas[chave].append(auto)
    
    # Mostrar estatísticas
    print(f"\n📋 Distribuição por ficheiro:")
    for chave, autos in sorted(agrupadas.items()):
        print(f"   {chave}: {len(autos)} automações")
    
    print(f"\n✅ Análise concluída!")
    print(f"   Total de ficheiros necessários: {len(agrupadas)}")

if __name__ == "__main__":
    main()
