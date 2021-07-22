from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
import time
import sys
import pprint

def Report(R):
    print(R, end = "", flush = True)

class Scrapper:
    def __init__(self):
        # self.TF = TasksFile
        self.SemesterLabels = []
        self.SemestersData = []
        self.token = "0"
        self.driver = webdriver.Chrome()
        #limiting the network speed to check if it works for slow internet users vvvvvvv
        # self.driver.set_network_conditions(
        # offline=False,
        # latency=5,  # additional latency (ms)
        # download_throughput=100 * 1024,  # maximal throughput
        # upload_throughput=100 * 1024)  # maximal throughput
        self.driver.get("https://portal.aaup.edu/faces/ui/login.xhtml")


    def Login(self, username, password):
        UsernameBar = self.driver.find_element_by_id("lognForm:j_idt17") #getting user's bar
        PasswordBar = self.driver.find_element_by_id("lognForm:j_idt21") #getting password's bar
        UsernameBar.send_keys(username) #sending the name
        PasswordBar.send_keys(password) #sending the pass
        self.driver.find_element_by_xpath("/html/body/div[1]/form/div/div/div[5]/button/span[2]").click() #logging in
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "ui-growl-item")))
            Report("|-|")
            self.driver.quit()
            sys.exit()
        except TimeoutException:
            Report("|+|")


    def GetToken(self): #getting the user's token
        #getting the url which has the token in it at the end vvvvv
        href = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, "menu-form:j_idt69"))).find_element_by_tag_name("a").get_attribute("href")
        self.token = href.partition("Token=")[2] #extracting the token from that url
    

    def NavigateToScheduale(self): #navigating to the schedual site
        #this is the default url which directs you to your schedual vvvvvv
        url = "https://portal.aaup.edu/faces/ui/pages/student/schedule/index.xhtml?javax.faces.Token="
        self.driver.get(url + self.token) # adding the token and getting to the site


    def GetSemestersLabels(self): #Getting all related schedual info
        #geting the options 
        SemestersLi = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents:semesters_items"]'))).find_elements_by_tag_name("li")
        for li in SemestersLi[1:]: #loops in the options + excluding the first useless option
            self.SemesterLabels.append(li.get_attribute("innerHTML"))


    def GetInfoFromSemesterTable(self):
        try:
            for i in range(1, len(self.SemesterLabels)):
                #gets the schedual's labels buttons VVVVVVV
                SemesterBtn = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents\:semesters_items"))).find_elements_by_tag_name("li")[i]
                self.driver.execute_script("arguments[0].click()", SemesterBtn)# clicks on the button, used this way cuz the elements are invisible
                #waits until the schedual loads VVVV                           #if i didn't use this method i should have click on the menu to make them show then click on the label
                WebDriverWait(self.driver, 3).until(EC.invisibility_of_element_located((By.CLASS_NAME, "j_idt323_modal")))
                time.sleep(1) #sleeps to let the rows load 100%
                #extracts the rows of data
                SemesterDataRows = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, "contents:j_idt270_data"))).find_elements_by_tag_name("tr")
                for PieceOfData in SemesterDataRows: #loops through these rows
                    TempSemesterData = []
                    for RawDataContainer in PieceOfData.find_elements_by_tag_name("td")[:-2]:#loops through these pieces of data but ignores the last 2
                        TempSemesterData.append(RawDataContainer.find_elements_by_class_name("ui-widget")[0]
                        .get_attribute("innerHTML")) #extracts the raw data from the label
                    self.SemestersData.append(TempSemesterData) #appends all the raw data to array
        except StaleElementReferenceException:
            Report("|-|")
            self.driver.quit()
            sys.exit()
        # pprint.PrettyPrinter(indent=4).pprint(self.SemestersData)      



if __name__=='__main__':
    scrapper = Scrapper()
    Report("$Trying to log in...")
    scrapper.Login(sys.argv[1] , sys.argv[2])
    #btw these prints that you gonna see next are nothing but just to give simple info i will remove them later
    # time.sleep(0.2)
    Report("$Trying to get the token...")
    scrapper.GetToken()
    Report("|+|") #Token has been obtained!
    # time.sleep(0.2)
    Report("$Navigating to schedules page...")
    scrapper.NavigateToScheduale()
    Report("|+|") #Navigated into Scheduals
    # time.sleep(0.2)
    Report("$Getting the semesters...")
    scrapper.GetSemestersLabels()
    Report("|+|") #Got the semesters of your Scheduals
    # time.sleep(0.2)
    # Report("$Collecting data...")
    scrapper.GetInfoFromSemesterTable()
    Report("|+|") #Got the data of each one of your scheduals
    # time.sleep(0.2)
    # scrapper.driver.get("http://localhost:4000/WebSite/index.php")
    # input("Press Enter to continue...") #for testing no more
    Report("DONE")
    scrapper.driver.quit()