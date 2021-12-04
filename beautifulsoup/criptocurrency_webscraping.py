import requests
from bs4 import BeautifulSoup as bs

url = 'https://coinmarketcap.com/'
html = requests.get(url)
html = html.text
soup3 = bs(html, 'html.parser')
# the table with the criptocurrencies and their data is located in a tbody html tag
table = soup3.tbody
rows = table.contents
# currency name and value are inside the 3rd and 4th td tags inside each tr tag
currencies = {}

# the 10 first currencies have their names and values inside p tags
for row in rows[:10]:
    td_name = row.contents[2]
    td_name_p_tags = td_name.find_all('p')
    coin_name, coin_symbol = td_name_p_tags[0].string, td_name_p_tags[1].string
    coin_value = row.contents[3].span.string
    # euro conversion
    # as of 4th December, 2021: 1 USD = 0.8839375 €
    coin_value = coin_value.replace(',','').replace('$','')
    CONVERSION = 0.8839375
    coin_value_dollars = float(coin_value)
    coin_value_euro = coin_value_dollars * CONVERSION
    coin_value = {'USD': coin_value_dollars, 'Euro': coin_value_euro}
    # add the currency to the dictionary
    currencies[coin_name] = [coin_name, coin_symbol, coin_value]
    #print(f'Currency: {coin_name}, {coin_symbol}. Current value: {coin_value}')

# the rest of currencies have their names and values inside span tags
# currency name, symbol and value are located in 3rd td inside tr tag
# inside the td tag, they are inside span tags
for row in rows[10:]:
    td_name = row.contents[2]
    td_name_spans = td_name.find_all('span')
    coin_name, coin_symbol = td_name_spans[1].string, td_name_spans[2].string
    # <span>$<!-- -->92.85</span></td>
    # span with currency value has a comment inside
    coin_value = row.contents[3].span.contents
    # remove the comment in position 1 --> ['$', ' ', '0.18']
    coin_value.pop(1)
    # join the dollar sign and value
    #coin_value  = ''.join(coin_value)

    # euro conversion
    # as of 4th December, 2021: 1 USD = 0.8839375 €
    CONVERSION = 0.8839375
    coin_value_dollars = float(coin_value[1])
    coin_value_euro = coin_value_dollars * CONVERSION
    coin_value = {'USD': coin_value_dollars, 'Euro': coin_value_euro}  
    
    currencies[coin_name] = [coin_name, coin_symbol, coin_value]
    #print(f'Currency: {coin_name}, {coin_symbol}. Current value: {coin_value}')

for coin, info in currencies.items():
    print(f'{coin:<20}\t${info[2]["USD"]:<10.2f}\t{info[2]["Euro"]:.2f} €')