class DataType:
    # Clase base para todos los tipos de datos
    def __init__(self, name, size, alignment):
        self.name = name  # Nombre del tipo
        self.size = size  # Tamaño en bytes
        self.alignment = alignment  # Requisitos de alineación


class AtomicType(DataType):
    # Representa un tipo atómico (nombre, tamaño y alineación)
    pass


class StructType(DataType):
    # Representa un struct con una lista de tipos y calcula tamaños/alineaciones
    def __init__(self, name, types):
        super().__init__(name, 0, 0)
        self.types = types  # Lista de tipos que forman el struct
        self.size_unpacked = 0  # Tamaño sin empaquetar
        self.wasted_unpacked = 0  # Bytes desperdiciados sin empaquetar
        self.size_packed = 0  # Tamaño empaquetado
        self.size_optimized = 0  # Tamaño optimizado
        self.wasted_optimized = 0  # Bytes desperdiciados optimizado
        self.calculate_size_and_alignment()

    def calculate_size_and_alignment(self):
        # Calcula tamaños y alineaciones en tres modos: sin empaquetar, empaquetado y optimizado
        self.calculate_unpacked()
        self.size_packed = sum(t.size for t in self.types)  # Tamaño empaquetado
        self.calculate_optimized()

    def calculate_unpacked(self):
        # Calcula tamaño y bytes desperdiciados sin empaquetar
        offset = 0
        max_alignment = 0
        for t in self.types:
            if offset % t.alignment != 0:
                padding = t.alignment - (offset % t.alignment)
                offset += padding  # Agrega relleno para respetar alineación
            max_alignment = max(max_alignment, t.alignment)
            offset += t.size  # Incrementa el tamaño
        if offset % max_alignment != 0:
            offset += max_alignment - (offset % max_alignment)
        self.size_unpacked = offset
        self.alignment = max_alignment
        self.wasted_unpacked = self.size_unpacked - sum(t.size for t in self.types)

    def calculate_optimized(self):
        # Calcula tamaño y bytes desperdiciados reordenando tipos de forma óptima
        sorted_types = sorted(self.types, key=lambda t: t.alignment, reverse=True)
        offset = 0
        max_alignment = 0
        for t in sorted_types:
            if offset % t.alignment != 0:
                offset += t.alignment - (offset % t.alignment)
            max_alignment = max(max_alignment, t.alignment)
            offset += t.size
        if offset % max_alignment != 0:
            offset += max_alignment - (offset % max_alignment)
        self.size_optimized = offset
        self.wasted_optimized = self.size_optimized - sum(t.size for t in self.types)


class UnionType(DataType):
    # Representa un union con tipos, calcula tamaños y alineaciones
    def __init__(self, name, types):
        super().__init__(name, 0, 0)
        self.types = types  # Lista de tipos que forman el union
        self.size_unpacked = 0  # Tamaño del union
        self.wasted_unpacked = 0  # Bytes desperdiciados en el union
        self.size_packed = 0  # Tamaño empaquetado
        self.size_optimized = 0  # Tamaño optimizado
        self.calculate_size_and_alignment()

    def calculate_size_and_alignment(self):
        # Calcula el tamaño máximo entre los tipos y respeta la alineación más alta
        max_size = max(t.size for t in self.types)
        max_alignment = max(t.alignment for t in self.types)
        if max_size % max_alignment != 0:
            max_size += max_alignment - (max_size % max_alignment)
        self.size_unpacked = max_size
        self.size_packed = max_size
        self.size_optimized = max_size
        self.alignment = max_alignment
        self.wasted_unpacked = self.size_unpacked - max(t.size for t in self.types)


