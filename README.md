# BoraJunto ✈️

**Plataforma web colaborativa para planejamento, organização e registro de viagens em grupo.**

---

## 🎯 Objetivo
Centralizar viagens, membros, convites, tarefas, documentos/comprovantes e fotos em uma aplicação web privada para o grupo. Chega de usar planilhas perdidas e grupos de mensagens caóticos; com o BoraJunto, cada detalhe da sua viagem fica organizado e acessível a todos os membros.

## 👥 Integrantes
* [Preencha o nome do integrante 1 aqui]
* [Preencha o nome do integrante 2 aqui]
* [Preencha o nome do integrante 3 aqui]

---

## 🛠️ Tecnologias Utilizadas

O sistema foi construído utilizando um stack tecnológico robusto e moderno baseado em Python:

* **Python 3.10+** (Linguagem base)
* **Flask** (Framework Web micro, utilizando Application Factory e Blueprints)
* **Flask-SQLAlchemy** (ORM para banco de dados)
* **Flask-Login** (Gerenciamento de sessão de usuários)
* **Flask-WTF** (Formulários e validações de segurança CSRF)
* **Jinja2** (Motor de templates)
* **Bootstrap 5** (Framework CSS de interface)
* **SQLite** (Banco de dados leve e portátil)
* **pytest** (Framework de testes automatizados)
* **python-dotenv** (Gerenciamento de variáveis de ambiente)

---

## ✅ Funcionalidades do MVP

* Cadastro de usuários
* Login/logout seguro
* Perfil do usuário
* Criação de viagens (definindo destinos e datas)
* Listagem das viagens do usuário
* Painel detalhado (Dashboard) da viagem
* Geração de convites seguros por link
* Entrada e associação de novos membros por convite
* Mural de logística (Tarefas)
* Atribuição de responsáveis nas tarefas
* Alteração de status dinâmico de tarefas (Pendente, Fazendo, Concluído)
* Upload de documentos/comprovantes com controle de extensões
* Download seguro de arquivos e verificação de privilégios de membro
* Galeria colaborativa de fotos com pré-visualização (timeline)
* Controle estrito de acesso por membro/dono da viagem
* Testes automatizados cobrindo os módulos principais

## ❌ Funcionalidades fora do escopo (Não implementadas no MVP)

* Divisão de custos financeiros
* Comentários diretos em fotos
* Botões de curtidas
* Chat interno de texto
* Notificações via e-mail ou push
* Exportação em PDF de cronogramas
* Integrações externas com APIs de turismo (Hotéis, Voos, Clima)

---

## 📂 Estrutura do Projeto

O código utiliza o padrão arquitetural de **Application Factory** e divide suas responsabilidades em **Blueprints**:

* `app.py`: O ponto de entrada que inicializa a aplicação.
* `borajunto/`: O pacote principal do projeto contendo a lógica de negócios.
* `borajunto/ext/`: Extensões Flask inicializadas de forma isolada (Configuração, DB, Login, WTF).
* `borajunto/models/`: Representações das tabelas do banco de dados via SQLAlchemy (Classes).
* `borajunto/forms/`: Definições dos formulários com Flask-WTF.
* `borajunto/views/`: Blueprints e rotas principais para gerenciar Viagens, Auth, Arquivos e Tarefas.
* `borajunto/services/`: Lógicas isoladas e funções de utilidade (como manipulação física de uploads).
* `templates/`: Páginas em HTML utilizando Jinja2 e integração visual com Bootstrap.
* `static/`: Arquivos CSS nativos, imagens e JavaScript complementar.
* `tests/`: Suíte completa de testes automatizados modulares com `pytest`.
* `instance/uploads/`: Diretório ignorado pelo controle de versão para armazenamento de uploads reais.

---

## 🚀 Como Instalar

Siga os passos abaixo para configurar o projeto no **Windows PowerShell**:

1. Crie o ambiente virtual:
   ```powershell
   py -m venv venv
   ```

2. Ative o ambiente virtual:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Atualize o gerenciador de pacotes:
   ```powershell
   python -m pip install --upgrade pip
   ```

4. Instale as dependências com o módulo editável (incluindo pacotes de dev/test):
   ```powershell
   python -m pip install -e ".[dev,test]"
   ```

---

## ⚙️ Como Configurar

1. O projeto vem com um modelo chamado `.env.example`. Não coloque chaves ou senhas reais diretamente no código ou no GitHub!
2. Crie ou copie o `.env.example` para `.env.dev` (ambiente de desenvolvimento local) ou apenas `.env` para produção:
   ```powershell
   cp .env.example .env.dev
   ```

---

## ▶️ Como Rodar

Com o ambiente virtual ativado e as configurações feitas, inicialize o banco de dados e inicie o servidor local:

1. **Gere o banco de dados e tabelas**:
   ```powershell
   flask init-db
   ```
   *(Atenção: Rodar este comando apagará todas as informações caso um banco anterior exista).*

2. **Inicie a aplicação**:
   ```powershell
   flask run
   ```

O console mostrará uma URL (provavelmente `http://127.0.0.1:5000`). Abra no navegador.

---

## 🧪 Como Testar

A aplicação acompanha uma base sólida de testes independentes rodando sob um SQLite em memória.

* **Executar os testes normais:**
  ```powershell
  pytest
  ```

* **Executar os testes verificando o nível de cobertura de código:**
  ```powershell
  pytest --cov=borajunto
  ```

---

## 🎬 Fluxo de Demonstração (MVP)

Abaixo o passo a passo completo das capacidades da plataforma, perfeito para avaliações acadêmicas:

1. **Criar usuário A**: Abra a rota principal e faça o cadastro.
2. **Fazer login**: Confirme o acesso com a conta criada.
3. **Criar viagem**: Na página "Minhas Viagens", adicione um destino e datas.
4. **Gerar convite**: Acesse a viagem gerada, clique em convites e crie o Link Mágico.
5. **Criar usuário B**: Abra outro navegador (ou guia anônima), cadastre um novo usuário B e logue.
6. **Entrar pelo convite**: Copie a URL do convite e abra usando a sessão do Usuário B. Ele passará a ser membro da viagem do Usuário A.
7. **Criar tarefa**: Crie uma tarefa pendente na página de detalhes de viagem.
8. **Alterar status**: Mova a tarefa de "Pendente" para "Fazendo" ou "Concluído".
9. **Enviar comprovante**: Clique no botão em formato de Anexo na tarefa e suba um documento PDF/Imagem.
10. **Baixar comprovante**: Simule o clique de download do arquivo como um membro autêntico da viagem.
11. **Enviar foto**: Na rota da Galeria, faça upload de uma foto da viagem com uma legenda e data.
12. **Ver galeria**: Deslize a timeline da sua viagem em formato de grid fotográfico.
13. **Rodar pytest**: Demonstre a estabilidade da sua plataforma disparando `pytest` no terminal provando não existir erros lógicos de backend.

---
Feito com dedicação para a disciplina de Engenharia de Software. 🚀
