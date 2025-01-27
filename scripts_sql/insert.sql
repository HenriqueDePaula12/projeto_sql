INSERT INTO usuarios (nome, email) VALUES 
('Pedro Rocha', 'pedrorocha@email.com'),
('Maria Oliveira', 'maria@email.com');

INSERT INTO livros (titulo, autor, status) VALUES 
('O Senhor dos Anéis', 'J.R.R. Tolkien', 'disponível'),
('Harry Potter e a Pedra Filosofal', 'J.K. Rowling', 'disponível');

INSERT INTO emprestimos (usuario_id, livro_id, prazo) VALUES
(1, 1, '2025-02-10'),  
(2, 2, '2025-02-15'); 