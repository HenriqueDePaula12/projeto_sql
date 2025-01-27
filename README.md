# Sobre o projeto
Olá!

Este é um projeto de criação de um sistema de biblioteca!

## Ferramentas usadas

![Python](https://img.shields.io/badge/Python-00000F?style=for-the-badge&logo=python&logoColor=white)
[![POSTGRESQL](https://img.shields.io/badge/POSTGRES-00000F?style=for-the-badge&logo=POSTGRESQL&logoColor=white)]()
![Docker](https://img.shields.io/badge/docker-00000F.svg?style=for-the-badge&logo=docker&logoColor=white)

## BIBLIOTECA

#### [biblioteca.py](script_python/biblioteca.py)

Este projeto é um sistema de biblioteca desenvolvido com Streamlit e PostgreSQL. Ele permite cadastrar usuários, cadastrar livros, registrar empréstimo de livros, ver livros emprestados e listar usuários com mais empréstimos.
Funcionalidades

Página Inicial

Configuração da Página: Define o título da página como "Sistema de Gerenciamento de Biblioteca"

Conexão com o Banco de Dados

Função conectar: Conecta ao banco de dados PostgreSQL usando variáveis de ambiente(arquivo .env) para as credenciais e configurações do banco. Cria a tabela cadastro se ela não existir.

Inserção de Usuários

Função inserir_usuario: Insere um novo usuário na tabela usuários. // Verifica se o usuário ja existe para evitar duplicatas e exibe uma mensagem de erro caso o nome do produto já esteja cadastrado. //

Inserção de Livros

Função inserir_livro: Insere livros através de nome e autor.

Registro de Empréstimo

Função registrar_emprestimo: Exibe um formulário para registrar empréstimo de livro onde é possível selecionar usuário, livro e prazo de empréstimo.

Listagem de Livros Emprestados

Função livros_emprestados: Exibe os livros emprestados aparecendo nome do livro, usuário pra quem foi emprestado e prazo do empréstimo.

Validações

Nome do Produto: Deve conter apenas letras minúsculas e espaços.

Valor do Produto: Deve ser um número com até duas casas decimais.

```python
import os
import streamlit as st
import psycopg2
from psycopg2 import sql, errors
import re

st.set_page_config(page_title='Cadastro De Produtos', page_icon='oak_tecnologia_logo.jpeg')

url = "https://media.licdn.com/dms/image/C4D0BAQEPoGN8sj3UqA/company-logo_200_200/0/1631643331492/oak_tecnologia_logo?e=1727308800&v=beta&t=CbbRtCdNcpY-bOowMlbShuzXnHU23mwiYAfzucd-Trw"
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(url)

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

with st.container():
    st.title("Sistema de Cadastro de Produtos")

def connect_db():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cadastro (
                id SERIAL PRIMARY KEY,
                nome_produto TEXT UNIQUE,
                descricao_produto TEXT,
                valor_produto DECIMAL(10, 2),
                disponivel VARCHAR(3)
            )
        """)
    conn.commit()
    return conn

def insert_product(conn, produto):
    try:
        with conn.cursor() as cursor:
            insert_query = sql.SQL(
                "INSERT INTO cadastro (nome_produto, descricao_produto, valor_produto, disponivel) VALUES (%s, %s, %s, %s)"
            )
            cursor.execute(insert_query, (
                produto['nome'], 
                produto['descricao'], 
                produto['valor'], 
                produto['disponivel']
            ))
        conn.commit()
    except errors.UniqueViolation:
        st.error(f"Erro: O produto '{produto['nome']}' já está cadastrado.")
        conn.rollback()

def load_products(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT nome_produto, descricao_produto, valor_produto, disponivel FROM cadastro")
        rows = cursor.fetchall()
        produtos = [{'nome': row[0], 'descricao': row[1], 'valor': str(row[2]), 'disponivel': row[3]} for row in rows]
    return produtos

def cadastro_produto():
    with st.form(key='produto_form'):
        nome = st.text_input('Nome do produto')
        descricao = st.text_input('Descrição do produto')
        valor = st.text_input('Valor do produto')
        disponivel = st.selectbox('Disponível para venda', ['sim', 'não'])
        submit_button = st.form_submit_button(label='Cadastrar')

    return submit_button, nome, descricao, valor, disponivel

def listagem_produtos(produtos):
    produtos = sorted(produtos, key=lambda x: float(x['valor']))
    st.table([{'Nome': p['nome'], 'Valor': p['valor']} for p in produtos])
    novo_produto = st.button('Novo Produto')
    return novo_produto

def main():
    conn = connect_db()
    produtos = load_products(conn)

    if 'view' not in st.session_state:
        st.session_state.view = 'cadastro' 

    if st.session_state.view == 'cadastro':
        submit_button, nome, descricao, valor, disponivel = cadastro_produto()
        
        if submit_button:
            produto = {
                'nome': nome,
                'descricao': descricao,
                'valor': valor,
                'disponivel': disponivel
            }

            if not re.match('^[a-z ]+$', produto['nome']):
                st.error("Erro: O nome do produto deve conter apenas letras minúsculas e sem caracteres especiais.")
            elif not re.match('^\d+(\.\d{1,2})?$', produto['valor']):
                st.error("Erro: O valor do produto deve conter apenas números e até duas casas decimais.")
            elif not any(p['nome'] == produto['nome'] for p in produtos):
                insert_product(conn, produto)
                st.success(f"Produto '{produto['nome']}' cadastrado com sucesso!")
                produtos = load_products(conn)
                st.session_state.view = 'listagem'
                st.experimental_rerun()
            else:
                st.error(f"Erro: O produto '{produto['nome']}' já está cadastrado.")

    if st.session_state.view == 'listagem':
        novo_produto = listagem_produtos(produtos)
        
        if novo_produto:
            st.session_state.view = 'cadastro'
            st.experimental_rerun()

if __name__ == '__main__':
    main()
```

## DOCKERFILE

#### [Dockerfile](scripts/Dockerfile)

Este Dockerfile contém as instruções necessárias para criação de uma imagem Docker personalizada que é usada para executar uma aplicação Streamlit de cadastro de produtos utilizando Python.

A imagem base utilizada é o Python 3.9 na sua versão "slim", que é uma versão mais leve do Python que reduz o tamanho da imagem final e melhorando a eficiência. Após, define-se o diretório de trabalho /app dentro do contêiner, garantindo que todos os comandos subsequentes sejam executados nesse diretório.

O próximo passo é copiar todo o conteúdo do diretório atual (que inclui o código fonte da aplicação) para o diretório de trabalho dentro do contêiner. Após isso, as dependências da aplicação são instaladas usando o pip, com base no arquivo requirements.txt, e a opção --no-cache-dir é utilizada para evitar o armazenamento de cache, mantendo a imagem mais leve.

A porta 8501 é exposta para que o Streamlit possa ser acessado externamente. Finalmente, o comando streamlit run stream.py é definido como o comando padrão que será executado quando o contêiner iniciar, iniciando a aplicação Streamlit e permitindo o acesso à interface de cadastro de produtos.


