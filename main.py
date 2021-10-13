import requests
from bs4 import BeautifulSoup

indeed_result = requests.get('https://kr.indeed.com/jobs?q=python&l&vjk=f53f70423a1cd729');

# print(stackoverflow_result);

indeed_soup = BeautifulSoup(indeed_result.text, "html.parser");

# print(stackoverflow_soup);

pagination = indeed_soup.find("div", {"class": "pagination"});

# print(pagination);

pages = pagination.find_all('a');

# print(pages);

spans = []

for page in pages :
  spans.append(page.find("span"));

  
print(spans[0:-1]);
