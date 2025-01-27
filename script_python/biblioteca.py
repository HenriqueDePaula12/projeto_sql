import streamlit as st
import psycopg2
import os

# Função para conectar ao banco de dados PostgreSQL
def conectar():
    conn = psycopg2.connect(
        os.getenv('DATABASE_URL')  # O Docker vai passar essa variável de ambiente automaticamente
    )
    return conn

# Função para inserir novos usuários
def inserir_usuario(nome, email):
    conn = conectar()
    cursor = conn.cursor()
    query = "INSERT INTO usuarios (nome, email) VALUES (%s, %s)"
    cursor.execute(query, (nome, email))
    conn.commit()
    cursor.close()
    conn.close()

# Função para inserir novos livros
def inserir_livro(titulo, autor):
    conn = conectar()
    cursor = conn.cursor()
    query = "INSERT INTO livros (titulo, autor) VALUES (%s, %s)"
    cursor.execute(query, (titulo, autor))
    conn.commit()
    cursor.close()
    conn.close()

# Função para registrar empréstimo
def registrar_emprestimo(usuario_id, livro_id, prazo):
    conn = conectar()
    cursor = conn.cursor()
    query = "INSERT INTO emprestimos (usuario_id, livro_id, prazo) VALUES (%s, %s, %s)"
    cursor.execute(query, (usuario_id, livro_id, prazo))
    conn.commit()
    cursor.close()
    conn.close()

# Função para exibir livros emprestados
def livros_emprestados():
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT livros.titulo, usuarios.nome AS usuario, emprestimos.prazo
    FROM emprestimos
    JOIN livros ON emprestimos.livro_id = livros.id
    JOIN usuarios ON emprestimos.usuario_id = usuarios.id
    WHERE emprestimos.devolvido = FALSE;
    """
    cursor.execute(query)
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    return livros

# Função para exibir usuários com mais empréstimos
def usuarios_com_mais_emprestimos():
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT usuarios.nome, COUNT(emprestimos.id) AS total_emprestimos
    FROM emprestimos
    JOIN usuarios ON emprestimos.usuario_id = usuarios.id
    GROUP BY usuarios.id
    ORDER BY total_emprestimos DESC;
    """
    cursor.execute(query)
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

# Interface do Streamlit
st.set_page_config(page_title="Sistema de Biblioteca", page_icon="📚", layout="wide")

st.title("📚 Sistema de Gerenciamento de Biblioteca")

# Menu de navegação
menu = ["Cadastrar Usuário", "Cadastrar Livro", "Registrar Empréstimo", "Livros Emprestados", "Usuários com Mais Empréstimos"]
opcao = st.sidebar.selectbox("Escolha uma opção", menu)

# Cadastrar Usuário
if opcao == "Cadastrar Usuário":
    st.header("Cadastrar Novo Usuário")
    nome = st.text_input("Nome do Usuário")
    email = st.text_input("Email do Usuário")
    
    if st.button("Cadastrar Usuário"):
        if nome and email:
            inserir_usuario(nome, email)
            st.success(f"Usuário {nome} cadastrado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos.")

# Cadastrar Livro
elif opcao == "Cadastrar Livro":
    st.header("Cadastrar Novo Livro")
    titulo = st.text_input("Título do Livro")
    autor = st.text_input("Autor do Livro")
    
    if st.button("Cadastrar Livro"):
        if titulo and autor:
            inserir_livro(titulo, autor)
            st.success(f"Livro '{titulo}' cadastrado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos.")

# Registrar Empréstimo
elif opcao == "Registrar Empréstimo":
    st.header("Registrar Empréstimo")
    
    # Listar usuários
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    
    usuario = st.selectbox("Selecione o Usuário", [u[1] for u in usuarios])
    
    # Listar livros disponíveis
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo FROM livros WHERE status = 'disponível'")
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    
    livro = st.selectbox("Selecione o Livro", [l[1] for l in livros])
    prazo = st.date_input("Prazo de Empréstimo")
    
    if st.button("Registrar Empréstimo"):
        if usuario and livro and prazo:
            usuario_id = [u[0] for u in usuarios if u[1] == usuario][0]
            livro_id = [l[0] for l in livros if l[1] == livro][0]
            registrar_emprestimo(usuario_id, livro_id, prazo)
            st.success(f"Empréstimo de '{livro}' para {usuario} registrado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos.")

# Livros Emprestados
elif opcao == "Livros Emprestados":
    st.header("Livros Emprestados")
    livros = livros_emprestados()
    if livros:
        for livro in livros:
            st.write(f"Livro: {livro[0]}, Usuário: {livro[1]}, Prazo: {livro[2]}")
    else:
        st.write("Não há livros emprestados no momento.")

# Usuários com Mais Empréstimos
elif opcao == "Usuários com Mais Empréstimos":
    st.header("Usuários com Mais Empréstimos")
    usuarios = usuarios_com_mais_emprestimos()
    if usuarios:
        for usuario in usuarios:
            st.write(f"Usuário: {usuario[0]}, Total de Empréstimos: {usuario[1]}")
    else:
        st.write("Não há empréstimos registrados.")
