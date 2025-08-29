
from hypercat.ml.transcat import ArchSpec, ModelHandle, lora_attach, quantize, NaturalTransformation

def test_nat_transformation_cert():
    arch = ArchSpec("Toy")
    models = [ModelHandle(arch, {"w": 0.2, "b": -0.3}),
              ModelHandle(arch, {"w": -0.1, "b": 0.05})]
    F = lora_attach(0.1); G = quantize(0.5)
    nat = NaturalTransformation(lhs=F>>G, rhs=G>>F, eps=0.35, metric=lambda a,b: sum((a.weights[k]-b.weights[k])**2 for k in a.weights)/len(a.weights))
    ok, worst = nat.certify(models)
    assert ok
