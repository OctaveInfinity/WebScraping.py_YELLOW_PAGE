import json
from requests_html import HTML, HTMLSession

session = HTMLSession()
MAX_PAGE = 5
company_dict = {}

def pars(search_string, company):
    try:
        parsed_element = str(company.find(search_string, first=True).text)
    except:    
        parsed_element = None
    
    return parsed_element

# Reading pages
for page in range(1, MAX_PAGE+1):
    page = f'https://www.yellowpages.com/austin-tx/plumbers?page={page}'
    response = session.get(page)
    companies = response.html.find('div.info')
    
    # Parsing companies 
    for company in companies:

        # Numbered_name 	
        numbered_name = pars('.n', company)
        if (numbered_name is None) or (numbered_name.find('. ') < 0):
            continue

        # Name
        name = pars('.business-name', company)
        if (name is None):
            continue

        # Directions 
        directions = pars('.links', company)
        if (directions is None) or (directions.find('Directions') < 0):
            continue
        
        # Address 
        address_part1 = pars('.street-address', company)
        address_part2 = pars('.locality', company)
        if (address_part1 is None) or (address_part2 is None):
            continue 
        address = ', '.join([address_part1, address_part2])

        # Phone 
        phone = pars('.phone', company)
        if (phone != None):
            phone = int(''.join([char for char in phone if char.isdigit()]))

        # Print
        print(numbered_name)
        print(address)
        print(phone)
        print()

        # Dictionary
        company_dict.update({name: {'Adress': address, 'Phone Number': phone}})

# JSON
with open('plumbing.json', 'w') as file_output:
	json.dump(company_dict, file_output, indent=4)

print(json.dumps(company_dict, indent=4))

# Summary
print('\n===============================================')        
print(len(company_dict), """- companies successfully parsed from 
https://www.yellowpages.com/austin-tx/plumbers.
All results saved to plumbing.json 
in local directory on your machine.""")
