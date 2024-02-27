from llama_index.readers.web import TrafilaturaWebReader

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
        try:
            return WebLoader._loader.load_data(web_urls)
        except Exception as e:
            print(e)
            return None





