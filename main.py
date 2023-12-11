import sys
from njuskalo.njuskalo_scrape import njuskalo_scrape
from olx.olx_scrape import olx_scrape


# Trebamo se odluciti da li scrape-at njuskalo ili olx

if __name__ == "__main__":
	if len(sys.argv) > 1:
		arg = sys.argv[1]
		if arg == "njuskalo":
			njuskalo_scrape()
		elif arg == "olx":
			olx_scrape()
		else:
			print("Invalid argument")
	else:
		print("No argument provided")
	

