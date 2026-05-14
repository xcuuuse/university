from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()

if __name__ == "__main__":
	with open("data-x.csv", "r") as fr:	
		with open("datamap.txt", "w") as fw:	
			i = 0
			fw.write("polygons["+str(i)+"] = new YMaps.Polygon([\n")
			
			for line in fr:
				#print line
				data = line.split(",")
				num1 = data[0].split("\n")[0]
				num2 = data[1].split("\n")[0]
								
				line = "	new YMaps.GeoPoint(" + str(num2) + ", " + str(num1) + "),\n"
				#line = "	new google.maps.LatLng(" + str(num1) + ", " + str(num2) + "),\n"
				
				fw.write(line);
				#break
		
			fw.write("]);\n")
			#fw.write("];\n")
			
			fr.close();
			fw.close();