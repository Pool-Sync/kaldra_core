# KALDRA v2.3 — Reconciliation Report

**Data**: 28 de Novembro de 2025
**Status**: CRITICAL DIAGNOSIS

Este relatório detalha as divergências encontradas entre a implementação atual (Codebase) e a documentação (Docs), servindo como base para o plano de execução da v2.3.

## 3.1 Divergências Críticas

1.  **Bias Engine "Fantasma"**:
    *   **Docs**: Descrevem um motor robusto com integração Perspective API e Detoxify.
    *   **Code**: `src/bias/detector.py` contém apenas stubs comentados e uma heurística básica (contagem de keywords).
    *   **Impacto**: O sistema não tem capacidade real de detecção de viés, apenas simulação.

2.  **LLM Client "Oco"**:
    *   **Code**: `KindraLLMScorer` está implementado, mas o cliente LLM é `None` por padrão.
    *   **Impacto**: O "cérebro" do sistema está desligado. Ele roda puramente em regras determinísticas ou retorna zeros se o fallback falhar.

3.  **Embeddings Simulados**:
    *   **Code**: `Delta144Engine` usa `np.random.RandomState` com seeds baseadas em texto para gerar "embeddings".
    *   **Impacto**: A busca vetorial não é semântica. Sinônimos não funcionam. É um hash sofisticado, não IA.

## 3.2 Documentos Obsoletos

*   **Docs de "Future Works" antigos**: Embora movidos para `archive/`, ainda podem existir referências a eles em outros docs.
*   **Referências a Kindra Mappings "Vazios"**: Vários docs de arquitetura mencionam que os JSONs de mapeamento precisam ser populados. **Isso é falso**. Eles já estão populados em `schema/kindras/`.

## 3.3 Documentos Duplicados ou Redundantes

*   `docs/math/TW369_ENGINE_SPEC.md` vs `docs/math/TW369_ADVANCED_DRIFT_MODELS.md`: Há sobreposição na descrição dos modelos de drift. Recomenda-se fundir ou distinguir claramente (Spec vs Implementation Details).

## 3.4 Features Implementadas mas Não Documentadas (CODE > DOCS)

1.  **Painlevé II Solver (RK45)**:
    *   A implementação numérica detalhada em `src/tw369/painleve/painleve2_solver.py` é de alta qualidade mas mal documentada nos specs de alto nível, que a tratam como "future work".

2.  **Kindra Mappings (Populated)**:
    *   A riqueza dos arquivos JSON em `schema/kindras/` (regras de boost/suppress específicas por vetor) não está refletida nos docs, que tratam isso como tarefa pendente.

## 3.5 Features Documentadas mas NÃO Implementadas (DOCS > CODE)

1.  **Data Lab Ingest Workers**:
    *   `docs/DATALAB_WORKERS.md` descreve workers de ingestão de notícias. O código em `src/datalab/` é apenas esqueleto.
2.  **Integrações de Bias Reais**:
    *   Como mencionado em 3.1.

## 3.6 Features Parcialmente Implementadas

1.  **Meta-Engines**:
    *   Estrutura de roteamento existe (`MetaRouter`), mas os "filósofos" (`Nietzsche`, etc.) são apenas funções simples, sem a profundidade teórica prometida nos docs.
2.  **Apps (Alpha/Geo/Product)**:
    *   Existem como classes, mas herdam comportamento genérico. Não possuem lógica de negócio específica (ex: cálculo de risco financeiro real no Alpha).

## 3.7 Riscos Técnicos

1.  **Dívida de Simulação**: O uso de embeddings aleatórios e heurísticas de bias cria uma falsa sensação de funcionalidade. O sistema "funciona" (não crasha), mas não produz inteligência real.
2.  **Dependência de Stubs**: A arquitetura depende fortemente de injeção de dependência (LLM Client, Bias Provider) que não está configurada no boot padrão.

## 3.8 Recomendações (Ordenadas)

1.  **PRIORIDADE 0 (v2.3)**: Injetar inteligência real.
    *   Implementar `KaldraLLMClient`.
    *   Substituir embeddings random por `sentence-transformers` ou API.
    *   Conectar Perspective API no Bias Engine.

2.  **PRIORIDADE 1 (v2.4)**: Refinar Matemática.
    *   Documentar e calibrar o solver Painlevé.
    *   Implementar persistência de estado para o Drift (memória).

3.  **PRIORIDADE 2 (v2.5+)**: Expandir Features.
    *   Evoluir Meta-Engines e Apps.

---

## v2.3 Completion Note (2025-11-28)

**A v2.3 eliminou a principal dívida de simulação** identificada neste relatório:

- ✅ **LLM Client "Oco" → RESOLVIDO**: `OpenAILLMClient` implementado com fallback para `DummyLLMClient`
- ✅ **Embeddings Simulados → RESOLVIDO**: `EmbeddingGenerator` com providers real (OpenAI/SentenceTransformers) + modo LEGACY
- ✅ **Bias Engine "Fantasma" → RESOLVIDO**: Arquitetura de providers com `PerspectiveProvider` + `HeuristicProvider`

**Os próximos gaps relevantes são**:
- TW369 real (Tracy-Widom estatística, não heurística)
- Memória de Drift (persistência de estado temporal)
- Especialização por App (Alpha/Geo/Product com lógica de negócio específica)
- Meta-Engines com profundidade filosófica real

**Status**: A base de "Real Intelligence" está estabelecida. v2.4+ focará em refinamento matemático e expansão de features.

