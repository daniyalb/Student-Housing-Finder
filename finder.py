from bs4 import BeautifulSoup
from datetime import datetime
from os.path import exists
import requests


def get_combos() -> tuple[tuple, tuple]:
    """ Generate all combinations of gendered keywords that could appear
    in the title or description of listings specifying if the poster
    is only looking for tenants of a certain gender
    """
    t1f = 'female'
    t2f = 'girl'
    t3f = 'woman'
    t1sf = 'females'
    t2sf = 'girls'
    t3sf = 'women'
    t1m = ' male'
    t2m = 'boy'
    t3m = ' man'
    t1sm = ' males'
    t2sm = 'boys'
    t3sm = ' men'
    t3 = ' only'
    t4 = ' student'
    combos_f = (t1f + t3, t2f + t3, t3f + t3, t3 + t1f, t3 + t2f, t3 + t3f,
                t1sf + t3, t2sf + t3, t3sf + t3, t3 + t1sf, t3 + t2sf,
                t3 + t3sf, t1f + t4, t1f, t2f, t3f)
    combos_m = (t1m + t3, t2m + t3, t3m + t3, t3 + t1m, t3 + t2m, t3 + t3m,
                t1sm + t3, t2sm + t3, t3sm + t3, t3 + t1sm, t3 + t2sm,
                t3 + t3sm, t1m + t4, t1m, t2m, t3m)
    return combos_f, combos_m


def price_formatter(price: str) -> int:
    """ Format the <price> so that it does not contain any dollar signs,
    decimals, or commas and return the price as an integer"""
    price = price[1:]
    price = price[:price.find('.')]
    price = price.replace(',', '')
    return int(price)


def check_included(info) -> str:
    """ Check if the listing says the accommodation is furnished or
    allows for pets, as specified in the container <info>, return
    'Yes' if it is, and 'No' otherwise
    """
    included = info.li.dl.dd.text
    if included == 'Yes':
        return 'Yes'
    return 'No'


def get_links() -> dict[str, None]:
    """ Read the links.txt file to generate a dictionary of all the URLs
    of listings that have already been searched and set the URL string
    as the key of the dictionary
    """
    links_dict = {}
    if exists('Program Files/links.txt'):
        with open('Program Files/links.txt', 'r') as txt:
            links = txt.readlines()
            for link in links:
                link = link.replace('\n', '')
                links_dict[link] = None
    return links_dict


