import requests
from bs4 import BeautifulSoup
import time
import re

def scrape_oozo_nl():
    base_url = "https://www.oozo.nl"
    # This is the page for Kralingen West, which corresponds to 3061 postal code area
    start_url = "/hulpdiensten/rotterdam/kralingen-crooswijk/kralingen-west"

    incidents = {"Ambulance": [], "Brandweer": [], "Politie": [], "Overig": []}
    scraped_links = set()

    page_num = 1
    while True:
        # p=1 is the first page, but the URL doesn't have the p parameter for the first page.
        if page_num == 1:
            url = f"{base_url}{start_url}"
        else:
            url = f"{base_url}{start_url}?p={page_num}"

        print(f"Scraping page {page_num}: {url}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {url}: {e}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        # Incident links have a specific pattern.
        # The regex is specific to the Kralingen-West area as per the user's request to focus on the 3061 postal code.
        # For a more generic scraper, this regex would need to be parameterized.
        links = soup.find_all('a', href=re.compile(r'/hulpdiensten/rotterdam/kralingen-crooswijk/kralingen-west/\w+/\d+'))

        if not links and page_num > 1:
            print("No more incidents found on page. Stopping.")
            break

        new_incidents_found_on_page = 0
        for link_tag in links:
            link_href = link_tag['href']

            if not link_href.startswith('http'):
                full_link = base_url + link_href
            else:
                full_link = link_href

            if full_link in scraped_links:
                continue

            scraped_links.add(full_link)
            new_incidents_found_on_page += 1

            title = link_tag.get_text(strip=True)

            subject = "Overig"
            if "/ambulance/" in full_link:
                subject = "Ambulance"
            elif "/brandweer/" in full_link:
                subject = "Brandweer"
            elif "/politie/" in full_link:
                subject = "Politie"

            incidents[subject].append({"title": title, "link": full_link})

        if new_incidents_found_on_page == 0 and page_num > 1:
             print("No new incidents found on this page, assuming end of results. Stopping.")
             break

        page_num += 1
        time.sleep(1)


    return incidents

def write_to_markdown(incidents):
    with open("incident_reports.md", "w", encoding="utf-8") as f:
        f.write("# Incident Reports for Rotterdam (Postal Code 3061)\n\n")
        f.write("This file contains a list of incident reports scraped from oozo.nl for the `3061` postal code area in Rotterdam (Kralingen West).\n\n")
        f.write("The incidents are grouped by service.\n\n")

        for subject in ["Ambulance", "Brandweer", "Politie", "Overig"]:
            items = incidents[subject]
            if items:
                f.write(f"## {subject}\n\n")
                for item in items:
                    title = item['title'].replace('[', '\\[').replace(']', '\\]')
                    f.write(f"* [{title}]({item['link']})\n")
                f.write("\n")

if __name__ == "__main__":
    print("Starting scraper...")
    all_incidents = scrape_oozo_nl()
    print(f"Scraped {sum(len(v) for v in all_incidents.values())} total incidents.")
    write_to_markdown(all_incidents)
    print("Scraping complete. Results saved to incident_reports.md")
