# 📱 Guia da Funcionalidade WhatsApp

## Visão Geral

A funcionalidade WhatsApp permite monitorar grupos do WhatsApp, identificar links de serviços em nuvem e baixar arquivos automaticamente. Os arquivos são renomeados com timestamp e organizados por data.

## 🚀 Funcionalidades

### ✅ Recursos Implementados

- **Monitoramento de Grupos**: Conecta ao WhatsApp Web e monitora grupos específicos
- **Detecção de Links**: Identifica links de serviços em nuvem nas mensagens
- **Download Automático**: Baixa arquivos de múltiplas fontes
- **Renomeação Inteligente**: Adiciona timestamp ao nome dos arquivos
- **Organização por Data**: Organiza arquivos em pastas por data
- **Interface Streamlit**: Interface gráfica intuitiva

### 🔗 Serviços Suportados

- **Google Drive**: Links diretos e compartilhados
- **OneDrive**: Links do Microsoft OneDrive
- **Dropbox**: Links do Dropbox
- **MEGA**: Links do MEGA
- **MediaFire**: Links do MediaFire
- **WhatsApp**: Arquivos anexados diretamente

## 🛠️ Instalação

### 1. Dependências

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

### 2. Configuração

Certifique-se de que as seguintes dependências estão instaladas:

```bash
pip install selenium webdriver-manager requests
```

### 3. Chrome WebDriver

Para funcionalidade completa do WhatsApp Web, você precisará do Chrome WebDriver:

```bash
# Instalar via webdriver-manager (automático)
from webdriver_manager.chrome import ChromeDriverManager
```

## 📋 Como Usar

### Interface Streamlit

1. **Acesse a aplicação**:
   ```bash
   streamlit run app/main.py
   ```

2. **Navegue para a aba WhatsApp**:
   - Clique na aba "📱 WhatsApp" na interface

3. **Configure as opções**:
   - **Nome do Grupo**: Nome exato do grupo do WhatsApp
   - **Pasta de Download**: Onde os arquivos serão salvos
   - **Máximo de Mensagens**: Quantidade de mensagens a processar

4. **Conecte ao WhatsApp**:
   - Clique em "🔗 Conectar ao WhatsApp"
   - Escaneie o QR code se necessário

5. **Execute o monitoramento**:
   - Clique em "🔍 Monitorar Mensagens"
   - Aguarde o processamento

6. **Baixe os arquivos**:
   - Clique em "⬇️ Baixar Arquivos"
   - Os arquivos serão baixados e renomeados

7. **Organize por data** (opcional):
   - Clique em "🗂️ Organizar por Data"

### Uso Programático

```python
from app.utils.tools import (
    whatsapp_connect,
    whatsapp_get_messages,
    extract_cloud_links,
    download_cloud_file,
    rename_file_with_timestamp
)

# Conectar ao WhatsApp
result = whatsapp_connect("minha_sessao")

# Obter mensagens
messages = whatsapp_get_messages("Grupo de Trabalho", 100)

# Extrair links
cloud_links = extract_cloud_links(messages)

# Baixar arquivos
for link in cloud_links:
    result = download_cloud_file(link["url"], "./downloads")
    if result["status"] == "success":
        # Renomear com timestamp
        new_path = rename_file_with_timestamp(
            result["file_path"], 
            link["timestamp"]
        )
```

## 🤖 Agentes da Crew

### 1. Monitor do WhatsApp (`whatsapp_monitor`)
- **Função**: Monitora grupos do WhatsApp
- **Responsabilidades**:
  - Conectar ao WhatsApp Web
  - Obter mensagens do grupo
  - Identificar arquivos e links

### 2. Baixador de Arquivos (`file_downloader`)
- **Função**: Baixa arquivos de múltiplas fontes
- **Responsabilidades**:
  - Baixar arquivos da nuvem
  - Baixar arquivos do WhatsApp
  - Gerenciar downloads

