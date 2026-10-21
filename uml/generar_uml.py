"""Genera los diagramas UML (PNG + .dot) con Graphviz.  Uso: python3 generar_uml.py"""
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PROY = AQUI.parent / "actividad5_proyecto" / "uml"

HEAD = '''digraph G {
  graph [rankdir=BT, bgcolor="white", nodesep=0.55, ranksep=0.75, pad=0.3, fontname="Helvetica"];
  node  [shape=plain, fontname="Helvetica", fontsize=11];
  edge  [fontname="Helvetica", fontsize=10, color="#1F3864", penwidth=1.4];
'''

def clase(nombre, atributos, metodos, abstracta=False, color="#DCE6F5", titulo_extra=""):
    n = f"<I>{nombre}</I>" if abstracta else nombre
    est = '<FONT POINT-SIZE="9">&laquo;abstract&raquo;</FONT><BR/>' if abstracta else ""
    attrs = "<BR ALIGN=\"LEFT\"/>".join(atributos) + "<BR ALIGN=\"LEFT\"/>" if atributos else " "
    mets = "<BR ALIGN=\"LEFT\"/>".join(metodos) + "<BR ALIGN=\"LEFT\"/>" if metodos else " "
    return f'''  {nombre} [label=<
    <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5" COLOR="#1F3864">
      <TR><TD BGCOLOR="{color}"><B>{est}{n}</B></TD></TR>
      <HR/><TR><TD ALIGN="LEFT">{attrs}</TD></TR>
      <HR/><TR><TD ALIGN="LEFT">{mets}</TD></TR>
    </TABLE>>];
'''

HERENCIA = 'arrowhead=onormal, arrowsize=1.2'
COMPOS   = 'arrowtail=diamond, arrowhead=none, dir=back, arrowsize=1.3'
ASOC     = 'arrowhead=vee'

def guardar(nombre, cuerpo, destinos):
    dot = HEAD + cuerpo + "}\n"
    for d in destinos:
        (d / f"{nombre}.dot").write_text(dot, encoding="utf-8")
        subprocess.run(["dot", "-Tpng", "-Gdpi=170", str(d / f"{nombre}.dot"),
                        "-o", str(d / f"{nombre}.png")], check=True)
    print("OK", nombre)

# ── 1. Personal universitario ───────────────────────────────────────────
c = ""
c += clase("PersonalUniversitario",
    ["- __dni: str", "# _nombres: str", "# _apellidos: str", "+ TARIFA_HORA_BASE: float = 75.0"],
    ["+ dni(): str", "+ nombre_completo(): str", "+ calcular_remuneracion(): float {abstract}", "+ __str__(): str"],
    abstracta=True, color="#FCE4D6")
c += clase("Docente",
    ["- _horas: int", "- _categoria: str", "+ FACTORES: dict"],
    ["+ calcular_remuneracion(): float"])
c += clase("Administrativo",
    ["- _salario_base: float", "- _bono: float"],
    ["+ calcular_remuneracion(): float"])
c += clase("Investigador",
    ["- _proyectos: int", "+ REMUNERACION_POR_PROYECTO = 1500.0"],
    ["+ calcular_remuneracion(): float"])
for s in ("Docente", "Administrativo", "Investigador"):
    c += f"  {s} -> PersonalUniversitario [{HERENCIA}];\n"
guardar("uml_personal_universitario", c, [AQUI])

# ── 2. LSP: violación ───────────────────────────────────────────────────
c = ""
c += clase("Figura", [], ["+ area(): float"], color="#FCE4D6")
c += clase("Rectangulo", ["# _ancho: float", "# _alto: float"],
           ["+ set_ancho(v)", "+ set_alto(v)", "+ area(): float"])
c += clase("Cuadrado", [], ["+ set_ancho(v)  «fuerza alto = v»", "+ set_alto(v)  «fuerza ancho = v»"], color="#F8CBAD")
c += "  Rectangulo -> Figura [%s];\n  Cuadrado -> Rectangulo [%s, color=\"#C00000\", label=\"  VIOLA LSP\", fontcolor=\"#C00000\"];\n" % (HERENCIA, HERENCIA)
guardar("uml_lsp_violacion", c, [AQUI])

# ── 3. LSP: solución ────────────────────────────────────────────────────
c = ""
c += clase("FiguraGeometrica", [], ["+ area(): float {abstract}", "+ perimetro(): float {abstract}"], abstracta=True, color="#FCE4D6")
c += clase("RectanguloInmutable", ["+ ancho: float", "+ alto: float"], ["+ area(): float", "+ perimetro(): float", "+ con_ancho(v): RectanguloInmutable"], color="#E2EFDA")
c += clase("CuadradoInmutable", ["+ lado: float"], ["+ area(): float", "+ perimetro(): float"], color="#E2EFDA")
c += f"  RectanguloInmutable -> FiguraGeometrica [{HERENCIA}];\n  CuadradoInmutable -> FiguraGeometrica [{HERENCIA}];\n"
guardar("uml_lsp_solucion", c, [AQUI])

# ── 4. Proyecto integrador: biblioteca ──────────────────────────────────
c = ""
c += clase("RecursoBibliografico",
    ["# _codigo: str", "# _titulo: str", "# _autor: str", "# _anio: int"],
    ["+ dias_prestamo(): int {abstract}", "+ calcular_multa(dias: int): float {abstract}", "+ tipo(): str", "+ descripcion(): str"],
    abstracta=True, color="#FCE4D6")
c += clase("LibroFisico", ["- _paginas: int", "- _ejemplares: int", "+ MULTA_DIARIA = 1.50"],
           ["+ dias_prestamo(): int  «7»", "+ calcular_multa(d): float", "+ descripcion(): str"])
c += clase("LibroDigital", ["- _formato: str", "- _tamano_mb: float"],
           ["+ dias_prestamo(): int  «14»", "+ calcular_multa(d): float  «0»", "+ descripcion(): str"])
c += clase("Revista", ["- _volumen: int", "- _numero: int", "+ MULTA_DIARIA = 2.00"],
           ["+ dias_prestamo(): int  «3»", "+ calcular_multa(d): float", "+ descripcion(): str"])
c += clase("Biblioteca", ["- nombre: str", "- _catalogo: list"], ["+ agregar(r)", "+ catalogo(): list"], color="#E2EFDA")
c += clase("Prestamo", ["+ dias_retraso: int"], ["+ multa(): float"], color="#E2EFDA")
c += clase("Usuario", ["+ codigo: str", "+ nombre: str"], [], color="#E2EFDA")
for s_ in ("LibroFisico", "LibroDigital", "Revista"):
    c += f"  {s_} -> RecursoBibliografico [{HERENCIA}];\n"
c += f'  Biblioteca -> RecursoBibliografico [{COMPOS}, label="  catálogo", taillabel="1", headlabel="0..*", labeldistance=2.6, labelangle=40];\n'
c += f'  Prestamo -> RecursoBibliografico [{ASOC}, style=dashed, label="  recurso"];\n'
c += f'  Prestamo -> Usuario [{ASOC}, style=dashed, label="  usuario"];\n'
c += "  {rank=same; Prestamo; RecursoBibliografico; Biblioteca}\n  Prestamo -> RecursoBibliografico -> Biblioteca [style=invis];\n"
c += "  {rank=same; Usuario; LibroFisico; LibroDigital; Revista}\n"
c += "  Usuario -> LibroFisico -> LibroDigital -> Revista [style=invis];\n"
guardar("uml_biblioteca", c, [AQUI, PROY])
