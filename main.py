'''
Sites I used:
'''

# https://www.youtube.com/watch?v=kCggyi_7pHg
# https://support.demandbase.com/hc/en-us/articles/205180803-Checking-the-API-Response-with-your-Browser#h_ceb239f5-4c35-4cb5-bea6-f62e785fd802

'''
Optinals URLS from Inspect -> network search (takem from "request URL"
'''
# Request URL - wss://api.livechatinc.com/v3.3/customer/rtm/ws?license_id=1083322
# https://www.10bis.co.il/NextApi/searchRestaurants?shoppingCartGuid=87942b52-261f-44ab-809c-b2663ec7d499&culture=he-IL&uiCulture=en&isMobileDevice=false&timestamp=1637138600619&deliveryMethod=delivery&cityName=Tel+Aviv-Yafo&streetName=Kibbutz+Galuyot+Road&houseNumber=917&latitude=32.0468378&longitude=34.786768&cityId=24&streetId=8175&isBigCity=true&addressKey=24-8175-917&locationType=residential&phone01=0506948960
# https://redirect.telepay.co.il
# https://www.10bis.co.il/NextApi/searchRestaurants?shoppingCartGuid=87942b52-261f-44ab-809c-b2663ec7d499&culture=he-IL&uiCulture=en&isMobileDevice=false&timestamp=1637138600619&deliveryMethod=delivery&cityName=Tel+Aviv-Yafo&streetName=Kibbutz+Galuyot+Road&houseNumber=917&latitude=32.0468378&longitude=34.786768&cityId=24&streetId=8175&isBigCity=true&addressKey=24-8175-917&locationType=residential&phone01=0506948960
# https://secure.livechatinc.com/customer/action/open_chat?license_id=1083322&group=9&embedded=1&widget_version=3&unique_groups=0
# https://www.10bis.co.il/NextApi/GetUserAddresses
# https://api.livechatinc.com/v3.3/customer/action/get_localization?license_id=1083322&version=d2add6860f3fd6ecfd82d77932ff9233_892271516b8eefb1cb715c82d5206ff2&language=he&group_id=9&jsonp=__lc_localization


from fastapi import FastAPI
from pydantic import BaseModel
import json
import requests

app = FastAPI()

'''
DATA EXPLORATION - here my goal is first to understand the data strusture and where in data I can get
answers to the question I have.
Trying to understand, type and structure of given data
'''


def internalUseDataEx():
    response = requests.get(
        'https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup')
    # print(dir(response))
    # print(help(response))
    '''
    Conclusions:
    What's intresting found under "data"
    '''
    j = response.json()
    # print(response.json())
    # print(j.keys())
    # print(j['Data'].keys())
    # print(j['ShoppingCartGuid'])
    # rint(j['Data']['categoriesList'])
    # print(type(j['Data']['categoriesList']))
    # print(len(j['Data']['categoriesList']))
    # for i in range(len(j['Data']['categoriesList'])):
    #     if j['Data']['categoriesList'][i]['categoryName'] == 'Drinks':
    #         for k in range(len(j['Data']['categoriesList'][i]['dishList'])):
    #             # print(j['Data']['categoriesList'][i]['dishList'][k])
    #             # print(type(j['Data']['categoriesList'][i]['dishList'][k]))
    #             DrinkDict = {k: v for k, v in j['Data']['categoriesList'][i]['dishList'][k].items() if
    #                          k in {'dishId', 'dishName', 'dishDescription', 'dishPrice'}}
    #             print(DrinkDict)

    # out_put_drinks = j['Data']['categoriesList'][i]['dishList']
    # DrinkDict = {k: v for k, v in out_put_drinks.items() if k in {'dishId','dishName','dishDescription','dishPrice'}}
    # print(DrinkDict)
    # print(j['Data']['categoriesList'][i])
    # print(type(j['Data']['categoriesList'][i]))
    # print(j['Data']['categoriesList'][i].keys())
    #
    # print(j['Data']['categoriesList'][i]['categoryName'])
    # print((j['Data']['categoriesList'][i]['categoryName']))

    '''
    Conclusions:
    The Json strusture in drill down folding data - where in this particular place the i is caputre the information about the
    category name - the list holds dicts - in each dict there is a diffrent category ID
    '''


internalUseDataEx()
Drinks_DB = []
Desserts_DB = []
Pizzas_DB = []
orderDB = []

response = requests.get('https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup')
j = response.json()

'''
This class will represent a Restaurant order contains
list of Drinks, Desserts and pizzas given by their ID
'''


class RestaurantOrder(BaseModel):
    Drinks: list
    Pizzas: list
    Desserts: list



def get_generic(type, specific=None):
    '''
    This function is generic function used to return all the items in the resturant belong to specific type (Pizza, Drinks, etc)
    Morover - useing specific we can get specific item (by his id) belong to specific type.
    :param type: The type of the item (Pizzas, Drinks, Desserts)
    :param specific: not require, if given - the id of the item
    :return: list contain a dict for each item with thw required data (dishId, dishName, dishDescription, dishPrice)
    '''
    re = []
    for i in range(len(j['Data']['categoriesList'])):
        if j['Data']['categoriesList'][i]['categoryName'] == type:
            for l in range(len(j['Data']['categoriesList'][i]['dishList'])):
                d = {k: v for k, v in j['Data']['categoriesList'][i]['dishList'][l].items() if
                     k in {'dishId', 'dishName', 'dishDescription', 'dishPrice'}}
                if not specific:
                    re.append(d)
                else:
                    if specific == d['dishId']:
                        re.append(d)
    return re

## http://127.0.0.1:8000/docs
## http://127.0.0.1:8000/
@app.get('/drinks')
def get_Drinks():
    return json.dumps(get_generic('Drinks'))


@app.get('/drinks/{drink_id}')
def get_SpecificDrink(drink_id: int):
    return json.dumps(get_generic('Drinks', drink_id))


@app.get('/pizzas')
def get_Pizzas():
    return json.dumps(get_generic('Pizzas'))


@app.get('/pizzas{pizza_id}')
def get_SpecificPizza(pizza_id: int):
    return json.dumps(get_generic('Pizzas', pizza_id))


@app.get('/desserts')
def get_Desserts():
    return json.dumps(get_generic('Desserts'))


@app.get('/desserts{dessert_id}')
def get_SpecificDessert(dessert_id: int):
    return json.dumps(get_generic('Desserts', dessert_id))


@app.post('/order')
def create_order(order: RestaurantOrder):
    total = 0
    for d in order.Drinks:
        re = get_generic('Drinks',int(d))
        if re:
            total += int(re[0]["dishPrice"])

    for p in order.Pizzas:
        re = get_generic('Pizzas', int(p))
        if re:
            total += int(re[0]["dishPrice"])

    for de in order.Desserts:
        re = get_generic('Desserts', int(de))
        if re:
            total += int(re[0]["dishPrice"])

    return total

'''
Test create_order
'''
#a = RestaurantOrder(Drinks=[2055846,2055838],Pizzas=[2055830,2055833],Desserts =[2055835])
#print(create_order(a))