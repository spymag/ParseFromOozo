import urllib.request
from lxml import html

def find_property_url_by_postcode(address_info):
    """
    Finds the property URL for a given address by scraping the postcode page on oozo.nl.
    """
    base_url = "https://www.oozo.nl"
    postcode_url = f"{base_url}/postcode/woningen/{address_info['postalcode']}"

    try:
        # Fetch the HTML of the postcode page
        req = urllib.request.Request(postcode_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            page_content = response.read()

        # Parse the HTML
        tree = html.fromstring(page_content)

        # Find all property links on the page
        property_links = tree.xpath('//a[contains(@href, "/woning/")]')

        # Search for the link that contains the street name and house number
        for link in property_links:
            full_address_text = "".join(link.xpath('.//text()')).strip()
            if address_info['street'].lower() in full_address_text.lower() and address_info['housenumber'] in full_address_text:
                return base_url + link.get('href')

    except urllib.error.HTTPError as e:
        print(f"Error fetching page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None

def main():
    """
    Main function to find and save the property URL.
    """
    address_of_interest = {
        "street": "Plantageweg",
        "housenumber": "8",
        "postalcode": "3061PH"
    }

    property_url = find_property_url_by_postcode(address_of_interest)

    if property_url:
        print(f"Found URL: {property_url}")
        # Write the URL to a file
        with open(f"{address_of_interest['street']}_{address_of_interest['housenumber']}.txt", 'w') as f:
            f.write(property_url)
    else:
        print("Could not find the property URL.")

if __name__ == '__main__':
    main()
