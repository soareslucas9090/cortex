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
            "name": "Gerenciamento De Usuários.Tipos",
            "description": """Rotas relacionadas com os tipos de usuários.\n
    Tipos padrões: "Admin", "TI", "Aluno", "Motorista", "Professor", "Diretor.Geral", "Diretor.Ensino", "Coordenador", "Tec.Administrativo", "Serv.Terceirizado", "Engenheiro", "Enfermeiro", "Medico", "Psicologo", "Nutricionista", "Odontologo", "Pedagogo", "Vigilante".""",
        },
        {
            "name": "Gerenciamento De Usuários.Enderecos",
            "description": "Rotas relacionadas com os endereços de usuários e empresas.\n",
        },
        {
            "name": "Gerenciamento De Usuários.Contatos",
            "description": "Rotas relacionadas com os contatos de usuários e empresas.",
        },
        {
            "name": "Gerenciamento De Usuários.Empresas",
            "description": "Rotas relacionadas com os dados de empresas.\nO IFPI é a única empresa padrão criada",
        },
        {
            "name": "Gerenciamento De Usuários.Usuários",
            "description": "Rotas relacionadas com os usuários",
        },
        {
            "name": "Gerenciamento De Usuários.Deficiencias",
            "description": """Rotas relacionadas os tipos de deficiências.\n
    Tipos padrões: "Deficiência física", "Deficiência auditiva", "Deficiência visual", "Deficiência intelectual", "Deficiência psicossocial ou por saúde mental", "Deficiência múltipla", "Deficiência", "Baixa Visão", "Surdez".""",
        },
        {
            "name": "Gerenciamento De Usuários.Inserir Vários Alunos",
            "description": "Rota para inserção de Alunos em Lote",
        },
        {
            "name": "Gerenciamento De Usuários.Inserir Vários Usuários",
            "description": "Rota para inserção de Alunos em Lote",
        },
        {
            "name": "Gerenciamento De Usuários.Solicitar Reset de Senha",
            "description": "Rota responsável por enviar o email para o reset de senha do usuário",
        },
        {
            "name": "Gerenciamento De Usuários.Confirmar Codigo Reset de Senha",
            "description": "Rota responsável por cnfirmar o código de reset do usuário",
        },
        {
            "name": "Gerenciamento De Usuários.Confirmar Reset de Senha",
            "description": "Rota responsável por receber a nova senha do usuário",
        },
        {
            "name": "Gerenciamento De Usuários.Setores",
            "description": """Rotas relacionadas com os setores dos usuários.\n
    Setores padrões: "Alunos", "Direcao Geral", "Direcao de Ensino", "Direcao de Administracao e Planejamento", "Coordenacao Informatica", "Coordenacao Tec Informatica", "Coordenacao Eletromecanica", "Coordenacao Tec Eletromecanica", "Coordenacao Edificacoes", "Coordenacao Tec Edificacoes", "Coordenacao Meio Ambiente", "Coordenacao Tec Meio Ambiente", "Coordenacao TADS", "Coordenacao Biologia", "Coordenacao Matematica", "Coordenacao PROFMAT", "Coordenacao de Compras e Licitacao", "Coordenacao de Controle Academico", "Coordenacao de Disciplina", "Coordenacao de Ed. Fisica", "Coordenacao de Extensao", "Coordenacao de Multimidia", "Coordenacao de Patrimônio e Almoxarifado", "Coordenacao de Pesquisa e Inovacao", "TI", "Biblioteca", "Casa da Leitura", "Departamento Contabilidade", "Departamento Apoio ao Ensino", "Departamento Logistica, Manutencao e Compras", "Enfermagem", "Engenharia", "Nutricao", "Psicologia", "Saude", "Servico Social", "Medico", "Odontologico", "Pedagogico", "Refeitorio", "Guarita", "Area Externa", "PROF ENS BAS TEC TECNOLOGICO-SUBSTITUTO", "ASSISTENTE EM ADMINISTRACAO", "ASSISTENTE DE ALUNO", "TEC DE TECNOLOGIA DA INFORMACAO", "PROFESSOR ENS BASICO TECN TECNOLOGICO", "ENGENHEIRO", "BIBLIOTECARIO-DOCUMENTALISTA", "VIGILANTE", "TECNICO EM AUDIOVISUAL", "CONTADOR", "AUXILIAR DE BIBLIOTECA", "AUX EM ADMINISTRACAO", "ADMINISTRADOR", "ENFERMEIRO", "TECNICO EM ELETROTECNICA", "TECNICO DE LABORATORIO", "PSICOLOGO", "TECNICO EM ARQUIVO", "ASSISTENTE SOCIAL", "TECNICO EM ASSUNTOS EDUCACIONAIS", "ODONTOLOGO", "SECRETARIO EXECUTIVO", "PEDAGOGO", "ASSISTENTE DE LABORATORIO", "MEDICO", "NUTRICIONISTA", "TECNICO EM ENFERMAGEM", "TECNICO EM SECRETARIADO", "ANALISTA DE TEC DA INFORMACAO", "LIMPEZA", "AUX. COZINHA".""",
        },
        {
            "name": "Gerenciamento De Usuários.Matriculas",
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
            "name": "Soticon.Rotas Automáticas",
            "description": """Rotas relacionadas com as rotas automáticas do ônibus.\n
            Dias válidos para criação de rotas automáticas: "segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo".""",
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
            "name": "Soticon.Declarar Aluno Faltante",
            "description": "Rota responsável por declarar aluno como faltante na fila do ônibus.",
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
