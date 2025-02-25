# -*- coding: utf-8 -*-
"""PYАД ЛР0 Трубников: Basic Math.ipynb"

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1--sXoRJ2-4jI1LrvfjnUCLXuorkW0-M-

### Задача 1 – Умножение матриц

Напишите функцию для умножения матриц, используя только списки и циклы.

Не забывайте проверить, что умножение выполнить возможно.
Напомним, что две матрицы могут быть перемножены, если число столбцов первой матрицы равно числу строк второй матрицы. Если матрица
$A$ имеет размер $m×n$ ($m$ строк и $nя$ столбцов), а матрица $B$ имеет размер $n×p$, то их произведение $C=AB$ будет иметь размер $m×p$.

Если $A=(a_{ij})$ — матрица размера $m×n$, а $B=(b_{jk})$ — матрица размера $n×p$, то элемент $c_{ik}$ матрицы $C=AB$ вычисляется по формуле:

$$c_{ik}=\sum_{j=1}^{n}a_{ij}b_{jk}$$

То есть каждый элемент новой матрицы является суммой произведений соответствующих элементов строки первой матрицы и столбца второй.
"""

import numpy as np

matrix1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

print(f"Произведение матриц:{[[sum(matrix1[i][j] * matrix2[j][k] for j in range(len(matrix2))) for k in range(len(matrix2[0]))] for i in range(len(matrix1))] if len(matrix1[0]) == len(matrix2) else None}")
matrix1 @ matrix2

"""### Задача 2 – Функции

Дано две функции:

\begin{matrix} F(x) = a_{11}x^2 + a_{12}x + a_{13}&(1) \\ P(x) = a_{21}x^2+a_{22}x + a_{23} &(2) \end{matrix}
​
* На вход программа должна принимать 2 строки. Каждая строка содержит 3 действительных числа через пробел: коэффициенты $a$.
* Необходимо найти точки экстремума функций (например, через функцию [`minimize_scalar()`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html), [`fmin()`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fmin.html) и др.) и определить, есть ли у функций общие решения при введенных коэффициентах на некотором диапазоне значений $x$, предусмотрев ситуации, когда решения есть, решений нет и решений бесконечно много.
"""

import numpy as np
from scipy.optimize import minimize_scalar, fsolve


def quadratic(x, a, b, c):
    return a * x**2 + b * x + c


a11, a12, a13 = map(float, input("Введите коэффициенты a11, a12, a13 через пробел: ").split())
a21, a22, a23 = map(float, input("Введите коэффициенты a21, a22, a23 через пробел: ").split())


F = lambda x: quadratic(x, a11, a12, a13)
P = lambda x: quadratic(x, a21, a22, a23)


ext_F = minimize_scalar(F)
ext_P = minimize_scalar(P)

print(f"Экстремум F(x): x = {ext_F.x:.5f}, F(x) = {ext_F.fun:.5f}")
print(f"Экстремум P(x): x = {ext_P.x:.5f}, P(x) = {ext_P.fun:.5f}")


def diff_func(x):
    return F(x) - P(x)


roots = fsolve(diff_func, np.linspace(-10, 10, 3))


unique_roots = sorted(set(filter(lambda r: np.isclose(diff_func(r), 0, atol=1e-5), roots)))

if len(unique_roots) == 0:
    print("Функции не имеют решений.")
elif len(unique_roots) == float('inf'):
    print("Функции совпадают на всем множестве.")
else:
    print(f"Общие решения: {', '.join(map(lambda r: f'x = {r:.5f}', unique_roots))}")

