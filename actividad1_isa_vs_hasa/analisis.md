# Actividad 1 — Análisis: Herencia (IS-A) vs Composición (HAS-A)

**Regla práctica:** si puedes decir *"X **es un** Y"* en TODOS los contextos donde se usa Y → herencia.
Si solo puedes decir *"X **tiene un** Y"* o *"X **usa** a Y"* → composición / asociación.

| # | Relación propuesta | Decisión | Clase base → Subclase | Justificación |
|---|--------------------|----------|-----------------------|---------------|
| 1 | Estudiante de Posgrado en relación a un Estudiante | **IS-A (herencia)** | `Estudiante` → `EstudiantePosgrado` | Un estudiante de posgrado *es un* estudiante: conserva código, matrícula y cursos, y solo añade asesor, tesis y línea de investigación. Puede sustituir a `Estudiante` en cualquier lugar (LSP). |
| 2 | Un Sensor IoT en relación a un Dispositivo | **IS-A (herencia)** | `Dispositivo` → `SensorIoT` | Un sensor *es un* dispositivo: hereda id, estado y encender/apagar; agrega lectura, unidad y frecuencia de muestreo. Se pueden guardar sensores, actuadores y gateways en una misma lista de `Dispositivo`. |
| 3 | Un Informe en relación a una Impresora | **HAS-A / asociación (composición)** | — (no hay herencia) | Un informe **no es** una impresora ni viceversa; son conceptos de dominios distintos. La impresora *usa* un informe (`imprimir(informe)`). Heredar crearía una jerarquía absurda, igual que `Automovil(Motor)`. |
| 4 | Un Libro Digital en relación a un Libro | **IS-A (herencia), con cuidado** | `Libro` → `LibroDigital` | Un libro digital *es un* libro (título, autor, ISBN). Cuidado con el LSP: la base `Libro` no debe tener atributos exclusivos del libro físico (peso, ejemplares). En el Proyecto Integrador se resolvió con una base más general `RecursoBibliografico`. |
| 5 | Una Motocicleta en relación a un Vehículo | **IS-A (herencia)** | `Vehiculo` → `Motocicleta` | Una motocicleta *es un* vehículo: placa, marca, acelerar, frenar. Añade cilindrada y tipo de casco. Es una relación taxonómica clásica y sustituible. |
| 6 | Un Departamento en relación a un Empleado | **HAS-A (composición/agregación)** | — (no hay herencia) | Un departamento **no es** un empleado: un departamento *tiene* empleados (`Departamento ◇── Empleado`). Heredar mezclaría el concepto de "unidad organizativa" con el de "persona". |

## Resumen
- **Herencia (IS-A):** 1, 2, 4, 5.
- **Composición / asociación (HAS-A):** 3, 6.
