# Script para adicionar campo api_env nas ferramentas que requerem API
import yaml

API_TOOLS = {
    'web_search_tool': 'OPENAI_API_KEY',
    'patent_database_tool': 'PATENT_API_KEY',
    'news_innovation_feed': 'NEWS_API_KEY',
    'database_query_tool': 'DB_API_KEY',
    # Adicione outras ferramentas e variáveis conforme necessário
}

with open('app/config/tools.yaml', 'r', encoding='utf-8') as f:
    tools = yaml.safe_load(f)

for tool, api_env in API_TOOLS.items():
    if tool in tools:
        tools[tool]['api_env'] = api_env

with open('app/config/tools.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(tools, f, allow_unicode=True, sort_keys=False)

print('Campo api_env adicionado nas ferramentas que requerem API.')
