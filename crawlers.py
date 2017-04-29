import sys
from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import helpers

class Bookeo():
    """
        BOOKEO Class for Bookeo site scrapping
    """
    def __init__(self, society, url_to_scrap, iframe=False):
        """Set the initial variables"""
        self.society = society
        self.url = url_to_scrap
        self.iframe = iframe
        self.datas = []

    def start_driver(self):
        """Load Display and Driver"""
        error = False
        #Start the Virtual Display
        try:
            self.display = Display(visible=0, size=(800,600))
            self.display.start()
        except:
            print("Error: Display can't start!")
            Error = True
        #Create Driver
        try:
            self.driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        except:
            print("Error: Driver can't start!")
            error = True
        #Stop the program if there's errors
        if error:
            sys.exit('Program stopped because of Display/Driver problem')

    def stop_driver(self):
        """Stop display and Driver"""
        #Strop Driver and Virtual Display
        try:
            self.driver.quit()
            self.display.stop()
        except:
            error = True
            print("Display or Driver not stopped correctly")


    def get_datas(self):
        """Scrap datas"""
        errors = []
        T_datas = []
        try:
            self.driver.get(self.url)
            errors.append("Scrapped Datas from " + self.url + " -> OK")
            if self.iframe:
                try:
                    self.iframe = self.driver.find_elements_by_tag_name('iframe')[0]
                    self.driver.switch_to_frame(self.iframe)
                    self.subiframe = self.driver.find_elements_by_tag_name('iframe')[0]
                    self.driver.switch_to_frame(self.subiframe)
                    self.page = BeautifulSoup(self.driver.page_source, 'html.parser')
                    try:
                        T_datas = self.page.select("table#cbtce_eventsgrid tbody tr")
                    except:
                        print("Error : Can't fetch datas")
                except:
                    print("## Error: Can't find the Bookeo iframe on the page")
            else:
                self.page = BeautifulSoup(self.driver.page_source, 'html.parser')
                T_datas = self.page.select("table#cbtce_eventsgrid tbody tr")
        except:
            errors = 'Error: Page "' + self.url + '" is not reachable'

        return [T_datas,errors]

    def parse_datas(self, datas, room):
        self.final_datas = []
        self.date = str
        self.room = room
        for i in range(0, len(datas)):
            if len(datas[i]) <= 3:
                try:
                    self.date = helpers.parse_scrap_date(datas[i].select('td')[0].string.replace("\n", "").strip())
                except:
                    self.date = "Error: E01"

            elif len(datas[i]) >= 4:
                if self.date == helpers.get_date_fr(1):
                    if datas[i].select('td')[1].string.strip().lower() == self.room.lower():
                        hour = datas[i].select('td')[0].string.strip()
                        room = datas[i].select('td')[1].string.strip()
                        try:
                            datas[i].select('div.smallbRight')[1]
                            text = "LIBRE"
                        except:
                            text = "OCCUPE"
                        try:
                            self.final_datas.append([self.society, room, self.date, hour[:5], text])
                        except:
                            print("Error: E02")
                else:
                    pass
        return self.final_datas

    def scrap_datas(self, room):
        self.start_driver()
        self.datas = self.parse_datas(self.get_datas()[0], room)
        self.stop_driver()
        return self.datas
