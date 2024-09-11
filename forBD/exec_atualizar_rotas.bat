@echo off
set PGPASSWORD=SenhaDoBanco
psql -U UsuarioDoBanco -d cortex -h localhost -c "select atualizar_rotas();"