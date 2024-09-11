# Cortex & SOTICON API

<img align="center" alt="Python" width="30" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"><span>&nbsp;&nbsp;&nbsp;</span>
<img align="center" alt="Django" width="30" src="https://cdn.worldvectorlogo.com/logos/django.svg"><span>&nbsp;&nbsp;&nbsp;</span>
<img align="center" alt="Django Rest Framework" height="40" src="https://i.imgur.com/dcVFAeV.png"><span>&nbsp;&nbsp;&nbsp;</span>
<img align="center" alt="PostgreSQL" width="36" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg"><span>&nbsp;&nbsp;&nbsp;</span>

## Sobre o Projeto
O projeto possui dois APPs nele, onde o principal é a API Cortex, que visa ser uma plataforma para servir dados de forma segura e estruturada para qualquer aplicação a ser implantada no IFPI - Floriano. O segundo APP é a API do SOTICON, o Sistema de Solicitação de Tickets do Ônibus.

As APIs seguem o padrão REST, mas não implementam todas as recomendações para o estado de RESTful (principalmente HATEOAS), mas segue as melhores recomendações equilibrando desempenho, simplicidade e fácil entendimento.

## Recursos implementados - Cortex
-   Criação, manutenção e busca com filtros de Tipos de Usuários, Endereços e Contatos, Empresas, Usuários, Setores e Matrícula.
-   Gerenciamento de permissões de acordo com o tipo de usuário (Em andamento, mas já implementado para os tipos Admin e TI)
-   Segurança e gerenciamento para diferentes tipos de usuários
-   Personalização de views de acordo com permissões de usuário
-   Segurança baseada em tokens jwt (access e refresh tokens)
-   Documentação Swagger Completa 
### Futuros incrementos
- Gerenciamento de permissões completo (com definição de permissão de alteração, criação, deleção e visualização para cada tipo de usuário e cada tabela do banco)
- Suporte a Logs de alterações de dados
- Suporte a Cache em Banco (Redis)
- Tuning de SQL nas pesquisas de requisições de grandes quantidade de dados
- Futura implementação de Frontend para gerenciamento do Cortex

## Recursos implementados - SOTICON
-   Criação, manutenção e busca com filtros de Rotas de Onibus, Usuários, Strikes de Usuários, Jutificativa de Strikes, e Tickets (reservas de ônibus)
-   Sistema otimizado de fila
-   Sistema de reserva otimizado para refletir a melhor organização da fila fisicamente
-   Suporte a reserva de ticket subjacente (reserva além do número máximo de pessoas, para casos de desistência)
-   Fechamento automático de rotas
### Futuros incrementos
- Strikes automáticos (em fase de implantação o sistema não estará com strikes ativos)
- Realocação automática de tickets subjacentes
- Suporte a Logs de alterações de dados
- Suporte a Cache em Banco (Redis)

## Segurança

A API do Cortex foi implementada com autenticação SimpleJWT, usando Django Rest Framework, a documentação foi feita com Swagger, via DRF-Spectacular, sendo totalmente funcional e testável. Para isso, é necessário Login com algum usuário válidos, onde tipos que não sejam Admin ou TI só conseguem visualizar os próprios dados e não permite alteração dos mesmos.

Abaixo um print da área de login da API com JWT, é necessário consummir a rota /api/token/, obter o token "access" e colar o valor recebido na opção circulada logo acima "Authorize"

<img src="https://i.imgur.com/5g4wTNA.png" alt="Rotas para autenticação">


Foram implementados filtros de pesquisa (query-params) na maioria das rotas para aplicação de filtros de pesquisas.

A documentação está na rota `/api/schema/swagger/`

# Rodando o projeto

Primeiro é necessária a criação de um Ambiente Virtual do Python (necessário versão 3.8 ou posterior do Python, mas recomendamos a 3.11), ou `venv`, para isso basta executar `python -m venv venv`. Ao término é necessário ativar a venv, então na mesma pasta que foi criado a pasta do ambiente virtual, rode o comando `venv\scripts\activate` e pronto.
Para instalar as dependências é necesário rodar o comando `pip install -r requirements.txt` com o Ambiente Virtual Ativo.
O código busca um arquivo `.env` para procurar as variáveis de ambiente necessárias, e caso não ache, usará as variáveis de ambiente instaladas no SO. O arquivo deve seguir os seguintes moldes:
```
secretKeyDjango=A chave secreta do Django, usada na criptografia de CSRF Token
secretKeyJWT=A chave secreta do Django Rest Framework, usada na criptografia dos JWT Tokens
debug=False
bdEngine=django.db.backends.postgresql
bdName=Nome do banco
bdUser=Usuário do Banco
bdPass=Senha do Banco
bdHost=Host do banco
bdPort=Porta do banco
allowedHosts=*
csrfTrustedOriginsANDcorsOriginWhitelist=IP do servidor que hosperdará o frontend da aplicação e permitirá acesso à API, caso seja mais de um, divida eles com virgulas sem espaço, como na variável abaixo
internalIPs=127.0.0.1,localhost,http://127.0.0.1,https://127.0.0.1,http://localhost,https://localhost
```
Colocar o arquivo `.env` na raiz do projeto ou adicionar estas variáveis diretamente no sistema.

Faça a criação do banco de dados com o comando `python manage.py migrate`.

