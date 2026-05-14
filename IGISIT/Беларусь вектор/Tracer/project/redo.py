from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()

if __name__ == "__main__":
	with open("data-x.csv", "r") as fr:	
		with open("datamap", "w") as fw:	
			i = 0
			#fw.write("polygonCoords["+str(i)+"] = [\n")
			fw.write("polygons["+str(i)+"] = new YMaps.Polygon([\n")
			
			for line in fr:
				#print line
				data = line.split("N")
				nums = data[0][1:100].split()
				num1 = float(nums[0]) + float(nums[1])/60 + float(nums[2])/3600
				
				nums = data[1][1:100].split("E")[0].split()
				num2 = float(nums[0]) + float(nums[1])/60 + float(nums[2])/3600
								
				line = "	new YMaps.GeoPoint(" + str(num2) + ", " + str(num1) + "),\n"
				#line = "	new google.maps.LatLng(" + str(num1) + ", " + str(num2) + "),\n"
				
				fw.write(line);
				#break
		
			fw.write("]);\n")
			#fw.write("];\n")
			
			fr.close();
			fw.close();