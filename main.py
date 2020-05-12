import requests
import json
import random

MaxAPIResults = 100 #Determined by subscribed tier
filenameOfAPI_Key = "API_Key"
mainMeat = "chicken,breast"
mainVeg = "broccoli"
mealsToMake = 5 #5 is maximum for DEVELOPER subscribe tier
similarityThreshold = 5 #The higher the number, the less likely the recipes are to being similar. 2 is minimum
spaceOffset = 30 #variable for formatting alphabetized shopping list file

#--sets the seed for random start of 1st recipe to match--#
start = random.randint(0,MaxAPIResults-1)

chickenIngred = ['alfredo','barbecue,sauce','cheese','garlic','mexican','potato','bacon','ketchup',
		'brown,sugar','cayenne','']
fishIngred = ['lemon','garlic','taco','flour','sugar','parsley','']
steakIngred = ['salt','sugar','worcestershire','garlic','oil','barbecue,sauce','seasoning','onion','']
porkIngred = ['salt','brown,sugar','oil','garlic','barbecue,sauce','paprika','seasoning','cayenne','']
sausageIngred = ['egg','cayenne','pepper','bacon','salt','cheese','onion','']
groundbeefIngred = ['taco','ketchup','potato','carrot','salt','pepper','cheese','tomato','onion','']

rawKeyIngredients = []
keyIngredients = []
chosenCuisine = []
cuisineType = []

#--This block gets API key from PRIVATE file--#
API_file = open(filenameOfAPI_Key,'r')
API_ID = API_file.readline()[:-1]
API_Key = API_file.readline()[:-1]
API_file.close()

print("* Welcome to Easy Recipes *\nFirst select main meat\n\n")
print("Type 1 for chicken breast")
print("Type 2 for fish")
print("Type 3 for steak")
print("Type 4 for pork")
print("Type 5 for sausage")
print("Type 6 for ground beef")

input1 = input()

if(input1 == "1"):
	mainMeat = "chicken,breast"
if(input1 == "2"):
	mainMeat = "fish"
if(input1 == "3"):
	mainMeat = "steak"
if(input1 == "4"):
	mainMeat = "pork"
if(input1 == "5"):
	mainMeat = "sausage"
if(input1 == "6"):
	mainMeat = "ground,beef"

print(mainMeat+" is your selected main meat. Type in main vegetable.")
input2 = input()
mainVeg = input2
print(mainVeg+" is your selected main vegetable. Please wait while system processes request..\n")

#r = requests.get('https://api.edamam.com/search?q='+mainVeg+','+mainMeat+'&app_id='+API_ID+'&app_key='+API_Key+'&from=0&to='+str(MaxAPIResults))
#data = r.json()

##--use this til final run--##
#data contains all recipes returned
with open("this.json") as f:
	data = json.load(f)

#--ingred is list of raw ingredients (ie 1/2 teaspoon of canola oil for recipe) to start--#
ingred = data["hits"][start]["recipe"]["ingredients"]

#--saves URL of recipe denoted by start--#
url = data["hits"][start]["recipe"]["url"]

#--saves name of recipe--#
recipeName = data["hits"][start]["recipe"]["label"]

#--saves serve amount--#
recipeAmount = data["hits"][start]["recipe"]["yield"]

##---This block extracts ingredients in amounts from dictionary---##
x = 0
for item in range(0, len(ingred)):
	for key,value in ingred[item].items():
		if(x % 2 == 0):
			if(not any(item in value for item in rawKeyIngredients)):	#If ingredient not repeated in the recipe's list, add to list of ingredients to match for ranking
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

shopList = open("shoppingList.txt", "w")
shopList.writelines(url+"\n"+recipeName+" (Serves : "+str(recipeAmount)+")\n")
shopList.close()
recipe1 = open("recipe1.txt", "w")
recipe1.writelines(url+"\n"+recipeName+" (Serves : "+str(recipeAmount)+")\n")
recipe1.close()

recipe1 = open("recipe1.txt", "a")
shopList = open("shoppingList.txt", "a")
for x in rawKeyIngredients:
	shopList.write(x+"\n")
	recipe1.write(x+"\n")
shopList.close()
recipe1.close()

