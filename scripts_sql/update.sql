UPDATE livros
SET status = 'disponível'
WHERE id = (SELECT livro_id FROM emprestimos WHERE id = 1);

UPDATE emprestimos
SET devolvido = TRUE
WHERE id = 1;
