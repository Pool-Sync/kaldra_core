# KALDRA — Handoff de Deploy (DEPLOY_HANDOFF.md)

Este documento define a visão operacional de deploy da arquitetura KALDRA, incluindo:

- Build das imagens Docker  
- Organização dos serviços  
- Modelo Kubernetes  
- Fluxo CI/CD  
- Estratégia de deploy em produção  
- Segurança e versionamento  

Ele fornece **o caminho do ambiente de desenvolvimento → staging → produção**.

---

# 1. Componentes do Deploy

O ecossistema KALDRA é composto por:

- **kaldra-core**  
  (biblioteca Python com Δ144, TW369, Kindras, Engine e Apps)

- **kaldra-api**  
  (API Gateway FastAPI que expõe rotas para Alpha, GEO, Product, Safeguard e Engine)

Serviços auxiliares:

- Docker  
- Docker Compose (dev)
- Kubernetes (produção)
- GitHub Actions (CI/CD)

---

# 2. Estrutura de Infra

```
infra/
├── docker/
│   ├── Dockerfile.core
│   ├── Dockerfile.api
│   └── docker-compose.dev.yml
│
├── k8s/
│   ├── namespace.yaml
│   ├── deployment-core.yaml
│   ├── deployment-api.yaml
│   ├── service-core.yaml
│   ├── service-api.yaml
│   └── NOTES.md
│
├── ci_cd/
│   ├── github-actions/
│   │   ├── kaldra-ci.yml
│   │   └── kaldra-release.yml
│   └── README_CICD.md
│
├── configs/
│   ├── env.example
│   ├── logging.yaml
│   └── settings.template.json
│
└── scripts/
    ├── dev_up.sh
    ├── dev_down.sh
    ├── build_images.sh
    └── lint_check.sh
```

---

# 3. Build de imagens Docker

## Build manual

```
bash infra/scripts/build_images.sh
```

Ou:

```
docker build -f infra/docker/Dockerfile.core -t kaldra-core:dev .
docker build -f infra/docker/Dockerfile.api -t kaldra-api:dev .
```

---

# 4. Deploy Local (docker-compose)

```
bash infra/scripts/dev_up.sh
```

Ou:

```
docker compose -f infra/docker/docker-compose.dev.yml up --build
```

---

# 5. Deploy Kubernetes (modelo de produção)

> Estes manifests são placeholders — precisam ser ajustados para o ambiente real.

### 5.1. Criar namespace

```
kubectl apply -f infra/k8s/namespace.yaml
```

### 5.2. Subir kaldra-core

```
kubectl apply -f infra/k8s/deployment-core.yaml
kubectl apply -f infra/k8s/service-core.yaml
```

### 5.3. Subir kaldra-api

```
kubectl apply -f infra/k8s/deployment-api.yaml
kubectl apply -f infra/k8s/service-api.yaml
```

---

# 6. CI/CD — GitHub Actions (modelo)

### 6.1. Pipeline de Integração Contínua

Arquivo:  
`infra/ci_cd/github-actions/kaldra-ci.yml`

Responsável por:

- Lint  
- Testes (futuros)  
- Validação de YAMLs/Dockerfiles  
- Garantir que o repo está saudável a cada push  

### 6.2. Pipeline de Release

Arquivo:  
`infra/ci_cd/github-actions/kaldra-release.yml`

Responsável por:

- Build das imagens Docker  
- (Futuro) Push para registry  
- (Futuro) Trigger de deploy para cluster  

---

# 7. Estratégia de Deploy Real (Visão)

Ambientes recomendados:

- **dev** → Docker Compose  
- **staging** → Kubernetes com imagens `:staging`  
- **prod** → Kubernetes com imagens `:prod`

Deploy:

- Armazenar imagens no GHCR (GitHub Container Registry)
- Versionar com tags (ex: `kaldra-core:v0.6.1`)
- Deploy automatizado via GitHub Actions (futuro)

---

# 8. Segurança (alto nível)

- Nunca commitar `.env`
- Secrets devem ser salvos em:
  - `GitHub → Secrets`
  - ou `Kubernetes → Secret`
- Não incluir credenciais em YAMLs
- Sempre validar:
  - permissão mínima
  - isolamento de rede
  - acesso controlado ao API Gateway

---

# 9. Fluxo Final (Dev → Deploy)

```
DEV:
    ↓
Rodar docker-compose dev
    ↓
Implementar engines e rotas
    ↓
Testar API /status
    ↓
CI (lint + tests)
    ↓
Build das imagens
    ↓
Tag e release
    ↓
STAGING:
    ↓
Deploy no cluster de teste
    ↓
Validação
    ↓
PROD:
    ↓
Deploy final via pipeline
```

---

# 10. Próximos Passos Recomendados

1. Implementar integração real no Gateway (`client_*`).  
2. Escrever testes nos motores (TW369, Δ144, Alpha…).  
3. Criar dashboard no frontend 4iam.ai.  
4. Ajustar manifests K8s para ambiente real.  
5. Ativar pipeline de release com container registry.

---

**Fim do DEPLOY_HANDOFF.md**
