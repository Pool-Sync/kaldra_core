# KALDRA — Handoff de Deploy (Local + Visão de Produção)

Este documento explica, de forma operacional, como:

1. Rodar o ecossistema KALDRA localmente usando Docker.
2. Entender quais serviços existem e como se conectam.
3. Preparar o caminho para um deploy real (produção/staging), usando a estrutura de `infra/`.

Atenção: tudo aqui assume a infraestrutura criada no Prompt 4:

* `infra/docker/Dockerfile.core`
* `infra/docker/Dockerfile.api`
* `infra/docker/docker-compose.dev.yml`
* `infra/scripts/*.sh`
* `infra/configs/*`
* `infra/k8s/*`
* `infra/docs/*`

---

## 1. Visão Geral da Arquitetura de Deploy

### 1.1. Repositório (raiz) Estrutura simplificada:
```bash
kaldra_core/           # raiz do projeto (monorepo)
├── core/              # kernel KALDRA (Δ144, TW369, Kindras, Engine, Apps)
├── data/              # JSONs e backups estáveis
├── docs/              # documentação de alto nível
├── kaldra_api/        # API Gateway (FastAPI)
└── infra/             # infraestrutura, docker, k8s, ci/cd, scripts
```

### 1.2. Serviços principais

* **kaldra-core**
  Container com:
  * core/ (arquetípico Δ144, TW369, Kindras, Engine, Apps)
  * código Python base do sistema.

* **kaldra-api**
  Container com:
  * kaldra_api/ (API Gateway FastAPI)
  * expõe endpoints HTTP para Alpha, Geo, Product, Safeguard, Engine.

No futuro, o **frontend 4iam.ai** vai consumir a kaldra-api via HTTP.

---

## 2. Pré-requisitos na máquina local

Instalar:

1. **Git**
2. **Python 3.11+** (para rodar scripts sem docker, se necessário)
3. **Docker** + **Docker Compose**
4. Opcional: bash (para usar scripts em infra/scripts/)

Verificações rápidas:

```bash
git --version
python --version
docker --version
docker compose version
```

---

## 3. Setup inicial do ambiente

### 3.1. Clonar o repositório

```bash
git clone <URL_DO_REPO_GITHUB> kaldra_core
cd kaldra_core
```

### 3.2. Configurar variáveis de ambiente

A estrutura do Prompt 4 prevê um arquivo de exemplo:

```bash
infra/configs/env.example
```

Copiar para .env na raiz ou em local combinado:

```bash
cp infra/configs/env.example .env
```

Ajustar valores se necessário (mantendo tudo genérico, sem segredos reais):

```env
ENV=dev
KALDRA_LOG_LEVEL=INFO
API_PORT=8000
CORE_SERVICE_URL=http://kaldra-core:9000
```

---

## 4. Rodando o KALDRA localmente com Docker

### 4.1. Subir a stack de desenvolvimento

Existem dois caminhos equivalentes: com script ou direto via docker compose.

#### Opção A — Via script (dev_up.sh)

```bash
bash infra/scripts/dev_up.sh
```

O script executa internamente:

```bash
docker compose -f infra/docker/docker-compose.dev.yml up --build
```

#### Opção B — Comando direto

```bash
docker compose -f infra/docker/docker-compose.dev.yml up --build
```

Isso vai:

* construir a imagem kaldra-core a partir do infra/docker/Dockerfile.core
* construir a imagem kaldra-api a partir do infra/docker/Dockerfile.api
* subir os dois containers:
  * kaldra-core
  * kaldra-api (exposto em localhost:8000)

### 4.2. Verificando se subiu

Em outro terminal, rodar:

```bash
docker ps
```

Você deve ver algo como:

* kaldra-core
* kaldra-api (porta 8000 → 8000)

### 4.3. Testando a API Gateway

O Prompt 3 definiu uma rota simples de status:

```http
GET http://localhost:8000/status/
```

Testar com curl:

```bash
curl http://localhost:8000/status/
```

Resposta esperada (placeholder):

```json
{
  "status": "KALDRA API Gateway online",
  "version": "0.1.0"
}
```

Se isso funciona, toda a stack de base (Docker, API, roteamento) está OK.

---

## 5. Desligando o ambiente local

### 5.1. Via script

```bash
bash infra/scripts/dev_down.sh
```

Que executa:

