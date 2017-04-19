#coding = utf-8

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import pytesseract
from PIL import Image,ImageEnhance,ImageOps

#driver = webdriver.Firefox() # Get local session of firefox
#driver.get("http://www.baidu.com") # Load page
#elem = browser.find_element_by_name("p") # Find the query box
#elem.send_keys("seleniumhq" + Keys.RETURN)
#time.sleep(0.2) # Let the page load, will be added to the API
#try:
#    browser.find_element_by_xpath("//a[contains(@href,'http://seleniumhq.org')]")
#except NoSuchElementException:
#    assert 0, "can't find seleniumhq"
#size = driver.find_element_by_name("wd").size  
#print(size)
  
#text = driver.find_element_by_id("jgwab").text  
#print(text)
  
#attribute = driver.find_element_by_xpath(".//input[@id='kw']").get_attribute('maxlength')  
#print(attribute)

#result = driver.find_element_by_partial_link_text("About Baidu").is_displayed()
#print(result)
 
#browser.find_element_by_id("kw").send_keys("selenium")
#browser.find_element_by_id("su").click()
#driver.quit()  

def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x<143 else 255)
    borderImage = ImageOps.expand(image,border=20,fill='white')
    borderImage.save(imagePath)
    
def funcimg(browser):
    browser.maximize_window()
    browser.save_screenshot('f://aa.png')     
    imgelement = browser.find_element_by_id("ValidateImage")
    #location = imgelement.location
    #size=imgelement.size
    #rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
    i=Image.open("f://aa.png")
    frame4=i.crop((695,460,772,486))
    frame4.save('f://frame4.jpg')
    im=Image.open('f://frame4.jpg')
    imgry = im.convert('L')
    sharpness =ImageEnhance.Contrast(imgry)
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("f://frame5.jpg")
    qq=Image.open('f://frame5.jpg')
    cleanImage('f://frame4.jpg')
    pytesseract.
    text=pytesseract.image_to_string(qq)
    print text
    browser.find_element_by_id("ValidateCode").send_keys(text)
    
browser = webdriver.Firefox()

browser.get("http://3.zxw66.cc/home/login_qqmail")
time.sleep(1)
#browser.switch_to.form("form1")

#browser.find_element_by_name("txt").send_keys("846239")
#brower.find_elements_by_class_name("btn").click()
browser.find_element_by_name("txt").send_keys("846239")
browser.find_element_by_name("form1").submit()

time.sleep(2)
link_windows = browser.current_window_handle 

browser.find_element_by_id("lnkk_1").click()

time.sleep(2)

all_handles = browser.window_handles

time.sleep(5)

for handle in all_handles:
    if handle != link_windows:
        browser.switch_to.window(handle)
        browser.switch_to.frame("topFrame")
        browser.find_element_by_name("loginName").send_keys("xxkk22")
        browser.find_element_by_name("loginPwd").send_keys("aa223344")
        browser.find_element_by_id("ValidateCode").click()  
        time.sleep(3)
        funcimg(browser)
        time.sleep(3)
        browser.find_element_by_id("M_Login").submit()
        time.sleep(1000)
        
browser.close()




