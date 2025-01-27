SELECT livros.titulo, usuarios.nome AS usuario, emprestimos.prazo
FROM emprestimos
JOIN livros ON emprestimos.livro_id = livros.id
JOIN usuarios ON emprestimos.usuario_id = usuarios.id
WHERE emprestimos.devolvido = FALSE;

SELECT usuarios.nome, COUNT(emprestimos.id) AS total_emprestimos
FROM emprestimos
JOIN usuarios ON emprestimos.usuario_id = usuarios.id
GROUP BY usuarios.id
ORDER BY total_emprestimos DESC;