def getRecipe(number, cuisine):
	r2 = requests.get('https://api.edamam.com/search?q='+mainVeg+','+mainMeat+','+cuisine+'&app_id='+API_ID+'&app_key='+API_Key+'&from=0&to='+str(MaxAPIResults))
	data2 = r2.json()
	ranks = []
	keptRanks1 = []
	recipeRankList = []
	x = 0
	if(len(data2["hits"]) < 1):
		return
	for y in range(0, len(data2["hits"]) - 1): #MaxAPIResults):		#for each recipe in returned results from API search
		tempIngred = []
		ingredi = data2["hits"][y]["recipe"]["ingredients"]		#temp dictionary for extracting recipe ingredients
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
		ranks.append((rank/len(tempIngred)) * 100)

	for k in range(0,similarityThreshold):
		try:
			keptRanks1.append(ranks.index(max(ranks)))
			del ranks[ranks.index(max(ranks))] #removes highest rank to get new highest next time
		except:
			x = 0

	recipeRank = keptRanks1[random.randint(0,len(keptRanks1) - 1)]
	x = 0
	while((recipeRank in recipeRankList) or (x < len(keptRanks1))):
		recipeRank = keptRanks1[random.randint(0,len(keptRanks1) - 1)]
		x += 1
	recipeRankList.append(recipeRank)
	ingredi = data2["hits"][recipeRank]["recipe"]["ingredients"]
	url = data2["hits"][recipeRank]["recipe"]["url"]
	recipeName = data["hits"][recipeRank]["recipe"]["label"]
	recipeAmount = data["hits"][recipeRank]["recipe"]["yield"]

	formatIngredients = []
	x = 0
	for item in range(0, len(ingredi)):
		for key,value in ingredi[item].items():
			if(x % 2 == 0):
				if(not any(item in value.lower() for item in formatIngredients)):
					formatIngredients.append(value.lower())
			x+=1
	shopList = open("shoppingList.txt", "a")
	recipeNumber = "recipe"+str(number+1)+".txt"
	recipe = open(recipeNumber, "w")
	recipe.writelines(url+"\n"+recipeName+" (Serves : "+str(recipeAmount)+")\n")
	shopList.write("\n"+url+"\n"+recipeName+" (Serves : "+str(recipeAmount)+")\n")
	recipe.close()
	recipe = open(recipeNumber, "a")
	for x in formatIngredients:
		shopList.write(x+"\n")
		recipe.write(x+"\n")
	recipe.close()
	shopList.close()

if(mainMeat == "chicken"):
	cuisineType = chickenIngred
elif(mainMeat == "groundbeef"):
	cuisineType = groundbeefIngred
elif(mainMeat == "steak"):
	cuisineType = steakIngred
elif(mainMeat == "fish"):
	cuisineType = fishIngred
elif(mainMeat == "sausage"):
	cuisineType = sausageIngred
elif(mainMeat == "pork"):
	cuisineType = porkIngred
else:
	cuisineType = chickenIngred

for h in range(1, mealsToMake):
	temp = cuisineType[random.randint(0,len(cuisineType)-1)]
	while(temp in chosenCuisine):
		temp = cuisineType[random.randint(0,len(cuisineType)-1)]
	chosenCuisine.append(temp)
#	getRecipe(h, chosenCuisine[h-1])
f2 = open("alphabetizeShopping.txt","w")
f2.writelines("")
f2.close()

alphabetizedList = [] # list that contains all the ingredients of all the recipes for using python built-in sort() method on later

def alphebetizeShopping(recipe):
	x = 0
	tempFile = open(recipe)
	keyIngredients = []
	for line in tempFile:
		if(x>=2):
			temp = line.lower()		#convert to lowercase for easier matching with allIngredients.txt
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
				spaces = spaceOffset - len(tempWord)
				if(len(tempWord) >= spaceOffset):
					keyIngredients.append(tempWord+": "+temp)
				else:
					tempWord += (":"+(" "*spaces))
					keyIngredients.append(tempWord+temp)
					alphabetizedList.append(tempWord+temp)
				x += 1
		else:
			x += 1
	f1.close()

for i in range(0,mealsToMake):
	recipe = "recipe"+str(i+1)+".txt"
	alphebetizeShopping(recipe)

alphabetizedList.sort()
with open("alphabetizeShopping.txt", "w") as f:
	f.writelines("")
with open("alphabetizeShopping.txt","a") as afile:
	for each in alphabetizedList:
		afile.write(each)

print("\nDone!")
