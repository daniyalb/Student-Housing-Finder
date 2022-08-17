from operator import is_
from bs4 import BeautifulSoup
import requests

t1f = 'female'
t2f = 'girl'
t1sf = 'females'
t2sf = 'girls'
t1m = ' male'
t2m = 'boy'
t1sm = ' males'
t2sm = 'boys'
t3 = ' only'
t4 = ' student'
COMBOS_F = (t1f + t3, t2f + t3, t3 + t1f, t3 + t2f, t1sf + t3, t2sf + t3, t3 + t1sf,
             t3 + t2sf, t1f + t4, t1f, t2f)
COMBOS_M = (t1m + t3, t2m + t3, t3 + t1m, t3 + t2m, t1sm + t3, t2sm + t3, t3 + t1sm,
             t3 + t2sm, t1m + t4, t1m, t2m)             

#city = input('Which city would you like to search in? ')
#city = city.lower() TODO: Unhide this and delete next line
city = 'london'
max_price = input('What is the highest price you are willing to rent for? $')
max_price = int(max_price)
pets = ''
while not pets == 'y' and not pets == 'n':
    pets = input('Do you require your housing to be pet-friendly? (y/n): ')
furnished = ''
while not furnished == 'y' and not furnished == 'n':
    furnished = input('Would you want your housing to be furnished? (y/n): ')
female_only = ''
while not female_only == 'y' and not female_only == 'n':
    female_only = input('Would female only accomodations work for you? (y/n): ')
male_only = ''
while not male_only == 'y' and not male_only == 'n':
    male_only = input('Would male only accomodations work for you? (y/n): ')
print('')

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

def _check_included(info) -> bool:
    included = info.li.dl.dd.text
    if included == 'Yes':
        return True
    return False

def link_explorer(link: str) -> tuple:
    html_text = requests.get(link).text
    content = BeautifulSoup(html_text, 'lxml')

    holder = content.find_all('ul', class_='itemAttributeList-1090551278') 
    is_furnished = pets_allowed = 'unknown'
    for info in holder:
        if not info.li is None:
            name = info.li.dl.dt.text
            if name == 'Furnished':
                is_furnished = _check_included(info)
            else:
                pets_allowed = _check_included(info)

    location = content.find('span', class_='address-3617944557').text
    description = content.find('div', class_='descriptionContainer-231909819').div.p.text

    return (is_furnished, pets_allowed, location, description)

def check_gender_only(gender: str, title: str, description: str) -> bool:
    """ Checks if title or description contain any wording
    if the listing is for males or females only, then sees if user
    would be okay with those accomodations, returns
    True if compatible, returns False otherwise.
    """
    title = title.lower()
    description = description.lower()
    if gender == 'female':
        combos = COMBOS_F
    else:
        combos = COMBOS_M
    for combo in combos:
        if combo in title or combo in description:
            return True
    return False


url = url_city_adder(city)

html_text = requests.get(url).text
content = BeautifulSoup(html_text, 'lxml')
all_results = content.find('div', class_='container-results large-images').find_next()
ads = all_results.find_all('div', class_='search-item regular-ad')
listings = {}
number = 1
for ad in ads:
    price = ad.find('div', class_='price').text.strip()
    if price == 'Please Contact':
        continue
    else:
        price = price_formatter(price)
        if price > max_price:
            continue
    time = ad.find('span', class_='date-posted').text
    if not time[0] == '<':
        continue
    title_link = ad.find('div', class_='title').a
    link = 'https://www.kijiji.ca' + title_link['href']
    is_furnished, pets_allowed, location, description = link_explorer(link) # TODO: FIX PETS ALLOWED
    if pets == 'y' and (not pets_allowed or pets_allowed == 'unknown'):
        continue
    if furnished == 'y' and (not is_furnished or is_furnished == 'unknown'):
        continue
    title = title_link.text.strip()
    only_females = check_gender_only('female', title, description)
    only_males = check_gender_only('male', title, description)
    listings[number] = (price, time, link, is_furnished, pets_allowed, location, description, title, only_females, only_males)
    number += 1

for listing in listings:
    price, time, link, is_furnished, pets_allowed, location, description, title, only_females, only_males = listings[listing]
    print(title)
    print(f'Price: {price}')
    print(f'Posted: {time}')
    print(link)
    print(f'Furnished: {is_furnished}')
    print(f'Pets allowed: {pets_allowed}')
    print(location)
    print(f'ONLY FEMALES: {only_females}')
    print(f'ONLY MALES: {only_males}')
    print('----------------------------------------------------------------')
