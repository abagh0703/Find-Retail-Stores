import googlemaps

gmaps = googlemaps.Client(key="AIzaSyAedyIz_Otj-9og3f61bCuufIUWDHuGNfY")

def load_map(addresses):
	for address in addresses:
		adr = address[1]
		loc = gmaps.geocode(adr)
		address[1] = loc