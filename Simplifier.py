from sympy.interactive import printing
printing.init_printing(use_latex=True)
import sympy
from sympy.interactive import printing
from sympy.parsing.sympy_parser import parse_expr
import re
import numpy as np
import math

def ApproxEqual(a,b, tolerance=1e-10):
    '''
    Check if a, and b are approximately equal
    '''
    if abs(a-b)<tolerance:
        return True
    else:
        return False

def ConstructFunction(FunctionName, Angle, PowerValue):
    #this function divides the cos^5x into the components
    if "sin" in FunctionName or "cos" in FunctionName:
        pass
    else:
        print("Expecting sine or cosine for the function name")
        input("Not expecting other functions. Likely to produce an error.")

    SIGN = int(PowerValue/np.abs(PowerValue))

    if ApproxEqual(PowerValue,int(PowerValue)) or ApproxEqual(PowerValue%1,0.5):
        SqrtPresent = ApproxEqual(PowerValue%1,0.5)
        if SqrtPresent:
            BaseFunction = FunctionName+"("+str(Angle)+")"+"**(1/2)"
        else:
            BaseFunction = ""
        #Case is integer or has an integer value
        IntPower = int(PowerValue)

        EvenCase = int(PowerValue)%2==0
        PowerValue = abs(PowerValue)
        ValueSet = np.ones(math.ceil(PowerValue/2.0))


        if EvenCase:
            #if the power of the function is even
            FunctionNameHolder = BaseFunction
            for count in range(len(ValueSet)):
                if "sin" in FunctionName:
                    if SIGN>0:
                        LoopFuncNameGen = "(1 - cos(2*("+str(Angle)+")))/2"
                    else:
                        LoopFuncNameGen = "1/((1 - cos(2*("+str(Angle)+")))/2)"
                elif "cos" in FunctionName:
                    if SIGN>0:
                        LoopFuncNameGen = "(1 + cos(2*("+str(Angle)+")))/2"
                    else:
                        LoopFuncNameGen = "1/((1 + cos(2*("+str(Angle)+")))/2)"
                if count==0:
                    FunctionNameHolder+=LoopFuncNameGen
                else:
                    FunctionNameHolder+="*"+LoopFuncNameGen

        else:
            #The odd case for power
            if SqrtPresent:
                FunctionNameHolder =  BaseFunction +"*"+ FunctionName+"("+str(Angle)+")"
            else:
                FunctionNameHolder = FunctionName+"("+str(Angle)+")"

            for count in range(len(ValueSet)-1):
                if "sin" in FunctionName:
                    if SIGN>0:
                        LoopFuncNameGen = "(1 - cos(2*("+str(Angle)+")))/2"
                    else:
                        LoopFuncNameGen = "1/((1 - cos(2*("+str(Angle)+")))/2)"
                elif "cos" in FunctionName:
                    if SIGN>0:
                        LoopFuncNameGen = "(1 + cos(2*("+str(Angle)+")))/2"
                    else:
                        LoopFuncNameGen = "1/((1 + cos(2*("+str(Angle)+")))/2)"
                FunctionNameHolder+="*"+LoopFuncNameGen

        Function2Return = sympy.sympify(FunctionNameHolder)
        return Function2Return
    else:
        print("Deconstruction of this power has not been constructed yet")
        input("Crash here...")
    return FunctionNameHolder


def ParseBracket(ExprString):
    #The expression string should start right after the left bracket stars
    LeftAngle = 1
    RightAngle = 0
    Expr = ""
    LastLoc = 0
    for Char in ExprString:
        LastLoc+=1
        if "(" in Char:
            LeftAngle+=1
        elif ")" in Char:
            RightAngle+=1
        Expr+=Char
        if LeftAngle==RightAngle:
            break
    return Expr[:-1], LastLoc

def FindAllAngles(Expression):
    '''
    This function should return all the angular expressions in the symbolic form
    '''
    Expression = str(Expression)

    #search for the expression for which to look angles for i.e. sin, cos, and tan
    SinValues = list(re.findall(r'sin', Expression))
    CosValues = list(re.findall(r'cos', Expression))
    TanValues = list(re.findall(r'tan', Expression))
    FunctionNames = CosValues+SinValues+TanValues

    AllAngles  = []
    for i in range(len(FunctionNames)):
        Location = Expression.rfind(FunctionNames[i])
        AngleExpr, _ = ParseBracket(Expression[Location+4:])
        AllAngles.append(AngleExpr)
    AllAngles = list(set(AllAngles))
    AllAngles = [parse_expr(exp) for exp in AllAngles]
    return AllAngles


