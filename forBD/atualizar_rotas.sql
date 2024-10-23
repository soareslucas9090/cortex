CREATE OR REPLACE FUNCTION atualizar_rotas() RETURNS VOID AS $$
DECLARE
    timezone_config TEXT;
    interval_time INTERVAL;
BEGIN
    -- Obtenha o fuso horário atual do banco
    timezone_config := current_setting('TimeZone');

    -- Verificando qual o fuso horário do banco
    IF timezone_config != 'America/Sao_Paulo' THEN
        SET TIMEZONE TO 'America/Sao_Paulo';
    END IF;

    interval_time := INTERVAL '15 minutes';

    UPDATE soticon_rota
    SET status = 'executada'
    WHERE status = 'espera'
    AND (
        data < CURRENT_DATE
        OR (data = CURRENT_DATE AND CURRENT_TIME > horario + interval_time)
    );
END;
$$ LANGUAGE plpgsql;