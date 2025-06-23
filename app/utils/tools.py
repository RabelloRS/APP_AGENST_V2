from datetime import datetime
from typing import Any, Dict, List, Optional
import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import numpy as np
import pandas as pd
from thefuzz import fuzz, process
from crewai_tools import WebsiteSearchTool


def read_excel_column(file_path: str, column_name: str) -> list:
    """Lê uma coluna específica de um arquivo Excel."""
    try:
        df = pd.read_excel(file_path)
        if column_name not in df.columns:
            raise ValueError(
                f"Coluna '{column_name}' não encontrada. Colunas disponíveis: {list(df.columns)}"
            )
        return df[column_name].astype(str).tolist()
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo Excel: {str(e)}")


def read_excel_file(file_path: str) -> Dict[str, Any]:
    """Lê um arquivo Excel completo e retorna informações estruturadas."""
    try:
        df = pd.read_excel(file_path)
        return {
            "columns": df.columns.tolist(),
            "rows": len(df),
            "data_types": df.dtypes.astype(str).to_dict(),
            "sample_data": df.head(5).to_dict("records"),
            "summary_stats": df.describe().to_dict()
            if df.select_dtypes(include=[np.number]).shape[1] > 0
            else {},
        }
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo Excel: {str(e)}")


def compare_text_similarity(list1: list, list2: list) -> dict:
    """Compara similaridade de textos entre duas listas."""
    matches = {}
    for text in list1:
        best_match, score = process.extractOne(
            text, list2, scorer=fuzz.token_sort_ratio
        )
        matches[text] = {"match": best_match, "score": score}
    return matches


def analyze_excel_similarity(
    file1_path: str, file2_path: str, column1: str, column2: str
) -> Dict[str, Any]:
    """Análise completa de similaridade entre duas planilhas."""
    try:
        # Ler as colunas
        list1 = read_excel_column(file1_path, column1)
        list2 = read_excel_column(file2_path, column2)

        # Comparar similaridade
        similarity_results = compare_text_similarity(list1, list2)

        # Calcular estatísticas
        scores = [result["score"] for result in similarity_results.values()]

        analysis = {
            "file1_info": {
                "file": file1_path,
                "column": column1,
                "total_items": len(list1),
            },
            "file2_info": {
                "file": file2_path,
                "column": column2,
                "total_items": len(list2),
            },
            "similarity_analysis": {
                "average_score": np.mean(scores),
                "median_score": np.median(scores),
                "max_score": max(scores),
                "min_score": min(scores),
                "high_similarity_count": len([s for s in scores if s >= 80]),
                "medium_similarity_count": len([s for s in scores if 50 <= s < 80]),
                "low_similarity_count": len([s for s in scores if s < 50]),
            },
            "detailed_matches": similarity_results,
            "recommendations": generate_similarity_recommendations(scores),
        }

        return analysis

    except Exception as e:
        raise Exception(f"Erro na análise de similaridade: {str(e)}")


def generate_similarity_recommendations(scores: List[float]) -> List[str]:
    """Gera recomendações baseadas nos scores de similaridade."""
    recommendations = []

    avg_score = np.mean(scores)
    high_similarity = len([s for s in scores if s >= 80])
    total_items = len(scores)

    if avg_score >= 85:
        recommendations.append(
            "✅ Alta similaridade geral - os dados são muito similares"
        )
    elif avg_score >= 70:
        recommendations.append("⚠️ Similaridade moderada - verificar inconsistências")
    else:
        recommendations.append("❌ Baixa similaridade - possível problema nos dados")

    if high_similarity / total_items >= 0.8:
        recommendations.append("✅ Mais de 80% dos itens têm alta similaridade")
    elif high_similarity / total_items >= 0.5:
        recommendations.append("⚠️ Apenas metade dos itens têm alta similaridade")
    else:
        recommendations.append("❌ Menos da metade dos itens têm alta similaridade")

    return recommendations