def ParsePower(Expression,Angle):
    '''
    This function takes in expression such as cos^5(x)
    and returns cos^2x cos^2x cos x. Cos^2x are linearized
    in the process.
    '''

    AngleStr = str(sympy.srepr(Angle))
    ExpressionRepr = str(sympy.srepr(Expression))

    #Find the power value
    Functions, PowerValues, Functions2Replace = FindPowerValue(ExpressionRepr, AngleStr)

    #Construct the function
    for f, p, Original in zip(Functions, PowerValues,Functions2Replace):
        ReplacingString = str(sympy.srepr(ConstructFunction(f, Angle, p)))
        ExpressionRepr = ExpressionRepr.replace("Pow("+Original+")", ReplacingString)

    #Return the parsed string
    return parse_expr(ExpressionRepr)




def FindPowerValue(StrExpr, AngleStr):
    '''
    This function takes in an expression and an angle, and finds the
    parses the value of power from the text of srepr sympy form
    '''


    StrExpr = str(StrExpr)
    NumPow = len(re.findall(r'Pow',StrExpr))

    Stop = len(StrExpr)
    FunctionNames = []
    PowerValues = []
    Text2Replace = []

    for i in range(NumPow):
        Location = StrExpr[:Stop].rfind(r'Pow')
        StrValue, EndLoc = ParseBracket(StrExpr[Location+4:])
        ExpectedExpr = StrExpr[Location+3:Location+4+EndLoc]


        NameFunc = ExpectedExpr[1:4]
        Stop=Location

        #Now processing the respective power
        if ("sin" in NameFunc or "cos" in NameFunc) and AngleStr in ExpectedExpr:
            #returns -1 if the expression is not found
            FloatPos = ExpectedExpr.rfind("Float")
            IntPos = ExpectedExpr.rfind("Integer")
            RationalPos = ExpectedExpr.rfind("Rational")
            Text2Replace.append(StrValue)
            if FloatPos>IntPos and FloatPos>RationalPos and FloatPos>0:
                RelevantString  =  ExpectedExpr[FloatPos:]
                RelevantString = RelevantString.split(",")[0]
                RelevantString = RelevantString.replace("Float","").replace("(","").replace(")","")
                RelevantString = RelevantString.replace("'","")
                FunctionNames.append(NameFunc)
                PowerValues.append(float(RelevantString))
            elif IntPos>FloatPos and IntPos>RationalPos and IntPos>0:
                RelevantString  =  ExpectedExpr[IntPos:]
                RelevantString = RelevantString.replace("Integer","").replace("(","").replace(")","")
                RelevantString.replace("\'","")
                FunctionNames.append(NameFunc)
                PowerValues.append(int(RelevantString))

            elif RationalPos>FloatPos and RationalPos>IntPos and IntPos>0:
                RelevantString  =  ExpectedExpr[RationalPos:]
                RelevantString = RelevantString.replace("Rational","").replace("(","").replace(")","")
                RelevantString.replace("\'","")
                Num, Den = RelevantString.split(",")
                Num = int(Num)
                Den = int(Den)
                PowerValues.append(float(Num/Den))
            else:
                print("Failed to parse the power expression")
                input("Please check the code at this point")

    return FunctionNames, PowerValues, Text2Replace







class SimplifyExpression():
    '''
    This function takes in sympy expression in trigonometry
    and converts them into linear cosine function
    '''
    #lam,theta = sympy.symbols('lambda theta')


    def __init__(self,SympyExpr):
        self.Expression = SympyExpr

    def  __repr__(self):
        return "Sympy expression"

    def LinearizeInCosine(self):
        cos, sin, tan  = sympy.cos, sympy.sin, sympy.tan
        NewExpr=""
        TempNewExpr=" "

        #now parse the functions
        while NewExpr!=TempNewExpr:
            if not(NewExpr):
                NewExpr = self.Expression
                TempNewExpr = NewExpr
                #Parse for power

            else:
                NewExpr = TempNewExpr




            Items = sympy.srepr(NewExpr)
            Angles = FindAllAngles(Items)



            for angle in Angles:

                #Change the angle
                TempNewExpr = TempNewExpr.subs(tan(angle), sin(angle)/cos(angle))

                #This uses simple trigonometric functions such as cos(A+B) expansion
                #as well as sin2x = 2sinxcosx
                TempNewExpr = sympy.trigsimp(TempNewExpr)

                #Use in built ex
                TempNewExpr = sympy.simplify(TempNewExpr)

                #Check for the power
                TempNewExpr=ParsePower(TempNewExpr,angle)


                #implementing cos^2(x) = (cos(2x)+1)/2
                #TempNewExpr = TempNewExpr.subs(cos(angle)*cos(angle), (cos(2*angle)+1)/2 )

                #implementing sin^2(x) = (1-cos(2x))/2
                #TempNewExpr = TempNewExpr.subs(sin(angle)*sin(angle), (1-cos(2*angle))/2 )


                #Replace sinx = sqrt(1-cos^2x)
                #TempNewExpr = TempNewExpr.subs(sin(angle), sympy.sqrt(1-cos(angle)))

                #write all trig functions in terms of
                #TempNewExpr = sympy.expand_trig(TempNewExpr)

        return NewExpr
