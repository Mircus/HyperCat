# HyperCat ActionList — Lean & Focused on Hyper‑Transformers
**Mission:** Keep HyperCat small, precise, and rigorous. Own *Hyper‑Transformers* and higher‑level NN architectures
(models that act on models, architecture rewrites, and deformation paths with certificates). LambdaCat owns agentic pipelines.

---

## 0) Scope & Non‑Goals
**Scope**
- Model categories for architectures/weights; meta‑transformers as endofunctors; deformation paths and rollback; proof‑bearing checks.
- Architecture rewrites with typed certificates; symmetry/gauge checks; ε‑commutation certificates for common recipes.

**Non‑Goals**
- No pipeline orchestration, routing, or LangGraph compilation here (lives in LambdaCat).
- No heavy HoTT/Lean stack; only minimal higher checks needed for coherence.

---

## 1) P0 Fundamentals — Hardening (immediate)
- [ ] **P0.1** Remove dead imports (`usabilitylayer.py`) or move to `experimental/`. Ensure `hypercat/*` imports only shipped modules.
- [ ] **P0.2** Finish `core.Category`: total `compose`, `compose_path`, identities, associativity checks; `get_hom(A,B)`; deterministic path hashing.
- [ ] **P0.3** Promote `diagram/CommutativityChecker` to public API returning `(ok, cert)`; `cert` is a minimal 2‑cell composition.
- [ ] **P0.4** CI: `pytest`, `ruff`, `mypy` (partial). Add smoke tests for `Category` and `CommutativityChecker`.
- [ ] **P0.5** Docs: one runnable import‑based example; clear “Stable vs Experimental” page.

---

## 2) Bicategory Kernel + Proof Terms (P0→P1)
- [ ] **P1.1** `higher/bicategory.py`: objects, 1‑cells (`Morphism`), 2‑cells (`TwoCell`), vertical/horizontal composition;
     named associators/unitors as invertible 2‑cells; `check_coherence()` on finite fixtures.
- [ ] **P1.2** Proof objects: 2‑cells are serializable (JSON) and used by `CommutativityChecker` to witness commutativity.
- [ ] **P1.3** `tikzcd` exporter for certificates.

**Deliverable:** bicategory core + tests; checker emits proof certificates.

---

## 3) Core Model Categories — TransCat & ArchCat (P0→P1)
- [ ] **P1.4** `ml/transcat.py` — **TransCat**: 
  - **Objects** = `(ArchSpec, ModelHandle)` (no heavy tensors in core; handles/refs only).
  - **Morphisms** = structure‑preserving **MetaOps** (LoRA attach/fuse, quantize, prune, reparam, distill). Each has an executable `apply()` (backend‑optional).
- [ ] **P1.5** `ml/archcat.py` — **ArchCat**:
  - **Objects** = typed **architecture graphs/DAGs**.
  - **Morphisms** = **typed rewrites** (pattern substitutions, head moves, width changes) with side‑conditions.
  - **Certificates**: rewrite witnesses as 2‑cells; optional ε‑bounds from micro‑eval after rewrite.

---

## 4) Meta‑Transformers (Endofunctors) & Natural Transformations (P1)
- [ ] **P1.6** Endofunctor API: `MetaTransformer(F): TransCat→TransCat` with unit/comp law tests on fixtures.
- [ ] **P1.7** Natural transformations between meta‑transformers (e.g., `Quantize∘Prune ⇒ Prune∘Quantize` on a class of models) with ε‑certificates.
- [ ] **P1.8** Learned meta‑transformers (wrappers):
  - **WeightFormer** (acts on parameter tokens; learned optimizer/meta‑adapter),
  - **GraphFormer** (acts on architecture graph; proposes certified surgeries),
  - **PromptHyperNet** (adapter weights from prompts/tasks).

---

## 5) Deformation Paths & Rollback (P1)
- [ ] **P1.9** `ml/deform.py`: `WeightManifold` (vectorization + metrics), `PathSpace` (γ: [0,1]→models), `Homotopy(f,g)`.
- [ ] **P1.10** Path calculus: pushforward along meta‑ops `F_*(γ)`; path functionals (loss, KL, curvature proxies) with light hooks to torch backends.
- [ ] **P1.11** Rollback: monotone‑risk rollback along γ with certificate that risk ≤ ε at rollback point.

---

