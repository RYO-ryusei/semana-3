"""
Práctica Semana 3 — Actividad 5: Proyecto Integrador (Sistema de Biblioteca UNAP)
Curso : SIS206 Programación Orientada a Objetos II — UNAP Puno — 2026-II
Alumno: Kevin Manuel Vilca Paco
Docente: Dr. Aldo Hernán Zanabria Gálvez

Jerarquía de herencia (IS-A):
    RecursoBibliografico (abstracta)
      ├── LibroFisico
      ├── LibroDigital
      └── Revista

Composición (HAS-A) de semanas previas:
    Biblioteca  ◆── RecursoBibliografico   (la biblioteca es dueña de sus recursos)
    Prestamo    ──> RecursoBibliografico / Usuario  (asociación)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override  # Python 3.12+


# ════════════════════════════════════════════════════════════════════════
# JERARQUÍA: RecursoBibliografico  (IS-A)
# ════════════════════════════════════════════════════════════════════════
class RecursoBibliografico(ABC):
    """Clase base abstracta de todo material que presta la biblioteca."""

    def __init__(self, codigo: str, titulo: str, autor: str, anio: int):
        if not codigo:
            raise ValueError("El código no puede estar vacío")
        if anio < 1450:
            raise ValueError(f"Año inválido: {anio}")
        self._codigo = codigo
        self._titulo = titulo
        self._autor = autor
        self._anio = anio

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def titulo(self) -> str:
        return self._titulo

    @abstractmethod
    def dias_prestamo(self) -> int:
        """Días máximos que el usuario puede tener el recurso."""

    @abstractmethod
    def calcular_multa(self, dias_retraso: int) -> float:
        """Multa en S/ por devolver con 'dias_retraso' días de atraso (>= 0)."""

    def tipo(self) -> str:
        return "Recurso"

    def descripcion(self) -> str:
        return f"[{self.tipo()}] {self._titulo} — {self._autor} ({self._anio})"

    def __str__(self) -> str:
        return self.descripcion()


class LibroFisico(RecursoBibliografico):
    MULTA_DIARIA = 1.50

    def __init__(self, codigo: str, titulo: str, autor: str, anio: int,
                 paginas: int, ejemplares: int = 1):
        super().__init__(codigo, titulo, autor, anio)
        if paginas <= 0 or ejemplares < 1:
            raise ValueError("Páginas y ejemplares deben ser positivos")
        self._paginas = paginas
        self._ejemplares = ejemplares

    @override
    def tipo(self) -> str:
        return "Libro físico"

    @override
    def dias_prestamo(self) -> int:
        return 7

    @override
    def calcular_multa(self, dias_retraso: int) -> float:
        return max(0, dias_retraso) * self.MULTA_DIARIA

    @override
    def descripcion(self) -> str:
        return (f"{super().descripcion()} · {self._paginas} págs · "
                f"{self._ejemplares} ejemplar(es)")


class LibroDigital(RecursoBibliografico):
    """El préstamo digital expira solo: no genera multa por retraso."""

    def __init__(self, codigo: str, titulo: str, autor: str, anio: int,
                 formato: str, tamano_mb: float):
        super().__init__(codigo, titulo, autor, anio)
        if formato.upper() not in {"PDF", "EPUB"}:
            raise ValueError(f"Formato no soportado: {formato}")
        if tamano_mb <= 0:
            raise ValueError("El tamaño debe ser positivo")
        self._formato = formato.upper()
        self._tamano_mb = tamano_mb

    @override
    def tipo(self) -> str:
        return "Libro digital"

    @override
    def dias_prestamo(self) -> int:
        return 14

    @override
    def calcular_multa(self, dias_retraso: int) -> float:
        return 0.0  # la licencia caduca automáticamente → contrato (>= 0) se cumple

    @override
    def descripcion(self) -> str:
        return (f"{super().descripcion()} · {self._formato} · "
                f"{self._tamano_mb:.1f} MB")


class Revista(RecursoBibliografico):
    MULTA_DIARIA = 2.00

    def __init__(self, codigo: str, titulo: str, autor: str, anio: int,
                 volumen: int, numero: int):
        super().__init__(codigo, titulo, autor, anio)
        if volumen < 1 or numero < 1:
            raise ValueError("Volumen y número deben ser positivos")
        self._volumen = volumen
        self._numero = numero

    @override
    def tipo(self) -> str:
        return "Revista"

    @override
    def dias_prestamo(self) -> int:
        return 3

    @override
    def calcular_multa(self, dias_retraso: int) -> float:
        return max(0, dias_retraso) * self.MULTA_DIARIA

    @override
    def descripcion(self) -> str:
        return f"{super().descripcion()} · Vol. {self._volumen} Nº {self._numero}"


# ════════════════════════════════════════════════════════════════════════
# COMPOSICIÓN / ASOCIACIÓN (HAS-A) — semanas previas
# ════════════════════════════════════════════════════════════════════════
@dataclass
class Usuario:
    codigo: str
    nombre: str


class Prestamo:
    """Asociación: un préstamo REFERENCIA a un recurso y a un usuario."""

    def __init__(self, usuario: Usuario, recurso: RecursoBibliografico,
                 dias_retraso: int = 0):
        self.usuario = usuario
        self.recurso = recurso
        self.dias_retraso = dias_retraso

    def multa(self) -> float:
        # Delegación polimórfica: no importa qué tipo de recurso sea
        return self.recurso.calcular_multa(self.dias_retraso)


class Biblioteca:
    """Composición: la biblioteca CONTIENE y administra su catálogo."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self._catalogo: list[RecursoBibliografico] = []

    def agregar(self, recurso: RecursoBibliografico) -> None:
        if any(r.codigo == recurso.codigo for r in self._catalogo):
            raise ValueError(f"Código duplicado: {recurso.codigo}")
        self._catalogo.append(recurso)

    @property
    def catalogo(self) -> list[RecursoBibliografico]:
        return list(self._catalogo)  # copia defensiva


