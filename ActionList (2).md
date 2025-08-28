# HyperCat ActionList — Hypercategories for Meta‑Models
**Focus:** Transformers-on-Transformers (meta-transformers) and deformation paths, without turning HyperCat into a HoTT/Lean prover.

---

## 0) Goals & Non‑Goals
**Goals**
- Provide **practical higher-structure** to model systems where **transformers act on transformers** (meta‑transforms) and where **models deform along paths** (homotopies in parameter/architecture space).
- Keep APIs **minimal, typed, testable**, and **PyTorch‑ready** (executable semantics). Produce **proof objects** (2‑cells) only where they add value (commutativity/coherence certificates).
- Interoperate with SHE-style hyperstructures: multi‑input/multi‑output operations (PROPs) and typed hypergraph rewrites.

**Non‑Goals**
- No foundational HoTT/Lean replica. No general theorem proving.
- No infinite machinery of (∞,1)-cat beyond small quasi‑categorical checks for coherence sanity.

---

## 1) Repo Hardening (P0 – immediate)
- [ ] **P0.1** Remove dead imports (`usabilitylayer.py`) or move to `experimental/`. Ensure `hypercat/*` imports only from shipped modules.
- [ ] **P0.2** Finish `core.Category`: total `compose`, `compose_path`, identities, associativity checks; `get_hom(A,B)`; deterministic equality/hash for paths.
- [ ] **P0.3** Make `diagram/CommutativityChecker` public API:
  ```python
  from hypercat.diagram import CommutativityChecker
  ok, cert = CommutativityChecker(cat).check(diagram)
  ```
  `cert` = minimal 2‑cell proof term (see §3).
- [ ] **P0.4** CI: `pytest`, `ruff`, `mypy` (partial). Add smoke tests for Category/Checker.
- [ ] **P0.5** Docs: “What works / Experimental”. One runnable example importing the package (no local path hacks).

---

## 2) Bicategory Kernel + Proof Terms (P0→P1)
- [ ] **P1.1** Add `higher/bicategory.py`:
  - Objects, 1‑cells (`Morphism`), 2‑cells (`TwoCell`), vertical/horizontal composition.
  - Named **associators/unitors** as invertible 2‑cells; `check_coherence()` (pentagon/triangle tests on finite fixtures).
- [ ] **P1.2** **Proof objects**: 2‑cells are first‑class and serializable (JSON). Integrate with `CommutativityChecker`: when a diagram commutes, return a 2‑cell witness (composition of generators).
- [ ] **P1.3** Minimal `tikzcd` exporter for proof certificates.

**Deliverable:** `Bicategory` with tests + checker emitting 2‑cell certificates.

---

## 3) Category of Transformers (TransCat) & Meta‑Transformers (P0→P1)
- [ ] **P1.4** Create `ml/transcat.py`:
  - **Objects** = `(ArchitectureSpec, WeightsHandle)` abstractions (no heavy tensors in core).
  - **Morphisms** = structure‑preserving maps between models: e.g., adapters (LoRA), quantize/dequantize, prune, reparameterize, distill. Each morphism carries an **executable** `apply()` that returns a new object (possibly lazy with a handle).
  - Registry for **PyTorch adapters** (in `ml/backends/torch/`), kept optional.
- [ ] **P1.5** **Meta‑Transformer** = **endofunctor** `F: TransCat → TransCat` (e.g., attach‑LoRA, Fuse‑LoRA, Quantize, Prune, Distill). Ensure functor laws are unit‑tested on small fixtures.
- [ ] **P1.6** **Natural transformations** between meta‑transformers (e.g., *Quantize∘Prune ⇒ Prune∘Quantize* on a restricted class). Provide construction helpers and checker emits 2‑cell certificates when the square commutes on a test family.

**Deliverables:** `TransCat`, endofunctor interface, 3 example meta‑transformers + 1 natural transformation with tests.

---

## 4) Deformation Paths & Homotopies (P1)
- [ ] **P1.7** Add `ml/deform.py`:
  - `WeightManifold`: wraps parameter vectorization and metrics (Frobenius, Fisher diag approx).
  - `PathSpace`: piecewise‑linear or ODE‑defined curves `γ: [0,1]→ models`.
  - `Homotopy(f,g)`: 2‑cell data witnessing a continuous deformation from model `f` to `g` along `γ`.
- [ ] **P1.8** **Path calculus**:
  - Pullback/pushforward along meta‑transformers: `F_*(γ)` and path derivatives.
  - Path functionals: loss along path `L(γ(t))`, curvature proxies (e.g., Hessian‑trace estimates).
- [ ] **P1.9** **Executables** (torch optional): sampling along path to produce **curves of metrics** (loss, KL, accuracy on a micro‑dataset), with lightweight hooks.

**Demos:**
1) Linear/affine weight interpolation between two fine‑tunes;
2) LoRA‑on/off homotopy;
3) Merge‑then‑quantize vs quantize‑then‑merge square with a certificate.

---

