import shapefile as sf
import mapnik
import time
from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()

	
def get_contour(mapName):
	shf = sf.Reader('data/' + mapName)
	shapes = shf.shapes()
	records = shf.records()
			
	cnt = 0
	
	
	lines = []
	num = 0
	
	type = ''
	with open("data.txt", "w") as f:	
		i = 0
		for shape in shapes:
		#shape = shapes[2]
		#if True:
			if type == 'google':
				f.write("polygonCoords["+str(i)+"] = [\n")
			elif type == 'yandex':
				f.write("polygons["+str(i)+"] = new YMaps.Polygon([\n")	
				
			for point in shape.points:
				if type == 'google':
					line = "	new google.maps.LatLng(" + str(point[1]) + ", " + str(point[0]) + "),\n"
				elif type == 'yandex':
					line = "	new YMaps.GeoPoint(" + str(point[0]) + ", " + str(point[1]) + "),\n"
				else:
					line = "," + str(point[1]) + ", " + str(point[0]) + "\n"
				f.write(line)
				
			if type == 'google':
				f.write("];\n")
			elif type == 'yandex':
				f.write("]);\n")
			i += 1
		f.close()
	
	

if __name__ == "__main__":
	import sys
	get_contour("areas")