# ════════════════════════════════════════════════════════════════════════
# POLIMORFISMO DINÁMICO sobre lista heterogénea
# ════════════════════════════════════════════════════════════════════════
def reporte_catalogo(recursos: list[RecursoBibliografico],
                     dias_retraso: int = 4) -> None:
    """Itera la lista heterogénea SIN usar isinstance()."""
    print("=" * 78)
    print(f"CATÁLOGO — multa simulada con {dias_retraso} días de retraso")
    print("=" * 78)
    total = 0.0
    for r in recursos:
        multa = r.calcular_multa(dias_retraso)  # ← método distinto por subclase
        total += multa
        print(r.descripcion())
        print(f"    Préstamo: {r.dias_prestamo():>2} días │ Multa: S/ {multa:>5.2f}")
    print("-" * 78)
    print(f"TOTAL MULTAS SIMULADAS: S/ {total:.2f}")


def verificar_contrato_recurso(r: RecursoBibliografico) -> bool:
    """Contrato LSP: descripción no vacía, préstamo > 0, multa >= 0 y sin retraso = 0."""
    return (
        len(r.descripcion()) > 0
        and r.dias_prestamo() > 0
        and r.calcular_multa(5) >= 0
        and r.calcular_multa(0) == 0
    )


if __name__ == "__main__":
    biblio = Biblioteca("Biblioteca Central — UNAP Puno")
    biblio.agregar(LibroFisico("LF-001", "Clean Code", "Robert C. Martin", 2008, 464, 3))
    biblio.agregar(LibroDigital("LD-001", "Design Patterns", "Gamma et al.", 1994, "pdf", 12.5))
    biblio.agregar(Revista("RV-001", "Revista de Ingeniería de Sistemas", "UNAP", 2025, 12, 2))

    reporte_catalogo(biblio.catalogo, dias_retraso=4)

    print()
    for r in biblio.catalogo:
        assert isinstance(r, RecursoBibliografico)
        assert verificar_contrato_recurso(r)
    print("Verificación LSP: OK — las 3 subclases sustituyen a RecursoBibliografico")

    print("\nPRÉSTAMO (asociación + delegación polimórfica)")
    print("-" * 78)
    u = Usuario("U-100", "Kevin Manuel Vilca Paco")
    for r, dias in zip(biblio.catalogo, (2, 10, 1)):
        p = Prestamo(u, r, dias_retraso=dias)
        print(f"{p.usuario.nombre} devolvió '{r.titulo}' con {dias} día(s) de retraso "
              f"→ multa S/ {p.multa():.2f}")

    print("\nVALIDACIÓN")
    print("-" * 78)
    try:
        biblio.agregar(Revista("RV-001", "Duplicada", "X", 2024, 1, 1))
    except ValueError as e:
        print(f"[OK] {e}")
