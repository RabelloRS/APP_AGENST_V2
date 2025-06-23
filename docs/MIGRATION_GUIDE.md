# Guia de Migração: Crews para Banco de Dados

A partir da refatoração, todas as crews são persistidas exclusivamente no banco de dados SQLite (`app/data/crews_database.db`).

## O que mudou?
- Não há mais leitura ou escrita de crews em arquivos JSON para persistência principal.
- O arquivo `crews_db_resumido.json` pode ser gerado apenas para exportação/visualização.

## Como migrar?
- Basta rodar o sistema normalmente. Se você tinha crews em JSON, migre manualmente para o banco usando a interface ou scripts.
- Após a migração, remova arquivos JSON antigos para evitar confusão.

## Exportação de Resumo
- Para exportar um resumo das crews para JSON, utilize a função utilitária disponível no sistema.

## Dúvidas?
Consulte a documentação ou abra uma issue.