def link_explorer(link: str) -> tuple:
    """ Get the HTML information of the listing's web page given by the
    URL <link> and determine if it's furnished, allows pets, its
    location, and description
    """
    html_text = requests.get(link).text
    content = BeautifulSoup(html_text, 'lxml')

    holder = content.find_all('ul', class_='itemAttributeList-1090551278')
    is_furnished = pets_allowed = 'unknown'
    for info in holder:
        if info.li is not None:
            name = info.li.dl.dt.text
            if name == 'Furnished':
                is_furnished = check_included(info)
            else:
                pets_allowed = check_included(info)

    location = content.find('div', class_='locationContainer-2867112055')
    try:
        location = location.span.text
    except AttributeError:
        location = 'Error'
    description = content.find('div',
                               class_='descriptionContainer-231909819')
    try:
        description = description.div.p.text
    except AttributeError:
        description = 'Error'

    return is_furnished, pets_allowed, location, description


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
    # _links:
    #   A dictionary that has strings as keys which are URLs of
    #   listings that have already been searched

    city: str
    max_price: int
    pets: bool
    furnished: bool
    female_only: bool
    male_only: bool
    _combos_f: tuple
    _combos_m: tuple
    _links: dict

    def __init__(self, city: str, max_price: int, pets: bool, furnished: bool,
                 female_only: bool, male_only: bool) -> None:
        """ Initialize the filters for this Finder instance along
        with the possible gender combinations and URLs of all sites
        that have been visited
        """
        self.city = city
        self.max_price = max_price
        self.pets = pets
        self.furnished = furnished
        self.female_only = female_only
        self.male_only = male_only
        self._combos_f, self._combos_m = get_combos()
        self._links = get_links()

    def _url_city_adder(self) -> str:
        """ Return the URL for the kijiji.ca search that matches the city
            specified in <self.city>
        """
        leading = 'https://www.kijiji.ca/b-for-rent/'
        ending = '?rb=true&ad=offering'
        if self.city == 'Mississauga / Peel Region':
            return leading + \
                   'mississauga-peel-region/student/k0c30349001l1700276' + \
                   ending
        elif self.city == 'Toronto':
            return leading + \
                   'city-of-toronto/student/k0c30349001l1700273' + ending
        elif self.city == 'Markham / York Region':
            return leading + 'markham-york-region/student/k0c30349001l1700274' \
                   + ending
        elif self.city == 'Oakville / Halton Region':
            return leading + \
                   'oakville-halton-region/student/k0c30349001l1700277' + ending
        elif self.city == 'Hamilton':
            return leading + 'hamilton/student/k0c30349001l80014' + ending
        elif self.city == 'Guelph':
            return leading + 'guelph/student/k0c30349001l1700242' + ending
        elif self.city == 'Kitchener / Waterloo':
            return leading + 'kitchener-waterloo/student/k0c30349001l1700212' \
                   + ending
        elif self.city == 'Oshawa / Durham Region':
            return leading + 'oshawa-durham-region/student/k0c30349001l1700275'\
                   + ending
        elif self.city == 'Kingston':
            return leading + 'kingston-on/student/k0c30349001l1700183' + ending
        elif self.city == 'London':
            return leading + 'london/student/k0c30349001l1700214' + ending

    def _check_gender_only(self, gender: str, title: str, description: str) \
            -> str:
        """ Retrieves the correct keyword combinations based on <gender>,
         then Checks if <title> or <description> contain any wording
        if the listing is for males or females only, returns a string
        specifying 'Yes' if it does, and 'No' otherwise
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
        """ Write all the URLs found in the <listings> dictionary to
        links.txt so that these listings are ignored when a search
        is performed again
        """
        with open('Program Files/links.txt', 'a') as txt:
            for link in listings:
                txt.write(f'{link}\n')
                self._links[link] = None

    def _record_results(self, listings: dict) -> tuple:
        """ Record the results found in <listings> into a txt file that
        has the current date and time in its name. Return the number
        of listings found and the name of the txt file in a tuple
        """
        if len(listings) == 0:
            return 0, ''

        now = datetime.now()
        date_time = now.strftime('%d|%m|%Y %H.%M.%S')

        with open(f'Results/{date_time}.txt', 'a') as txt:
            i = 1
            for link in listings:
                price, time, is_furnished, pets_allowed, location, title, \
                    only_females, only_males = listings[link]

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

        return len(listings), f'{date_time}.txt'

    def search(self) -> tuple:
        """ The main search method, it extracts the HTML data from the kijiji
        searhc and looks through each listing for relevent information and
        determines if it matches the filters specified by the user. If it
        does, the information of this listing is added to a dictionary
        """
        url = self._url_city_adder()

        html_text = requests.get(url).text
        content = BeautifulSoup(html_text, 'lxml')
        all_results = content.find('div',
                                   class_='container-results large-images'). \
            find_next()
        ads = all_results.find_all('div', class_='search-item regular-ad')
        listings = {}
        for ad in ads:
            title_link = ad.find('div', class_='title').a
            title = title_link.text.strip()
            link = 'https://www.kijiji.ca' + title_link['href']
            if link in self._links:
                continue
            price = ad.find('div', class_='price').text.strip()
            if price == 'Please Contact' or price == 'Swap / Trade':
                continue
            else:
                price = price_formatter(price)
                if price > self.max_price:
                    continue
            time = ad.find('span', class_='date-posted').text
            is_furnished, pets_allowed, location, description = \
                link_explorer(link)
            if self.pets and pets_allowed == 'No':
                continue
            if self.furnished and is_furnished == 'No':
                continue
            only_females = self._check_gender_only('female', title, description)
            only_males = self._check_gender_only('male', title, description)
            if not self.female_only and only_females == 'Yes':
                continue
            if not self.male_only and only_males == 'Yes':
                continue
            listings[link] = (price, time, is_furnished, pets_allowed, location,
                              title, only_females, only_males)
        return self._record_results(listings)
