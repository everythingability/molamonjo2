from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Select categories from
# https://gtr.ukri.org/search/classification?term=*&fetchSize=25&selectedSortableField=&selectedSortOrder=
'''
Archaeological Theory
Archaeology Of Human Origins
Archaeology of Literate Soc.
Architecture HTP
Environmental planning
Heritage Management
Landscape & Environ. Archaeol.
Prehistoric Archaeology
Science-Based Archaeology
'''
## Results in 
 url = 'https://gtr.ukri.org/search/classification?term=*&page=1&fetchSize=25&fields=&detailedAndFilter=false&selectedFacets=cHJvamVjdFJlc2VhcmNoVG9waWNzfEFyY2hhZW9sb2dpY2FsIFRoZW9yeXxzdHJpbmc=,cHJvamVjdFJlc2VhcmNoVG9waWNzfEFyY2hhZW9sb2d5IE9mIEh1bWFuIE9yaWdpbnN8c3RyaW5n,cHJvamVjdFJlc2VhcmNoVG9waWNzfEFyY2hhZW9sb2d5IG9mIExpdGVyYXRlIFNvYy58c3RyaW5n,cHJvamVjdFJlc2VhcmNoVG9waWNzfEFyY2hpdGVjdHVyZSBIVFB8c3RyaW5n,cHJvamVjdFJlc2VhcmNoVG9waWNzfEVudmlyb25tZW50YWwgcGxhbm5pbmd8c3RyaW5n,cHJvamVjdFJlc2VhcmNoVG9waWNzfEhlcml0YWdlIE1hbmFnZW1lbnR8c3RyaW5n,cHJvamVjdFJlc2VhcmNoVG9waWNzfExhbmRzY2FwZSAmIEVudmlyb24uIEFyY2hhZW9sLnxzdHJpbmc=,cHJvamVjdFJlc2VhcmNoVG9waWNzfFByZWhpc3RvcmljIEFyY2hhZW9sb2d5fHN0cmluZw==,cHJvamVjdFJlc2VhcmNoVG9waWNzfFNjaWVuY2UtQmFzZWQgQXJjaGFlb2xvZ3l8c3RyaW5n'


driver = webdriver.Firefox()
driver.get(url)
#assert "Python" in driver.title
#<a id="toCSV" class="btn-mini btn-css3 btn-responsive btn-css3-default" data-toggle="modal" href="#csvConfirm">CSV</a>

elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()