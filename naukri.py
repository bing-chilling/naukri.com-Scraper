from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

def main():
    with sync_playwright() as p:
        browser= p.firefox.launch(headless=False)
        page=browser.new_page()
        record= {'Title': [], 'Company': [], 'Years': [], 'Stars': [], 'Reviews': [], 'Salary': [], 'Location': [], 'Skills': []}
        for i in range(1,5):
            page.goto(f'https://www.naukri.com/it-jobs-{i}', timeout=0)
            meat= "//div[@class='list']"
            page.wait_for_selector(meat, timeout=0)
            html= page.inner_html(meat)
            soup= BeautifulSoup(html, 'lxml')
            jobs= soup.find_all('article', class_='jobTuple bgWhite br4 mb-8')
            
            for job in jobs:
                head= job.find('div', class_='jobTupleHeader')
                stars= head.find('span', class_='starRating fleft dot')
                count= head.find('a', class_='reviewsCount ml-5 fleft blue-text')
                tags= job.find('ul', class_='tags has-description').find_all('li')
                skills= []
                for tag in tags:
                    skills.append(tag.get_text())
                record['Skills'].append(skills)
                record['Salary'].append(head.find('li', class_='fleft grey-text br2 placeHolderLi salary').span.get_text())
                record['Location'].append(head.find('li', class_='fleft grey-text br2 placeHolderLi location').get_text()) 
                if stars:
                    record['Stars'].append(stars.get_text()) 
                    record['Reviews'].append(count.get_text())       
                else:
                    record['Stars'].append('NA')
                    record['Reviews'].append('NA')
                record['Title'].append(head.div.a.text)
                record['Company'].append(head.find('a', class_='subTitle ellipsis fleft').get_text())
                record['Years'].append(head.span.text)

        with open('result.json', 'w') as f:
            json.dump(record, f)

        browser.close()

if __name__=='__main__':
    main()