"""### Задача 3 – Коэффициент асимметрии и эксцесса

Напишите функцию, которая для случайной выборки рассчитывает коэффициенты асимметрии и эксцесса.

Коэффициент асимметрии:

$$A_3=\frac{m_3}{\sigma^3}$$

Коэффициент эксцесса:

$$E_4=\frac{m_4}{\sigma^4}-3$$

С помощью этих коэффициентов можно прикинуть, насколько близко распределение выборки к нормальному. Для расчета этих коэффициентов понадобится рассчитать центральные моменты третьего ($m_3$) и четвертого ($m_4$) порядка. Основные формулы, которые понадобятся для расчетов:
1. Момент второго порядка (он же – дисперсия):
$$m_2=D_e=\frac{∑(x_i-\overline{x_e})^2\times n_i}{n}$$
2. Момент третьего порядка:
$$m_3=\frac{∑(x_i-\overline{x_e})^3\times n_i}{n}$$
3. Момент четвертого порядка:
$$m_4=\frac{∑(x_i-\overline{x_e})^4\times n_i}{n}$$

В формулах выше $\overline{x_e}$ – это выборочное среднее.
$$\overline{x_e}=\frac{∑(x_i\times n_i)}{n},$$
где $x_i$ – $i$-е значение из выборки, $n_i$ – число раз, когда $x_i$ встретилось в выборке, $n$ – объем выборки.


Проверить корректность расчетов можно с помощью функции [`kurtosis`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html) для коэффициента эксцесса и функции [`skew`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html) из `scipy`.

**Коэффициент асимметрии** количественно определяет степень асимметрии распределения. Он показывает, в какую сторону распределение скошено относительно своего среднего значения.

1. Если коэффициент асимметрии больше 0, это означает, что "длинная часть" распределения находится справа от среднего (правостороннее распределение). Это может указывать на наличие выбросов или значений, превышающих среднее.
2. Если коэффициент меньше 0, "длинная часть" находится слева от среднего (левостороннее распределение). Это может свидетельствовать о большем количестве низких значений.
3. Коэффициент равен 0, что указывает на симметрию вокруг среднего значения.



**Эксцесс** измеряет остроту распределения по сравнению с нормальным распределением и показывает, насколько вероятны выбросы в данных.

1. Если эксцесс положителен (больше 0), это указывает на более острый пик и более тяжелые хвосты по сравнению с нормальным распределением. Это означает, что в данных больше выбросов.
2. Если эксцесс равен 0, это соответствует нормальному распределению, где пики и хвосты находятся на стандартном уровне.
3. Если эксцесс отрицателен (меньше 0), это говорит о более плоском пике и легких хвостах, что указывает на меньшую вероятность выбросов.
"""

from scipy.stats import kurtosis, skew

kurtosis([2,3,5,7,8]), skew([2,3,5,7,8])

kurtosis([2,3,2,5,7,2,2,8]), skew([2,3,2,5,7,2,2,8])

import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot([2,3,2,5,7,2,2,8], kde=True);

import numpy as np
from scipy.stats import skew, kurtosis

def compute_asymmetry_and_kurtosis(sample):
    n = len(sample)
    mean_x = np.mean(sample)
    m2 = np.sum((sample - mean_x) ** 2) / n
    m3 = np.sum((sample - mean_x) ** 3) / n
    m4 = np.sum((sample - mean_x) ** 4) / n

    A3 = m3 / (m2 ** (3 / 2))
    E4 = (m4 / (m2 ** 2)) - 3

    return A3, E4


np.random.seed(42)
sample = np.random.normal(0, 1, 1000)  # Нормальное распределение


A3, E4 = compute_asymmetry_and_kurtosis(sample)


A3_scipy = skew(sample)
E4_scipy = kurtosis(sample, fisher=True)

print(f"Коэффициент асимметрии (расчет): {A3:.5f}, (scipy): {A3_scipy:.5f}")
print(f"Коэффициент эксцесса (расчет): {E4:.5f}, (scipy): {E4_scipy:.5f}")

"""### Куда и как сдавать работу?

По инструкции в гитхаб – https://shy-question-39d.notion.site/1150ea832e418032bfc3d3e827c380fb?pvs=74

**Устная защита работ не требуется, но вам могут быть заданы вопросы прямо в вашем пул-реквесте!**
"""

