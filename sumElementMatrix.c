#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Función para llenar la matriz con valores aleatorios
void llenarMatriz(double **matriz, int filas, int columnas) {
    for (int i = 0; i < filas; i++) {
        for (int j = 0; j < columnas; j++) {
            matriz[i][j] = (double)rand() / RAND_MAX; // Valores aleatorios entre 0 y 1
        }
    }
}

// Función para sumar la matriz recorriendo primero por filas
double sumarPorFilas(double **matriz, int filas, int columnas) {
    double suma = 0.0;
    for (int i = 0; i < filas; i++) {
        for (int j = 0; j < columnas; j++) {
            suma += matriz[i][j];
        }
    }
    return suma;
}

// Función para sumar la matriz recorriendo primero por columnas
double sumarPorColumnas(double **matriz, int filas, int columnas) {
    double suma = 0.0;
    for (int j = 0; j < columnas; j++) {
        for (int i = 0; i < filas; i++) {
            suma += matriz[i][j];
        }
    }
    return suma;
}

// Función para asignar memoria para una matriz de tamaño filas x columnas
double **asignarMatriz(int filas, int columnas) {
    double **matriz = (double **)malloc(filas * sizeof(double *));
    if (matriz == NULL) return NULL;

    for (int i = 0; i < filas; i++) {
        matriz[i] = (double *)malloc(columnas * sizeof(double));
        if (matriz[i] == NULL) {
            for (int k = 0; k < i; k++) free(matriz[k]);
            free(matriz);
            return NULL;
        }
    }
    return matriz;
}

// Función para liberar la memoria asignada a una matriz
void liberarMatriz(double **matriz, int filas) {
    for (int i = 0; i < filas; i++) free(matriz[i]);
    free(matriz);
}

int main() {
    int tamañosN[] = {100, 1000, 10000, 100000};
    int tamañosM[] = {100, 1000, 10000, 100000};
    int numTamañosN = sizeof(tamañosN) / sizeof(tamañosN[0]);
    int numTamañosM = sizeof(tamañosM) / sizeof(tamañosM[0]);

    for (int tn = 0; tn < numTamañosN; tn++) {
        for (int tm = 0; tm < numTamañosM; tm++) {
            int N = tamañosN[tn];
            int M = tamañosM[tm];

            printf("\nTamaño de la matriz: %d x %d\n", N, M);

            double **matriz = asignarMatriz(N, M);
            if (matriz == NULL) {
                printf("La matriz %d x %d es demasiado grande para asignar en memoria.\n", N, M);
                continue;
            }

            llenarMatriz(matriz, N, M);

            // Medición recorriendo por filas
            clock_t inicio = clock();
            double sumaFilas = sumarPorFilas(matriz, N, M);
            clock_t fin = clock();
            double tiempoFilas = (double)(fin - inicio) / CLOCKS_PER_SEC;
            printf("Suma por filas: %f, Tiempo: %f segundos\n", sumaFilas, tiempoFilas);

            // Medición recorriendo por columnas
            inicio = clock();
            double sumaColumnas = sumarPorColumnas(matriz, N, M);
            fin = clock();
            double tiempoColumnas = (double)(fin - inicio) / CLOCKS_PER_SEC;
            printf("Suma por columnas: %f, Tiempo: %f segundos\n", sumaColumnas, tiempoColumnas);

            liberarMatriz(matriz, N, M);
        }
    }

    return 0;
}