## 5) PROPs/Operads for Transformer Composition (P1)
- [ ] **P1.10** `algebraic/prop.py`: multi‑in/multi‑out operations for **string‑diagram** representation of model pipelines (e.g., *[embed, encoder, head]* blocks).
- [ ] **P1.11** `algebraic/multicategory.py`: (colored) **multicategories** for typed module composition; substitution via trees.
- [ ] **P1.12** Bridge: ordinary `Category` ↔ unary multicategory; `MonoidalCategory` as algebra over a PROP.
- [ ] **P1.13** Minimal **diagram‑to‑torch** compiler that instantiates pipelines from PROP graphs (toy‑scale).

**Deliverable:** Typed pipeline builder with validation (arity/types), plus round‑trip with the diagram checker.

---

## 6) Profunctors & Equipments (P1→P2)
- [ ] **P2.1** `higher/profunctor.py`: profunctors `Aᵒᵖ×B→Set` with finite coend composition; natural transformations.
- [ ] **P2.2** **Equipment** (double category) where functors have companions/conjoints. Use this to formalize **dataset‑conditioned relations** between models (e.g., performance correspondences), and **lenses** for data/model splits.
- [ ] **P2.3** Squares encode **training loops** vs **architecture transforms**; certificates show commutation (e.g., *train then quantize* ≈ *quantize then train (few steps)* within tolerance).

**Deliverables:** toy equipment + example “almost commuting” squares with quantitative witness (gap bounds printed).

---

## 7) Minimal Quasi‑Categorical Checks (P2 – optional)
- [ ] **P2.4** `higher/sset.py`, `higher/quasicat.py`: finite simplicial set utilities + inner‑horn filler checks up to dimension 3 for small nerves.
- [ ] **P2.5** `nerve(Category)` + tests; `mapping_space(x,y)` sanity on toy examples.
- [ ] **P2.6** Use quasi‑cat checks to validate **homotopy‑coherent** rewrite families (optional).

---

## 8) Tests, Demos, and Docs (always‑on)
- [ ] **T.1** Unit tests: Category, Bicategory, 2‑cells, TransCat functors/NatTrans, Deformations, PROP typing, Profunctor composition.
- [ ] **T.2** Micro‑demos (CPU‑only):
  - `demos/meta/00_lora_attach.ipynb` — meta‑transformer as endofunctor
  - `demos/meta/01_deform_interpolate.ipynb` — path sampling + metrics
  - `demos/meta/02_square_quantize_merge.ipynb` — 2‑cell certificate + curves
- [ ] **D.1** Docs: “Modeling Transformers‑on‑Transformers with HyperCat” (10–12 pages): definitions, APIs, worked examples, limits.

---

## 9) Milestones (30/60/90 days)
**Day 0–10 (v0.1)**
- P0 hardening (core + checker), Bicategory + proof objects, TransCat skeleton + one meta‑transformer (LoRA‑attach), demo 00, CI.

**Day 11–25 (v0.2)**
- More meta‑transformers (Quantize, Prune), NatTrans square, Deformation PathSpace + demo 01, PROP typing + toy compiler.

**Day 26–45 (v0.3)**
- Profunctors + Equipment + demo 02, quantitative “almost commute” squares; optional quasi‑cat checks; docs.

---

## 10) Risks & Mitigations
- **Heavy weights**: avoid shipping tensors in core; use handles/adapters.
- **Backend churn**: keep backends in `ml/backends/*`, version‑pinned; mock in tests.
- **Scope creep**: stick to endofunctors + 2‑cells + paths; delay full (∞,1) stack.
- **Performance**: demos use tiny models/micro‑datasets; no GPU dependency in CI.

---

## 11) File/Module Plan
```
src/hypercat/
  core/
    core.py                        # Category, Object, Morphism hardening
  diagram/
    enhanced_diagram_checker.py    # CommutativityChecker (public API + certs)
  higher/
    bicategory.py                  # Bicategory, TwoCell, coherence checks
    profunctor.py                  # Profunctors + composition (P2)
    sset.py, quasicat.py           # (optional) small quasi-cat utilities (P2)
  algebraic/
    prop.py                        # PROPs (multi-in/out ops)
    multicategory.py               # Colored multicategories
  ml/
    transcat.py                    # Category of Transformers (objects/morphisms)
    deform.py                      # WeightManifold, PathSpace, Homotopy
    backends/
      torch/
        adapters.py                # LoRA attach/fuse, quantize, prune (toy)
  demos/
    meta/00_lora_attach.ipynb
    meta/01_deform_interpolate.ipynb
    meta/02_square_quantize_merge.ipynb
tests/
  test_core_category.py
  test_bicategory.py
  test_checker_certs.py
  test_transcat_functors.py
  test_deform_paths.py
  test_prop_typing.py
  test_profunctor_comp.py
```

---

## 12) Concrete Acceptance Criteria
- **AC‑1** `CommutativityChecker` returns `(ok, cert)` with a non‑empty cert on at least 3 non‑trivial diagrams; `tikzcd` export compiles.
- **AC‑2** `TransCat`: at least **3 endofunctors** (LoRA‑attach, Quantize, Prune) and **1 natural transformation** proven on a finite test set.
- **AC‑3** `PathSpace`: interpolate between two models, compute `(loss, KL)` curve on micro‑dataset; plot saved by demo.
- **AC‑4** `PROP` pipeline: well‑typed instantiation of a toy transformer stack; checker validates wiring; round‑trip to executable.
- **AC‑5** Profunctor composition works on a 3‑object toy example; one equipment square demo renders and passes a commutation tolerance check.
