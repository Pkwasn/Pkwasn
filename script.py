import requests
from bs4 import BeautifulSoup

URL = "https://inciweb.nwcg.gov/accessible-view/"

def main():

    data = get_data()
    fires = parse_document(data)
    fires.sort(key=lambda x: int(x[3][:len(x)-4]), reverse=True)

    markdown = "Top 10 Largest Fires by Acreage in the Past 2 Weeks\n\n | Incident Name | Acres | Location | Date and Time |\n|:---|:---|:---|:---|\n"

    for fire in fires[:10]:
        markdown += f"| [{fire[0]}]({fire[1]}) | {fire[3]} | {fire[2]} | {fire[4]} |\n"

    open("./README.md", "w", encoding="utf-8").write(markdown)

def get_data():
    """Requests the HTML document from InciWeb

    Returns
    -------
    str
        Raw un-parsed HTML document.

    """

    with requests.get(URL) as response:

        print("Document recieved")
        return response.text

def parse_document(html):
    """Parses HTML document for relevant information

    Relevant Information: Incident Name, Link to incident description, Location (State),
        Time Updated (Only ongoing incidents will be updated)

    Returns
    -------
    list
        List of all fires with relavant data
    """
    fires = list()

    soup = BeautifulSoup(html, 'html.parser').find('tbody')
    for child in soup.children:

        name = str(child.contents[0].string)
        _url = URL[:len(URL)-17] + str(child.contents[0].find('a', href=True)['href']) # We perform string manipulation since 'accessible-view/' is not included in incident link
        location = str(child.contents[2].string)
        acres = str(child.contents[3].string)
        time = str(child.contents[4]['data-sort-value']) # the id 'data-sort-value' has a more accurate time

        fire_data = [name, _url, location, acres, time]
        fires.append(fire_data)

    print("Data parsed")
    return fires

if __name__ == "__main__":

    main()
