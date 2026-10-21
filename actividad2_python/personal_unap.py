"""
Práctica Semana 3 — Actividad 2: Jerarquía PersonalUniversitario (Python 3.12+)
Curso : SIS206 Programación Orientada a Objetos II — UNAP Puno — 2026-II
Alumno: Kevin Manuel Vilca Paco
Docente: Dr. Aldo Hernán Zanabria Gálvez

Demuestra: herencia (IS-A), clase base abstracta, @override, super(),
validaciones en subclases y polimorfismo dinámico en planilla().
"""
from abc import ABC, abstractmethod
from typing import override  # Python 3.12+


class PersonalUniversitario(ABC):
    """Clase base abstracta para todo el personal de la UNAP."""

    TARIFA_HORA_BASE = 75.0  # S/ por hora

    def __init__(self, dni: str, nombres: str, apellidos: str):
        self.__dni = self._validar_dni(dni)
        self._nombres = nombres
        self._apellidos = apellidos

    @staticmethod
    def _validar_dni(dni: str) -> str:
        if not (dni.isdigit() and len(dni) == 8):
            raise ValueError(f"DNI inválido: {dni!r} (debe tener 8 dígitos)")
        return dni

    @property
    def dni(self) -> str:
        return self.__dni

    @property
    def nombre_completo(self) -> str:
        return f"{self._apellidos}, {self._nombres}"

    @abstractmethod
    def calcular_remuneracion(self) -> float:
        """Cada subclase define su propio cálculo."""
        ...

    def __str__(self) -> str:
        return f"{self.nombre_completo} → S/ {self.calcular_remuneracion():.2f}"


class Docente(PersonalUniversitario):
    FACTORES = {"Auxiliar": 1.0, "Asociado": 1.4, "Principal": 1.8}

    def __init__(self, dni: str, nombres: str, apellidos: str,
                 horas: int, categoria: str):
        super().__init__(dni, nombres, apellidos)
        # Validar horas > 0 y <= 40
        if not (0 < horas <= 40):
            raise ValueError(f"Horas fuera de rango: {horas} (debe estar en 1..40)")
        # Validar categoría en FACTORES
        if categoria not in self.FACTORES:
            raise ValueError(
                f"Categoría inválida: {categoria!r} "
                f"(use: {', '.join(self.FACTORES)})"
            )
        # Asignar atributos
        self._horas = horas
        self._categoria = categoria

    @override
    def calcular_remuneracion(self) -> float:
        # horas * TARIFA_HORA_BASE * factor de categoría
        return self._horas * self.TARIFA_HORA_BASE * self.FACTORES[self._categoria]


class Administrativo(PersonalUniversitario):
    def __init__(self, dni: str, nombres: str, apellidos: str,
                 salario_base: float, bono: float = 0.0):
        super().__init__(dni, nombres, apellidos)
        # Validar salario_base > 0
        if salario_base <= 0:
            raise ValueError("El salario base debe ser mayor que 0")
        if bono < 0:
            raise ValueError("El bono no puede ser negativo")
        # Asignar atributos
        self._salario_base = salario_base
        self._bono = bono

    @override
    def calcular_remuneracion(self) -> float:
        # salario_base + bono
        return self._salario_base + self._bono


class Investigador(PersonalUniversitario):
    """Investigador a tiempo completo — remunerado por proyectos activos."""

    REMUNERACION_POR_PROYECTO = 1500.0

    def __init__(self, dni: str, nombres: str, apellidos: str,
                 proyectos: int):
        super().__init__(dni, nombres, apellidos)
        if proyectos < 1:
            raise ValueError("Debe tener al menos 1 proyecto activo")
        self._proyectos = proyectos

    @override
    def calcular_remuneracion(self) -> float:
        return self._proyectos * self.REMUNERACION_POR_PROYECTO


def planilla(personal: list[PersonalUniversitario]) -> None:
    """Imprime la planilla usando polimorfismo — sin isinstance()."""
    total = 0.0
    print("=" * 60)
    print("PLANILLA PERSONAL UNIVERSITARIO — UNAP PUNO")
    print("=" * 60)
    for p in personal:
        print(p)  # llama __str__ → calcular_remuneracion polimórfico
        total += p.calcular_remuneracion()
    print("-" * 60)
    print(f"TOTAL PLANILLA: S/ {total:.2f}")


def crear_personal() -> list[PersonalUniversitario]:
    """Lista heterogénea usada también por la Actividad 3."""
    return [
        Docente("12345678", "Juan Carlos", "Mamani Quispe", 16, "Asociado"),
        Docente("23456789", "María Elena", "Quispe Torres", 12, "Principal"),
        Administrativo("34567890", "Pedro", "Huanca Lazo", 2800.0, 350.0),
        Investigador("45678901", "Ana Lucía", "Flores Ramos", 2),
    ]


def probar_validaciones() -> None:
    """Muestra que las validaciones de las subclases rechazan datos inválidos."""
    casos = [
        ("DNI con 7 dígitos",
         lambda: Docente("1234567", "X", "Y", 10, "Auxiliar")),
        ("Horas = 50 (máx. 40)",
         lambda: Docente("12345678", "X", "Y", 50, "Auxiliar")),
        ("Categoría inexistente",
         lambda: Docente("12345678", "X", "Y", 10, "Titular")),
        ("Salario base negativo",
         lambda: Administrativo("12345678", "X", "Y", -100.0)),
        ("Investigador sin proyectos",
         lambda: Investigador("12345678", "X", "Y", 0)),
        ("Instanciar clase abstracta",
         lambda: PersonalUniversitario("12345678", "X", "Y")),
    ]
    print("\nPRUEBA DE VALIDACIONES")
    print("-" * 60)
    for descripcion, crear in casos:
        try:
            crear()
            print(f"[FALLO] {descripcion}: no lanzó excepción")
        except (ValueError, TypeError) as e:
            print(f"[OK] {descripcion}\n     → {type(e).__name__}: {e}")


if __name__ == "__main__":
    personal = crear_personal()
    planilla(personal)

    # Verificar LSP — todos son PersonalUniversitario
    for p in personal:
        assert isinstance(p, PersonalUniversitario)
        assert p.calcular_remuneracion() > 0
    print("\nVerificación LSP: OK — todos los objetos respetan el contrato base")

    probar_validaciones()
