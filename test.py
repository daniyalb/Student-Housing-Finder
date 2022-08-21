from operator import is_
from bs4 import BeautifulSoup
from datetime import datetime
import requests   


class Finder:
    """ The Finder class

        This class contains the methods used to search through Kijiji 
        listings using the filters provided in the attributes to this class.
        This class is also responsible for writing all of the results of the
        search into a txt file in order to display these results.

        === Public Attributes ===
        city:
             A string representing the city in which listings should be searched
        max_price:
             An integer representing the maximum price the user is willing to
             rent for
        pets:
             A boolean which indicates if the user would like pet-friendly 
             accomodations or not
        furnished:
             A boolean which indicates whether the user would like furnished
             accomodations or not
        female_only:
             A boolean representing whether the user would like accomodations
             that are female-only or not
        male_only:
             A boolean representing whether the user would like accomodations
             that are male-only or not
    """
    # === Private Attributes ===
    # _combos_f:
    #   A tuple that contains combinations of key words in the 
    #   title/description of the listings that would indicate
    #   that the listing is only looking for females
    # _combos_m:
    #   A tuple that contains combinations of key words in the 
    #   title/description of the listings that would indicate
    #   that the listing is only looking for males

    city: str
    max_price: int
    pets: bool
    furnished: bool
    female_only: bool
    male_only: bool
    
    def __init__(self, city: str, max_price: int, pets: bool, 
    furnished: bool, female_only: bool, male_only: bool) -> None:
        """ Initialize the attributes for this class
        """
        self.city = city
        self.max_price = max_price
        self.pets = pets
        self.furnished = furnished
        self.female_only = female_only
        self.male_only = male_only
        self._combos_f, self._combos_m = self._get_combos()
        self._listings = {}

    def _get_combos(self) -> tuple[tuple]:
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
        combos_f = (t1f + t3, t2f + t3, t3 + t1f, t3 + t2f, t1sf + t3, t2sf + t3, t3 + t1sf,
                    t3 + t2sf, t1f + t4, t1f, t2f)
        combos_m = (t1m + t3, t2m + t3, t3 + t1m, t3 + t2m, t1sm + t3, t2sm + t3, t3 + t1sm,
                    t3 + t2sm, t1m + t4, t1m, t2m)
        return combos_f, combos_m 

    def _url_city_adder(self) -> str:
        if self.city == 'mississauga / peel region':
            return 'https://www.kijiji.ca/b-for-rent/mississauga-peel-region/student/k0c30349001l1700276?rb=true&ad=offering'
        elif self.city == 'toronto':
            return 'https://www.kijiji.ca/b-for-rent/city-of-toronto/student/k0c30349001l1700273?rb=true&ad=offering'
        elif self.city == 'markham / york region':
            return 'https://www.kijiji.ca/b-for-rent/markham-york-region/student/k0c30349001l1700274?rb=true&ad=offering'
        elif self.city == 'oakville / halton region':
            return 'https://www.kijiji.ca/b-for-rent/oakville-halton-region/student/k0c30349001l1700277?rb=true&ad=offering'
        elif self.city == 'hamilton':
            return 'https://www.kijiji.ca/b-for-rent/hamilton/student/k0c30349001l80014?rb=true&ad=offering'
        elif self.city == 'guelph':
            return 'https://www.kijiji.ca/b-for-rent/guelph/student/k0c30349001l1700242?rb=true&ad=offering'
        elif self.city == 'kitchener / waterloo':
            return 'https://www.kijiji.ca/b-for-rent/kitchener-waterloo/student/k0c30349001l1700212?rb=true&ad=offering'
        elif self.city == 'oshawa / durham region':
            return 'https://www.kijiji.ca/b-for-rent/oshawa-durham-region/student/k0c30349001l1700275?rb=true&ad=offering'
        elif self.city == 'kingston':
            return 'https://www.kijiji.ca/b-for-rent/kingston-on/student/k0c30349001l1700183?rb=true&ad=offering'
        elif self.city == 'london':
            return 'https://www.kijiji.ca/b-for-rent/london/student/k0c30349001l1700214?rb=true&ad=offering'

    def _price_formatter(self, price: str) -> str:
        price = price[1:]
        price = price[:price.find('.')]
        price = price.replace(',', '')
        return int(price)

    def _check_included(self, info) -> str:
        included = info.li.dl.dd.text
        if included == 'Yes':
            return 'Yes'
        return 'No'

    def _link_explorer(self, link: str) -> tuple:
        html_text = requests.get(link).text
        content = BeautifulSoup(html_text, 'lxml')

        holder = content.find_all('ul', class_='itemAttributeList-1090551278') 
        is_furnished = pets_allowed = 'unknown'
        for info in holder:
            if not info.li is None:
                name = info.li.dl.dt.text
                if name == 'Furnished':
                    is_furnished = self._check_included(info)
                else:
                    pets_allowed = self._check_included(info)

        location = content.find('div', class_='locationContainer-2867112055')
        if location == None:
            location = 'Error'
        else:
            location = location.span.text
        description = content.find('div', class_='descriptionContainer-231909819')
        if description == None:
            description = 'Error'
        else:
            description = description.div.p.text

        return (is_furnished, pets_allowed, location, description)

    def _check_gender_only(self, gender: str, title: str, description: str) -> str:
        """ Checks if title or description contain any wording
        if the listing is for males or females only, then sees if user
        would be okay with those accomodations, returns
        'Yes' if compatible, returns 'No' otherwise.
        """
        title = title.lower()
        description = description.lower()
        if gender == 'female':
            combos = self._combos_f
        else:
            combos = self._combos_m
        for combo in combos:
            if combo in title or combo in description:
                return 'Yes'
        return 'No'

    def _record_results(self, listings: dict) -> tuple:
        now = datetime.now()
        date_time = now.strftime('%d|%m|%Y %H.%M.%S')

        with open(f'{date_time}.txt', 'a') as txt:
            i = 1
            for link in listings:
                price, time, is_furnished, pets_allowed, location, title, only_females, only_males = listings[link]

                txt.write(f'Listing #{i}:\n')
                txt.write(f'{title}\n')
                txt.write(f'Price: {price}\n')
                txt.write(f'Posted: {time}\n')
                txt.write(f'Link: {link}\n')
                txt.write(f'Furnished: {is_furnished}\n')
                txt.write(f'Pets Allowed: {pets_allowed}\n')
                txt.write(f'Location: {location}\n')
                txt.write(f'Only Females: {only_females}\n')
                txt.write(f'Only Males: {only_males}\n\n\n')
                i += 1

        return (len(listings), f'{date_time}.txt')

    def search(self) -> tuple:
        url = self._url_city_adder()

        html_text = requests.get(url).text
        content = BeautifulSoup(html_text, 'lxml')
        all_results = content.find('div', class_='container-results large-images').find_next()
        ads = all_results.find_all('div', class_='search-item regular-ad')
        temp_listings = {}
        for ad in ads:
            title_link = ad.find('div', class_='title').a
            link = 'https://www.kijiji.ca' + title_link['href']
            if link in self._listings:
                continue
            price = ad.find('div', class_='price').text.strip()
            if price == 'Please Contact' or price == 'Swap / Trade':
                continue
            else:
                price = self._price_formatter(price)
                if price > self.max_price:
                    continue
            time = ad.find('span', class_='date-posted').text
            if not time[0] == '<':
                continue
            is_furnished, pets_allowed, location, description = self._link_explorer(link)
            if self.pets and (pets_allowed == 'No' or pets_allowed == 'unknown'):
                continue
            if self.furnished and (is_furnished == 'No' or is_furnished == 'unknown'):
                continue
            title = title_link.text.strip()
            only_females = self._check_gender_only('female', title, description) # TODO: add filtering for these results
            only_males = self._check_gender_only('male', title, description)
            self._listings[link] = (price, time, is_furnished, pets_allowed, location, title, only_females, only_males)
            temp_listings[link] = self._listings[link]
        return self._record_results(temp_listings)


