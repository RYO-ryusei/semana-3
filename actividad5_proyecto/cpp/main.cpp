// main.cpp — Práctica S3, Actividad 5 (C++17)
// Compilar: g++ -std=c++17 -Wall -Wextra -o biblioteca main.cpp
#include "biblioteca.hpp"

int main() {
    Biblioteca biblio("Biblioteca Central - UNAP Puno");
    biblio.agregar(std::make_unique<LibroFisico>(
        "LF-001", "Clean Code", "Robert C. Martin", 2008, 464, 3));
    biblio.agregar(std::make_unique<LibroDigital>(
        "LD-001", "Design Patterns", "Gamma et al.", 1994, "PDF", 12.5));
    biblio.agregar(std::make_unique<Revista>(
        "RV-001", "Revista de Ingenieria de Sistemas", "UNAP", 2025, 12, 2));

    reporteCatalogo(biblio.catalogo(), 4);

    std::cout << "\n";
    for (const auto& r : biblio.catalogo()) {
        if (!verificarContratoRecurso(*r)) {
            std::cout << "LSP violado por: " << r->titulo() << "\n";
            return 1;
        }
    }
    std::cout << "Verificacion LSP: OK - las 3 subclases sustituyen a "
                 "RecursoBibliografico\n";

    std::cout << "\nVALIDACION\n" << std::string(78, '-') << "\n";
    try {
        biblio.agregar(std::make_unique<Revista>("RV-001", "Duplicada", "X", 2024, 1, 1));
    } catch (const std::invalid_argument& e) {
        std::cout << "[OK] " << e.what() << "\n";
    }
    return 0;
}
