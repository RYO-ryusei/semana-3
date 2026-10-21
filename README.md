# Práctica Calificada — Semana 3: Herencia y Polimorfismo

**Universidad Nacional del Altiplano — Puno**
Escuela Profesional de Ingeniería de Sistemas
**Curso:** SIS206 — Programación Orientada a Objetos II · Semestre 2026-II

| | |
|---|---|
| **Estudiante** | Kevin Manuel Vilca Paco |
| **Docente** | Dr. Aldo Hernán Zanabria Gálvez |
| **Tema** | Herencia, sobrescritura, polimorfismo dinámico y Principio de Sustitución de Liskov (LSP) |
| **Lenguajes** | Python 3.12+ · C++17 |

## Estructura del repositorio

```
Practica_Semana3_POO2_Kevin_Vilca/
├── README.md
├── informe/                         ← Informe completo (Word y PDF)
├── actividad1_isa_vs_hasa/        ← Análisis IS-A vs HAS-A
├── actividad2_python/               ← Jerarquía PersonalUniversitario (Python)
├── actividad3_lsp/                  ← Verificación LSP + Cuadrado/Rectángulo
├── actividad4_cpp/                  ← Jerarquía en C++17 (virtual / override)
├── actividad5_proyecto/             ← Proyecto Integrador: Sistema de Biblioteca
│   ├── python/   cpp/   uml/
├── uml/                             ← Diagramas UML (PNG + código .dot)
└── salidas/                         ← Salida real de cada programa
```

## Cómo ejecutar

**Python (requiere 3.12 o superior por `typing.override`):**
```bash
python3 actividad2_python/personal_unap.py
python3 actividad3_lsp/lsp_verificacion.py
python3 actividad5_proyecto/python/biblioteca.py
```

**C++17 (g++ con `-Wall -Wextra -pedantic`, sin warnings):**
```bash
cd actividad4_cpp && make run
cd ../actividad5_proyecto/cpp && make run
```

**Regenerar los diagramas UML (requiere Graphviz):**
```bash
python3 uml/generar_uml.py
```

## Subir a GitHub

```bash
git init
git add .
git commit -m "feat(semana3): jerarquía de herencia y polimorfismo"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/<tu-repositorio>.git
git push -u origin main
```

## Resumen de resultados

| Actividad | Contenido | Resultado |
|---|---|---|
| 1 | Análisis IS-A vs HAS-A (6 casos) | 4 herencia, 2 composición |
| 2 | Jerarquía de personal en Python | Planilla total **S/ 9450.00**, validaciones OK |
| 3 | LSP: contrato + Cuadrado/Rectángulo | Cuadrado **viola** el LSP; rediseño correcto incluido |
| 4 | Jerarquía en C++17 | Compila sin warnings; mismo total **S/ 9450.00** |
| 5 | Proyecto Integrador (Biblioteca) | 1 base abstracta + 3 subclases, Python y C++, UML |
