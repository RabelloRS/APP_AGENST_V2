"""
Exemplo de demonstração do MVP - Análise de Planilhas Excel

Desenvolvido pela Propor Engenharia
Responsável Técnico: Eng. Civil Rodrigo Emanuel Rabello
CREA-RS: 167.175-D | CNPJ: 41.556.670/0001-76
"""

import os
import sys
from pathlib import Path

import pandas as pd

# Adicionar o diretório raiz ao path para importar o módulo app
sys.path.append(str(Path(__file__).parent.parent))

# Importar as ferramentas do sistema
from app.utils.tools import (analyze_excel_similarity, detect_data_patterns,
                             generate_excel_report, validate_excel_file)


def create_sample_excel_files():
    """Cria arquivos Excel de exemplo para demonstração"""

    # Criar dados de exemplo - Lista de materiais de construção
    materials_old = {
        "Material": [
            "Cimento Portland CP-II",
            "Areia Média",
            "Brita 1",
            "Aço CA-50",
            "Tijolo Cerâmico",
            "Argamassa",
            "Tinta Acrílica",
            "Telha Cerâmica",
            "Viga Pré-moldada",
            "Bloco de Concreto",
        ],
        "Quantidade": [50, 100, 80, 2000, 5000, 30, 20, 200, 10, 800],
        "Unidade": [
            "sacos",
            "m³",
            "m³",
            "kg",
            "un",
            "sacos",
            "galões",
            "un",
            "un",
            "un",
        ],
        "Preço_Unit": [
            25.50,
            45.00,
            65.00,
            3.20,
            0.85,
            18.00,
            45.00,
            2.50,
            150.00,
            1.20,
        ],
    }

    materials_new = {
        "Material": [
            "Cimento Portland CP-II",
            "Areia Média",
            "Brita 1",
            "Aço CA-50",
            "Tijolo Cerâmico",
            "Argamassa",
            "Tinta Acrílica",
            "Telha Cerâmica",
            "Viga Pré-moldada",
            "Bloco de Concreto",
            "Cimento CP-III",  # Novo material
            "Tinta Esmalte",  # Novo material
        ],
        "Quantidade": [45, 95, 75, 2100, 4800, 28, 22, 180, 12, 750, 30, 15],
        "Unidade": [
            "sacos",
            "m³",
            "m³",
            "kg",
            "un",
            "sacos",
            "galões",
            "un",
            "un",
            "un",
            "sacos",
            "galões",
        ],
        "Preço_Unit": [
            26.00,
            47.00,
            68.00,
            3.25,
            0.88,
            19.00,
            48.00,
            2.60,
            155.00,
            1.25,
            28.00,
            52.00,
        ],
    }

    # Criar DataFrames
    df_old = pd.DataFrame(materials_old)
    df_new = pd.DataFrame(materials_new)

    # Salvar arquivos temporários
    temp_dir = Path("temp_examples")
    temp_dir.mkdir(exist_ok=True)

    file1_path = temp_dir / "materiais_antigos.xlsx"
    file2_path = temp_dir / "materiais_novos.xlsx"

    df_old.to_excel(file1_path, index=False)
    df_new.to_excel(file2_path, index=False)

    return str(file1_path), str(file2_path)


