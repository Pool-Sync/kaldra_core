# KALDRA — Ambiente Local (LOCAL_DEV.md)

Este documento explica como rodar o ecossistema KALDRA **localmente**, usando a infraestrutura criada em `infra/`.  
O objetivo é permitir desenvolvimento, debugging e testes sem dependências externas.

---

# 1. Arquitetura Geral

O ambiente local roda dois serviços principais via Docker:

- **kaldra-core** → contém o núcleo Δ144, TW369, Kindras, Engine e Apps.  
- **kaldra-api** → API Gateway FastAPI, exposto em `localhost:8000`.

Ambos são orquestrados por:

```
infra/docker/docker-compose.dev.yml
```

---

# 2. Pré-requisitos

Instale:

- Git  
- Python 3.11+ (opcional para rodar API puro)  
- Docker  
- Docker Compose  
- Bash (opcional para scripts)

Verifique:

```
git --version
python --version
docker --version
docker compose version
```

---

# 3. Clonar o Repositório

```
git clone <URL_DO_REPO>
cd kaldra_core
```

---

# 4. Configurar Variáveis de Ambiente

Copie o template:

```
cp infra/configs/env.example .env
```

Conteúdo sugerido:

```
ENV=dev
API_PORT=8000
CORE_SERVICE_URL=http://kaldra-core:9000
KALDRA_LOG_LEVEL=INFO
```

---

# 5. Subir o Ambiente Local (Docker)

## Opção A — Usando script

```
bash infra/scripts/dev_up.sh
```

## Opção B — Comando direto

```
docker compose -f infra/docker/docker-compose.dev.yml up --build
```

Isso vai:

- construir a imagem `kaldra-core`
- construir a imagem `kaldra-api`
- iniciar ambos os containers

---

# 6. Verificar se está rodando

```
docker ps
```

Você deve ver:

- `kaldra-core`
- `kaldra-api`

---

# 7. Testar API Gateway

Abra:

```
http://localhost:8000/status/
```

Ou use curl:

```
curl http://localhost:8000/status/
```

Retorno esperado:

```json
{
  "status": "KALDRA API Gateway online",
  "version": "0.1.0"
}
```

---

# 8. Derrubar o ambiente

## Opção A — Script

```
bash infra/scripts/dev_down.sh
```

## Opção B — Docker Compose

```
docker compose -f infra/docker/docker-compose.dev.yml down
```

---

# 9. Rodar API sem Docker (modo dev puro)

```
cd kaldra_api
pip install -r requirements.txt
uvicorn kaldra_api.main:app --reload --port 8000
```

---

# 10. Checklist rápido

- [ ] Clonou o repo  
- [ ] Criou `.env`  
- [ ] Subiu Docker com sucesso  
- [ ] API responde em `/status`  
- [ ] Containers aparecem em `docker ps`  

---

# 11. Próximos passos

Depois que o ambiente local estiver funcionando:

1. Implementar rotas reais no Gateway.  
2. Implementar integrações com `kaldra_engine`.  
3. Criar testes unitários em `kaldra_api/tests/`.  
4. Configurar deploy real com base no documento `DEPLOY_HANDOFF.md`.

---

**Fim do LOCAL_DEV.md**
