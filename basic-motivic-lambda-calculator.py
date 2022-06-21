#BASIC CALCULATOR FOR MOTIVIC LAMBDA ALGEBRA

#
#Examples for each of the main functions are commented out below
#
#INSTRUCTIONS FOR IDLE USERS:
#to run, open this .py file in IDLE, and enter a command as below
#


#SAMPLE COMMANDS

#Prints the differential on \lambda_1\lambda_3\lambda_5\tau + \lambda_3^3 \tau:
#ReduceDiff([[1,3,5,'t'],[3,3,3,'t']])


#Prints the sum of two polynomials:
#AddPoly([[2,0,'r'],[1,1,'t','r']],[[2,0,'r'],[1,0]])


#Prints the product of two polynomials:
#MultPoly([[1,1,2,'t']],[[3,5,1,'r','r']])





#BELOW HERE IS THE CODE FOR THE CALCULATOR ITSELF


import math

#DATA STRUCTURES
    #a monomial has the form [a,b,c,d,...,e], i.e. is an array
    #a polynomial has the form [mon1, mon2, mon3, ..., monN], i.e. is an array of arrays
    #a list of polynomials has the form [poly1, poly2, poly3, ..., polyN], i.e. is an array of arrays of arrays


#HELPER FUNCTIONS

#binomail coefficients mod two
def LucasLemma(a,b):
    if a<0 or b<0:
        return False
    if a<b:
        return False
    if (~a & b):
        return False
    else:
        return True

#adem relations for pair of generators
def ReducePair(r,s):
    output = []
    if r=='t':
        if not s=='t' and not s=='r':
            if (s%2)==1:
                output.append([s,'t'])
                output.append([s+1,'r'])
                return output
            else:
                output.append([s,'t'])
                output.append([s+1,'t','r'])
                output.append([s+2,'r','r'])
                return output
    if r=='r':
        if not s=='r':
            output.append([s,r])
            return output
    if 2*r>=s:
        output.append([r,s])
        return output
    b=s-2*r-1
    if (r%2)==0 and (b%2)==1:
        for c in range(0,math.ceil(b/2)):
            if LucasLemma(b-1-c,c) and (c%2)==0:
                output.append([r+b-c,1+2*r+c,'t'])
            if LucasLemma(b-1-c,c) and (c%2)==1:
                output.append([r+b-c,1+2*r+c])
        for c in range(0,math.ceil(b/2)+1):
            if LucasLemma(math.floor(b/2) - math.floor(c/2),math.floor(c/2)):
                output.append([r+b+1-c,1+2*r+c,'r'])
    else:
        for c in range (0,math.ceil(b/2)):
            if LucasLemma(b-1-c,c):
                output.append([r+b-c,1+2*r+c])
    return output

#checks admissibility of pair
def AdmPair(r,s):
    if r=='r':
        if not s=='r':
            return False
    if r=='t':
        if not (s=='t' or s=='r'):
            return False
    if s=='t':
        if not r=='r':
            return True
    if s=='r':
        return True
    if 2*r<s:
        return False
    else:
        return True


#DIFFERENTIALS WITHOUT REDUCTION

#differential on generator
def DiffGen(b):
    output = []
    if b=='r':
        return output
    if b=='t':
        output.append([0,'r'])
        return output
    for c in range (1,math.ceil(b/2)+1):
        if LucasLemma(b-c,c):
            output.append([b-c,c-1])
    return output

#differential on monomial
def LeibnizMon(mon):
    output=[]
    for i in range(0,len(mon)):
        diff = DiffGen(mon[i])
        for j in range(0,len(diff)):
            output.append(mon[:i]+diff[j]+mon[i+1:])
    return output

#differential on polynomial            
def LeibnizPoly(poly):
    output=[]
    for i in range(0,len(poly)):
        output= output+LeibnizMon(poly[i])
    return output

#REDUCING POLYNOMIALS

#multiplicatively reduces a polynomial
def MultReduce(poly):
    output = []
    while len(poly)>0:
        mon=poly[0]
        poly=poly[1:]
        if  len(mon)>1:
            monDone=False
            i=0
            while not monDone:
                if not AdmPair(mon[i],mon[i+1]):
                    monDone=True
                    change=ReducePair(mon[i],mon[i+1])
                    if len(change)>0:
                        for j in range(0,len(change)):
                            poly.append(mon[:i]+change[j]+mon[i+2:])
                        i=len(mon)
                    else:
                        i=len(mon)
                i=i+1
                if i==(len(mon)-1):
                    output.append(mon)
                    monDone=True
    return output