Depois de criar o banco, acesse ele por algum cliente, como o DBeaver, e crie a função do arquivo `atualizar_rotas.sql` localizado na pasta `/forBD/`. Este código é necessário para o fechamento automático de rotas. Após isso:
- Caso seu sistema seja Linux, siga o tutorial para a criação da schedule presente no arquivo `Schedule atualizar rotas.txt` (na mesma pasta que o arquivo sql), sendo necessário a instalação do `pg_cron`.
- Caso se sistema seja Windows, siga as etapas descritas no arquivo `Schedule atualizar rotas.txt`, que irá criar uma Tarefa Agendada para executar um comando SQL que rodará a função `atualizar_rotas();` a cada 20 minutos. Um detalhe importante para este caso é que o arquivo `exec_atualizar_rotas.bat` precisa ser editado com as as credenciais e nome de banco corretos para pleno funcionamento, sendo possível fazer referência a uma variável de ambiente no sistema com `%nome_da_variavel%`.

Crie um super usuário com o comando `python manage.py createsuperuser` e forneça os dados que vão ser pedidos.

Com tudo configurado, o servidor para rodar o sistema em qualquer computador com Windows 8+ ou Server 2012+ é o "Waitress", e o comando para iniciar é:
`waitress-serve --port=8000 cortex.wsgi:application`

O servidor para rodar o sistema em um computador Linux é o "Gunicorn", e o comando é:
`gunicorn cortex.wsgi --workers 2 --bind :8000 --access-logfile -`

O serviço rodará no IP local, sendo acessível pela porta 8000 (é necessário a liberação da porta no Firewall do sistema e da rede. A porta também pode ser mudada por qualquer uma disponível). Exemplo: Servidor com IP `10.7.1.10`, o serviço ficará disponível em `http://10.7.1.10:8000`. Para rodar o sistema em HTTPS é necessário configurações adicionais no servidor.

## Lógica

Abaixo está o DER do Cortex:

<img src="https://i.imgur.com/aVCLgAw.png" alt="DER do Cortex">

### Explicando os relacionamentos - Cortex
- **gerUsuarios_user** é a tabela que contém os dados dos usuários. Todo usuário pertence a um tipo, e pode ou não estar relacionado a um contato, e também pode ou não estar relacionado a uma empresa. O campo que serve para Login é o `gerUsuarios_user.cpf`, e o campo que guarda o status de atividade do usuário é `gerUsuarios_user.is_active`. O atributo `gerUsuarios_user.email` deve receber o email instituicional do usuário, pois o email pessoal fica guardado em outra tabela, e este campo pode ser nulo, para cobrir casos em que um usuário não possue um email instituicional (como terceirizados). Os campos `gerUsuarios_user.is_staff` e `gerUsuarios_user.is_superuser` não são usados na lógica padrão da API, mas podem ser importantes em implementações futuras em que se mexa nestes dados diretamente do painel Admin do Django. ***A tabela gerUsuarios_user Contém os usuários cadastrados na API para servir de base para outros sistemas, mas é RECOMENDADO que TODOS os sistemas de tecerceiros possuam sua própria tabela de usuários, e guardem apenas uma tabela ao id da tabela gerUsuarios_user***.
- **gerUsuarios_tipo** guarda os tipos possíveis dos usuários, sendo que vários deles são previamente carregados com a aplicação (vide documentação para detalhes)
- **gerUsuarios_setor ** & **gerUsuarios_setor_user** guardam a relação entre os setores que os usuários pertecem, que podem ser 0 ou vários.
- **gerUsuarios_matricula** é responsável por detalhar as matrículas que o usuário possue. Sendo assim, um usuário pode ter nenhuma, uma ou várias matrículas, mas é sempre bom lembrar que somente é recomendado que uma esteja ativa.
- **gerUsuarios_contato** possue os campos que salvam os meios de contatos "personalizados" para cada usuário ou empresa.
- **gerUsuarios_endereco** guarda os dados do endereço do usuário ou empresa, e está relacionada com a tabela contato.
- **gerUsuarios_empresa** é a tabela que é responsável por detalhar a instituição a qual pertence o usuário. Técnicos Administrativos, professores, alunos e outros usuários devem ser associado à empresa IFPI - Campus Floriano (criada automaticamente), mas usuários terceirzados e/ou temporários podem e dever ser associados às suas respectivas empresas.

Abaixo está o DER do SOTICON:

<img src="https://i.imgur.com/yI8ycIf.png" alt="DER do Cortex">

### Explicando os relacionamentos - Soticon

- **soticon_usersoticon** é a tabela que guarda os usuários do sistema SOTICON, e além da referencia ao usuário da API, também há um contante das faltas e um estato de atividade.
- **soticon_strike** guarda os strikes recebidos pelos usuários por suas faltas.
- **soticon_justificativa** se relaciona diretamente com soticon_strike e é responsável por guardar as justificativas dadas pelos aluno ao seu strike.
- **soticon_tickets** armazena os dados da reserva dos alunos ao ônibus. Uma vez criada não é apagada, e altera somente o id do usuário que fez a reserva, mas evitar escritas desnecessárias no banco.
- **soticon_posicaofila** armazena as posições padrões da fila para o ônibus.
- **soticon_rota** contém os dados das rotas de ônibus cadastradas no sistema.
- **soticon_regras** conterá as regras de negócio da aplicação, como o número de pessoas na fila "primária" do ônibus (quantas pessoas cabem, no caso) e outros dados em geral.


## Autenticação

 O Access Token da API tem duração de 15 minutos, enquanto o Refresh Token tem duração de 40 minutos.
