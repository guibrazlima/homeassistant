#!/usr/bin/env python3
"""
Script para reorganizar automações do Home Assistant - Fase 2
Categoriza, adiciona IDs descritivos e descrições
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple
import unicodedata

# Diretório base
BASE_DIR = Path("/data/homeassistant/automations")

# Mapeamento de categorias (regex do alias -> categoria/ficheiro)
CATEGORIAS = {
    # PORTÕES E PORTARIAS
    r".*[Cc]allback.*gate.*": ("portoes_portarias", "portao_principal.yaml"),
    r".*[Gg]arage.*light.*gate.*": ("portoes_portarias", "portao_principal.yaml"),
    r".*[Pp]ort[ãaá]o.*": ("portoes_portarias", "portao_principal.yaml"),
    r".*[Gg]ate.*": ("portoes_portarias", "portao_principal.yaml"),
    r".*[Pp]ortaria.*": ("portoes_portarias", "portaria_video.yaml"),
    
    # VEÍCULO ELÉTRICO
    r".*[Cc]arro.*carregador.*": ("veiculo_eletrico", "ev_carregamento.yaml"),
    r".*wallbox.*": ("veiculo_eletrico", "ev_carregamento.yaml"),
    r".*[Cc][Ff]os.*": ("veiculo_eletrico", "ev_carregamento.yaml"),
    r".*EV.*": ("veiculo_eletrico", "ev_carregamento.yaml"),
    r".*[Cc]arrega.*excesso.*": ("veiculo_eletrico", "ev_excesso_solar.yaml"),
    
    # PISCINA
    r".*[Pp]iscina.*[Ff]iltr.*": ("piscina", "piscina_filtragem.yaml"),
    r".*[Pp]iscina.*[Pp]erist.*": ("piscina", "piscina_bomba_peristaltica.yaml"),
    r".*[Pp]iscina.*[Bb]omba.*": ("piscina", "piscina_bomba_peristaltica.yaml"),
    r".*[Pp]iscina.*[Tt]emperat.*": ("piscina", "piscina_temperatura.yaml"),
    r".*[Pp]iscina.*[Cc]obertura.*": ("piscina", "piscina_cobertura.yaml"),
    r".*[Pp]iscina.*": ("piscina", "piscina_geral.yaml"),
    
    # ILUMINAÇÃO
    r".*[Ll]ight.*": ("iluminacao", "luzes_geral.yaml"),
    r".*[Ll]uz.*[Ss]ala.*": ("iluminacao", "luzes_interior.yaml"),
    r".*[Ll]uz.*[Qq]uarto.*": ("iluminacao", "luzes_interior.yaml"),
    r".*[Ll]uz.*[Cc]ozinha.*": ("iluminacao", "luzes_interior.yaml"),
    r".*[Ll]uz.*[Gg]aragem.*": ("iluminacao", "luzes_interior.yaml"),
    r".*[Ll]uz.*[Ee]xterior.*": ("iluminacao", "luzes_exterior.yaml"),
    r".*[Ll]uz.*[Ee]xternal.*": ("iluminacao", "luzes_exterior.yaml"),
    
    # CLIMA
    r".*AC.*": ("clima", "aquecimento_arrefecimento.yaml"),
    r".*[Aa]quec.*": ("clima", "aquecimento_arrefecimento.yaml"),
    r".*[Aa]rrefe.*": ("clima", "aquecimento_arrefecimento.yaml"),
    r".*[Vv]entil.*": ("clima", "ventilacao.yaml"),
    
    # ENERGIA SOLAR
    r".*[Ss]olar.*": ("energia_solar", "paineis_solares.yaml"),
    r".*FV.*": ("energia_solar", "paineis_solares.yaml"),
    r".*[Ww]atchdog.*FV.*": ("energia_solar", "paineis_solares.yaml"),
    r".*[Ee]xcesso.*": ("energia_solar", "otimizacao_consumo.yaml"),
    
    # SEGURANÇA
    r".*[Aa]larme.*": ("seguranca", "alarmes.yaml"),
    r".*[Ss]ecurity.*": ("seguranca", "alarmes.yaml"),
    
    # SISTEMA
    r".*[Ss]peed[Tt]est.*": ("sistema", "monitorizacao.yaml"),
    r".*[Ww]atchdog.*": ("sistema", "watchdogs.yaml"),
    r".*[Mm]onitor.*": ("sistema", "monitorizacao.yaml"),
}

def remover_acentos(texto: str) -> str:
    """Remove acentos de uma string"""
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def gerar_id_descritivo(alias: str, old_id: str) -> str:
    """Gera ID descritivo baseado no alias"""
    # Remove emojis e caracteres especiais
    texto = re.sub(r'[^\w\s-]', '', alias)
    # Remove acentos
    texto = remover_acentos(texto)
    # Lowercase
    texto = texto.lower()
    # Remove espaços extras
    texto = re.sub(r'\s+', '_', texto.strip())
    # Remove underscores múltiplos
    texto = re.sub(r'_+', '_', texto)
    # Limita tamanho
    texto = texto[:50]
    # Remove underscore no início/fim
    texto = texto.strip('_')
    
    return texto if texto else f"auto_{old_id}"

def gerar_descricao_base(automacao: Dict) -> str:
    """Gera descrição básica se não existir"""
    alias = automacao.get('alias', '')
    trigger = automacao.get('trigger', [])
    
    if not isinstance(trigger, list):
        trigger = [trigger]
    
    # Tenta identificar tipo de trigger
    trigger_info = []
    for t in trigger:
        if isinstance(t, dict):
            platform = t.get('platform', '')
            if platform == 'state':
                entity = t.get('entity_id', 'entidade')
                trigger_info.append(f"mudança de estado em {entity}")
            elif platform == 'time':
                at_time = t.get('at', 'horário definido')
                trigger_info.append(f"horário ({at_time})")
            elif platform == 'numeric_state':
                entity = t.get('entity_id', 'sensor')
                trigger_info.append(f"valor numérico de {entity}")
            elif platform == 'event':
                event_type = t.get('event_type', 'evento')
                trigger_info.append(f"evento {event_type}")
    
    if trigger_info:
        desc = f"Automação ativada por {', '.join(trigger_info[:2])}."
    else:
        desc = "Automação do Home Assistant."
    
    return desc

def categorizar_automacao(automacao: Dict) -> Tuple[str, str]:
    """Determina categoria e ficheiro baseado no alias"""
    alias = automacao.get('alias', '')
    
    for pattern, (categoria, ficheiro) in CATEGORIAS.items():
        if re.match(pattern, alias, re.IGNORECASE):
            return categoria, ficheiro
    
    # Default
    return "sistema", "outros.yaml"

def processar_automacao(automacao: Dict) -> Dict:
    """Processa uma automação adicionando melhorias"""
    # Gerar novo ID se for numérico
    old_id = automacao.get('id', '')
    if old_id.isdigit() or not old_id:
        alias = automacao.get('alias', '')
        novo_id = gerar_id_descritivo(alias, old_id)
        automacao['id'] = novo_id
    
    # Adicionar descrição se vazia
    if not automacao.get('description') or automacao.get('description') == '':
        automacao['description'] = gerar_descricao_base(automacao)
    
    # Adicionar mode se não existir
    if 'mode' not in automacao:
        automacao['mode'] = 'single'
    
    # Adicionar max_exceeded se mode for single e não existir
    if automacao.get('mode') == 'single' and 'max_exceeded' not in automacao:
        automacao['max_exceeded'] = 'warning'
    
    return automacao

def ler_yaml(filepath: Path) -> List[Dict]:
    """Lê ficheiro YAML e retorna lista de automações"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
            if isinstance(content, list):
                return content
            elif content:
                return [content]
            else:
                return []
    except Exception as e:
        print(f"❌ Erro ao ler {filepath}: {e}")
        return []

