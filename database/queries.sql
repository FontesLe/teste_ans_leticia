SELECT 
    o.razao_social,
    o.uf,
    SUM(d.valor) AS total_despesas
FROM 
    demonstracoes d
JOIN 
    operadoras o ON d.registro_ans = o.registro_ans
WHERE 
    d.conta LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND d.periodo = (
        SELECT CONCAT(QUARTER(CURDATE()), 'T', YEAR(CURDATE()))
    )
GROUP BY 
    o.razao_social, o.uf
ORDER BY 
    total_despesas DESC
LIMIT 10;

SELECT 
    o.razao_social,
    o.uf,
    SUM(d.valor) AS total_despesas
FROM 
    demonstracoes d
JOIN 
    operadoras o ON d.registro_ans = o.registro_ans
WHERE 
    d.conta LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND d.data >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY 
    o.razao_social, o.uf
ORDER BY 
    total_despesas DESC
LIMIT 10;