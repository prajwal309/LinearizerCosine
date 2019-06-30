#This module is to test the results for cosine function
from Simplifier import *
import sympy


cos, sin, tan  = sympy.cos, sympy.sin, sympy.tan
phi,theta = sympy.symbols('phi theta')


#Expr2Test =  [cos(2*theta)*cos(2*theta)]




Expr2Test =  [cos(2*phi-theta)*cos(2*phi-theta),1/(cos(2*phi-theta)*cos(2*phi-theta)),
              cos(2*phi-3*theta)*cos(2*phi-theta), tan(2*phi-theta)*tan(2*phi-theta),
              cos(2*phi-theta)*cos(2*phi-theta)*cos(2*phi-theta)+cos(2*phi-theta)*cos(2*phi-theta),
              cos(2*phi-theta)**4*sin(2*phi-theta)**2,
              cos(2*phi-theta)**3.5*sin(2*phi-theta),
              cos(2*phi-theta)**3*sin(2*phi-theta)]


PrintFlag = True

for Expr in Expr2Test:
    LinearMethod = SimplifyExpression(Expr)

    #For printing
    if PrintFlag:
        print("Original expression:")
        print("\\begin{equation}")
        print(sympy.latex(Expr))
        print("\\end{equation}")

    Result = LinearMethod.LinearizeInCosine()

    if PrintFlag:
        print("\nFinal expression:")
        print("\\begin{equation}")
        print(sympy.latex(Result))
        print("\\end{equation}")

        print("\n**************************************\n")
