-- ==========================================
-- CUSTO TOTAL DE MANUTENÇÃO POR ÔNIBUS
-- ==========================================

SELECT
    o.prefixo,
    o.modelo,
    SUM(m.custo) AS custo_total_manutencao,
    COUNT(m.id_manutencao) AS quantidade_manutencoes
FROM manutencao m
INNER JOIN onibus o
    ON m.id_onibus = o.id_onibus
GROUP BY
    o.prefixo,
    o.modelo
ORDER BY
    custo_total_manutencao DESC;

-- ==========================================
-- QUANTIDADE DE VIAGENS POR LINHA
-- ==========================================

SELECT
    l.numero AS linha,
    l.itinerario,
    COUNT(v.id_viagem) AS quantidade_viagens,
    SUM(v.km_percorridos) AS km_total
FROM viagem v
INNER JOIN linha l
    ON v.id_linha = l.id_linha
GROUP BY
    l.numero,
    l.itinerario
ORDER BY
    quantidade_viagens DESC;


-- ==========================================
-- QUILOMETRAGEM TOTAL POR ÔNIBUS
-- ==========================================

SELECT
    o.prefixo,
    o.modelo,
    COUNT(v.id_viagem) AS quantidade_viagens,
    SUM(v.km_percorridos) AS km_total,
    AVG(v.km_percorridos) AS km_medio
FROM viagem v
INNER JOIN onibus o
    ON v.id_onibus = o.id_onibus
GROUP BY
    o.prefixo,
    o.modelo
ORDER BY
    km_total DESC;

-- ==========================================
-- MANUTENÇÕES AINDA ABERTAS
-- ==========================================

SELECT
    o.prefixo,
    o.modelo,
    m.tipo_manutencao,
    m.data_abertura,
    m.custo,
    m.status_manutencao
FROM manutencao m
INNER JOIN onibus o
    ON m.id_onibus = o.id_onibus
WHERE m.status_manutencao = 'Aberta'
ORDER BY
    m.data_abertura ASC;

-- ==========================================
-- RANKING DE MOTORISTAS POR VIAGENS
-- ==========================================

SELECT
    m.nome AS motorista,
    COUNT(v.id_viagem) AS quantidade_viagens,
    SUM(v.km_percorridos) AS km_total
FROM viagem v
INNER JOIN motorista m
    ON v.id_motorista = m.id_motorista
GROUP BY
    m.nome
ORDER BY
    quantidade_viagens DESC;

-- ==========================================
-- CUSTO MÉDIO DE MANUTENÇÃO POR TIPO
-- ==========================================

SELECT
    tipo_manutencao,
    COUNT(id_manutencao) AS quantidade_manutencoes,
    SUM(custo) AS custo_total,
    AVG(custo) AS custo_medio
FROM manutencao
GROUP BY
    tipo_manutencao
ORDER BY
    custo_total DESC;

    