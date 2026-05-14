# -*- coding: utf-8 -*- 

from math import *

# Трансформация геодезических и геоцентрических координат
# из системы координат WGS-84 в систему координат СК-42 и
# наоборот...
Pi = 3.14159265358979
Ro = 206264.8062
Rd = 1.7453292 * 10 ** -2
Rm = 2.9088821 * 10 ** -4
Rs = 4.8481368 * 10 ** -6
# Эллипсоид Красовского (Пулково 1942)
aP = 6378245
alP = 1 / 298.3
e2P = 2 * alP - alP ** 2
# Эллипсоид GRS80 (WGS84)
aW = 6378137
alW = 1 / 298.257223563
e2W = 2 * alW - alW ** 2
# Вспомогательные значения для преобразования эллипсоидов
a = (aP + aW) / 2
e2 = (e2P + e2W) / 2
Da = aW - aP
de2 = e2W - e2P
# Линейные элементы трансформирования, в метрах
dx = 23.92
dy = -141.27
dz = -80.9
# Угловые элементы трансформирования, в секундах
wx = 0
wy = -0.371
wz = -0.849
# Дифференциальное различие масштабов
ms = -0.124 * 10 ** -6




def WGS84TOSK42B(B, L, H):
    return B - dB(B, L, H) / 3600
	
def SK42TOWGS84B(B, L, H):
    return B + dB(B, L, H) / 3600

def WGS84TOSK42L(B, L, H):
    return L - dL(B, L, H) / 3600

def SK42TOWGS84L(B, L, H):
	return L + dL(B, L, H) / 3600

def WGS84TOSK42H(B, L, H):
    return H - dH(B, L, H)

def SK42TOWGS84H(B, L, H):
    return H + dH(B, L, H)

def dB(Bd, Ld, H):
	B = Bd * Pi / 180
	L = Ld * Pi / 180
	M = a * (1 - e2) * (1 - e2 * sin(B) ** 2) ** -1.5
	N = a * (1 - e2 * sin(B) ** 2) ** -0.5
	return (Ro / (M + H)) * (N / a * e2 * sin(B) * cos(B) * Da + 
		(N ** 2 / a ** 2 + 1) * N * sin(B) * cos(B) * de2 / 2 - (dx * cos(L) + dy * sin(L)) * sin(B) + dz * cos(B)) - wx * sin(L) * (1 + e2 * cos(2 * B)) + wy * cos(L) * (1 + e2 * cos(2 * B)) - Ro * ms * e2 * sin(B) * cos(B)

def dL(Bd, Ld, H): 
	B = Bd * Pi / 180
	L = Ld * Pi / 180
	N = a * (1 - e2 * sin(B) ** 2) ** -0.5
	return Ro / ((N + H) * cos(B)) * (dy * cos(L) - dx * sin(L)) + tan(B) * (1 - e2) * (wx * cos(L) + wy * sin(L)) - wz

def dH(Bd, Ld, H): 
	B = Bd * Pi / 180
	L = Ld * Pi / 180
	N = a * (1 - e2 * sin(B) ** 2) ** -0.5
	return N * sin(B) ** 2 * de2 / 2 - (a / N) * Da + (dx * cos(L) + dy * sin(L)) * cos(B) + dz * sin(B) - N * e2 * sin(B) * cos(B) * (wx / Ro * sin(L) - wy / Ro * cos(L)) + (a ** 2 / N + H) * ms

def WGS84TOSK42X(X , Y , Z ): 
	ry = wy / 3600 * Pi / 180
	rz = wz / 3600 * Pi / 180
	return (1 - ms) * X - (1 - ms) * rz * Y + (1 - ms) * ry * Z - dx

def WGS84TOSK42Y(X , Y , Z ): 
	rz = wz / 3600 * Pi / 180 
	return (1 - ms) * Y + (1 - ms) * rz * X - dy

def WGS84TOSK42Z(X , Y , Z ): 
	ry = wy / 3600 * Pi / 180 
	return (1 - ms) * Z - (1 - ms) * ry * X - dz

def SK42TOWGS84X(X , Y , Z ): 
	ry = wy / 3600 * Pi / 180
	rz = wz / 3600 * Pi / 180
	return (1 + ms) * X + (1 - ms) * rz * Y - (1 - ms) * ry * Z + dx

def SK42TOWGS84Y(X , Y , Z ): 
	rz = wz / 3600 * Pi / 180
	return (1 + ms) * Y - (1 - ms) * rz * X + dy

def SK42TOWGS84Z(X , Y , Z ): 
	ry = wy / 3600 * Pi / 180 
	return (1 + ms) * Z + (1 - ms) * ry * X + dz
	
def transform(pt):
	return (SK42TOWGS84B(pt[0], pt[1], 0), SK42TOWGS84L(pt[0], pt[1], 0))

