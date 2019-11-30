import json
from requests_html import HTML, HTMLSession

session = HTMLSession()
company_dict = {}
MAX_PAGE = 5

def parse_function(search_string, company_element):
    try:
        parsed = str(company_element.find(search_string, first=True).text)
    except:    
        parsed = None
    
    return parsed

# Reading pages
for page_count in range(1, MAX_PAGE+1):
    page_link = f'https://www.yellowpages.com/austin-tx/plumbers?page={page_count}'
    response = session.get(page_link)
    companies_list = response.html.find('div.info')
    print('page_count: ', page_count, '\n')
        
    # Parsing companies 
    for company in companies_list:

        # Numbered_name 	
        numbered_name = parse_function('.n', company)
        if (numbered_name.find('. ') < 0) or (numbered_name is None):
            continue

        # Name
        name = parse_function('.business-name', company)
        if (name is None):
            continue

        # Directions 
        directions = parse_function('.links', company)
        if  (directions.find('Directions') < 0) or (directions is None):
            continue
        
        # Address 
        address_part1 = parse_function('.street-address', company)
        address_part2 = parse_function('.locality', company)
        if (address_part1 is None) or (address_part2 is None):
            continue 
        address = ', '.join([address_part1, address_part2])

        # Phone 
        phone = parse_function('.phone', company)
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
