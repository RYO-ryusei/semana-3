"""
Práctica Semana 3 — Actividad 3: Verificación del Principio de Sustitución de Liskov
Curso : SIS206 Programación Orientada a Objetos II — UNAP Puno — 2026-II
Alumno: Kevin Manuel Vilca Paco
Docente: Dr. Aldo Hernán Zanabria Gálvez

Parte A: contrato invariante sobre PersonalUniversitario (TODAS las subclases pasan).
Parte B: Cuadrado hereda de Rectangulo  → VIOLA el LSP.
Parte C: rediseño correcto (hermanos bajo una Figura abstracta) → cumple el LSP.
"""
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

# Reutilizamos la jerarquía de la Actividad 2
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "actividad2_python"))
from personal_unap import PersonalUniversitario, crear_personal  # noqa: E402


# ════════════════════════════════════════════════════════════════════════
# PARTE A — Contrato de la jerarquía PersonalUniversitario
# ════════════════════════════════════════════════════════════════════════
def verificar_contrato_personal(p: PersonalUniversitario) -> bool:
    """
    Contrato que TODA subclase debe satisfacer:
    1. nombre_completo retorna string no vacío
    2. calcular_remuneracion() retorna valor > 0
    3. str(p) contiene el nombre completo
    """
    ok = True
    ok = ok and isinstance(p.nombre_completo, str) and len(p.nombre_completo) > 0
    ok = ok and p.calcular_remuneracion() > 0
    ok = ok and p.nombre_completo in str(p)
    return ok


def parte_a() -> None:
    print("=" * 64)
    print("PARTE A — Contrato LSP sobre PersonalUniversitario")
    print("=" * 64)
    personal = crear_personal()
    for p in personal:
        estado = "OK " if verificar_contrato_personal(p) else "FALLA"
        print(f"[{estado}] {type(p).__name__:<14} {p.nombre_completo}")
    assert all(verificar_contrato_personal(p) for p in personal)
    print("→ Todas las subclases superan el contrato: LSP respetado.\n")


# ════════════════════════════════════════════════════════════════════════
# PARTE B — Violación clásica: Cuadrado hereda de Rectangulo
# ════════════════════════════════════════════════════════════════════════
class Figura:
    def area(self) -> float: ...


class Rectangulo(Figura):
    def __init__(self, ancho: float, alto: float):
        self._ancho = ancho
        self._alto = alto

    def set_ancho(self, v: float) -> None: self._ancho = v
    def set_alto(self, v: float) -> None: self._alto = v
    def area(self) -> float: return self._ancho * self._alto


class Cuadrado(Rectangulo):
    def __init__(self, lado: float):
        super().__init__(lado, lado)

    def set_ancho(self, v: float) -> None:
        self._ancho = v
        self._alto = v  # fuerza ambos lados iguales

    def set_alto(self, v: float) -> None:
        self._ancho = v
        self._alto = v


def test_rectangulo(r: Rectangulo) -> None:
    """Test que DEBERÍA pasar para cualquier Rectangulo según LSP."""
    r.set_ancho(4)
    r.set_alto(5)
    area_esperada = 20.0
    assert r.area() == area_esperada, (
        f"LSP violado: area={r.area()}, esperado={area_esperada}"
    )


def parte_b() -> None:
    print("=" * 64)
    print("PARTE B — Cuadrado hereda de Rectangulo (violación del LSP)")
    print("=" * 64)
    rect = Rectangulo(2, 2)
    test_rectangulo(rect)  # OK
    print("[OK ] test_rectangulo(Rectangulo)  → área = 20.0")

    cuad = Cuadrado(2)
    try:
        test_rectangulo(cuad)  # FALLA — viola LSP
    except AssertionError as e:
        print(f"[FALLA] test_rectangulo(Cuadrado) → {e}")
        print("LSP VIOLADO en Cuadrado.")
        print("Solución: no heredar Cuadrado de Rectangulo; "
              "usar composición o interfaz independiente.\n")


# ════════════════════════════════════════════════════════════════════════
# PARTE C — Rediseño que SÍ cumple el LSP
#   Figura (abstracta)
#    ├── RectanguloInmutable(ancho, alto)
#    └── CuadradoInmutable(lado)
#   Son "hermanos": ninguno promete lo que el otro no puede cumplir.
#   Al ser inmutables, no existen set_ancho / set_alto que rompan el contrato.
# ════════════════════════════════════════════════════════════════════════
class FiguraGeometrica(ABC):
    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimetro(self) -> float: ...


@dataclass(frozen=True)
class RectanguloInmutable(FiguraGeometrica):
    ancho: float
    alto: float

    def area(self) -> float:
        return self.ancho * self.alto

    def perimetro(self) -> float:
        return 2 * (self.ancho + self.alto)

    def con_ancho(self, v: float) -> "RectanguloInmutable":
        return RectanguloInmutable(v, self.alto)  # devuelve un objeto NUEVO


@dataclass(frozen=True)
class CuadradoInmutable(FiguraGeometrica):
    lado: float

    def area(self) -> float:
        return self.lado ** 2

    def perimetro(self) -> float:
        return 4 * self.lado


def verificar_contrato_figura(f: FiguraGeometrica) -> bool:
    """Contrato: área y perímetro positivos y consistentes (área ≤ (perím/4)²)."""
    return f.area() > 0 and f.perimetro() > 0 and f.area() <= (f.perimetro() / 4) ** 2


def parte_c() -> None:
    print("=" * 64)
    print("PARTE C — Rediseño sin herencia Cuadrado→Rectangulo (cumple LSP)")
    print("=" * 64)
    figuras: list[FiguraGeometrica] = [
        RectanguloInmutable(4, 5),
        CuadradoInmutable(3),
    ]
    for f in figuras:
        estado = "OK " if verificar_contrato_figura(f) else "FALLA"
        print(f"[{estado}] {type(f).__name__:<20} área={f.area():>5.1f}  "
              f"perímetro={f.perimetro():>5.1f}")
    assert all(verificar_contrato_figura(f) for f in figuras)
    r = RectanguloInmutable(2, 2).con_ancho(4)
    assert r.con_ancho(4).area() == 8
    print("→ Cualquier FiguraGeometrica es sustituible por otra: LSP respetado.")


if __name__ == "__main__":
    parte_a()
    parte_b()
    parte_c()
