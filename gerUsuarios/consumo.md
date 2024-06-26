# Rotas para o APP gerUsuarios

## Tipos

### GET /tipos/

Retorna todos os tipos.

### GET /tipos/?tipo=x

Retorna todos os tipos com o nome igual a x.

### GET /tipos/{id}

Retorna o objeto com o ID igual a id.

### POST /tipos/

Cria um novo tipo.
- Parâmetros necessários:
  - nome (string): O nome do tipo.
- Parâmetros opcionais:
  - is_ativo (boolean): status "ativo" do tipo.
- Necessário que o usuário seja do tipo Admin ou TI.

### PATCH /tipos/{id}/

Atualiza um tipo existente.
- Parâmetros necessários:
  - nome (string): O novo nome do tipo.
- Parâmetros opcionais:
  - is_ativo (boolean): status "ativo" do tipo.
- Necessário que o usuário seja do tipo Admin ou TI.

### DELETE /tipos/{id}/

Remove um tipo existente.
- Necessário que o usuário seja do tipo Admin ou TI.
- Preferível tornar "is_ativo" como False.

## Endereços

### GET /enderecos/

Retorna todos os endereços.

### GET /enderecos/{id}

Retorna o objeto com o ID igual a id.

### POST /enderecos/

Cria um novo endereço.
- Parâmetros necessários:
  - logradouro (string): O logradouro do endereço.
  - bairro (string): O bairro do endereço.
  - cep (string): O CEP do endereço.
  - complemento (string, opcional): O complemento do endereço.
  - num_casa (inteiro): O número da casa do endereço.
- Parâmetros opcionais:
  - is_ativo (boolean): status "ativo" do endereço.

### PATCH /enderecos/{id}/

Atualiza um endereço existente.
- Parâmetros necessários:
  - logradouro (string): O novo logradouro do endereço.
  - bairro (string): O novo bairro do endereço.
  - cep (string): O novo CEP do endereço.
  - complemento (string, opcional): O novo complemento do endereço.
  - num_casa (inteiro): O novo número da casa do endereço.
- Parâmetros opcionais:
  - is_ativo (boolean): status "ativo" do endereço.

### DELETE /enderecos/{id}/

Remove um endereço existente.

## Contatos

### GET /contatos/

Retorna todos os contatos.

### GET /contatos/?email=x

Retorna o contato com o email igual a x.

### GET /contatos/?tel=x

Retorna o contato com o telefone igual a x.

### GET /contatos/{id}

Retorna o objeto com o ID igual a id.

### POST /contatos/

Cria um novo contato.
- Parâmetros necessários:
  - endereco (inteiro): O ID do endereço associado ao contato.
  - email (string): O email do contato.
  - tel (string): O telefone do contato.
- Parâmetros opcionais:
  - is_ativo (boolean): status "ativo" do contato.

### PATCH /contatos/{id}/

Atualiza um contato existente.
- Parâmetros necessários:
  - endereco (inteiro): O novo ID do endereço associado ao contato.
  - email (string): O novo email do contato.
  - tel (string): O novo telefone do contato.
- Parâmetros opcionais:
  - is_ativo (boolean): status "ativo" do contato.

### DELETE /contatos/{id}/

Remove um contato existente.

## Empresas

### GET /empresas/

Retorna todas as empresas.

### GET /empresas/?nome=x

Retorna a empresa com o nome igual a x.

### GET /empresas/?cnpj=x

Retorna a empresa com o CNPJ igual a x.

### GET /empresas/{id}

Retorna o objeto com o ID igual a id.

### POST /empresas/

Cria uma nova empresa.
- Parâmetros necessários:
  - contato (inteiro): O ID do contato associado à empresa.
  - nome (string): O nome da empresa.
  - cnpj (string): O CNPJ da empresa.
- Parâmetros opcionais:
  - is_ativo (boolean): status "ativo" da empresa.

### PATCH /empresas/{id}/

Atualiza uma empresa existente.
- Parâmetros necessários:
  - contato (inteiro): O novo ID do contato associado à empresa.
  - nome (string): O novo nome da empresa.
  - cnpj (string): O novo CNPJ da empresa.
- Parâmetros opcionais:
  - is_ativo (boolean): status "ativo" da empresa.

### DELETE /empresas/{id}/

Remove uma empresa existente.

## Usuários

### GET /users/

Retorna todos os usuários.

### POST /users/

Cria um novo usuário.
- Parâmetros necessários:
  - cpf (string): O CPF do usuário.
  - nome (string): O nome do usuário.
  - email (string): O email do usuário.
  - tipo (inteiro): O ID do tipo do usuário.
  - data_nascimento (data): A data de nascimento do usuário.
  - password (string): A senha do usuário.

### PATCH /users/{id}/

Atualiza um usuário existente.
- Parâmetros necessários:
  - cpf (string): O novo CPF do usuário.
  - nome (string): O novo nome do usuário.
  - email (string): O novo email do usuário.
  - tipo (inteiro): O novo ID do tipo do usuário.
  - data_nascimento (data): A nova data de nascimento do usuário.

### DELETE /users/{id}/

Remove um usuário existente.

## Setores

### GET /setores/

Retorna todos os setores.

### POST /setores/

Cria um novo setor.
- Parâmetros necessários:
  - nome (string): O nome do setor.

### PATCH /setores/{id}/

Atualiza um setor existente.
- Parâmetros necessários:
  - nome (string): O novo nome do setor.

### DELETE /setores/{id}/

Remove um setor existente.

## Setor Users

### GET /setorusers/

Retorna todas as associações entre setores e usuários.

### POST /setorusers/

Cria uma nova associação entre setor e usuário.
- Parâmetros necessários:
  - setor (inteiro): O ID do setor.
  - user (inteiro): O ID do usuário.

### PATCH /setorusers/{id}/

Atualiza uma associação entre setor e usuário existente.
- Parâmetros necessários:
  - setor (inteiro): O novo ID do setor.
  - user (inteiro): O novo ID do usuário.

### DELETE /setorusers/{id}/

Remove uma associação entre setor e usuário existente.

## Tipos de Matrícula

### GET /tiposmatricula/

Retorna todos os tipos de matrícula.

### POST /tiposmatricula/

Cria um novo tipo de matrícula.
- Parâmetros necessários:
  - descricao (string): A descrição do tipo de matrícula.

### PATCH /tiposmatricula/{id}/

Atualiza um tipo de matrícula existente.
- Parâmetros necessários:
  - descricao (string): A nova descrição do tipo de matrícula.

### DELETE /tiposmatricula/{id}/

Remove um tipo de matrícula existente.

## Matrículas

### GET /matriculas/

Retorna todas as matrículas.

### POST /matriculas/

Cria uma nova matrícula.
- Parâmetros necessários:
  - user (inteiro): O ID do usuário associado à matrícula.
  - tipo_matricula (inteiro): O ID do tipo de matrícula.
  - matricula (string): O número da matrícula.
  - expedicao (data): A data de expedição da matrícula.

### PATCH /matriculas/{id}/

Atualiza uma matrícula existente.
- Parâmetros necessários:
  - user (inteiro): O novo ID do usuário associado à matrícula.
  - tipo_matricula (inteiro): O novo ID do tipo de matrícula.
  - matricula (string): O novo número da matrícula.
  - expedicao (data): A nova data de expedição da matrícula.

### DELETE /matriculas/{id}/

Remove uma matrícula existente.
