from bs4 import BeautifulSoup
import requests
"""
city = input('Which city would you like to search in? ')
city = city.lower()
max_price = input('What is the highest price you are willing to rent for? ')
pets = ''
while not pets == 'y' and not pets == 'n':
    pets = input('Do you require your housing to be pet-friendly? (y/n): ')
female_only = ''
while not female_only == 'y' and not female_only == 'n':
    female_only = input('Would you like housing that is female only? (y/n): ')
shared = ''
while not shared == 'y' and not shared == 'n':
    shared = input('Would you be okay with shared accomodations? (y/n): ')
furnished = ''
while not furnished == 'y' and not furnished == 'n':
    furnished = input('Would you want your housing to be furnished? (y/n): ')
"""
city = 'mississauga / peel region'

def url_city_adder(city: str) -> str:
    if city == 'mississauga / peel region':
        return 'https://www.kijiji.ca/b-for-rent/mississauga-peel-region/student/k0c30349001l1700276?rb=true&ad=offering'
    elif city == 'toronto':
        return 'https://www.kijiji.ca/b-for-rent/city-of-toronto/student/k0c30349001l1700273?rb=true&ad=offering'
    elif city == 'markham / york region':
        return 'https://www.kijiji.ca/b-for-rent/markham-york-region/student/k0c30349001l1700274?rb=true&ad=offering'
    elif city == 'oakville / halton region':
        return 'https://www.kijiji.ca/b-for-rent/oakville-halton-region/student/k0c30349001l1700277?rb=true&ad=offering'
    elif city == 'hamilton':
        return 'https://www.kijiji.ca/b-for-rent/hamilton/student/k0c30349001l80014?rb=true&ad=offering'
    elif city == 'guelph':
        return 'https://www.kijiji.ca/b-for-rent/guelph/student/k0c30349001l1700242?rb=true&ad=offering'
    elif city == 'kitchener / waterloo':
        return 'https://www.kijiji.ca/b-for-rent/kitchener-waterloo/student/k0c30349001l1700212?rb=true&ad=offering'
    elif city == 'oshawa / durham region':
        return 'https://www.kijiji.ca/b-for-rent/oshawa-durham-region/student/k0c30349001l1700275?rb=true&ad=offering'
    elif city == 'kingston':
        return 'https://www.kijiji.ca/b-for-rent/kingston-on/student/k0c30349001l1700183?rb=true&ad=offering'
    elif city == 'london':
        return 'https://www.kijiji.ca/b-for-rent/london/student/k0c30349001l1700214?rb=true&ad=offering'

def price_formatter(price: str) -> str:
    price = price[1:]
    price = price[:price.find('.')]
    price = price.replace(',', '')
    return int(price)

def link_explorer(link: str) -> tuple:
    html_text = requests.get(link).text
    content = BeautifulSoup(html_text, 'lxml')
    furnished = content.find('dl', class_='itemAttribute-3080139557')
    if not furnished is None and not furnished.dd.text == 'No':
        is_furnished = True
    else:
        is_furnished = False
    location = content.find('span', class_='address-3617944557').text
    description = content.find('div', class_='descriptionContainer-231909819').div.p.text
    return (is_furnished, location, description)


url = url_city_adder(city)

html_text = requests.get(url).text
content = BeautifulSoup(html_text, 'lxml')
all_results = content.find('div', class_='container-results large-images').find_next()
ads = all_results.find_all('div', class_='search-item regular-ad')
listings = {}
for ad in ads:
    price = ad.find('div', class_='price').text.strip()
    if price == 'Please Contact':
        continue
    else:
        price = price_formatter(price)
        print(price)
    time = ad.find('span', class_='date-posted').text
    if not time[0] == '<':
        continue
    print(time)
    title_link = ad.find('div', class_='title').a
    link = 'https://www.kijiji.ca' + title_link['href']
    print(link)
    is_furnished, location, description = link_explorer(link)
    print(is_furnished)
    print(location)
    print('****************************************************************')
    print(description)
    print('****************************************************************')
    title = title_link.text.strip()
    print(title)
    print('----------------------------------------------------------------')