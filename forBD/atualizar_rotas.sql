CREATE OR REPLACE FUNCTION atualizar_rotas() RETURNS VOID AS $$
BEGIN
    UPDATE soticon_rota
    SET status = 'executada'
    WHERE status = 'espera'
    AND (
        data < CURRENT_DATE
        OR (data = CURRENT_DATE AND horario < CURRENT_TIME + INTERVAL '10 minutes')
    );
END;
$$ LANGUAGE plpgsql;