#additively reduces a polynomial
def AddReduce(poly):
        i=0
        j=1
        done=False
        while not done:
            if i+1>=len(poly):
                done=True
                return poly
            if poly[i]==poly[j]:
                poly=poly[0:i]+poly[i+1:j]+poly[j+1:]
                if i+1>=len(poly):
                    done=True
                    return poly
                j=i+1
            else:
                j=j+1
                if j>=len(poly):
                    i=i+1
                    j=i+1

#multiplicatively then additively reduces a polynomial
def Reduce(poly):
    return AddReduce(MultReduce(poly))

#
#
#MAIN FUNCTIONS: REDUCED DIFFERENTIAL OF POLYNOMIAL, ADDING AND MUTIPLYING POLYNOMIALS
#
#


#returns fully reduced differential on a polynomial
def ReduceDiff(poly):
    print("Input:")
    print(poly)
    print("Differential:")
    return Reduce(LeibnizPoly(poly))

#adds polynomials and reduces
def AddPoly(poly1,poly2):
    return AddReduce(poly1+poly2)

#multiplies polynomials 
def MultPoly(poly1,poly2):
    output=[]
    for i in range(0,len(poly1)):
        for j in range(0,len(poly2)):
            output.append(poly1[i]+poly2[j])
    return Reduce(output)




#CODE FOR EXTRACTING INFO ABOUT MONOMIALS AND POLYNOMIALS

#returns number of taus in a monomial
def numT(mon):
    count=0
    for i in range(0,len(mon)):
        if mon[i]=='t':
            count=count+1
    return count

#returns number of rhos in a monomial
def numR(mon):
    count=0
    for i in range(0,len(mon)):
        if mon[i]=='r':
            count=count+1
    return count

#determines if mon1 is less than mon2 (sorry for bad naming, equality returns false)
def LEQ(mon1,mon2):
    if numR(mon1)>numR(mon2):
        return True
    if numR(mon1)<numR(mon2):
        return False
    if numT(mon1)>numT(mon2):
        return True
    if numT(mon1)<numT(mon2):
        return False
    for i in range(0,min(len(mon1),len(mon2))):
        if isinstance(mon1[i],int) and isinstance(mon2[i],int):
            if mon1[i]<mon2[i]:
                return True
            if mon1[i]>mon2[i]:
                return False
    if len(mon1)>len(mon2):
        return True
    if len(mon1)<len(mon2):
        return False
    return False

#gets leading term in a polynomial
def getLead(poly):
    output = poly[0]
    for i in range(0,len(poly)):
        if LEQ(output,poly[i]):
            output=poly[i]
    return output

#returns admissibility of monomial
def isAdmissible(mon):
    for i in range(0,len(mon)-1):
        if mon[i+1]=='r':
            if not mon[i]=='r':
                return False
        if mon[i+1]=='t':
            if not (mon[i]=='r' or mon[i]=='t'):
                return False
        if mon[i]=='t' or mon[i]=='r':
            return False
        if 2*mon[i]<mon[i+1]:
            return False
    return True


#returns stem of monomial
def stem(mon):
    out=0
    for i in range(0,len(mon)):
        if isinstance(mon[i], int):
            out=out+mon[i]
        if mon[i]=='r':
            out=out-1
    return out

#returns weight of monomial
def weight(mon):
    out=0
    for i in range(0,len(mon)):
        if isinstance(mon[i], int):
            out=out+math.ceil(mon[i]/2)
        if mon[i]=='r':
            out=out-1
        if mon[i]=='t':
            out=out-1
    return out

#returns coweight of monomial
def coweight(mon):
    return stem(mon)-weight(mon)

#returns filtration of monomial
def filt(mon):
    out=0
    for i in range(0,len(mon)):
        if isinstance(mon[i],int):
            out=out+1
    return out

#removes rhos and taus from a monomial
def removeRT(mon):
    output=[]
    for i in range(0,len(mon)):
        if isinstance(mon[i],int):
            output.append(mon[i])
    return output

def removeRhos(poly,amount):
    output=[]
    for i in range(0,len(poly)):
        output.append([])
        for j in range(0,len(poly[i])-amount):
            output[i].append(poly[i][j])
    return output


