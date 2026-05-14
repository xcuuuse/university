# coding=cp1251

import mapnik
from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()


path = "d:/Devel/Python/mapnik/borders/"
w,h = 1024,768
m = mapnik.Map(w, h)

# Instantiate a map object with given width, height and spatial reference system
#m = mapnik.Map(w,h,"+proj=latlong +datum=WGS84")
# Set background colour to 'steelblue'.  
# You can use 'named' colours, #rrggbb, #rgb or rgb(r%,g%,b%) format
#m.background = mapnik.Color('rgb(90%,90%,90%)')

# Now lets create a style and add it to the Map.
#s = mapnik.Style()
# A Style can have one or more rules. A rule consists of a filter, min/max scale 
# demoninators and 1..N Symbolizers. If you don't specify filter and scale denominators
# you get default values :
#   Filter =  'ALL' filter (meaning symbolizer(s) will be applied to all features) 
#   MinScaleDenominator = 0
#   MaxScaleDenominator = INF  
# Lets keep things simple and use default value, but to create a map we 
# we still must provide at least one Symbolizer. Here we  want to fill countries polygons with 
# greyish colour and draw outlines with a bit darker stroke. 

#riversRule=mapnik.Rule()
#r.symbols.append(mapnik.PolygonSymbolizer(mapnik.Color('#f2eff9')))
#riversRule.symbols.append(mapnik.LineSymbolizer(mapnik.Color('steelblue'),1))
#s.rules.append(riversRule)

#townsRule=mapnik.Rule()
#townsRule.symbols.append(mapnik.PolygonSymbolizer(mapnik.Color('#ff0000')))
#townsRule.symbols.append(mapnik.LineSymbolizer(mapnik.Color('#000000'),0.2))
#townsRule.filter = mapnik.Filter("[CODE] = '41100000'")
#s.rules.append(townsRule)

#m.append_style('basic style',s)


mapfile = "styles.xml"
mapnik.load_map(m, mapfile)


#, "hydro_line", "hydro_s"
mapNames = ["areas", "districts", "towns", "hydro_l", "hydro_s"]
for mapName in mapNames:
	# Here we instantiate our data layer, first by giving it a name and srs (proj4 projections string), and then by giving it a datasource.
	projString = "+proj=utm +zone=32 +ellps=krass +datum=WGS84 +units=m +no_defs"
	#projString = "+proj=latlong +ellps=krass +towgs84=23.92,-141.27,-80.9,0,0,0,0"
	lyr = mapnik.Layer(mapName,projString)
	# Then provide the full filesystem path to a shapefile in WGS84 or EPSG 4326 projection without the .shp extension
	# A sample shapefile can be downloaded from http://mapnik-utils.googlecode.com/svn/data/world_borders.zip
	lyr.datasource = mapnik.Shapefile(file = path + 'datad/' + mapName)
	lyr.styles.append('basic style')
	m.layers.append(lyr)


#env = mapnik.Envelope(25, 51, 30, 55)
env = lyr.envelope()
print env
m.zoom_to_box(env)
ipshell()
#a = m.layers[1].datasource.all_features()[0].attributes["F9"]
#ipshell()


if True:
	# Write the data to a png image called world.png in the base directory of your user
	render_file = path+'world.png'
	im = mapnik.Image(w,h)
	#mapnik.render_to_file(m,render_file, 'png')
	print "rendering..."
	mapnik.render(m,im)
	print "finished"
	im.save(render_file)
	import os
	os.system(render_file)