## 6) Symmetry & Gauge Invariance (P1)
- [ ] **P1.12** Permutation invariance checks (neuron/head permutations) and reparameterization invariances (e.g., equivalent factorizations) on small fixtures.
- [ ] **P1.13** Quotient metrics under symmetries; certs that meta‑ops respect required invariances.

---

## 7) Minimal Quasi‑Categorical Sanity (P2 – optional)
- [ ] **P2.1** `higher/sset.py`, `higher/quasicat.py`: finite simplicial sets; inner‑horn checks up to dim 3 for small nerves.
- [ ] **P2.2** `nerve(Category)` + mapping‑space sanity tests on toy examples.
- [ ] **P2.3** Use to validate homotopy‑coherent families of rewrites (optional).

---

## 8) Tests, Demos, and Docs (always‑on)
- [ ] **T.1** Unit tests: core category laws, bicategory 2‑cells, TransCat/ArchCat basics, meta‑transformer laws, deformation paths, symmetry checks.
- [ ] **T.2** CPU‑only micro‑demos:
  - `demos/hyper/00_certified_lora_fuse.ipynb` — LoRA fuse with ε‑certificate + rollback γ.
  - `demos/hyper/01_weightformer_vs_sgd.ipynb` — meta‑update vs SGD; symmetry checks; certificates.
  - `demos/hyper/02_graph_surgery_invariance.ipynb` — architecture rewrite + ε‑commutation with quantizer.
- [ ] **D.1** Tech note (10–12 pp): *Hyper‑Transformers with HyperCat* — definitions, APIs, proofs, examples, limits.

---

## 9) Milestones (30/60/90)
**Day 0–10 (v0.1)** — P0 fundamentals, Bicategory+certs, TransCat skeleton, one MetaOp (LoRA‑attach), Demo 00 stub, CI.

**Day 11–25 (v0.2)** — ArchCat with typed rewrites + certs; more MetaOps (Quantize, Prune); first Natural Transformation with ε‑bound; Deformation PathSpace; Demo 01.

**Day 26–45 (v0.3)** — WeightFormer/GraphFormer wrappers; symmetry checks; ε‑commutation demo (quantize↔prune); Demo 02; docs pass.

---

## 10) Risks & Mitigations
- **Backend drag**: keep torch adapters optional and thin; mock in tests.
- **Scope creep**: no pipeline logic; defer profunctors/PROPs until clearly needed for model/data correspondences.
- **Performance**: tiny models + micro‑suites in CI; certify deltas with ε bounds.

---

## 11) File/Module Plan (updated)
```
src/hypercat/
  core/
    core.py                        # hardened Category/Object/Morphism
  diagram/
    enhanced_diagram_checker.py    # CommutativityChecker (+ proof certs)
  higher/
    bicategory.py                  # Bicategory, TwoCell, coherence checks
    sset.py, quasicat.py           # optional small quasi-cat utilities (P2)
  ml/
    transcat.py                    # TransCat objects/morphisms (MetaOps)
    archcat.py                     # ArchCat typed rewrites + certificates
    deform.py                      # WeightManifold, PathSpace, Homotopy
    backends/
      torch/
        adapters.py                # LoRA attach/fuse, quantize, prune (toy)
  demos/
    hyper/00_certified_lora_fuse.ipynb
    hyper/01_weightformer_vs_sgd.ipynb
    hyper/02_graph_surgery_invariance.ipynb
tests/
  test_core_category.py
  test_bicategory.py
  test_checker_certs.py
  test_transcat.py
  test_archcat_rewrites.py
  test_deform_paths.py
  test_symmetry_checks.py
```

---

## 12) Acceptance Criteria (HC lean & mean)
- **AC‑1** Checker returns `(ok, cert)` with non‑empty 2‑cell proofs on ≥3 non‑trivial diagrams; `tikzcd` export compiles.
- **AC‑2** TransCat ships ≥3 MetaOps (LoRA‑attach, Quantize, Prune) with unit/comp law tests.
- **AC‑3** ArchCat performs ≥2 typed rewrites with certificates; micro‑eval produces ε‑bounds.
- **AC‑4** Natural Transformation: `Quantize∘Prune ⇒ Prune∘Quantize` certified within ε on a toy family.
- **AC‑5** Deformation path γ between two models with metrics (loss, KL) and rollback guarantee demonstrated in Demo 00/01.
- **AC‑6** Symmetry checks pass on at least one WeightFormer or GraphFormer wrapper.