def escrever_yaml(filepath: Path, automacoes: List[Dict], header: str = ""):
    """Escreve automações em ficheiro YAML"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        if header:
            f.write(header)
            f.write("\n")
        
        yaml.dump(automacoes, f, 
                  allow_unicode=True,
                  default_flow_style=False,
                  sort_keys=False,
                  width=float("inf"))

def criar_header(categoria: str, ficheiro: str, num_automacoes: int) -> str:
    """Cria header para ficheiro YAML"""
    emojis = {
        "portoes_portarias": "🚪",
        "veiculo_eletrico": "🚗",
        "piscina": "🏊",
        "iluminacao": "💡",
        "clima": "🌡️",
        "energia_solar": "☀️",
        "seguranca": "🔐",
        "sistema": "⚙️"
    }
    
    nomes = {
        "portoes_portarias": "PORTÕES E PORTARIAS",
        "veiculo_eletrico": "VEÍCULO ELÉTRICO",
        "piscina": "PISCINA",
        "iluminacao": "ILUMINAÇÃO",
        "clima": "CLIMA",
        "energia_solar": "ENERGIA SOLAR",
        "seguranca": "SEGURANÇA",
        "sistema": "SISTEMA"
    }
    
    emoji = emojis.get(categoria, "📁")
    nome = nomes.get(categoria, categoria.upper())
    
    return f"""# {'=' * 70}
