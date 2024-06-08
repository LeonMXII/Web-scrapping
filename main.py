"""
main
class="vacancy-serp-content"

span
class="serp-item__title-link-wrapper"

div
class="bloko-columns-row"

div
class="g-user-content"

div
data-qa="vacancy-salary"

a
class="bloko-link bloko-link_kind-tertiary"

p
data-qa="vacancy-view-location"

"""


import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json

def get_headers():
    return Headers(browser='chrome', os='win').generate()

url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

main_response = requests.get(url, headers=get_headers())
main_html = main_response.text
main_soup = BeautifulSoup(main_html, "lxml")


tag_vacancy = main_soup.find("main", class_="vacancy-serp-content")
vacancy = tag_vacancy.find_all("span", class_="serp-item__title-link-wrapper")


parsed_data = []

for span in vacancy:
    tag_a = span.find("a")
    link = tag_a["href"]
    # link = f"https://spb.hh.ru{link}"


    div_response = requests.get(link, headers=get_headers())
    div_soup = BeautifulSoup(div_response.text, "lxml")
    div_body_tag = div_soup.find("div", class_="bloko-columns-row")
    vacancy_text = div_body_tag.find("div", class_="g-user-content").text


    if "Django" or "Flask" in vacancy_text:
        salary = div_body_tag.find("div", {"data-qa": "vacancy-salary"}).text
        name = div_body_tag.find("a", class_="bloko-link bloko-link_kind-tertiary").text
        city = div_body_tag.find("p", {"data-qa": "vacancy-view-location"}).text

        parsed_data.append(
            {
                "Ссылка": link,
                "Заработная плата": salary,
                "Название компании": name,
                "Город": city
            }
        )

json_ = json.dumps(parsed_data, indent=10, ensure_ascii=False)

with open("data.json", "w", encoding="utf-8") as file:
    file.write(json_)