def detect_data_patterns(file_path: str, column_name: str) -> Dict[str, Any]:
    """Detecta padrões nos dados de uma coluna."""
    try:
        df = pd.read_excel(file_path)
        column_data = df[column_name]

        patterns = {
            "data_type": str(column_data.dtype),
            "unique_values": column_data.nunique(),
            "null_values": column_data.isnull().sum(),
            "duplicates": column_data.duplicated().sum(),
        }

        # Detectar padrões específicos
        if column_data.dtype == "object":
            # Padrões em texto
            text_data = column_data.astype(str)
            patterns["text_patterns"] = {
                "avg_length": text_data.str.len().mean(),
                "max_length": text_data.str.len().max(),
                "min_length": text_data.str.len().min(),
                "common_prefixes": detect_common_prefixes(text_data),
                "common_suffixes": detect_common_suffixes(text_data),
            }
        elif pd.api.types.is_numeric_dtype(column_data):
            # Padrões numéricos
            numeric_data = column_data.astype(float)
            patterns["numeric_patterns"] = {
                "range": f"{numeric_data.min()} - {numeric_data.max()}",
                "distribution": "normal" if abs(numeric_data.skew()) < 1 else "skewed",
                "outliers": detect_outliers(numeric_data),
            }

        return patterns

    except Exception as e:
        raise Exception(f"Erro ao detectar padrões: {str(e)}")


def detect_common_prefixes(data: pd.Series) -> List[str]:
    """Detecta prefixos comuns em dados textuais."""
    prefixes = []
    for i in range(1, 6):  # Verificar prefixos de 1 a 5 caracteres
        prefix_counts = data.str[:i].value_counts()
        common = prefix_counts[prefix_counts >= len(data) * 0.1]  # 10% ou mais
        prefixes.extend(common.index.tolist())
    return list(set(prefixes))[:5]  # Retornar até 5 prefixos únicos


def detect_common_suffixes(data: pd.Series) -> List[str]:
    """Detecta sufixos comuns em dados textuais."""
    suffixes = []
    for i in range(1, 6):  # Verificar sufixos de 1 a 5 caracteres
        suffix_counts = data.str[-i:].value_counts()
        common = suffix_counts[suffix_counts >= len(data) * 0.1]  # 10% ou mais
        suffixes.extend(common.index.tolist())
    return list(set(suffixes))[:5]  # Retornar até 5 sufixos únicos


def detect_outliers(data: pd.Series) -> Dict[str, Any]:
    """Detecta outliers em dados numéricos."""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = data[(data < lower_bound) | (data > upper_bound)]

    return {
        "count": len(outliers),
        "percentage": len(outliers) / len(data) * 100,
        "values": outliers.tolist(),
    }


def generate_excel_report(analysis_results: Dict[str, Any]) -> str:
    """Gera um relatório estruturado da análise."""
    report = f"""
# Relatório de Análise de Dados

## Resumo Executivo
- **Arquivo 1:** {analysis_results.get('file1_info', {}).get('file', 'N/A')}
- **Arquivo 2:** {analysis_results.get('file2_info', {}).get('file', 'N/A')}
- **Score Médio de Similaridade:** {analysis_results.get('similarity_analysis', {}).get('average_score', 0):.2f}%

## Análise Detalhada
- **Similaridade Alta (≥80%):** {analysis_results.get('similarity_analysis', {}).get('high_similarity_count', 0)} itens
- **Similaridade Média (50-79%):** {analysis_results.get('similarity_analysis', {}).get('medium_similarity_count', 0)} itens
- **Similaridade Baixa (<50%):** {analysis_results.get('similarity_analysis', {}).get('low_similarity_count', 0)} itens

## Recomendações
"""
    for rec in analysis_results.get("recommendations", []):
        report += f"- {rec}\n"

    return report


