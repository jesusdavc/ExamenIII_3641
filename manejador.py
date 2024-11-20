class DataType:
    def __init__(self, name, size, alignment):
        self.name = name
        self.size = size
        self.alignment = alignment

class AtomicType(DataType):
    pass

class StructType(DataType):
    def __init__(self, name, types):
        super().__init__(name, 0, 0)  # Tamaño y alineación se calcularán
        self.types = types
        self.calculate_size_and_alignment()

    def calculate_size_and_alignment(self):
        # Calcular tamaño y alineación teniendo en cuenta las reglas de alineación
        ...

class UnionType(DataType):
    def __init__(self, name, types):
        super().__init__(name, 0, 0)
        self.types = types
        self.calculate_size_and_alignment()

    def calculate_size_and_alignment(self):
        # Calcular tamaño y alineación para un union
        ...

class DataTypeManager:
    def __init__(self):
        self.data_types = {}

    def define_atomic(self, name, size, alignment):
        if name in self.data_types:
            print(f"Error: el tipo {name} ya ha sido definido.")
            return
        self.data_types[name] = AtomicType(name, size, alignment)

    def define_struct(self, name, types):
        if name in self.data_types:
            print(f"Error: el tipo {name} ya ha sido definido.")
            return
        for t in types:
            if t not in self.data_types:
                print(f"Error: el tipo {t} no ha sido definido.")
                return
        self.data_types[name] = StructType(name, [self.data_types[t] for t in types])

    def define_union(self, name, types):
        if name in self.data_types:
            print(f"Error: el tipo {name} ya ha sido definido.")
            return
        for t in types:
            if t not in self.data_types:
                print(f"Error: el tipo {t} no ha sido definido.")
                return
        self.data_types[name] = UnionType(name, [self.data_types[t] for t in types])

    def describe(self, name):
        if name not in self.data_types:
            print(f"Error: el tipo {name} no ha sido definido.")
            return
        data_type = self.data_types[name]
        # Describir el tipo, incluyendo tamaño, alineación y bytes desperdiciados
        ...

    def run(self):
        while True:
            action = input("Ingrese una acción: ")
            if action == "SALIR":
                break
            self.process_action(action)

    def process_action(self, action):
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
    manager = DataTypeManager()
    manager.run()
