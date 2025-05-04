# Importa as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt

# Lê o arquivo CSV contendo os dados de vendas
df = pd.read_csv('vendas.csv')

# Exibe o DataFrame original (antes de qualquer processamento)
print(df, '\n')

# Padroniza os nomes das colunas: remove espaços e substitui por "_"
df.columns = df.columns.str.strip().str.replace(' ', '_')

# Cria a coluna "Total" multiplicando a quantidade pelo preço unitário
df['Total'] = df['Quantidade'] * df['Preco_Unitario']

# Cria uma linha com o total geral das vendas para adicionar no final do DataFrame
linha_total = {
    'Data': '',
    'Produto': '',
    'Quantidade': '',
    'Preco_Unitario': '',
    'Cidade': '',
    'Total': df['Total'].sum()
}

# Adiciona a linha de totais ao final do DataFrame
df.loc[len(df)] = linha_total

# Exibe o DataFrame com a linha de total
print(df, '\n')

# Converte as colunas "Quantidade" e "Preco_Unitario" para tipo numérico
# Valores inválidos são transformados em NaN (Not a Number)
df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce')
df['Preco_Unitario'] = pd.to_numeric(df['Preco_Unitario'], errors='coerce')

# Remove as linhas com valores ausentes em "Quantidade" ou "Preco_Unitario"
df = df.dropna(subset=['Quantidade', 'Preco_Unitario'])

# Agrupa os dados por produto e soma as quantidades vendidas
quantidade = df.groupby('Produto')['Quantidade'].sum()

# Identifica o produto mais vendido (maior quantidade)
protudo_mais_vendido = quantidade.idxmax()
quantidade_maxima = quantidade.max()

# Exibe o produto mais vendido
print(f"O produto mais vendido foi '{protudo_mais_vendido}' com {quantidade_maxima} unidades.\n")

# Gera um gráfico de barras da quantidade vendida por produto
quantidade.plot(x='Produto', y='Quantidade', kind='bar', title='Quantidade Vendida por Produto')
plt.xlabel('Produto')
plt.ylabel('Quantidade')
plt.tight_layout()
plt.show()

# Agrupa os dados por cidade e soma o total vendido
faturamento_cidades = df.groupby('Cidade')['Total'].sum()

# Identifica a cidade com maior faturamento
cidade_mais_faturou = faturamento_cidades.idxmax()
maximo_faturado = faturamento_cidades.max()

# Gera um gráfico de pizza com a participação de faturamento por cidade
faturamento_cidades.plot(kind='pie', autopct='%1.1f%%', title='Faturamento por Cidade')
plt.ylabel('')  # Remove o rótulo do eixo Y (não é necessário para gráfico de pizza)
plt.tight_layout()
plt.show()

# Exibe a cidade com maior faturamento
print(f"A cidade que mais fatorou foi '{cidade_mais_faturou}' com o valor {maximo_faturado} reais. \n")

# Calcula e exibe o faturamento total da empresa
faturamento_total = df['Total'].sum()
print(f"O faturamento Total de vendas com todas as Unidades foi '{faturamento_total:.2f}'.")

# Converte a coluna "Data" para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'])

# Cria uma nova coluna com ano e mês para análise mensal
df['AnoMes'] = df['Data'].dt.to_period('M')

# Agrupa os dados por mês e calcula o faturamento mensal
faturamento_mensal = df.groupby('AnoMes')['Total'].sum()

# Exibe o faturamento mensal
print(f"O faturamento Mensal foi '{faturamento_mensal}'")

# Gera um gráfico de linha mostrando a evolução do faturamento ao longo dos meses
faturamento_mensal.plot(kind='line', marker='o', title='Faturamento Mensal')
plt.xlabel('Mês')
plt.ylabel('Total (R$)')
plt.tight_layout()
plt.show()