# BCP Plus — One-Pager de Rollout

**Objetivo:** evoluir o contador atual de **3 dimensões** para as **13 dimensões** do BCP Plus, com resultados repetíveis o suficiente para monitorar velocidade das equipes e comparáveis ao longo do tempo.

**Status do plano:** completo e auditado como **READY** (11 epics, stories e critérios de aceite escritos). Execução ainda **não iniciada** (0/11 epics).

---

## Por que o repo precisa evoluir

| Hoje | Alvo (nível adequado) |
|---|---|
| 3 dimensões (Boundaries, Interface Elements, Business Rules) | **13 dimensões** BCP Plus (7 funcionais + 3 NFR + as 3 atuais) |
| Mesma seção da story alimenta 2 prompts → **double-counting** | **Element Router**: cada elemento em **exatamente 1** dimensão |
| Sem medição de repetibilidade | **Stability harness**: CV por dimensão < 20% (intrínsecas) / < 25% (maturidade) |
| Resultados sem rastreabilidade | Todo resultado carrega **`calibration_id`** — só comparável se o ID bate |
| Lógica duplicada por entry point | CLI/API/MCP/SDK usam **uma** função de orquestração |

---

## Caminho de rollout (ordenado, com portões)

```
e01 refactor ──HARD GATE──> e02 Element Router ──> e04 harness ──> e08 tuning ──HARD GATE──> e09 publish
  (base)         (mata           |                  (mede CV)      (CV ≈ 10-15%)     (whitepaper +
                double-count)     ├─> e05 dims funcionais simples                     OKF ruler)
                                  ├─> e06 dims funcionais complexas
                                  └─> e07 dims NFR
                                        e10 OKF output / e11 OKF domain (paralelos)
```

1. **e01** — Refactor das 3 dimensões em módulos puros (base, preserva comportamento)
2. **e02** — Element Router: fim do double-counting *(depende de e01 — HARD GATE)*
3. **e03** — Limpeza de config de provider *(independente, entra a qualquer hora)*
4. **e04** — Stability harness (record / report / replay)
5. **e05 / e06 / e07** — As 10 novas dimensões (funcionais simples, funcionais complexas, NFR)
6. **e08** — Tuning até CV agregado ≈ 10-15% *(depende de e04–e07)*
7. **e09** — Whitepaper evolution + bundle OKF do ruler *(depende de e08 — HARD GATE)*
8. **e10 / e11** — Saída OKF dos resultados / entrada de conhecimento de domínio

---

## Definição de "adequado" (critérios de aceite)

- Nenhum elemento contado em duas dimensões (provado por golden fixtures)
- 13 dimensões, cada uma com Identity Rule + decision table **sem adjetivos** (critério objetivo)
- CV por dimensão dentro da meta; CV agregado ≈ 10-15% no bucket de maturidade `reliable`
- Todo resultado com bloco de proveniência `calibration_id`
- Um único ponto de orquestração para todos os entry points

---

## Riscos / decisões para alinhar na reunião

- **Custo de API:** protocolo de estabilidade = 25 iterações × ~14 chamadas × N stories. Controlado por sampling determinístico + replay offline (custo zero no replay).
- **Rebaseline:** números pré-Router são tratados como **incomparáveis** (ADR-0004) — não há migração histórica planejada. Decidir se alguma equipe consumidora precisa disso.
- **Recalibração ao trocar de modelo:** trocar o modelo LLM exige rodar o protocolo completo de recalibração (ADR-0011), como evento deliberado — nunca swap automático.
- **Drift de escopo a reconciliar:** e10/e11 ainda não estão no `SCOPE_LATEST.yaml`; texto do hard gate e08→e09 conflita com `docs/bcp-ruler/` já commitado; `tech-stack.md` desatualizado; `app.py` sem epic associado.

---

## Próximo passo

Iniciar **e01** (0/3 stories) — destrava todo o resto via o hard gate e01→e02. Baseline técnico está verde (54 testes, 88% cobertura, mypy limpo).

*Referências: `specs/PLAN.md`, `specs/release-plan.yaml`, `specs/product/SCOPE_LATEST.yaml`, `specs/PLAN-AUDIT_LATEST.md`, `specs/ADRS/`.*