class DataTypeManager:
    # Clase que administra los tipos definidos y ejecuta acciones
    def __init__(self):
        self.data_types = {}  # Diccionario de tipos definidos

    def define_atomic(self, name, size, alignment):
        # Define un tipo atómico y verifica duplicados
        if name in self.data_types:
            print(f"Error: el tipo {name} ya ha sido definido.")
            return
        self.data_types[name] = AtomicType(name, size, alignment)

    def define_struct(self, name, types):
        # Define un struct y verifica duplicados y tipos no definidos
        if name in self.data_types:
            print(f"Error: el tipo {name} ya ha sido definido.")
            return
        for t in types:
            if t not in self.data_types:
                print(f"Error: el tipo {t} no ha sido definido.")
                return
        self.data_types[name] = StructType(name, [self.data_types[t] for t in types])

    def define_union(self, name, types):
        # Define un union y verifica duplicados y tipos no definidos
        if name in self.data_types:
            print(f"Error: el tipo {name} ya ha sido definido.")
            return
        for t in types:
            if t not in self.data_types:
                print(f"Error: el tipo {t} no ha sido definido.")
                return
        self.data_types[name] = UnionType(name, [self.data_types[t] for t in types])

    def describe(self, name):
        # Muestra detalles del tipo (tamaños y bytes desperdiciados)
        if name not in self.data_types:
            print(f"Error: el tipo {name} no ha sido definido.")
            return

        data_type = self.data_types[name]
        if isinstance(data_type, AtomicType):
            self._describe_atomic(data_type)
        elif isinstance(data_type, StructType):
            self._describe_struct(data_type)
        elif isinstance(data_type, UnionType):
            self._describe_union(data_type)
        else:
            print(f"Error: tipo {name} desconocido.")

    def _describe_atomic(self, atomic):
        # Describe un tipo atómico
        print(f"Tipo Atómico: {atomic.name}")
        print(f"Tamaño: {atomic.size} bytes")
        print(f"Alineación: {atomic.alignment} bytes")

    def _describe_struct(self, struct):
        # Describe un struct en sus tres configuraciones
        print(f"Struct: {struct.name}")
        print(f"  Sin empaquetar:")
        print(f"    Tamaño: {struct.size_unpacked} bytes")
        print(f"    Bytes desperdiciados: {struct.wasted_unpacked} bytes")
        print(f"  Empaquetado:")
        print(f"    Tamaño: {struct.size_packed} bytes")
        print(f"    Bytes desperdiciados: {struct.size_packed - sum(t.size for t in struct.types)} bytes")
        print(f"  Optimizado:")
        print(f"    Tamaño: {struct.size_optimized} bytes")
        print(f"    Bytes desperdiciados: {struct.wasted_optimized} bytes")

    def _describe_union(self, union):
        # Describe un union en sus configuraciones
        print(f"Union: {union.name}")
        print(f"  Sin empaquetar:")
        print(f"    Tamaño: {union.size_unpacked} bytes")
        print(f"    Bytes desperdiciados: {union.wasted_unpacked} bytes")
        print(f"  Empaquetado:")
        print(f"    Tamaño: {union.size_packed} bytes")
        print(f"    Bytes desperdiciados: 0 bytes (no aplica)")
        print(f"  Optimizado:")
        print(f"    Tamaño: {union.size_optimized} bytes")
        print(f"    Bytes desperdiciados: 0 bytes (no aplica)")

    def run(self):
        # Ejecuta un ciclo para procesar acciones del usuario
        while True:
            action = input("Ingrese una acción: ")
            if action == "SALIR":
                break
            self.process_action(action)

    def process_action(self, action):
        # Procesa acciones como ATOMICO, STRUCT, UNION y DESCRIBIR
        parts = action.split()
        if parts[0] == "ATOMICO":
            self.define_atomic(parts[1], int(parts[2]), int(parts[3]))
        elif parts[0] == "STRUCT":
            self.define_struct(parts[1], parts[2:])
        elif parts[0] == "UNION":
            self.define_union(parts[1], parts[2:])
        elif parts[0] == "DESCRIBIR":
            self.describe(parts[1])
        else:
            print("Acción no reconocida.")


if __name__ == "__main__":
    # Punto de entrada: inicia el simulador
    manager = DataTypeManager()
    manager.run()
