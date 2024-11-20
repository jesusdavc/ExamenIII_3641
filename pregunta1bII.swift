//Tipo de Datos


struct Persona {
    let nombre: String
    let edad: Int
}

struct ConjuntoDePersonas {
    var personas: [Persona]
}
//Funciones solicitadas 
extension ConjuntoDePersonas {
    func cantidadDePersonas() -> Int {
        return personas.count
    }
}

extension ConjuntoDePersonas {
    func mayoresDeEdad() -> [Persona] {
        return personas.filter { $0.edad >= 18 }
    }
}

extension ConjuntoDePersonas {
    func nombreMasComun() -> String? {
        let nombresFrecuencia = personas.reduce(into: [:]) { conteo, persona in
            conteo[persona.nombre, default: 0] += 1
        }
        return nombresFrecuencia.max(by: { $0.value < $1.value })?.key
    }
}

//Ejemplo de uso

let conjunto = ConjuntoDePersonas(personas: [
    Persona(nombre: "Ana", edad: 20),
    Persona(nombre: "Luis", edad: 17),
    Persona(nombre: "Ana", edad: 22),
    Persona(nombre: "Pedro", edad: 30),
    Persona(nombre: "Luis", edad: 25)
])

// Cantidad de personas en el conjunto
print("Cantidad de personas: \(conjunto.cantidadDePersonas())") 
// Salida: Cantidad de personas: 5

// Subconjunto de personas mayores de edad
let mayores = conjunto.mayoresDeEdad()
print("Mayores de edad: \(mayores.map { $0.nombre })") 
// Salida: Mayores de edad: ["Ana", "Ana", "Pedro", "Luis"]

// Nombre más común en el conjunto
if let nombreComun = conjunto.nombreMasComun() {
    print("Nombre más común: \(nombreComun)") 
    // Salida: Nombre más común: Ana
}

