from requests_html import HTML, HTMLSession

MAX_PAGE = 3

session = HTMLSession()

for page in range(1, MAX_PAGE+1):
    page = f'https://www.yellowpages.com/austin-tx/plumbers?page={page}'
    response = session.get(page)

    companies = response.html.find('div.info')

    for company in companies:

        # numbered_name ------------------------------------------------	
        numbered_name = company.find('.n', first=True).text
        if numbered_name.find('. ') < 0:
            continue

        # directions ---------------------------------------------------
        links = company.find('.links', first=True).text
        if links.find('Directions') < 0:
            continue

        # address -------------------------------------------------------
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

        # phone --------------------------------------------------------
        try:
            phone = company.find('.phone', first=True).text
        except Exception as e:
            phone = None
        else:
            phone = ''.join([char for char in phone if char.isdigit()]) # must be int

        # Print --------------------------------------------------------
        print(numbered_name)
        print(address_part1, address_part2, sep=', ')
        print(phone)

        print()	



        