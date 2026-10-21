// ── personal_unap.hpp — Práctica S3, Actividad 4 ────────────────────────
// Curso : SIS206 Programación Orientada a Objetos II — UNAP Puno — 2026-II
// Alumno: Kevin Manuel Vilca Paco
// Docente: Dr. Aldo Hernán Zanabria Gálvez
//
// Jerarquía de personal universitario en C++17:
//   - destructor virtual en la base
//   - método virtual puro calcularRemuneracion()
//   - override en cada subclase
//   - polimorfismo con vector<unique_ptr<Base>>
#pragma once
#include <iomanip>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class PersonalUniversitario {
protected:
    std::string dni_;
    std::string nombres_;
    std::string apellidos_;

    static std::string validarDni(std::string dni) {
        if (dni.size() != 8 ||
            dni.find_first_not_of("0123456789") != std::string::npos)
            throw std::invalid_argument("DNI invalido: '" + dni +
                                        "' (debe tener 8 digitos)");
        return dni;
    }

public:
    PersonalUniversitario(std::string dni, std::string nombres,
                          std::string apellidos)
        : dni_(validarDni(std::move(dni))),
          nombres_(std::move(nombres)),
          apellidos_(std::move(apellidos)) {}

    virtual ~PersonalUniversitario() = default;  // destructor virtual OBLIGATORIO

    virtual float calcularRemuneracion() const = 0;  // método virtual puro

    virtual std::string identificarse() const {
        return apellidos_ + ", " + nombres_ + " (DNI: " + dni_ + ")";
    }
};

class Docente : public PersonalUniversitario {
    int horas_;
    float tarifa_ = 75.0f;
    float factor_;

    static float resolverFactor(const std::string& cat) {
        if (cat == "Auxiliar") return 1.0f;
        if (cat == "Asociado") return 1.4f;
        if (cat == "Principal") return 1.8f;
        throw std::invalid_argument("Categoria invalida: " + cat);
    }

public:
    Docente(std::string dni, std::string nombres, std::string apellidos,
            int horas, const std::string& categoria)
        : PersonalUniversitario(std::move(dni), std::move(nombres),
                                std::move(apellidos)),
          horas_(horas), factor_(resolverFactor(categoria)) {
        if (horas <= 0 || horas > 40)
            throw std::invalid_argument("Horas fuera de rango [1,40]");
    }

    float calcularRemuneracion() const override {
        return horas_ * tarifa_ * factor_;
    }
};

class Administrativo : public PersonalUniversitario {
    float salarioBase_;
    float bono_;

public:
    Administrativo(std::string dni, std::string nombres, std::string apellidos,
                   float salarioBase, float bono = 0.0f)
        : PersonalUniversitario(std::move(dni), std::move(nombres),
                                std::move(apellidos)),
          salarioBase_(salarioBase), bono_(bono) {
        if (salarioBase_ <= 0)
            throw std::invalid_argument("Salario base debe ser positivo");
        if (bono_ < 0)
            throw std::invalid_argument("El bono no puede ser negativo");
    }

    float calcularRemuneracion() const override {
        return salarioBase_ + bono_;
    }
};

class Investigador : public PersonalUniversitario {
    static constexpr float REMUNERACION_POR_PROYECTO = 1500.0f;
    int proyectos_;

public:
    Investigador(std::string dni, std::string nombres, std::string apellidos,
                 int proyectos)
        : PersonalUniversitario(std::move(dni), std::move(nombres),
                                std::move(apellidos)),
          proyectos_(proyectos) {
        if (proyectos_ < 1)
            throw std::invalid_argument("Debe tener al menos 1 proyecto activo");
    }

    float calcularRemuneracion() const override {
        return static_cast<float>(proyectos_) * REMUNERACION_POR_PROYECTO;
    }
};

// inline: permite incluir este header en varios .cpp sin romper la ODR
inline void planilla(const std::vector<std::unique_ptr<PersonalUniversitario>>& p) {
    float total = 0.0f;
    std::cout << std::string(60, '=') << "\n";
    std::cout << "PLANILLA PERSONAL UNIVERSITARIO — UNAP PUNO\n";
    std::cout << std::string(60, '=') << "\n";
    for (const auto& persona : p) {
        std::cout << std::fixed << std::setprecision(2)
                  << persona->identificarse()
                  << " S/ " << persona->calcularRemuneracion() << "\n";
        total += persona->calcularRemuneracion();
    }
    std::cout << std::string(60, '-') << "\n";
    std::cout << "TOTAL: S/ " << total << "\n";
}
