import requests
import json
import random

MaxAPIResults = 100 #Determined by subscribed tier
filenameOfAPI_Key = "API_Key"
mainMeat = "chicken"
mainVeg = "broccoli"

#--sets the seed for random start of 1st recipe to match--#
#start = random.randint(0,MaxAPIResults - 1)
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
for each in rawKeyIngredients:
	f1 = open("allIngredients.txt")
	temp = each.lower()
	print(temp)
	tempWord = ""
	for line in f1:
		if (temp.find(line[:-1].lower()) > -1):
			if (len(line[:-1].lower()) > len(tempWord)):
				tempWord = line[:-1].lower()
	if(not any(item in tempWord for item in keyIngredients)):
		keyIngredients.append(tempWord)


	#open allIngredients.txt and save to a list
	#use find for each line (ing) in allIngredients.txt, find in keyIngredients
	#if the above is true, replace string at keyIngredients at index each with (ing)
	#use find command
for x in keyIngredients:
	print(x)
#	print(each)

#keyIngredients now contains ingredients to match with other recipes
#now go through all recipes iningred and rank them by amount of matching ingredients compared to total ingredients by using find again
#if a recipe is chicken and oil and that's it. score a higher rank than a recipe that has chicken, oil, salt, pepper, oregano, carrrots, mahogny, etc