if __name__ == '__main__':
    city = 'mississauga / peel region'
    max_price = 1500
    pets = False
    furnished = False
    female_only = False
    male_only = False
    find = Finder(city, max_price, pets, furnished, female_only, male_only)
    find.search()


#city = input('Which city would you like to search in? ')
#city = city.lower() TODO: Unhide this and delete next line

"""
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

def _check_included(info) -> str:
    included = info.li.dl.dd.text
    if included == 'Yes':
        return 'Yes'
    return 'No'

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

def check_gender_only(gender: str, title: str, description: str) -> str:
    title = title.lower()
    description = description.lower()
    if gender == 'female':
        combos = COMBOS_F
    else:
        combos = COMBOS_M
    for combo in combos:
        if combo in title or combo in description:
            return 'Yes'
    return 'No'


url = url_city_adder(city)

html_text = requests.get(url).text
content = BeautifulSoup(html_text, 'lxml')
all_results = content.find('div', class_='container-results large-images').find_next()
ads = all_results.find_all('div', class_='search-item regular-ad')
listings = {}
number = 1
for ad in ads:
    price = ad.find('div', class_='price').text.strip()
    if price == 'Please Contact' or price == 'Swap / Trade':
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
    is_furnished, pets_allowed, location, description = link_explorer(link)
    if pets == 'y' and (pets_allowed == 'No' or pets_allowed == 'unknown'):
        continue
    if furnished == 'y' and (is_furnished == 'No' or is_furnished == 'unknown'):
        continue
    title = title_link.text.strip()
    only_females = check_gender_only('female', title, description)
    only_males = check_gender_only('male', title, description)
    listings[number] = (price, time, link, is_furnished, pets_allowed, location, description, title, only_females, only_males)
    number += 1

with open('Results.txt', 'a') as txt:
    i = 1
    for listing in listings:
        price, time, link, is_furnished, pets_allowed, location, description, title, only_females, only_males = listings[listing]

        txt.write(f'Listing #{i}:\n')
        txt.write(f'{title}\n')
        txt.write(f'Price: {price}\n')
        txt.write(f'Posted: {time}\n')
        txt.write(f'Link: {link}\n')
        txt.write(f'Furnished: {is_furnished}\n')
        txt.write(f'Pets Allowed: {pets_allowed}\n')
        txt.write(f'{location}\n')
        txt.write(f'Only Females: {only_females}\n')
        txt.write(f'Only Males: {only_males}\n\n\n')
        i += 1
"""