def validate_excel_file(file_path: str) -> Dict[str, Any]:
    """Valida um arquivo Excel e retorna informações sobre sua estrutura."""
    try:
        df = pd.read_excel(file_path)
        
        validation = {
            "is_valid": True,
            "file_path": file_path,
            "file_size_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2),
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "duplicate_rows": df.duplicated().sum(),
            "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        }
        
        # Verificar problemas comuns
        issues = []
        if df.empty:
            issues.append("Arquivo está vazio")
        if df.isnull().sum().sum() > len(df) * 0.5:
            issues.append("Mais de 50% dos dados são nulos")
        if df.duplicated().sum() > len(df) * 0.1:
            issues.append("Mais de 10% das linhas são duplicadas")
            
        validation["issues"] = issues
        validation["has_issues"] = len(issues) > 0
        
        return validation
        
    except Exception as e:
        return {
            "is_valid": False,
            "error": str(e),
            "file_path": file_path
        }


# ============================================================================
# FERRAMENTAS PARA WHATSAPP
# ============================================================================


def whatsapp_connect(session_name: str) -> Dict[str, Any]:
    """Estabelece conexão com o WhatsApp Web."""
    try:
        # Implementação simulada para demonstração
        # Em produção, você precisaria usar selenium ou uma biblioteca específica
        
        return {
            "status": "connected",
            "session_name": session_name,
            "message": "WhatsApp Web conectado (simulação). Em produção, use selenium."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "session_name": session_name,
            "error": str(e)
        }


def whatsapp_get_messages(group_name: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Obtém mensagens de um grupo específico do WhatsApp."""
    try:
        # Esta é uma implementação simulada
        # Em produção, você precisaria usar uma biblioteca como python-whatsapp-sdk
        # ou selenium para interagir com o WhatsApp Web
        
        messages = []
        # Simular mensagens para demonstração
        for i in range(min(limit, 10)):
            messages.append({
                "id": f"msg_{i}",
                "text": f"Mensagem de exemplo {i}",
                "timestamp": datetime.now().isoformat(),
                "sender": f"Usuário {i % 3}",
                "has_file": i % 3 == 0,
                "file_name": f"arquivo_{i}.pdf" if i % 3 == 0 else None,
                "file_url": f"https://drive.google.com/file/d/example_{i}" if i % 3 == 0 else None
            })
        
        return messages
        
    except Exception as e:
        raise Exception(f"Erro ao obter mensagens: {str(e)}")


def extract_cloud_links(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extrai links de serviços em nuvem das mensagens."""
    cloud_links = []
    
    # Padrões para diferentes serviços de nuvem
    patterns = {
        "google_drive": r"https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)",
        "google_drive_share": r"https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)",
        "onedrive": r"https://1drv\.ms/[a-zA-Z0-9_-]+",
        "dropbox": r"https://www\.dropbox\.com/[a-zA-Z0-9_-]+",
        "mega": r"https://mega\.nz/[a-zA-Z0-9_-]+",
        "mediafire": r"https://www\.mediafire\.com/[a-zA-Z0-9_-]+"
    }
    
    for message in messages:
        text = message.get("text", "")
        
        for service, pattern in patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                cloud_links.append({
                    "message_id": message.get("id"),
                    "service": service,
                    "url": match if service == "google_drive" else text,
                    "timestamp": message.get("timestamp"),
                    "sender": message.get("sender")
                })
    
    return cloud_links


def download_cloud_file(cloud_link: str, output_path: str) -> Dict[str, Any]:
    """Baixa arquivo de serviços em nuvem."""
    try:
        # Criar diretório se não existir
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        # Extrair nome do arquivo da URL
        parsed_url = urlparse(cloud_link)
        
        if "drive.google.com" in cloud_link:
            # Google Drive
            file_id = parse_qs(parsed_url.query).get('id', [None])[0]
            if not file_id:
                # Tentar extrair do path
                path_parts = parsed_url.path.split('/')
                file_id = path_parts[-1] if path_parts else None
            
            if file_id:
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                response = requests.get(download_url, stream=True)
                
                # Tentar obter nome do arquivo do header
                filename = response.headers.get('content-disposition', '')
                if 'filename=' in filename:
                    filename = filename.split('filename=')[1].strip('"')
                else:
                    filename = f"google_drive_file_{file_id}"
                
                file_path = os.path.join(output_path, filename)
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return {
                    "status": "success",
                    "file_path": file_path,
                    "file_size": os.path.getsize(file_path),
                    "source": "google_drive"
                }
        
        # Para outros serviços, implementar conforme necessário
        return {
            "status": "not_implemented",
            "message": f"Download para {parsed_url.netloc} não implementado ainda"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "cloud_link": cloud_link
        }


def download_whatsapp_file(message: Dict[str, Any], output_path: str) -> Dict[str, Any]:
    """Baixa arquivo anexado a uma mensagem do WhatsApp."""
    try:
        # Criar diretório se não existir
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        if not message.get("has_file"):
            return {
                "status": "no_file",
                "message": "Mensagem não contém arquivo"
            }
        
        # Em produção, você precisaria implementar a lógica real de download
        # do WhatsApp Web usando selenium ou uma biblioteca específica
        
        # Simulação para demonstração
        filename = message.get("file_name", "arquivo_whatsapp")
        file_path = os.path.join(output_path, filename)
        
        # Criar arquivo de exemplo
        with open(file_path, 'w') as f:
            f.write(f"Arquivo baixado do WhatsApp - {message.get('timestamp')}")
        
        return {
            "status": "success",
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "source": "whatsapp",
            "original_message": message.get("id")
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message_id": message.get("id")
        }


def rename_file_with_timestamp(file_path: str, timestamp: str) -> str:
    """Adiciona timestamp ao nome do arquivo."""
    try:
        # Converter timestamp para formato de data/hora
        if isinstance(timestamp, str):
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        else:
            dt = timestamp
        
        # Formatar data/hora
        timestamp_str = dt.strftime("%Y%m%d_%H%M%S")
        
        # Obter extensão do arquivo
        file_ext = Path(file_path).suffix
        file_name = Path(file_path).stem
        
        # Criar novo nome
        new_name = f"{timestamp_str}_{file_name}{file_ext}"
        new_path = Path(file_path).parent / new_name
        
        # Renomear arquivo
        Path(file_path).rename(new_path)
        
        return str(new_path)
        
    except Exception as e:
        raise Exception(f"Erro ao renomear arquivo: {str(e)}")


def organize_files_by_date(files_list: List[Dict[str, Any]], base_path: str) -> Dict[str, Any]:
    """Organiza arquivos em pastas por data de download."""
    try:
        organized_files = {}
        
        for file_info in files_list:
            file_path = file_info.get("file_path")
            timestamp = file_info.get("timestamp")
            
            if not file_path or not timestamp:
                continue

            # Converter timestamp para data
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = timestamp
            
            # Criar pasta por data
            date_folder = dt.strftime("%Y-%m-%d")
            folder_path = Path(base_path) / date_folder
            folder_path.mkdir(parents=True, exist_ok=True)
            
            # Mover arquivo para pasta
            file_name = Path(file_path).name
            new_file_path = folder_path / file_name
            
            if Path(file_path).exists():
                Path(file_path).rename(new_file_path)
                organized_files[file_path] = str(new_file_path)

        return {
            "status": "success",
            "organized_files": organized_files,
            "base_path": base_path
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "files_list": files_list
        }


def simple_research_tool(topic: str) -> str:
    """
    Ferramenta de pesquisa simples que utiliza o WebsiteSearchTool do CrewAI para pesquisar um tópico na web.
    """
    try:
        # Verificar se o tópico é válido
        if not topic or len(topic.strip()) < 3:
            return f"Erro: Tópico de pesquisa muito curto ou vazio. Forneça um tópico com pelo menos 3 caracteres."

        # Criar instância da ferramenta
        try:
            search_tool = WebsiteSearchTool()
        except Exception as tool_error:
            return f"Erro ao inicializar WebsiteSearchTool: {tool_error}"

        # Executar pesquisa
        try:
            print(f"🔍 Executando pesquisa web para: {topic}")
            result = search_tool.run(topic)
            if result and len(str(result)) > 20:
                return str(result)
            else:
                return f"Pesquisa para '{topic}' retornou resultado vazio ou muito curto. Tente reformular a pesquisa."
        except Exception as search_error:
            return f"Erro na execução da pesquisa para '{topic}': {search_error}"
    except Exception as e:
        return f"Erro geral na pesquisa para '{topic}': {e}"


# === FERRAMENTAS DE AVALIAÇÃO DE CREWS ===

def crew_performance_analyzer(
    execution_data: dict, performance_metrics: Optional[list] = None
) -> str:
    """
    Analisa a performance geral da crew, tempo de execução, qualidade das entregas e colaboração entre agentes
    """
    try:
        if performance_metrics is None:
            performance_metrics = ['efficiency', 'quality', 'collaboration', 'completeness']
        
        analysis = {
            'execution_time': execution_data.get('duration', 'N/A'),
            'status': execution_data.get('status', 'unknown'),
            'agents_count': execution_data.get('agents_count', 0),
            'tasks_count': execution_data.get('tasks_count', 0),
            'success_rate': 'N/A'
        }
        
        report = f"""
=== ANÁLISE DE PERFORMANCE DA CREW ===

📊 MÉTRICAS GERAIS:
• Tempo de Execução: {analysis['execution_time']}
• Status da Execução: {analysis['status']}
• Número de Agentes: {analysis['agents_count']}
• Número de Tarefas: {analysis['tasks_count']}

📈 ANÁLISE DE PERFORMANCE:
• Eficiência Temporal: {'Boa' if 'completed' in analysis['status'] else 'Necessita Melhoria'}
• Qualidade da Entrega: {'Analisando outputs individuais...'}
• Colaboração entre Agentes: {'Sem conflitos detectados' if analysis['agents_count'] > 1 else 'Agente único'}

🎯 INDICADORES-CHAVE:
• Completude das Tarefas: {'100%' if analysis['status'] == 'completed' else 'Incompleto'}
• Uso de Recursos: {'Otimizado' if analysis['execution_time'] else 'A analisar'}
        """
        
        return report.strip()
        
    except Exception as e:
        return f"Erro na análise de performance da crew: {str(e)}"

def agent_output_quality_checker(
    agent_outputs: dict, quality_criteria: Optional[list] = None
) -> str:
    """
    Avalia a qualidade, completude e relevância dos outputs produzidos por cada agente individualmente
    """
    try:
        if quality_criteria is None:
            quality_criteria = ['relevance', 'completeness', 'accuracy', 'clarity']
        
        analysis_report = "=== ANÁLISE DE QUALIDADE DOS OUTPUTS DOS AGENTES ===\n\n"
        
        for agent_name, output in agent_outputs.items():
            output_length = len(str(output)) if output else 0
            
            quality_score = min(100, max(10, output_length / 10))  # Score básico baseado no tamanho
            
            analysis_report += f"""
🤖 AGENTE: {agent_name}
• Tamanho do Output: {output_length} caracteres
• Score de Qualidade: {quality_score:.1f}/100
• Completude: {'Boa' if output_length > 100 else 'Insuficiente'}
• Relevância: {'A verificar conteúdo específico'}
• Clareza: {'Boa' if output_length > 50 else 'Limitada'}

"""
        
        return analysis_report
        
    except Exception as e:
        return f"Erro na verificação de qualidade dos outputs: {str(e)}"

def tool_usage_evaluator(
    tools_used: dict, task_requirements: Optional[dict] = None
) -> str:
    """
    Analisa se as ferramentas foram utilizadas adequadamente por cada agente
    """
    try:
        evaluation_report = "=== AVALIAÇÃO DO USO DE FERRAMENTAS ===\n\n"
        
        for agent_name, agent_tools in tools_used.items():
            evaluation_report += f"""
🔧 AGENTE: {agent_name}
• Ferramentas Disponíveis: {len(agent_tools) if agent_tools else 0}
• Ferramentas Listadas: {', '.join(agent_tools) if agent_tools else 'Nenhuma'}
• Adequação: {'Adequado' if agent_tools else 'Sem ferramentas - PROBLEMA!'}
• Sugestões: {'Verificar se as ferramentas são específicas para as tarefas executadas'}

"""
        
        # Recomendações gerais
        evaluation_report += """
🎯 RECOMENDAÇÕES GERAIS:
• Verificar se cada agente tem as ferramentas adequadas para sua especialização
• Considerar adicionar ferramentas de validação e verificação
• Avaliar se existem ferramentas subutilizadas que poderiam melhorar a performance
• Implementar ferramentas de colaboração entre agentes quando necessário
        """
        
        return evaluation_report
        
    except Exception as e:
        return f"Erro na avaliação do uso de ferramentas: {str(e)}"

def workflow_efficiency_analyzer(
    workflow_data: dict, execution_timeline: Optional[list] = None
) -> str:
    """
    Avalia a eficiência do fluxo de trabalho entre agentes, identificando gargalos e pontos de melhoria
    """
    try:
        analysis_report = "=== ANÁLISE DE EFICIÊNCIA DO FLUXO DE TRABALHO ===\n\n"
        
        # Análise básica do fluxo
        agents_count = workflow_data.get('agents_count', 0)
        tasks_count = workflow_data.get('tasks_count', 0)
        duration = workflow_data.get('duration', 'N/A')
        
        analysis_report += f"""
📋 VISÃO GERAL DO FLUXO:
• Agentes Envolvidos: {agents_count}
• Tarefas Executadas: {tasks_count}
• Duração Total: {duration}
• Paralelização: {'Possível' if agents_count > 1 else 'Limitada (agente único)'}

🔍 ANÁLISE DE EFICIÊNCIA:
• Sequenciamento: {'Sequencial' if tasks_count > 1 else 'Tarefa única'}
• Gargalos Identificados: {'Analisando dependências...'}
• Oportunidades de Otimização: {'Verificar possibilidade de execução paralela'}

💡 SUGESTÕES DE MELHORIA:
• Considerar paralelização de tarefas independentes
• Verificar se a ordem das tarefas está otimizada
• Avaliar se há agentes subutilizados
• Implementar sistema de feedback entre agentes
        """
        
        return analysis_report
        
    except Exception as e:
        return f"Erro na análise de eficiência do fluxo: {str(e)}"

def recommendation_generator(
    analysis_results: dict, improvement_areas: Optional[list] = None
) -> str:
    """
    Gera recomendações específicas e acionáveis para melhorar agentes, ferramentas e tarefas
    """
    try:
        if improvement_areas is None:
            improvement_areas = ['agents', 'tools', 'tasks', 'workflow']
        
        recommendations = "=== RECOMENDAÇÕES DE MELHORIA ===\n\n"
        
        # Recomendações para Agentes
        recommendations += """
🤖 MELHORIAS NOS AGENTES:
1. CONFIGURAÇÃO:
   • Revisar backstory para ser mais específico e detalhado
   • Ajustar goals para serem mais precisos e mensuráveis
   • Verificar se o role está alinhado com as tarefas executadas

2. ESPECIALIZAÇÃO:
   • Considerar criar agentes mais especializados para tarefas específicas
   • Avaliar se há sobreposição de responsabilidades entre agentes
   • Verificar se os agentes têm conhecimento suficiente para suas tarefas

"""
        
        # Recomendações para Ferramentas
        recommendations += """
🔧 OTIMIZAÇÃO DE FERRAMENTAS:
1. ADEQUAÇÃO:
   • Verificar se cada agente tem todas as ferramentas necessárias
   • Considerar adicionar ferramentas de validação específicas
   • Implementar ferramentas de comunicação entre agentes

2. EFICIÊNCIA:
   • Avaliar ferramentas que podem acelerar o processo
   • Considerar ferramentas de automação para tarefas repetitivas
   • Implementar ferramentas de controle de qualidade

"""
        
        # Recomendações para Tarefas
        recommendations += """
📋 REFINAMENTO DE TAREFAS:
1. CLAREZA:
   • Tornar descrições mais específicas e detalhadas
   • Definir outputs esperados de forma mais precisa
   • Incluir critérios de qualidade nas descrições

2. ESTRUTURA:
   • Considerar dividir tarefas complexas em subtarefas
   • Verificar dependências entre tarefas
   • Implementar sistema de validação de entregas

"""
        
        # Priorização
        recommendations += """
🎯 PRIORIZAÇÃO DAS MELHORIAS:
1. ALTA PRIORIDADE:
   • Corrigir agentes sem ferramentas adequadas
   • Melhorar descrições de tarefas pouco claras
   • Implementar validações de qualidade

2. MÉDIA PRIORIDADE:
   • Otimizar fluxo de trabalho
   • Adicionar ferramentas de eficiência
   • Refinar backstories dos agentes

3. BAIXA PRIORIDADE:
   • Implementar funcionalidades avançadas
   • Otimizações de performance menores
   • Melhorias cosméticas na documentação
        """
        
        return recommendations
        
    except Exception as e:
        return f"Erro na geração de recomendações: {str(e)}"

def execution_summary_builder(crew_data: dict, execution_results: dict) -> str:
    """
    Constrói um resumo estruturado e detalhado da execução da crew para análise
    """
    try:
        summary = "=== RESUMO ESTRUTURADO DA EXECUÇÃO ===\n\n"
        
        # Informações básicas
        summary += f"""
📊 INFORMAÇÕES BÁSICAS:
• Crew: {crew_data.get('name', 'N/A')}
• Tópico: {execution_results.get('topic', 'N/A')}
• Status: {execution_results.get('status', 'N/A')}
• Duração: {execution_results.get('duration', 'N/A')}
• Timestamp: {execution_results.get('timestamp', 'N/A')}

"""
        
        # Análise dos agentes
        agents = crew_data.get('agents', [])
        summary += f"👥 AGENTES ENVOLVIDOS ({len(agents)}):\n"
        for i, agent in enumerate(agents, 1):
            agent_role = getattr(agent, 'role', 'N/A') if hasattr(agent, 'role') else 'N/A'
            agent_tools = getattr(agent, 'tools', []) if hasattr(agent, 'tools') else []
            summary += f"   {i}. {agent_role} - {len(agent_tools)} ferramentas\n"
        
        summary += "\n"
        
        # Análise das tarefas
        tasks = crew_data.get('tasks', [])
        summary += f"📋 TAREFAS EXECUTADAS ({len(tasks)}):\n"
        for i, task in enumerate(tasks, 1):
            task_desc = getattr(task, 'description', 'N/A') if hasattr(task, 'description') else 'N/A'
            summary += f"   {i}. {task_desc[:100]}{'...' if len(task_desc) > 100 else ''}\n"
        
        summary += "\n"
        
        # Resultado final
        result = execution_results.get('result', '')
        result_length = len(str(result))
        summary += f"""
📄 RESULTADO FINAL:
• Tamanho do Output: {result_length} caracteres
• Qualidade Aparente: {'Boa' if result_length > 500 else 'Limitada' if result_length > 100 else 'Insuficiente'}
• Completude: {'Completo' if result_length > 200 else 'Incompleto'}
"""
        
        return summary
        
    except Exception as e:
        return f"Erro na construção do resumo de execução: {str(e)}"
