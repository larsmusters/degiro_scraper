import requests
import pprint
from bs4 import BeautifulSoup

URL = 'https://www.monster.com/jobs/search/?q=Software-Developer&where=Australia'
URL = 'https://www.funda.nl/koop/den-haag/beschikbaar/0-250000/50+woonopp/3-dagen/+30km/sorteer-datum-af/p2/'
page = requests.get(URL)

pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(page.text)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='content')

pp.pprint(results.prettify())

job_elems = results.find_all('li')

#for each in job_elems:
##    print(each, end='\n'*2)
#    
#    # If it contains this then it is an ad.
#    try:
#        each['data-mux']
#        continue
#    except:
#        pass
##    if each.find('section',id="bad2") is not None:
##        continue
#    
#    
#    title_elem = each.find('h2', class_='title')
#    company_elem = each.find('div', class_='company')
#    location_elem = each.find('div', class_='location')
#    
#    if None in (title_elem, company_elem, location_elem):
##        print(each)
#        print(title_elem)
#        print(company_elem)
#        print(location_elem)
#        continue    
#    print(title_elem.text.strip())
#    print(company_elem.text.strip())
#    print(location_elem.text.strip())
#    print()
#    
#python_jobs = results.find_all('h2', string = lambda text:'python'in text.lower())
#
#for each in python_jobs:
#    link = each.find('a')['href']
#    print(each.text.strip())
#    print(f"Apply here: {link}\n")