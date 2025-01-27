# 📚 Sistema de Gerenciamento de Biblioteca
Este é um sistema simples para o gerenciamento de uma biblioteca, desenvolvido utilizando Streamlit e PostgreSQL. O objetivo é facilitar o cadastro de usuários e livros, o registro de empréstimos e a consulta dos livros emprestados e dos usuários com mais empréstimos.

## init.sql

#### [init.sql](project_sql/init.sql)

Script para criação das nossas tabelas.
``` 
-- Criação da tabela de usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_cadastro DATE DEFAULT CURRENT_DATE
);

-- Criação da tabela de livros
CREATE TABLE livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('disponível', 'emprestado')) DEFAULT 'disponível'
);

-- Criação da tabela de empréstimos
CREATE TABLE emprestimos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id),
    livro_id INT REFERENCES livros(id),
    data_emprestimo DATE DEFAULT CURRENT_DATE,
    prazo DATE,
    devolvido BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    CONSTRAINT fk_livro FOREIGN KEY (livro_id) REFERENCES livros(id)
);
```

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
Certifique-se de criar um arquivo .env no diretório raiz com a variável de ambiente DATABASE_URL configurada para apontar para o banco de dados PostgreSQL. 

```python 
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco
```

3. Usar Docker Compose
Se você usa Docker Compose, crie um arquivo docker-compose.yml com a configuração do serviço e execute:

```docker-compose up --build```

Acesse a aplicação no seu navegador em: http://localhost:8501.

## O sistema utiliza as seguintes tabelas no banco de dados PostgreSQL:

Usuarios: Contém informações dos usuários da biblioteca.    
Livros: Contém informações sobre os livros disponíveis.     
Emprestimos: Registra os empréstimos feitos pelos usuários, incluindo o livro, usuário e prazo.

## Tecnologias Utilizadas
Streamlit: Para criar a interface interativa do sistema.    
PostgreSQL: Para armazenar dados dos usuários, livros e empréstimos.

### Recursos Criados

#### Prints Sistema Biblioteca

![sistema](prints/sistema.png)
![cadastro_Usuario](prints/cadastro_usuario.png)
![cadastro_livro](prints/cadastro_livro.png)
![emprestimo_livro](prints/emprestimo_livro.png)
![livros_emprestados](prints/livros_emprestados.png)
