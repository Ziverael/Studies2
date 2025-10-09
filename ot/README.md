
# Optimization Theory

## Grading rules

40 pt - exam
12 pt - from two mini projects
any number of points from exams

To pass, min: 23pt

Exam: 10.02.2026 10:00

# Lecture 1

Optimization is a selection of the best element from a set of available alternatives.
If we have a choice criterion that can be described using a function - this means minimizing or maximizing this function.
We do it with mathematical analysis - computing derivatives, etc

Example:

$$
\begin{gathered}
2000+\ln(a)-20p\\
f(p,a) = sell\cdot \text{product price} - advert - capital =(2000+\ln(a)-20p)(p-2)-a-20\,000,\\
f_p=2000+\ln(a)+40-20p-1=0\\    
f_a=\frac{p-2}{a}-1=0\\
\end{gathered}    
$$
$$
a=p-2\Rightarrow2039\ln(p-2)=40p
$$
This equation is had to compute even numerically.

Example2:
| Package size    | price |
| -------- | ------- |
| 100    | 160\$    |
| 50    | 90\$    |
| 20    | 45\$    |
| 10    | 28\$    |


We sell each product for 5\$. We need to buy 3791 units. How to optimize this.
Profits to maximize: $5u-160x_{100} - 90x_{50} - 45x_{20} - 28x_{10}$
Constraints:
$$\begin{gathered}
u\le3791,\\
160x_{100} - 90x_{50} - 45x_{20} - 28x_{10}\ge u,\\
x_{100},x_{50},x_{20},x_{10}\ge 0,
\end{gathered}
$$

Problems:
* computing derivatives is useless- the are never zero
* Maxmimum in on the boundary - more precisely, in one of the vertices of the set of possible solutions.

**More generally**

How to search through


### Goals of optimization theory

Providinv numerical tools ffor finding minimizers or maximizers nased on derivatives of functions.

Giving analytical toolf to transform constrained problems ino somethin that can be solved using derivative-based methods.

Providing efficient way to solve the problems that caoont be solved using derivative-based approach (linear, discrete).

### Vocabulary

Generic optimization problem: mimnimize (maximize) f(x) subject to $x\in D$.

$f$ - objective funtion (cost <- minimize, reward <- maximize)

$x$ - variable

$D$ - feasible set

if $D$ is deined using equalities or inequalities, these (in)equalities are called constrains

$\argmin f(x)/\argmax f(x)$ - optimal solution (minimizer or maximizer).