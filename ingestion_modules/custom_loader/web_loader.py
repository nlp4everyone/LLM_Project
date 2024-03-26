from llama_index.readers.web import TrafilaturaWebReader
import requests
from bs4 import BeautifulSoup
class WebLoader():
    # Default loader
    _loader = TrafilaturaWebReader()

    @staticmethod
    def replace_loader(loader):
        # Replace loader
        WebLoader._loader = loader

    @staticmethod
    def load_documents(web_urls:list):
        # Return document from url
        if not isinstance(web_urls,list):
            raise Exception("Web urls must be a list of website")
        # Try catch
        # try:
        return WebLoader._loader.load_data(web_urls)
        # except Exception as e:
        #     raise Exception(e)
        #     return None

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





