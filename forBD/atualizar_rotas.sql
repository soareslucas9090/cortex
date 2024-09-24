CREATE OR REPLACE FUNCTION atualizar_rotas() RETURNS VOID AS $$
DECLARE
    timezone_config TEXT;
    interval_time INTERVAL;
BEGIN
    -- Obtenha o fuso horário atual do banco
    timezone_config := current_setting('TimeZone');

    -- Verificando qual o fuso horário do banco
    IF timezone_config = 'America/Sao_Paulo' THEN
        interval_time := INTERVAL '10 minutes';
    ELSEIF timezone_config = 'UTC' THEN
        interval_time := INTERVAL '-2 hours -50 minutes';
    ELSE
        -- Fuso horário não previsto
        interval_time := INTERVAL '10 minutes';
    END IF;

    UPDATE soticon_rota
    SET status = 'executada'
    WHERE status = 'espera'
    AND (
        data < CURRENT_DATE
        OR (data = CURRENT_DATE AND horario < CURRENT_TIME + interval_time)
    );
END;
$$ LANGUAGE plpgsql;