def demonstrate_excel_analysis():
    """Demonstra a análise completa de planilhas Excel"""

    print("🏗️ Demonstração do MVP - Agentes de Engenharia da Propor")
    print("📞 Propor Engenharia - Eng. Civil Rodrigo Emanuel Rabello")
    print("=" * 70)

    # Criar arquivos de exemplo
    print("📁 Criando arquivos de exemplo...")
    file1_path, file2_path = create_sample_excel_files()

    print("✅ Arquivo 1 criado: " + file1_path)
    print("✅ Arquivo 2 criado: " + file2_path)

    # Validar arquivos
    print("\n🔍 Validando arquivos...")
    validation1 = validate_excel_file(file1_path)
    validation2 = validate_excel_file(file2_path)

    if validation1["is_valid"] and validation2["is_valid"]:
        print(
            "✅ Arquivo 1: "
            + str(validation1["total_rows"])
            + " linhas, "
            + str(validation1["total_columns"])
            + " colunas"
        )
        print(
            "✅ Arquivo 2: "
            + str(validation2["total_rows"])
            + " linhas, "
            + str(validation2["total_columns"])
            + " colunas"
        )
    else:
        print("❌ Erro na validação dos arquivos")
        return

    # Analisar similaridade
    print("\n📊 Analisando similaridade entre as colunas 'Material'...")
    try:
        analysis_results = analyze_excel_similarity(
            file1_path, file2_path, "Material", "Material"
        )

        print("✅ Análise concluída!")
        print(
            "📈 Score médio de similaridade: "
            + str(analysis_results["similarity_analysis"]["average_score"])
            + "%"
        )
        print(
            "🎯 Itens com alta similaridade (≥80%): "
            + str(analysis_results["similarity_analysis"]["high_similarity_count"])
        )

        # Detectar padrões
        print("\n🔍 Detectando padrões nos dados...")
        patterns1 = detect_data_patterns(file1_path, "Material")
        patterns2 = detect_data_patterns(file2_path, "Material")

        print("📊 Padrões detectados no arquivo 1:")
        print("   - Tipo de dados: " + patterns1["data_type"])
        print("   - Valores únicos: " + str(patterns1["unique_values"]))
        print("   - Valores nulos: " + str(patterns1["null_values"]))

        print("📊 Padrões detectados no arquivo 2:")
        print("   - Tipo de dados: " + patterns2["data_type"])
        print("   - Valores únicos: " + str(patterns2["unique_values"]))
        print("   - Valores nulos: " + str(patterns2["null_values"]))

        # Gerar relatório
        print("\n📄 Gerando relatório detalhado...")
        report = generate_excel_report(analysis_results)

        # Salvar relatório
        report_path = Path("temp_examples/relatorio_analise.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)

        print("✅ Relatório salvo em: " + str(report_path))

        # Mostrar recomendações
        print("\n💡 Recomendações:")
        for rec in analysis_results["recommendations"]:
            print("   - " + rec)

        # Mostrar algumas correspondências
        print("\n🔍 Exemplos de correspondências:")
        matches = analysis_results["detailed_matches"]
        sorted_matches = sorted(
            matches.items(), key=lambda x: x[1]["score"], reverse=True
        )

        print("Top 3 melhores correspondências:")
        for i, (original, match_info) in enumerate(sorted_matches[:3], 1):
            print(
                "   "
                + str(i)
                + ". '"
                + original
                + "' → '"
                + match_info["match"]
                + "' (Score: "
                + str(match_info["score"])
                + "%)"
            )

        print("\nTop 3 piores correspondências:")
        for i, (original, match_info) in enumerate(sorted_matches[-3:], 1):
            print(
                "   "
                + str(i)
                + ". '"
                + original
                + "' → '"
                + match_info["match"]
                + "' (Score: "
                + str(match_info["score"])
                + "%)"
            )

    except Exception as e:
        print("❌ Erro durante a análise: " + str(e))

    finally:
        # Limpar arquivos temporários
        print("\n🧹 Limpando arquivos temporários...")
        try:
            os.remove(file1_path)
            os.remove(file2_path)
            print("✅ Arquivos temporários removidos")
        except Exception:
            print("⚠️ Não foi possível remover alguns arquivos temporários")


def demonstrate_agent_integration():
    """Demonstra como integrar com os agentes do sistema"""

    print("\n🤖 Demonstração da Integração com Agentes")
    print("=" * 50)

    print("Este exemplo mostra como o sistema de agentes pode ser usado para:")
    print("1. Analisar automaticamente as diferenças entre planilhas")
    print("2. Gerar relatórios estruturados")
    print("3. Fornecer recomendações baseadas na análise")
    print("4. Detectar padrões e anomalias nos dados")

    print("\n📋 Fluxo de trabalho com agentes:")
    print("   📤 Upload de arquivos → Validação automática")
    print("   🔍 Análise de similaridade → Detecção de padrões")
    print("   📊 Geração de métricas → Recomendações inteligentes")
    print("   📄 Relatório estruturado → Download automático")

    print("\n🎯 Benefícios para engenharia civil:")
    print("   - Comparação de orçamentos de diferentes fornecedores")
    print("   - Análise de variações em projetos")
    print("   - Controle de qualidade de dados")
    print("   - Detecção de inconsistências em planilhas")


if __name__ == "__main__":
    # Executar demonstração
    demonstrate_excel_analysis()
    demonstrate_agent_integration()

    print("\n🎉 Demonstração concluída!")
    print("\nPara usar o sistema completo:")
    print("1. Execute: streamlit run app/main.py")
    print("2. Acesse a aba 'Execução'")
    print("3. Selecione 'Crew de Análise de Planilhas'")
    print("4. Faça upload dos arquivos Excel")
    print("5. Configure as opções de análise")
    print("6. Execute a análise!")