# {emoji} {nome}
# {'=' * 70}
# Ficheiro: {ficheiro}
# Automações: {num_automacoes}
# Última atualização: 2025-11-11
# Migrado automaticamente - Fase 2
# {'=' * 70}

"""

def main():
    print("🚀 Iniciando Fase 2 - Categorização e Melhorias...")
    print("=" * 70)
    
    # Ler ficheiros migrados
    ficheiros_migrados = [
        BASE_DIR / "sistema" / "todas_automacoes_migradas.yaml",
        BASE_DIR / "sistema" / "automacoes_root_migradas.yaml"
    ]
    
    todas_automacoes = []
    for filepath in ficheiros_migrados:
        if filepath.exists():
            print(f"\n📖 Lendo {filepath.name}...")
            automacoes = ler_yaml(filepath)
            print(f"   ✓ {len(automacoes)} automações encontradas")
            todas_automacoes.extend(automacoes)
    
    print(f"\n📊 Total de automações a processar: {len(todas_automacoes)}")
    print("=" * 70)
    
    # Agrupar por categoria/ficheiro
    agrupadas = {}
    for auto in todas_automacoes:
        # Processar automação (adicionar IDs, descrições, mode)
        auto_processada = processar_automacao(auto)
        
        # Categorizar
        categoria, ficheiro = categorizar_automacao(auto_processada)
        chave = f"{categoria}/{ficheiro}"
        
        if chave not in agrupadas:
            agrupadas[chave] = []
        
        agrupadas[chave].append(auto_processada)
        
        alias = auto_processada.get('alias', 'Sem alias')
        novo_id = auto_processada.get('id', 'sem_id')
        print(f"   ✓ {alias[:50]:<50} → {chave}")
    
    print("\n" + "=" * 70)
    print("📋 Distribuição por ficheiro:")
    print("=" * 70)
    for chave, autos in sorted(agrupadas.items()):
        print(f"   {chave:<45} {len(autos):>3} automações")
    
    # Escrever ficheiros
    print("\n" + "=" * 70)
    print("💾 Criando ficheiros...")
    print("=" * 70)
    
    for chave, autos in agrupadas.items():
        categoria, ficheiro = chave.split('/')
        filepath = BASE_DIR / categoria / ficheiro
        
        # Criar header
        header = criar_header(categoria, ficheiro, len(autos))
        
        # Escrever
        escrever_yaml(filepath, autos, header)
        print(f"   ✓ Criado: {chave} ({len(autos)} automações)")
    
    print("\n" + "=" * 70)
    print("✅ FASE 2 CONCLUÍDA!")
    print("=" * 70)
    print(f"   📊 {len(todas_automacoes)} automações processadas")
    print(f"   📁 {len(agrupadas)} ficheiros criados")
    print(f"   ✨ IDs descritivos adicionados")
    print(f"   📝 Descrições geradas")
    print(f"   ⚙️  Mode e max_exceeded configurados")
    print("=" * 70)

if __name__ == "__main__":
    main()
