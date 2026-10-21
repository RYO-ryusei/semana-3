// biblioteca.hpp — Práctica S3, Actividad 5: Proyecto Integrador (C++17)
// Curso : SIS206 Programación Orientada a Objetos II — UNAP Puno — 2026-II
// Alumno: Kevin Manuel Vilca Paco
// Docente: Dr. Aldo Hernán Zanabria Gálvez
//
// Jerarquía IS-A:  RecursoBibliografico  <|--  LibroFisico / LibroDigital / Revista
// Composición:     Biblioteca  ◆--  RecursoBibliografico  (unique_ptr = dueña)
#pragma once
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// ───────────────────────── Clase base abstracta ─────────────────────────
class RecursoBibliografico {
protected:
    std::string codigo_;
    std::string titulo_;
    std::string autor_;
    int anio_;

public:
    RecursoBibliografico(std::string codigo, std::string titulo,
                         std::string autor, int anio)
        : codigo_(std::move(codigo)), titulo_(std::move(titulo)),
          autor_(std::move(autor)), anio_(anio) {
        if (codigo_.empty())
            throw std::invalid_argument("El codigo no puede estar vacio");
        if (anio_ < 1450)
            throw std::invalid_argument("Anio invalido: " + std::to_string(anio_));
    }

    virtual ~RecursoBibliografico() = default;  // destructor virtual OBLIGATORIO

    const std::string& codigo() const { return codigo_; }
    const std::string& titulo() const { return titulo_; }

    virtual int diasPrestamo() const = 0;                    // virtual puro
    virtual double calcularMulta(int diasRetraso) const = 0;  // virtual puro
    virtual std::string tipo() const { return "Recurso"; }

    virtual std::string descripcion() const {
        return "[" + tipo() + "] " + titulo_ + " - " + autor_ + " (" +
               std::to_string(anio_) + ")";
    }
};

// ───────────────────────────── Subclases ────────────────────────────────
class LibroFisico : public RecursoBibliografico {
    static constexpr double MULTA_DIARIA = 1.50;
    int paginas_;
    int ejemplares_;

public:
    LibroFisico(std::string codigo, std::string titulo, std::string autor,
                int anio, int paginas, int ejemplares = 1)
        : RecursoBibliografico(std::move(codigo), std::move(titulo),
                               std::move(autor), anio),
          paginas_(paginas), ejemplares_(ejemplares) {
        if (paginas_ <= 0 || ejemplares_ < 1)
            throw std::invalid_argument("Paginas y ejemplares deben ser positivos");
    }

    std::string tipo() const override { return "Libro fisico"; }
    int diasPrestamo() const override { return 7; }
    double calcularMulta(int diasRetraso) const override {
        return std::max(0, diasRetraso) * MULTA_DIARIA;
    }
    std::string descripcion() const override {
        return RecursoBibliografico::descripcion() + " | " +
               std::to_string(paginas_) + " pags | " +
               std::to_string(ejemplares_) + " ejemplar(es)";
    }
};

class LibroDigital : public RecursoBibliografico {
    std::string formato_;
    double tamanoMb_;

public:
    LibroDigital(std::string codigo, std::string titulo, std::string autor,
                 int anio, std::string formato, double tamanoMb)
        : RecursoBibliografico(std::move(codigo), std::move(titulo),
                               std::move(autor), anio),
          formato_(std::move(formato)), tamanoMb_(tamanoMb) {
        if (formato_ != "PDF" && formato_ != "EPUB")
            throw std::invalid_argument("Formato no soportado: " + formato_);
        if (tamanoMb_ <= 0)
            throw std::invalid_argument("El tamano debe ser positivo");
    }

    std::string tipo() const override { return "Libro digital"; }
    int diasPrestamo() const override { return 14; }
    double calcularMulta(int) const override { return 0.0; }  // licencia caduca sola
    std::string descripcion() const override {
        std::ostringstream os;
        os << RecursoBibliografico::descripcion() << " | " << formato_ << " | "
           << std::fixed << std::setprecision(1) << tamanoMb_ << " MB";
        return os.str();
    }
};

class Revista : public RecursoBibliografico {
    static constexpr double MULTA_DIARIA = 2.00;
    int volumen_;
    int numero_;

public:
    Revista(std::string codigo, std::string titulo, std::string autor,
            int anio, int volumen, int numero)
        : RecursoBibliografico(std::move(codigo), std::move(titulo),
                               std::move(autor), anio),
          volumen_(volumen), numero_(numero) {
        if (volumen_ < 1 || numero_ < 1)
            throw std::invalid_argument("Volumen y numero deben ser positivos");
    }

    std::string tipo() const override { return "Revista"; }
    int diasPrestamo() const override { return 3; }
    double calcularMulta(int diasRetraso) const override {
        return std::max(0, diasRetraso) * MULTA_DIARIA;
    }
    std::string descripcion() const override {
        return RecursoBibliografico::descripcion() + " | Vol. " +
               std::to_string(volumen_) + " No. " + std::to_string(numero_);
    }
};

// ─────────────────── Composición: Biblioteca ◆── Recurso ─────────────────
class Biblioteca {
    std::string nombre_;
    std::vector<std::unique_ptr<RecursoBibliografico>> catalogo_;

public:
    explicit Biblioteca(std::string nombre) : nombre_(std::move(nombre)) {}

    void agregar(std::unique_ptr<RecursoBibliografico> r) {
        auto repetido = std::any_of(catalogo_.begin(), catalogo_.end(),
            [&](const auto& x) { return x->codigo() == r->codigo(); });
        if (repetido)
            throw std::invalid_argument("Codigo duplicado: " + r->codigo());
        catalogo_.push_back(std::move(r));
    }

    const std::vector<std::unique_ptr<RecursoBibliografico>>& catalogo() const {
        return catalogo_;
    }
    const std::string& nombre() const { return nombre_; }
};

// ─────────────────── Polimorfismo dinámico (sin dynamic_cast) ────────────
inline void reporteCatalogo(
    const std::vector<std::unique_ptr<RecursoBibliografico>>& recursos,
    int diasRetraso) {
    std::cout << std::string(78, '=') << "\n"
              << "CATALOGO - multa simulada con " << diasRetraso
              << " dias de retraso\n"
              << std::string(78, '=') << "\n";
    double total = 0.0;
    for (const auto& r : recursos) {
        double multa = r->calcularMulta(diasRetraso);  // despacho por vtable
        total += multa;
        std::cout << r->descripcion() << "\n"
                  << "    Prestamo: " << std::setw(2) << r->diasPrestamo()
                  << " dias | Multa: S/ " << std::fixed << std::setprecision(2)
                  << std::setw(5) << multa << "\n";
    }
    std::cout << std::string(78, '-') << "\n"
              << "TOTAL MULTAS SIMULADAS: S/ " << total << "\n";
}

// Contrato LSP que toda subclase debe cumplir
inline bool verificarContratoRecurso(const RecursoBibliografico& r) {
    return !r.descripcion().empty() && r.diasPrestamo() > 0 &&
           r.calcularMulta(5) >= 0.0 && r.calcularMulta(0) == 0.0;
}
