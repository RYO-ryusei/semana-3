// main.cpp — Práctica S3, Actividad 4
// Compilar: g++ -std=c++17 -Wall -Wextra -o personal main.cpp
#include "personal_unap.hpp"

int main() {
    std::vector<std::unique_ptr<PersonalUniversitario>> personal;
    personal.push_back(std::make_unique<Docente>(
        "12345678", "Juan Carlos", "Mamani Quispe", 16, "Asociado"));
    personal.push_back(std::make_unique<Docente>(
        "23456789", "Maria Elena", "Quispe Torres", 12, "Principal"));
    personal.push_back(std::make_unique<Administrativo>(
        "34567890", "Pedro", "Huanca Lazo", 2800.0f, 350.0f));
    personal.push_back(std::make_unique<Investigador>(
        "45678901", "Ana Lucia", "Flores Ramos", 2));

    planilla(personal);  // polimorfismo dinámico vía vtable

    // Verificación de validaciones (equivalente a la versión Python)
    std::cout << "\nPRUEBA DE VALIDACIONES\n" << std::string(60, '-') << "\n";
    auto probar = [](const std::string& caso, auto&& crear) {
        try {
            crear();
            std::cout << "[FALLO] " << caso << ": no lanzo excepcion\n";
        } catch (const std::invalid_argument& e) {
            std::cout << "[OK] " << caso << "\n     -> invalid_argument: "
                      << e.what() << "\n";
        }
    };
    probar("DNI con 7 digitos",
           [] { Docente("1234567", "X", "Y", 10, "Auxiliar"); });
    probar("Horas = 50 (max. 40)",
           [] { Docente("12345678", "X", "Y", 50, "Auxiliar"); });
    probar("Categoria inexistente",
           [] { Docente("12345678", "X", "Y", 10, "Titular"); });
    probar("Salario base negativo",
           [] { Administrativo("12345678", "X", "Y", -100.0f); });
    probar("Investigador sin proyectos",
           [] { Investigador("12345678", "X", "Y", 0); });

    return 0;  // unique_ptr libera cada objeto; el destructor virtual garantiza
               // que se ejecute el destructor de la subclase real
}
