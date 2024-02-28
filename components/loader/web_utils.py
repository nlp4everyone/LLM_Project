import requests
from bs4 import BeautifulSoup
class Utils():
    @staticmethod
    def get_sub_link(root_url):
        reqs = requests.get(root_url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        external_urls = []
        sub_urls = []

        for link in soup.find_all('a'):
            # Remove space
            url_link = str(link.get('href'))
            # Strip
            url_link = url_link.strip()

            # Sub link case
            if url_link.startswith("/"):
                sub_urls.append(root_url+url_link)
            elif url_link.startswith("http"):
                external_urls.append(url_link)
            else:
                pass
                # print(url_link)
        # Unique url
        sub_urls = list(set(sub_urls))
        external_urls = list(set(external_urls))
        return sub_urls,external_urls