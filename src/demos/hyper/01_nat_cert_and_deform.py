
from hypercat.ml.transcat import ArchSpec, ModelHandle, lora_attach, quantize, NaturalTransformation
from hypercat.ml.deform import Deformation
from hypercat.diagram.commutativity_checker import Diagram, Relation, CommutativityChecker

def main():
    arch = ArchSpec("TinyT", meta={"layers":2})
    m0 = ModelHandle(arch, {"w": 0.2, "b": -0.3})
    m1 = ModelHandle(arch, {"w": 0.9, "b": 0.1})

    F = lora_attach(0.1)
    G = quantize(0.5)

    # ε-certificate
    nat = NaturalTransformation(lhs=F>>G, rhs=G>>F, eps=0.3, metric=lambda a,b: sum((a.weights[k]-b.weights[k])**2 for k in a.weights)/len(a.weights))
    ok, worst = nat.certify([m0, m1])
    print("Nat. transf. cert:", ok, "worst Δ=", worst)

    # Diagram certificate
    rels = [Relation((F.name,G.name), (G.name,F.name), "swap_recipes")]
    ok2, cert = CommutativityChecker(rels).check(Diagram((F.name,G.name), (G.name,F.name)))
    print("Diagram cert:", ok2, cert.steps)

    # Deformation path
    end = (F>>G).op.apply(m0)
    path = Deformation.between(m0, end, steps=5)
    for i, p in enumerate(path.points):
        t = i/(len(path.points)-1) if len(path.points)>1 else 0.0
        print(f"t={t:.2f} weights={p.weights}")

if __name__ == "__main__":
    main()
