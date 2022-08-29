from operator import is_
from bs4 import BeautifulSoup
from datetime import datetime
from os.path import exists
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
        self._links = self._get_links()

    def _get_combos(self) -> tuple[tuple, tuple]:
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
        return (combos_f, combos_m)

    def _get_links(self) -> dict[str, None]:
        links_dict = {}
        if exists('Program Files/links.txt'):
            with open('Program Files/links.txt', 'r') as txt:
                links = txt.readlines()
                for link in links:
                    link = link.replace('\n', '')
                    links_dict[link] = None
        return links_dict

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

    def _record_links(self, listings: dict) -> None:
        with open('Program Files/links.txt', 'a') as txt:
            for link in listings:
                txt.write(f'{link}\n')
                self._links[link] = None
            

    def _record_results(self, listings: dict) -> tuple:
        if len(listings) == 0:
            return (0, '')

        now = datetime.now()
        date_time = now.strftime('%d|%m|%Y %H.%M.%S')

        with open(f'Results/{date_time}.txt', 'a') as txt:
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

        self._record_links(listings)

        return (len(listings), f'{date_time}.txt')

    def search(self) -> tuple:
        url = self._url_city_adder()

        html_text = requests.get(url).text
        content = BeautifulSoup(html_text, 'lxml')
        all_results = content.find('div', class_='container-results large-images').find_next()
        ads = all_results.find_all('div', class_='search-item regular-ad')
        listings = {}
        for ad in ads:
            title_link = ad.find('div', class_='title').a
            link = 'https://www.kijiji.ca' + title_link['href']
            if link in self._links:
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
            listings[link] = (price, time, is_furnished, pets_allowed, location, title, only_females, only_males)
        return self._record_results(listings)


if __name__ == '__main__':
    city = 'mississauga / peel region'
    max_price = 1500
    pets = False
    furnished = False
    female_only = False
    male_only = False
    find = Finder(city, max_price, pets, furnished, female_only, male_only)
    find.search()