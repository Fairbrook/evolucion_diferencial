import functools
from matplotlib import pyplot as plt
import numpy as np
from evolution import DiferentialEvolution

domain = (0, np.pi)
m = 10


# Ecuacion general
def F(x, i) -> float:
    return -np.sin(x) * np.power(np.sin((i * x**2) / np.pi), 2 * m)


# Ecuación a dos dimensiones
def f(x, y):
    return F(x, 1) + F(y, 2)


# Punto a buscar
# print(f(2.20,1.57))


def evaluate(point):
    x, y = point
    return f(x, y)


evol = DiferentialEvolution(34, domain)
evol.initial_population(20)
best = evol.get_best(evaluate)
worst = evol.get_worst(evaluate)
generation = 0
indexes = []
bests = []
averages = []
while abs(evaluate(worst)- evaluate(best)) > 0.01:
    generation += 1
    indexes.append(generation)
    evol.iteration(evaluate)

    avg = functools.reduce(lambda res, indv: res + evaluate(indv),
                           evol.population, 0) / len(evol.population)
    averages.append(avg)

    best = evol.get_best(evaluate)
    bests.append(best)
    worst = evol.get_worst(evaluate)
   

best_x, best_y = best
best_z = f(best_x, best_y)

# Graficación del proceso
resolution = 150
fig = plt.figure(figsize=plt.figaspect(0.4))
fig.suptitle("Busqueda de solución mediante evolución diferencial")
fig.tight_layout(pad=10)

# Evolucion
ax = fig.add_subplot(1, 2, 2)
ax.set_title("Evolución")
ax.plot(indexes, [evaluate(x) for x in bests], label="Mejores")
ax.plot(indexes, averages, label="Promedios")
ax.set_xlabel("Generación")
ax.set_ylabel("Evaluación")
ax.legend()

# Grafica de la función
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.set_title("Función de Michalewicz")
x = np.linspace(0, np.pi, resolution)
y = np.linspace(0, np.pi, resolution)
X, Y = np.meshgrid(x, y)
Z = F(X, 1) + F(Y, 2)
ax.contourf(X, Y, Z, resolution)
ax.scatter(best_x, best_y, best_z, label="Mejor punto encontrado")
ax.legend()

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.85,
                    wspace=0.4,
                    hspace=0.4)
plt.figtext(
    0.5,
    0.01,
    f"Mejor punto encontrado x={best_x:.3f} y={best_y:.3f} z={best_z:.3f}",
    ha="center",
    fontsize=10,
)
plt.show()