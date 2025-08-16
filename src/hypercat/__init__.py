from importlib.metadata import version, PackageNotFoundError

__all__ = [
	"core",
	"agents",
	"extras",
	"plugins",
]

try:
	__version__ = version("hypercat")
except PackageNotFoundError:
	__version__ = "0.0.0"

# Minimal friendly re-exports for the new core API
from .core.presentation import Obj, ArrowGen, Formal1, Presentation  # noqa: E402,F401
