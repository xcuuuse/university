import shapefile as sf
import mapnik
import time
from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()


#path = "d:/Devel/Python/mapnik/borders/"
#w,h = 1024,768
#m = mapnik.Map(w, h)

#mapfile = "styles.xml"
#mapnik.load_map(m, mapfile)


def envelopes_intersect(e1, e2):
	return (e1[0] >= e2[0] and e1[0] <= e2[2] and e1[1] >= e2[1] and e1[1] <= e2[3]) or ((e1[2] >= e2[0] and e1[2] <= e2[2] and e1[3] >= e2[1] and e1[3] <= e2[3]))

	
def checkSimpleLinesIntersection(x1, x2, x3, x4, y1, y2, y3, y4):	
	divider = ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
	if (divider != 0):
		ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / divider
		ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / divider
		loLim = -1
		hiLim = 2
		if (ua >= loLim and ua <= hiLim and ub >= loLim and ub <= hiLim):
			return (x1 + ua * (x2 - x1), y1 + ua * (y2- y1))
		else:
			return False
	else:
		print "Zero division: ", x1, x2, x3, x4, y1, y2, y3, y4
		return False
			
	
	
def generate_intersections(mapName, courtesy, filterCode):
	shf = sf.Reader('data/' + mapName)
	shapes = shf.shapes()
	records = shf.records()
	for codeIndex in xrange(len(shf.fields)):
		if shf.fields[codeIndex][0] == "CODE":
			break
			
	codeIndex -= 1		

	unique = set()
	inter = set()
	cnt = 0

	
	
	
	lines = []
	for num in xrange(len(shapes)):
		shape = shapes[num]
		record = records[num]
		if record[codeIndex] == filterCode:
			lines.append(shape.points)
	
	
	
	time1 = time.clock()
	
	minValue = -100000
	maxValue = 100000
	env = []
	total = len(lines)
	for i in xrange(total):
		left = maxValue
		top = maxValue
		right = minValue
		bottom = minValue
		
		for pt in lines[i]:
			left = min(left, pt[0])
			top = min(top, pt[1])
			right = max(right, pt[0])
			bottom = max(bottom, pt[1])
			
		env.append((left, top, right, bottom))
	
	cntPos = 0
	cntNeg = 0
	print "Envelopes ready"
	
	pointEnvelopes = []
	for i in xrange(total):
		lineEnvelope = []
		for ptI in xrange(len(lines[i]) - 1):
			i1 = lines[i][ptI]
			i2 = lines[i][ptI + 1]
			envI = (min(i1[0], i2[0]), min(i1[1], i2[1]), max(i1[0], i2[0]), max(i1[1], i2[1]))
			lineEnvelope.append(envI)
		pointEnvelopes.append(lineEnvelope)
		
	print "Point envelopes ready"
	
	intersected = []
	for i in xrange(total):
		interForI = []
		intersected.append(interForI)
		for j in xrange(i+1, total):
			if envelopes_intersect(env[i], env[j]):
				cntPos += 1
				interForI.append(j)
			else:
				cntNeg += 1
				
	print "intersections:",cntPos,"/",cntNeg,"ratio",cntNeg/cntPos
	
	
	cntPos = 0
	cntNeg = 0
	linesIntersections = []
	for i in xrange(total):
		interForI = intersected[i]
		#print i, len(interForI)
		for j in interForI: # interForI contains indicies!
			for ptI in xrange(len(lines[i]) - 1):
				for ptJ in xrange(len(lines[j]) - 1):
					envI = pointEnvelopes[i][ptI]
					envJ = pointEnvelopes[j][ptJ]
					if envelopes_intersect(envI, envJ):
						cntPos += 1
						linesIntersections.append((i, ptI, j, ptJ))
					else:
						cntNeg += 1
		
	print "intersections:",cntPos,"/",cntNeg,"ratio",cntNeg/cntPos
	
	finalResult = []
	cntPos = 0
	cntNeg = 0
	for intersection in linesIntersections:
		i, ptI, j, ptJ = intersection		
		x1, y1 = lines[i][ptI]
		x2, y2 = lines[i][ptI + 1]
		x3, y3 = lines[j][ptJ]
		x4, y4 = lines[j][ptJ + 1]
	
		res = checkSimpleLinesIntersection(x1, x2, x3, x4, y1, y2, y3, y4)
		if not res:
			cntNeg += 1
		else:
			cntPos += 1
			finalResult.append(res)
		
	print "intersections:",cntPos,"/",cntNeg,"ratio",cntNeg/cntPos
	
	print len(inter),"out of",len(unique),"out of",cnt
	time2 = time.clock()
	print 'Code time %.3f seconds' % (time2 - time1)
	
	
	
	wr = sf.Writer()
	wr = sf.Writer(sf.POINT)
	wr.field("CODE")
	for point in finalResult:
		wr.point(point[0], point[1])
		wr.record("debug-intersect")
	wr.save('data/intersections')
	print "Intersections written"

	
	

if __name__ == "__main__":
	import sys
	courtesy = 3
	if len(sys.argv) > 1:
		courtesy = int(sys.argv[1])
	
	lrName = "hydro_l"
	filterCode = '31410000'
	print 'Generating intersection on layer',lrName,"for code",filterCode
	print 'Courtesy set to', courtesy
	generate_intersections(lrName, courtesy, filterCode)

#mapNames = ["intersections", "hydro_l"]
#for mapName in mapNames:
#	projString = "+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
#	lyr = mapnik.Layer(mapName,projString)
#	lyr.datasource = mapnik.Shapefile(file = path + 'data/' + mapName)
#	lyr.styles.append('basic style')
#	m.layers.append(lyr)

#env = lyr.envelope()
#m.zoom_to_box(env)




#if True:
	# Write the data to a png image called world.png in the base directory of your user
#	render_file = path+'world.png'
#	im = mapnik.Image(w,h)
	#mapnik.render_to_file(m,render_file, 'png')
#	print "rendering..."
#	mapnik.render(m,im)
#	print "finished"
#	im.save(render_file)
#	import os
#	os.system(render_file)