import requests
import json
import random

MaxAPIResults = 100 #Determined by subscribed tier
filenameOfAPI_Key = "API_Key"
mainMeat = "chicken"
mainVeg = "broccoli"

#--sets the seed for random start of 1st recipe to match--#
#start = random.randint(0,MaxAPIResults)
start = 0

measurementUnits = ['teaspoons','tablespoons','cups','containers','packets','bags','quarts','pounds','cans','bottles',
		'pints','packages','ounces','jars','heads','gallons','drops','bars','boxes','pinches',
		'bunches','layers','slices','links','bulbs','stalks','squares','sprigs', 'oz',
		'fillets','pieces','legs','thighs','cubes','granules','strips','trays','leaves','loaves','halves']

#--transform liquid measurements to cups--#
#-amount is parsed amount. unit is parsed unit-#
def transformToCups(amount, unit):
	if unit == "cups":
		return amount
	elif unit == "quarts":
		return amount / 16
	elif unit == "quarts":
		return amount / 4
	elif unit == "pints":
		return amount / 2
	elif unit == "ounces":
		return amount * 8
	elif unit == "tablespoons":
		return amount * 16
	elif unit == "teaspoons":
		return amount * 48
	else:
		return amount

rawKeyIngredients = []
keyIngredients = []
ranks = []

#--This block gets API key from PRIVATE file--#
API_file = open(filenameOfAPI_Key,'r')
API_ID = API_file.readline()[:-1]
API_Key = API_file.readline()[:-1]
API_file.close()
#r = requests.get('https://api.edamam.com/search?q=' + mainVeg + ',' + mainMeat + '&app_id=' + API_ID + '&app_key=' + API_Key + '&from=0&to=100')
#data = r.json()

##--use this til final run--##
#data contains all recipes returned
with open("this.json") as f:
	data = json.load(f)

#--ingred is list of raw ingredients ie 1/2 teaspoon of canola oil for recipe to start--#
ingred = data["hits"][start]["recipe"]["ingredients"]

#--prints URL of recipe denoted by start--#
url = data["hits"][start]["recipe"]["url"]
print(url)

##---This block prints ingredients in amounts---##
x = 0
for item in range(0, len(ingred)):
	for key,value in ingred[item].items():
		if(x % 2 == 0):
			#print(value)
			rawKeyIngredients.append(value)
		x+=1

#--Put key ingredients in list to parse recipes for matches--#
for each in rawKeyIngredients:		#rawKeyingredients is entire text of ingredient, amount, chopped/canned, etc
	temp = each.lower()		#convert to lowercase for easier matching with allIngredients.txt
	f1 = open("allIngredients.txt")
	tempWord = ""
	for line in f1:		#Go through each line of allIngredients.txt
		if (temp.find(line[:-1].lower()) > -1):		#if any string from temp is found in allIngredients.txt - newline character
			if (len(line[:-1].lower()) > len(tempWord)):		#update longest word. Ideally, the longest match is the most specific ingredient
				tempWord = line[:-1].lower()
	if(len(tempWord) == 0):		#If ingredient is not found in known ingredients in allIngredients.txt file
		print("***************" + temp + " -> Not found in allIngredients.txt. Please add.***************")
		tempWord = temp
	if(not any(item in tempWord for item in keyIngredients)):	#If ingredient not repeated in the recipe's list, add to list of recipes to match for ranking
		keyIngredients.append(tempWord)
f1.close()

x = 0
for y in range(0, MaxAPIResults):		#for each recipe in returned results from API search
	tempIngred = []
	ingredi = data["hits"][y]["recipe"]["ingredients"]		#temp dictionary for extracting recipe ingredients
	for item in range(0, len(ingredi)):
		for key,value in ingredi[item].items():
			if(x % 2 == 0):
				tempIngred.append(value.lower())
			x+=1

	rank = 0
	for each in tempIngred:		#for each dictionary of extracted recipe ingredient list
		match = False
		for item in keyIngredients:
			if (each.find(item) > -1):
				match = True
		if(match):
			rank += 1

#for x in keyIngredients:
#	print(x)


	ranks.append((rank/len(tempIngred)) * 100)
for x in ranks:
	print(x)
##ranks currently contains raw rank of all returned API recipes


#keyIngredients now contains ingredients to match with other recipes
#now go through all recipes iningred and rank them by amount of matching ingredients compared to total ingredients by using find again
#if a recipe is chicken and oil and that's it. score a higher rank than a recipe that has chicken, oil, salt, pepper, oregano, carrrots, mahogny, etc
