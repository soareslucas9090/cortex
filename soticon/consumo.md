# Documentação da API para o App Soticon

Rotas da API para o aplicativo soticon, acessível via `host/api/soticon/v1/`

## Usuários

### GET /users/

Retorna todos os usuários.

### GET /users/{id}

Retorna o objeto de usuário com o ID especificado.
Retorna junto as informações de tickets reservado e não usados para a data atual.

### GET /users/?usuario=x

Retorna o user_soticon com o user = x.
Retorna junto as informações de tickets reservado e não usados para a data atual.

### POST /users/

Cria um novo usuário.
- Parâmetros necessários:
  - usuario (int): O id de usuário do app gerUsuarios.
  - faltas (int): O número de faltas do usuário, começa sempre com 0.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

### PATCH /users/{id}/

Atualiza um usuário existente.
- Parâmetros opcionais (ao menos um):
  - usuario (int): O id de usuário do app gerUsuarios.
  - faltas (int): O número de faltas do usuário, começa sempre com 0.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

### DELETE /users/{id}/

Exclui um usuário existente.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

## Strikes

### GET /strikes/

Retorna todos os strikes.

### GET /strikes/{id}

Retorna o objeto de strike com o ID especificado.

### GET /strikes/?nome=x

Retorna todos os strikes do aluno com o nome = x.

### POST /strikes/

Cria um novo strike.
- Parâmetros necessários:
  - user_soticon (inteiro): O ID do usuário associado ao strike.
  - data: Data do strike do usuário.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

### PATCH /strikes/{id}

Atualiza um usuário existente.
- Parâmetros opcionais (ao menos um):
  - user_soticon (inteiro): O ID do usuário associado ao strike.
  - data (string): Data do strike do usuário.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

### DELETE /strikes/{id}/

Exclui um strike existente.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

## Justificativas

### GET /justificativas/

Retorna todas as justificativas.

### GET /justificativas/{id}

Retorna o objeto de justificativa com o ID especificado.

### POST /justificativas/

Cria uma nova justificativa.
- Parâmetros necessários:
  - strike (inteiro): O ID do strike associado à justificativa.
  - data (string): Data da justificativa do usuário.
  - obs (string): O motivo da justificativa.
- Acesso apenas para usuários autenticados.

### PATCH /justificativas/

Cria uma nova justificativa.
- Parâmetros opcionais (ao menos um):
  - strike (inteiro): O ID do strike associado à justificativa.
  - data (string): Data da justificativa do usuário.
  - obs (string): O motivo da justificativa.
- Acesso apenas para usuários autenticados.

### DELETE /justificativas/{id}/

Exclui uma justificativa existente.
- Acesso apenas para usuários autenticados.

## Posições

### GET /posicoes/

Retorna todas as posições na fila.

### GET /posicoes/{id}

Retorna o objeto de posição com o ID especificado.

### POST /posicoes/

Cria uma nova posição na fila.
- Parâmetros necessários:
  - num_ticket (inteiro): O número do ticket.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

### PATCH /posicoes/

Cria uma nova posição na fila.
- Parâmetros opcionais:
  - num_ticket (inteiro): O número do ticket.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

### DELETE /posicoes/{id}/

Exclui uma posição existente na fila.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

## Rotas

### GET /rotas/

Retorna todas as rotas.

### GET /rotas/{id}

Retorna o objeto de rota com o ID especificado.

### GET /rotas/?status=x

Retorna todos as rotas com status = x.

### GET /rotas/?data=x

Retorna todos as rotas com a data = x.
- O formato da data é "YYYY-MM-DD"

### GET /rotas/?data_valida=x

Retorna todos as rotas validas para agendamento (status="espera") com a data = x.
- O formato da data é "YYYY-MM-DD"

### POST /rotas/

Cria uma nova rota.
- Parâmetros necessários:
  - obs (string): Detalhes sobre a rota.
  - data (string): O data da rota.
  - status (string): O status da rota.
  - horario (string): O horário da horario.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

### PATCH /rotas/{id}/

Atualiza uma rota existente.
- Parâmetros opcionais (ao menos um):
  - obs (string): Detalhes sobre a rota.
  - data (string): O data da rota.
  - status (string): O status da rota.
  - horario (string): O horário da horario.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

### DELETE /rotas/{id}/

Exclui uma rota existente.
- Acesso apenas para usuários autenticados do tipo Admin ou TI.

## Tickets

### GET /tickets/

Retorna todos os tickets.

### GET /tickets/{id}

Retorna o objeto de ticket com o ID especificado.

### GET /tickets/?rota=x

Retorna todos os tickets com a rota = x.

### GET /tickets/?usuario=x

Retorna todos os tickets reservados e não usados para as rotas do dia do user_soticon = x.

### POST /tickets/

Cria um novo ticket.
- Parâmetros necessários:
  - rota (inteiro): O ID da rota associada ao ticket.
  - user_soticon (inteiro): O ID do usuário associado ao ticket.
  - usado (boolean): O status "usado" do ticket
  - reservado (boolean): O status "reservado" do ticket
  - posicao_fila (inteiro): O ID da posição da fila associada ao ticket.
- Acesso apenas para usuários autenticados.

### PATCH /tickets/{id}/

Atualiza um ticket existente.
- Parâmetros opcionais (ao menos um):
  - rota (inteiro): O ID da rota associada ao ticket.
  - user_soticon (inteiro): O ID do usuário associado ao ticket.
  - usado (boolean): O status "usado" do ticket
  - reservado (boolean): O status "reservado" do ticket
  - posicao_fila (inteiro): O ID da posição da fila associada ao ticket.
- Acesso apenas para usuários autenticados.

### DELETE /tickets/{id}/

Exclui um ticket existente.
- Acesso apenas para usuários autenticados.

## Reservar Ticket

### POST /reservar_ticket/

Reserva um ticket para um usuário, ou desreserva caso tenha um ticket reservado.
- Parâmetros necessários:
  - rota (inteiro): O ID da rota para a qual o ticket está sendo reservado/desreservado (o status da rota deve ser "espera").
  - user_soticon (inteiro): O ID do usuario para o qual o ticket está sendo reservado/desreservado.
- Acesso apenas para usuários autenticados.

## Verificar Tickets

### PUT /verificar_tickets/

Verifica um ticket para um usuário.
- Parâmetros necessários:
  - user_soticon (inteiro): O ID do usuário cujo ticket está sendo verificado.
  - rota (inteiro): O ID da rota para a qual o ticket está sendo verificado.

