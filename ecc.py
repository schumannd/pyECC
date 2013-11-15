#!/usr/bin/python
import sys, os
from Point import Point

def addEC(p1, p2, a, p):
	if p1.x == p2.x and p1.y == p2.y:
		m = (3*p1.x*p1.x + a)*modularInverse(2*p1.y, p) % p
		x3 = (m*m - 2*p1.x) % p
		y3 = -(p1.y + m*(x3 - p1.x)) % p
	elif p1.x == p2.x and p1.y != p2.y:
		raise Exception("reached Infinity")
	elif p1.x != p2.x and p1.y != p2.y:
		m = (p2.y -p1.y)*modularInverse(p2.x-p1.x, p) % p
		x3 = (m*m - (p1.x + p2.x)) % p
		y3 = -(p2.y + m*(x3 - p2.x)) % p
	return Point(x3,y3)

def mulEC(Point, factor, a, p):
	if factor == 1:
		solution = Point
	elif factor % 2 == 0:
		halfPoint = mulEC(Point, factor/2, a, p)
		solution = addEC(halfPoint, halfPoint, a, p)
	else:
		halfPoint = mulEC(Point, factor-1, a, p)
		solution = addEC(halfPoint, Point, a, p)
	return solution

def main():
	N = 182755680224874988969105090392374859247
	A = 286458106491124997002528249079664631375
	p = 231980187997634794246138521723892165531
	cypherArray = []
	cleartext = ""
	with open(sys.argv[1], "r") as textFile:
		for line in textFile:
			x = line.split(' ')
			cypherArray.append(Point(Point(int(x[0]),int(x[1])), Point(int(x[2]),int(x[3]))))
	for cypher in cypherArray:
		clearPoint = decrypt(cypher.x, cypher.y, N, A, p)
		cleartext += str(chr(clearPoint.x))
	print cleartext


def decrypt(Y, Alpha, privateN, a, p):
	negativePoint = mulEC(Alpha, privateN, a, p)
	negativePoint.y = negativePoint.y*-1
	return addEC(negativePoint, Y, a, p)

def bruteForce(p, a, b, G, P):
	current = Point(G.x, G.y)
	N = 1
	while current.x != P.x or current.y != P.y:
		current = addEC(current, G, a, p)
		N +=1
		if N%1000000 == 0:
			print N
	return N

def pulverizer(a, b): # a > b
	x1, y1, x2, y2 = 1, 0, 0, 1
	while b != 0:
		q, r = a//b, a%b
		x, y = x1 - q*x2, y1 - q*y2
		a, b, x1, y1, x2, y2 = b, r, x2, y2, x, y
		# print str(q)+", "+str(r)+", "+str(a)+", "+str(b)+", "+str(x1)+", "+str(y1)+", "+str(x2)+", "+str(y2)
	return a, x1, y1

def modularInverse(e, phi):
	g, x, y = pulverizer(e, phi)
	if g != 1:
		raise Exception('modular inverse does not exist')
	else:
		return x % phi

if __name__ == "__main__":
	sys.exit(main())