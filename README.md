# CIIE 2020/21 :: Videojuego 2D con Pygame
## INSERTE AQUÍ TÍTULO

TAREAS DISPONIBLES EN https://tasks.office.com/


AQUÍ SE ESCRIBIRÁN COSAS



### EJEMPLO CAMPO CÓDIGO
    NOMBRE:      Alonso Rodriguez Iglesias
    EMAIL:       alonso.rodriguez@udc.es
    COMPILACION: makefile (CC: mpicc)
    EJECUCION:   mpirun --oversubscribe -np numprocs ./main m k n alfa test debug time

    MPI:         openmpi 4.0.3-1 [https://www.archlinux.org/packages/extra/x86_64/openmpi/]
    ENTORNO:     Linux 5.6.13-1-ck-ivybridge #1 SMP PREEMPT x86_64 GNU/Linux
    DISTRO:      Arch Linux Rolling

    CPU:         Intel(R) Core(TM) i5-3230M CPU @ 2.60GHz
    RAM:         7,6 GiB DDR3 @ 1600 MHz

### EJEMPLO ENUMERACIÓN
El funcionamiento de la práctica es el siguiente:
1. Leemos los parámetros, que se encuentran documentados en el propio código.
2. Verificamos que los parámetros son válidos. En caso de no serlo, abortamos el programa y mostramos un mensaje de error.
3. El proceso #0 distribuye los datos leídos por línea de comandos.
4. El proceso #0 inicializa las matrices.
5. El proceso #0 define los comunicadores fila y columna.
6. Cada proceso calcula mpp, kpp y npp (*pp = * por proceso // * per process) y reserva memoria para localA, localB, y localC, así como para bufA y bufB.
7. ETC

### EJEMPLO TABLA
| Parámetro | Descripción |
|-----------|-------------|
| m         | Valor m de la matriz |
| k         | Valor k de la matriz |
| n         | Valor n de la matriz |
| alfa      | Factor de escalado alfa |
| test      | Indica si queremos comprobar errores en la matriz de resultado |
| debug     | Indica si queremos mostrar las matrices por stdout |
| time      | Indica si queremos imprimir los tiempos de cada proceso |

### EJEMPLO CAMPO CON CÓDIGO
    [alonso@anarchy-alonso:AC/p3]$ make
    mpicc -Wall -g   -c -o main.o main.c
    mpicc -Wall -g  -o main main.o -lm

### EJEMPLO CAMPO CON TEXTO
AAA PLACEHOLDER