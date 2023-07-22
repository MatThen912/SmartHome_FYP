from django.conf import settings
from hashlib import md5 as md5_constructor
from django.core.cache import cache

def clear_cache_for_path(path, key_prefix=None):
    if key_prefix is None:
      key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
    
    args = md5_constructor(path)
    path = args.hexdigest()
    header_key = 'views.decorators.cache.cache_header.%s.%s' % (key_prefix, path)
    headers = cache.get(header_key)
  
    ctx = md5_constructor()
    if headers:
      for header in headers:
        ctx.update(header)
      
    cache.delete(header_key)
  
    page_key = 'views.decorators.cache.cache_page.%s.%s.%s' % (key_prefix, path, ctx.hexdigest())
    cache.delete(page_key)

class BreadCrumb:
    def __init__(self, base_url="/home", base_text="CCB Smart Poultry"):
        self.__crumbs = []

        data = {}
        data['url'] = base_url
        data['base_text'] = base_text

        self.add_page(base_url, base_text)

    def __repr__(self):
        return f"Breadcrumb object {str(self)}"
    def __str__(self):
        breadcrumbs = ""
        for crumb in self.__crumbs:
            breadcrumbs += f"/{crumb['text']}" 
        return breadcrumbs

    def to_dict(self):
        """
        convert breadcrumbs object to python dictionary 
        """
        return {
            'breadcrumbs' : {
                'crumbs' : self.__crumbs,
                'main_title' : self.main_title
            }
        } 

    def add_page(self, url, text):
        """
        params :
            url - The url of the page in the breadcrumb (href)
            text - Text to show (inner text of href)
        Add page to the breadcrumb 
        """
        data = {}
        data['url'] = url
        data['text'] = text
        self.__crumbs.append(data)

    def set_title(self, title):
        """
        SET the breadcrumb title page title
        """
        self.main_title = title
