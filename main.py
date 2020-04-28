import requests
import json
import random

MaxAPIResults = 100 #Determined by subscribed tier
filenameOfAPI_Key = "API_Key"
measurementUnits = ['teaspoons','tablespoons','cups','containers','packets','bags','quarts','pounds','cans','bottles',
		'pints','packages','ounces','jars','heads','gallons','drops','bars','boxes','pinches',
		'bunches','layers','slices','links','bulbs','stalks','squares','sprigs',
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

dairyIngredients = ['buttermilk', 'cottage', 'cream', 'creamer', 'creamy', 'creme', 'ghee', 'half-and-half', 
		'milk', 'yogurt']
cheeses = ['bocconcini', 'mozzarella', 'gouda', 'swiss', 'brie', 'cheddar']
meats = ['bacon', 'beefs', 'burgers', 'chorizo', 'frankfurters', 'giblets', 'ham', 'lambs', 'livers', 
		'meatballs', 'meatloaves', 'meats', 'mignon', 'mincemeat', 'pepperonis', "porks", 
		'prosciutto', 'ribs', 'roasts', 'sausages', 'sirloin', 'tripe', 'veal', 'venison', 'kielbasas',
		'liverwurst', 'wieners', 'cotechino', 'linguica', 'pastrami', 'sauerbraten',
		'picadillo', 'carcass', 'brains', 'mortadella', 'rounds', 'sweetbread', 
		'embutido', 'hash', 'broil', 'brisket', 'franks', 'pigs', 'chops', 'scrapple', 
		'barbeque', 'spareribs']
poultry = ['bologna', 'bratwursts', 'chicken', 'ducks', 'goose', 'pollo', 'salami', 'turkey', 'wings']
fish = ['albacores', 'bass', 'catfish', 'cods', 'fish', 'flounder', 'grouper', 'haddock', 'halibut', 'mahi',
		'monkfish', 'salmon', 'shark', 'snapper', 'sole', 'swordfishes', 'trouts', 'tunas', 'bluefish',
		'bonito', 'rockfish', 'mackerel', 'naruto', 'drum', 'marlin', 'tilapia', 'carp', 'kingfish',
		'mullets', 'whitefish', 'kippers', 'torsk', 'saltfish']
seafoods = ['anchovies', 'calamaris', 'clams', 'crabs', 'crabmeat', 'crawfish', 'lobsters', 'mussels', 
		'oysters', 'prawns', 'scallops', 'seafood', 'shrimps', 'squids', 'snails', 'shellfish', 'caviar']
mainProteins = ['beans', 'chickpeas', 'nuts', 'seeds', 'tofu', 'whey', 'buckwheat', 'soybeans',
		'soy', 'tempeh', 'lentils', 'masoor', 'gluten', 'pine', 'falafel', 'portobello']
fruits = ['apples', 'apricots', 'bananas', 'blackberries', 'blueberries', 'cantaloupe', 'cherries', 'citrons', 
		'citrus', 'coconuts', 'cranberries', 'currants', 'elderberries', 'figs', 'fruitcakes', 'fruits', 
		'gooseberries', 'grapefruit', 'grapes', 'guava', 'honeydew', 'huckleberries', 'kiwis','kumquats', 
		'lemonade', 'lemons', 'limes', 'mangoes', 'marrons', 'mincemeat', 'mulberries', 'nectarines', 'oranges', 
		'papayas', 'peaches', 'pears', 'persimmon', 'persimmons', 'pineapples', 'plums', 'prunes', 'raisins', 
		'raspberries', 'slushies', 'smoothies', 'sorrel', 'strawberries', 'tangerines', 'watermelons', 'yuzu',
		'lingonberries', 'plantains', 'juniper', 'lingonberries', 'pomegranates', 'serviceberries', 
		'zinfandel', 'lychees', 'carambola', 'uvas']
vegetables = ['artichokes', 'arugula', 'asparagus', 'avocados', 'bamboo', 'beets', 'broccoli', 'cabbage', 
		'calzones', 'carrots', 'cauliflower', 'celery', 'chilis', 'chives', 'choy', 'cilantro', 'coleslaw', 
		'coriander', 'cucumber', 'cucumbers', 'dates', 'eggplant', 'eggplants', 'endive', 'escarole', 
		'galangal', 'haystacks', 'jicama', 'kale', 'kohlrabi', 'kucai', 'leeks', 'lettuce', 
		'mushrooms', 'okra', 'olives', 'onions', 'parsley', 'parsnips', 'peas', 'peppers', 'pickles', 
		'pizzas', 'potatoes', 'pumpkins', 'radishes', 'rutabagas', 'salad', 'sauerkraut', 'shallots', 'slaws', 
		'spinach', 'sprouts', 'squash', 'tamarind', 'taros', 'tomatillo', 'tomatillos', 'tomatoes', 'turnips', 
		'vegetable', 'vegetables', 'veggies', 'watercress', 'yams', 'zucchinis', 'chervil', 'daikon', 'iceberg',
		'nopales', 'pimentos', 'radicchio', 'karengo', 'nori', 'succotash', 'truffle', 'chard', 'fries', 'leaves',
		'browns', 'romain', 'palm', 'sorghum', 'aloo', 'haricots', 'caprese', 'salata', 'shiitake']
sauces = ['alfredo', 'applesauce', 'chutney', 'cannoli', 'dips', 'guacamole', 'hummus', 'paste', 'spreads',
		'tahini', 'tzatziki', 'denjang', 'salsa', 'sauce', 'tapenade', 'coating', 'teriyaki',
		'aioli', 'checca', 'amatriciana', 'ragu', 'marinara', 'soy']
condiments = ['dressing', 'jam', 'ketchup', 'marinade', 'marjoram', 'mayonnaise', 'mirin', 'mustard', 
		'pesto', 'relish', 'shoyu', 'tamari', 'vinaigrette', 'gochujang']
soups = ['broth', 'chowder', 'dashi', 'soup', 'stew', 'jambalaya', 'gumbo', 'gazpacho', 'goulash', 'pho',
		'slumgullion', 'cioppino', 'minestrone']
nuts = ['almonds', 'butternuts', 'candlenuts', 'cashews', 'chestnuts', 'hazelnuts', 'macadamia', 'nuts', 
		'peanuts', 'pecans', 'pistachios', 'walnuts', 'nuts']
alcoholicIngredients = ['anisette', 'beer', 'bitters', 'bourbon', 'brandy', 'cacao', 'chambord', 'champagne', 
		'cognac', 'eggnog', 'kirsch', 'kirschwasser', 'liqueur', 'rum', 'schnapps', 'sherry', 'ale',
		'spritz', 'tequila', 'vermouth', 'vodka', 'whiskey', 'wine', 'campari', 'alcohol', 'absinthe',
		'cachaca', 'liquor', 'cointreau', 'curacao', 'sake', 'sec', 'calvados', 'galliano', 'lillet',
		'margaritas', 'coladas', 'negroni', 'mojitos', 'mimosas', 'bahama', 'slammer', 'sauvignon', 'chablis',
		'martinis', 'tequinis', 'spritzs', 'cosmopolitan', 'hurricanes', 'sangria', 'sex', "shaggy's", 'nipples',
		'stoli']
spices = ['allspice', 'anise', 'arrowroot', 'basil', 'bay', 'capers', 'caraway', 'cardamom', 'cassava', 
		'cayenne', 'chocolate', 'cilantro', 'cinnamon', 'cloves', 'cocoa', 'coriander', 'cumin', 'dill', 
		'fennel', 'flax', 'garlic', 'ginger', 'herbs', 'kalonji', 'mace', 'masala', 'miso', 'monosodium', 
		'nutmeg', 'oregano', 'paprika', 'pepper', 'peppercorns', 'pimento', 'poppy', 'poppyseed', 
		'powder','rhubarb', 'rosemary', 'saffron', 'sage', 'salt', 'savory', 'seasoning', 'sesame', 'spices', 
		'sunflower', 'tarragon', 'thyme', 'turmeric', 'vanilla', 'watercress', 'spearmint', 'comfort']
spicy = ['angelica', 'dijon', 'horseradish', 'jerk', 'wasabi', 'spicy']
hotPeppers = ['jalapenos', 'pepperoncinis', 'chiles']
grains = ['bagels', 'baguettes', 'barley', 'biscuits', 'bran', 'bread', 'buns', 'cereal', 'corn', 'cornbread',
		'cornstarch', 'couscous', 'crackers', 'croutons', 'crusts', 'dough', 'granola', 'hominy', 'kasha', 
		'masa', 'matzo', 'millet', 'muffins', 'oats', 'pitas', 'popcorn', 'pretzels', 'quinoa', 'rice', 'rolls', 
		'shortbread', 'sourdough', 'stuffing', 'tapioca', 'toasts', 'tortillas', 'wheat', 'kaiser', 'cornmeal',
		'breadcrumbs', 'graham', 'bulgur', 'farina', 'oatmeal', 'croissants', 'polenta', 'grits', 'pumpernickel',
		'sago', 'seitan', 'grains', 'taters', 'risotto', 'shells', 'amarettini', 'mochi', 'cornflakes', 'pilaf',
		'puppies']
pastas = ['farfalle', 'fettuccine', 'lasagnas', 'linguine', 'mac', 'macaroni', 'manicotti', 'noodles', 'pasta',
		'farfel', 'vermicelli', 'tagliatelle', 'cannelloni', 'penne']
cookingLiquids = ['oil', 'vinegar', 'water', 'snow', 'ice']
bakingIngredients = ['ammonia', 'baking', 'eggs', 'flour', 'margarine', 'yeast', 'bisquick®']
cookingFats = ['butter', 'gelatin', 'gravy', 'lard', 'lecithin', 'ovalette', 'shortening', 'xanthan', 'suet']
extras = ['carnations', 'coloring', 'dust', 'flowers', 'lilies', 'spray', 'toppings', 'drippings', 'powdered',]
flavorings = ['extract', 'flavorings', 'mint', 'pandan', 'hickory', 'flavored', 'mesquite', 'wood',
		'hardwood']

# words with succeeding noun ("milk" or "cake")
nonDairyMilks = ['almond', 'soy', 'coconut']


keyIngredients = []

#--This block gets API key from PRIVATE file--#
API_file = open(filenameOfAPI_Key,'r')
API_ID = API_file.readline()[:-1]
API_Key = API_file.readline()[:-1]
API_file.close()
#r = requests.get('https://api.edamam.com/search?q=broccoli,chicken&app_id=' + API_ID + '&app_key=' + API_Key + '&from=0&to=100')
#data = r.json()

##--use this til final run--##
#data contains all recipes returned
with open("this.json") as f:
	data = json.load(f)

#--sets the seed for random start of 1st recipe to match--#
start = random.randint(0,MaxAPIResults - 1)

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
			keyIngredients.append(value)
		x+=1

#--Put key ingredients in list to parse recipes for matches--#
for each in keyIngredients:
	print(each)
