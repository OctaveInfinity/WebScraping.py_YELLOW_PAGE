import json
from requests_html import HTML, HTMLSession

MAX_PAGE = 5

session = HTMLSession()

company_dict = {}

# Reading pages --------------------------------------------------------
for page in range(1, MAX_PAGE+1):
    page = f'https://www.yellowpages.com/austin-tx/plumbers?page={page}'
    response = session.get(page)
    companies = response.html.find('div.info')
    
    # Parsing companies ------------------------------------------------
    for company in companies:

        # Numbered_name ------------------------------------------------	
        try:
            numbered_name = str(company.find('.n', first=True).text)
        except Exception as e:
            numbered_name = None
                
        if (numbered_name.find('. ') < 0):
            continue

        # Name ---------------------------------------------------------	
        try:
            name = str(company.find('.business-name', first=True).text)
        except Exception as e:
            name = None

        # Directions ---------------------------------------------------
        try:
            directions = str(company.find('.links', first=True).text)
        except Exception as e:
            directions = None
            
        if (directions.find('Directions') < 0):
            continue

        # Address ------------------------------------------------------
        try:
            address_part1 = str(company.find('.street-address', first=True).text)
        except Exception as e:
            address_part1 = None

        try:
            address_part2 = str(company.find('.locality', first=True).text)
        except Exception as e:
            address_part2 = None

        if (address_part1 is None) or (address_part2 is None):
            continue 

        address = ', '.join([address_part1, address_part2])

        # Phone --------------------------------------------------------
        try:
            phone = str(company.find('.phone', first=True).text)
        except Exception as e:
            phone = None
        else:
            phone = int(''.join([char for char in phone if char.isdigit()]))

        # Print --------------------------------------------------------
        print(numbered_name)
        print(address)
        print(phone)
        print()	

        # Dictionary -------------------------------------------------
        company_dict.update({name: {'Adress': address, 'Phone Number': phone}})

# JSON ===============================================================

with open('plumbing.json', 'w') as file_output:
	json.dump(company_dict, file_output, indent=4)

print(json.dumps(company_dict, indent=4))

print('\n===============================================')        
print(len(company_dict), """- companies successfully parsed from 
https://www.yellowpages.com/austin-tx/plumbers.
All results saved to plumbing.json 
in local directory on your machine.""")
