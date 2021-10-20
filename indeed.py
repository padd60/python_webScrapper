import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://kr.indeed.com/jobs?q=python&limit={LIMIT}&radius=25'


def get_last_page():
    result = requests.get(URL)

    # print(indeed_result);

    soup = BeautifulSoup(result.text, "html.parser")

    # print(indeed_soup);

    pagination = soup.find("div", {"class": "pagination"})

    # print(pagination);

    links = pagination.find_all('a')

    # print(links);

    pages = []

    for link in links[:-1]:  # 처음부터 next 안걸리게 뒤에서 -1 해주어 제거해줌
        # pages.append(link.find("span").string);
        pages.append(int(link.string))
        # 해당 a태그로 소팅한 html에서 태그 내부 문자열이 페이지 숫자 하나라서 .string으로 줄일 수 있게됨

    # pages = pages[0:-1] next라는 문구가 문자열이라 int 메서드로 숫자형으로 변경 시 에러

    # print(pages); 모든 페이지 출력

    max_page = pages[-1]

    # print(max_page);  #마지막 페이지 출력

    return max_page


def extract_job(html):
    title = html.find('h2', {'class': 'jobTitle'}).find(
        'span', title=True).string
    company = html.find('span', {'class': 'companyName'})
    company_anchor = company.find('a')
    if company_anchor is not None:
        company = company_anchor.string
    else:
        company = company.string

    location = html.find('div', {'class': 'companyLocation'}).string
    job_id = html["data-jk"]

    return {'title': title, 'company': company, 'location': location, 'link': f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: Page: {page}")
        result = requests.get(f"{URL}&start={page * LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all('a', {'class': 'fs-unmask'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
