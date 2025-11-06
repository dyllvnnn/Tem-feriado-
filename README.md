# Tem feriado? - PDF Analyzer

Uma aplicação Tkinter para analisar arquivos PDF e identificar quais datas contidas neles são feriados brasileiros.

## Instalação

1. Clone este repositório:
\`\`\`bash
git clone <seu-repositorio>
cd holiday-checker
\`\`\`

2. Crie um ambiente virtual (recomendado):
\`\`\`bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
\`\`\`

3. Instale as dependências:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Uso

Execute a aplicação:
\`\`\`bash
python main.py
\`\`\`

1. Clique em "📁 Choose File" para selecionar um arquivo PDF
2. Clique em "🔍 Analyze PDF" para analisar as datas
3. Visualize os resultados na área de resultados

## Funcionalidades

- ✅ Interface moderna com Tkinter
- ✅ Leitura de arquivos PDF
- ✅ Extração de datas em múltiplos formatos (DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)
- ✅ Integração com API de feriados públicos
- ✅ Identificação de feriados brasileiros
- ✅ Exibição de resultados em tempo real

## Estrutura do Projeto

\`\`\`
holiday-checker/
├── main.py              # Arquivo principal com interface Tkinter
├── pdf_handler.py       # Funções para leitura de PDF
├── api_handler.py       # Integração com API de feriados
├── requirements.txt     # Dependências do projeto
└── README.md            # Este arquivo
\`\`\`

## API Utilizada

- **Nager.Date API**: https://date.nager.at/api/v3/PublicHolidays/

Esta API fornece feriados públicos para diversos países, incluindo Brasil (BR).

## Commits do Git

### Commit 1: Interface Tkinter
\`\`\`bash
git add main.py
git commit -m "Commit 1: Add Tkinter interface for PDF file selection"
\`\`\`

### Commit 2: Integração PDF + API
\`\`\`bash
git add pdf_handler.py api_handler.py requirements.txt
git commit -m "Commit 2: Add PDF reading and holiday API integration"
\`\`\`

### Commit 3: Exibição de Resultados
\`\`\`bash
git add .
git commit -m "Commit 3: Add holiday results display in interface"
\`\`\`

## Licença

MIT
