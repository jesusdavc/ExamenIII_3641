//Definición de tipo de dato Church
indirect enum Church {
    case cero                  // Representa el numeral cero.
    case sucesor(Church)       // Representa el sucesor de un numeral.
}
//Funciones 
extension Church {
    // Suma de dos numerales de Church
    func sumar(_ otro: Church) -> Church {
        switch self {
        case .cero:
            return otro
        case .sucesor(let anterior):
            return .sucesor(anterior.sumar(otro))
        }
    }

    // Multiplicación de dos numerales de Church
    func multiplicar(_ otro: Church) -> Church {
        switch self {
        case .cero:
            return .cero
        case .sucesor(let anterior):
            return otro.sumar(anterior.multiplicar(otro))
        }
    }
}
//Ejemplo de uso. Más la función imprimir.
// Definir algunos numerales de Church
let cero = Church.cero
let uno = Church.sucesor(cero)
let dos = Church.sucesor(uno)
let tres = Church.sucesor(dos)

// Realizar operaciones
let suma = dos.sumar(tres)          // 2 + 3 = 5
let multiplicacion = dos.multiplicar(tres) // 2 * 3 = 6

// Mostrar resultados
func imprimir(_ numeral: Church) -> String {
    switch numeral {
    case .cero:
        return "Cero"
    case .sucesor(let anterior):
        return "Suc(\(imprimir(anterior)))"
    }
}

print("Suma: \(imprimir(suma))")          // Salida: Suma: Suc(Suc(Suc(Suc(Suc(Cero)))))
print("Multiplicación: \(imprimir(multiplicacion))") // Salida: Multiplicación: Suc(Suc(Suc(Suc(Suc(Suc(Cero))))))
