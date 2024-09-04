SPECTACULAR_SETTINGS = {
    "TITLE": "API Cortex - Soticon",
    "DESCRIPTION": "",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "TAGS": [
        # Autenticação
        {
            "name": "Auth",
            "description": "Rotas Relacionadas com a autenticação de usuário",
        },
        # Gerenciamento de Usuários
        {
            "name": "GerenciamentoDeUsuários.Tipos",
            "description": """Rotas relacionadas com os tipos de usuários.\n
    Tipos padrões: "Admin", "TI", "Aluno", Motorista", "Professor", "TI", "Diretor.Geral", "Diretor.Ensino", "Coordenador", "Tec.Administrativo", "Serv.Terceirizado".""",
        },
        {
            "name": "GerenciamentoDeUsuários.Enderecos",
            "description": "Rotas relacionadas com os endereços de usuários e empresas.\n",
        },
        {
            "name": "GerenciamentoDeUsuários.Contatos",
            "description": "Rotas relacionadas com os contatos de usuários e empresas.",
        },
        {
            "name": "GerenciamentoDeUsuários.Empresas",
            "description": "Rotas relacionadas com os dados de empresas.\nO IFPI é a única empresa padrão criada",
        },
        {
            "name": "GerenciamentoDeUsuários.Usuários",
            "description": "Rotas relacionadas com os usuários",
        },
        {
            "name": "GerenciamentoDeUsuários.Setores",
            "description": """Rotas relacionadas com os setores dos usuários.\n
    Setores padrões: "Direcao Geral", "Direcao de Ensino", "Docente", "Coordenacao Informatica", "Coordenacao Eletromecanica","Coordenacao Edificacoes","Coordenacao Meio Ambiente","Coordenacao TADS","Coordenacao Biologia", "Coordenacao Matematica", "Biblioteca", "Contabilidade", "Saude", "Multimeios", "CODIS", "Refeitorio", "Guarita".""",
        },
        {
            "name": "GerenciamentoDeUsuários.Matriculas",
            "description": "Rotas relacionadas com as matrículas de usuários",
        },
        # Soticon
        {
            "name": "Soticon.UsersSoticon",
            "description": "Rotas relacionadas com os usuários do Soticon.",
        },
        {
            "name": "Soticon.Strikes",
            "description": "Rotas relacionadas com strikes dos usuários.",
        },
        {
            "name": "Soticon.Justificativas",
            "description": "Rotas relacionadas com as justificativas dos strikes.",
        },
        {
            "name": "Soticon.PosicaoFila",
            "description": "Rotas relacionadas com as posições cadastradas na fila.",
        },
        {
            "name": "Soticon.Rotas",
            "description": "Rotas relacionadas com as rotas do ônibus.",
        },
        {
            "name": "Soticon.Tickets",
            "description": "Rotas relacionadas com tickets reservados.",
        },
        {
            "name": "Soticon.Regras",
            "description": "Rotas relacionadas com as regras de negócio.",
        },
        {
            "name": "Soticon.Reservar Tickets",
            "description": "Rota responsável pela reserva de tickets.",
        },
        {
            "name": "Soticon.Verificar Tickets",
            "description": "Rota responsável por verificar os tickets.",
        },
        {
            "name": "Soticon.Finalizar Rota",
            "description": "Rota responsável por finalizar uma rota.",
        },
    ],
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}
