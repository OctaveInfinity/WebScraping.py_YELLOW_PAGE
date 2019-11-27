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

        print(numbered_name)