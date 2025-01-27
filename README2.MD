# 📚 Sistema de Gerenciamento de Biblioteca
Este é um sistema simples para o gerenciamento de uma biblioteca, desenvolvido utilizando Streamlit e PostgreSQL. O objetivo é facilitar o cadastro de usuários e livros, o registro de empréstimos e a consulta dos livros emprestados e dos usuários com mais empréstimos.

## Funcionalidades
1. Cadastrar Usuário
Permite cadastrar novos usuários no sistema, fornecendo nome e e-mail.

2. Cadastrar Livro
Permite cadastrar novos livros na biblioteca, incluindo título e autor.

3. Registrar Empréstimo
Facilita o registro de empréstimos, associando um livro a um usuário e determinando o prazo para devolução.

4. Livros Emprestados
Exibe uma lista de livros que estão atualmente emprestados, com informações sobre o usuário e o prazo de devolução.

5. Usuários com Mais Empréstimos
Exibe uma lista dos usuários que mais realizaram empréstimos, com a contagem total de empréstimos realizados.

## Como usar
1. Pré-requisitos
Docker e Docker Compose instalados na sua máquina.
Banco de dados PostgreSQL configurado com as tabelas usuarios, livros e emprestimos.

2. Configuração
Criar um arquivo .env no diretório raiz com a variável de ambiente DATABASE_URL configurada para apontar para o banco de dados PostgreSQL. 

DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco

3. Usar Docker Compose
Se você usa Docker Compose, crie um arquivo docker-compose.yml com a configuração do serviço e executa no terminal:

```docker-compose up --build```

Acesse a aplicação no seu navegador em: http://localhost:8501.

## O sistema utiliza as seguintes tabelas no banco de dados PostgreSQL:

Usuarios: Informações dos usuários da biblioteca.    
Livros: Informações sobre os livros disponíveis.     
Emprestimos: Registra os empréstimos feitos pelos usuários, incluindo o livro, usuário e prazo.

## Tecnologias Utilizadas
Streamlit: Utilizado para criar nosso front-end    
PostgreSQL: Para armazenar dados dos usuários, livros e empréstimos.