```bash
docker compose -f infra/docker/docker-compose.dev.yml down
```

### 5.2. Limpeza manual (se necessário)

Para parar e remover containers, caso algo fique preso:

```bash
docker compose -f infra/docker/docker-compose.dev.yml down
docker ps -a     # conferir o que ficou
```

---

## 6. Rodar componentes sem Docker (modo "dev puro")

Em alguns casos, pode ser útil rodar o API Gateway direto com Python (sem container).

### 6.1. Rodar apenas o kaldra_api local

Dentro do repo:

```bash
cd kaldra_api
pip install -r requirements.txt
uvicorn kaldra_api.main:app --reload --port 8000
```

Isso expõe a mesma rota:

```bash
curl http://localhost:8000/status/
```

> Observação: nessa abordagem, qualquer integração com o kaldra_core ainda depende de você ter o pacote visível no PYTHONPATH ou instalado via pip install -e . na raiz.

---

## 7. Pipeline conceitual de deploy (visão de produção)

> Tudo abaixo é **conceitual** — os manifests e workflows criados no Prompt 4 são placeholders a serem preenchidos com detalhes reais de ambiente.

### 7.1. Build de imagens

Usar o script:

```bash
bash infra/scripts/build_images.sh
```

Ou manualmente:

```bash
docker build -f infra/docker/Dockerfile.core -t kaldra-core:dev .
docker build -f infra/docker/Dockerfile.api -t kaldra-api:dev .
```

Em ambiente real, essas imagens seriam:

* Taggeadas por versão (kaldra-core:v0.1.0)
* Push para um registry (Docker Hub, GHCR, etc.)

### 7.2. Deploy em orquestrador (Kubernetes — modelo)

Arquivos em infra/k8s/:

* namespace.yaml
* deployment-api.yaml
* deployment-core.yaml
* service-api.yaml
* service-core.yaml

Fluxo típico (conceitual):

```bash
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/deployment-core.yaml
kubectl apply -f infra/k8s/service-core.yaml
kubectl apply -f infra/k8s/deployment-api.yaml
kubectl apply -f infra/k8s/service-api.yaml
```

Cada manifest deve ser ajustado com:

* nome das imagens
* recursos (CPU/memória)
* variáveis de ambiente
* secrets (via mecanismo de secrets do cluster, não com valores em YAML)

---

## 8. CI/CD (alto nível)

Os workflows em infra/ci_cd/github-actions/ foram pensados como modelo.

### 8.1. kaldra-ci.yml

Responsável por:

* checar formatação (ex: black, ruff) — mesmo que ainda seja placeholder
* rodar testes (pytest) — depois que existirem
* rodar lint em YAMLs / Dockerfiles, se desejado

### 8.2. kaldra-release.yml

Responsável por:

* build das imagens Docker
* (posteriormente) push para registry
* (opcional) disparar um deploy no cluster

Tudo isso ainda é skeleton, sem credenciais nem endpoints reais.

---

## 9. Ordem prática de uso no trabalho diário

1. **Clonar o repo e configurar .env.**

2. **Subir a stack local com Docker**
   ```bash
   bash infra/scripts/dev_up.sh
   ```

3. **Testar se a API responde**
   ```bash
   curl http://localhost:8000/status/
   ```

4. **Desenvolver engines / lógica no core/ e kaldra_api/.**

5. **Rodar lint/checks** (no futuro) com
   ```bash
   bash infra/scripts/lint_check.sh
   ```

6. **Parar o ambiente quando terminar**
   ```bash
   bash infra/scripts/dev_down.sh
   ```

7. **Quando estiver estável**:
   * usar build_images.sh para gerar imagens
   * ajustar CI/CD e manifests de k8s conforme o ambiente real.

---

## 10. Checklist rápido para confirmar que o deploy local está OK

* [ ] Docker e Docker Compose instalados.
* [ ] Repo clonado e .env criado a partir de infra/configs/env.example.
* [ ] Comando `bash infra/scripts/dev_up.sh` roda sem erro.
* [ ] Containers kaldra-core e kaldra-api aparecem em `docker ps`.
* [ ] `curl http://localhost:8000/status/` retorna JSON com status e version.
* [ ] `bash infra/scripts/dev_down.sh` derruba a stack corretamente.
* [ ] Imagens kaldra-core:dev e kaldra-api:dev podem ser construídas com build_images.sh.