### 3. Organizador de Arquivos (`file_organizer`)
- **Função**: Organiza e renomeia arquivos
- **Responsabilidades**:
  - Adicionar timestamps aos nomes
  - Organizar por data
  - Criar estrutura de pastas

## 📋 Tarefas da Crew

### 1. Monitoramento (`whatsapp_monitoring_task`)
```yaml
description: "Monitorar grupo do WhatsApp '{group_name}' em busca de mensagens com arquivos e links de serviços em nuvem"
expected_output: "Lista de mensagens encontradas com arquivos e links identificados, incluindo timestamps"
```

### 2. Download (`file_download_task`)
```yaml
description: "Baixar arquivos identificados das mensagens do WhatsApp e links de serviços em nuvem"
expected_output: "Arquivos baixados com sucesso e relatório de downloads realizados"
```

### 3. Organização (`file_organization_task`)
```yaml
description: "Organizar arquivos baixados, adicionar timestamps aos nomes e criar estrutura de pastas organizada"
expected_output: "Arquivos organizados com nomes padronizados incluindo data e hora, estrutura de pastas criada"
```

## 🔧 Ferramentas Disponíveis

### Conexão e Monitoramento
- `whatsapp_connect()`: Estabelece conexão com WhatsApp Web
- `whatsapp_get_messages()`: Obtém mensagens de um grupo
- `extract_cloud_links()`: Extrai links de serviços em nuvem

### Download
- `download_cloud_file()`: Baixa arquivos de serviços em nuvem
- `download_whatsapp_file()`: Baixa arquivos anexados ao WhatsApp

### Organização
- `rename_file_with_timestamp()`: Adiciona timestamp ao nome do arquivo
- `organize_files_by_date()`: Organiza arquivos em pastas por data

## 📁 Estrutura de Arquivos

```
downloads/
├── whatsapp/
│   ├── 2024-01-15/
│   │   ├── 20240115_143022_arquivo1.pdf
│   │   └── 20240115_143045_arquivo2.xlsx
│   └── 2024-01-16/
│       └── 20240116_091230_arquivo3.docx
```

## ⚠️ Limitações e Observações

### Versão Atual (Demonstração)
- **Simulação**: Esta versão usa dados simulados para demonstração
- **WhatsApp Web**: Em produção, requer implementação completa com Selenium
- **Autenticação**: Necessário escanear QR code manualmente

### Para Produção
- Implementar autenticação automática
- Adicionar suporte a múltiplos grupos
- Implementar monitoramento contínuo
- Adicionar tratamento de erros robusto
- Implementar cache de sessão

## 🔒 Segurança

### Boas Práticas
- Use sessões temporárias
- Não compartilhe credenciais
- Monitore logs de acesso
- Implemente rate limiting
- Valide URLs antes do download

### Privacidade
- Respeite as políticas do WhatsApp
- Não armazene mensagens desnecessariamente
- Implemente limpeza automática de dados
- Siga as diretrizes de GDPR/LGPD

## 🐛 Solução de Problemas

### Problemas Comuns

1. **Erro de Conexão**:
   - Verifique se o Chrome está instalado
   - Confirme se o webdriver está atualizado
   - Verifique a conectividade com a internet

2. **QR Code não aparece**:
   - Aguarde mais tempo para carregamento
   - Verifique se o WhatsApp Web está acessível
   - Tente recarregar a página

3. **Downloads falham**:
   - Verifique permissões de escrita na pasta
   - Confirme se os links ainda são válidos
   - Verifique espaço em disco

4. **Arquivos não renomeados**:
   - Verifique formato do timestamp
   - Confirme permissões de arquivo
   - Verifique se o arquivo não está em uso

## 📞 Suporte

Para suporte técnico:
- **Email**: suporte@propor.com.br
- **Telefone**: 51 99164-6794
- **Responsável**: Eng. Civil Rodrigo Emanuel Rabello

## 📄 Licença

Este software é desenvolvido pela Propor Engenharia e está sujeito aos termos da licença incluída no projeto. 