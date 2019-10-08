
from selenium import webdriver
from time import sleep
from selenium.webdriver import support
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup



driver = webdriver.Chrome()
driver.get("https://passport.bilibili.com/login")

driver.maximize_window()
sleep(0.5)

#输入账号密码并点击登陆
m_username = driver.find_element_by_id("login-username")
m_username.clear()
m_username.send_keys("18340018912")
sleep(0.5)

m_password = driver.find_element_by_id("login-passwd")
m_password.clear()
m_password.send_keys("yang5972181")
sleep(0.5)

m_login = driver.find_element_by_class_name("btn-login")
m_login.click()
sleep(1.5)



#截取背景图片
slice = driver.find_element_by_class_name("geetest_canvas_slice")
js = "document.getElementsByClassName(\"geetest_canvas_slice\")[0].style.display=\"none\";"
driver.execute_script(js)

driver.switch_to.default_content()
screenshot = driver.get_screenshot_as_png()
screenshot = Image.open(BytesIO(screenshot))
screenshot.save("D:\\screen1.png")

print(slice.location)
x = slice.location['x']
y = slice.location['y']
w = slice.size['width']
h = slice.size['height']
bg_image = screenshot.crop((x,y,x+w,y+h))
bg_image.save("D:\\bg.png")




#截取完整图片
full_bg = driver.find_element_by_class_name("geetest_canvas_fullbg")
js = "document.getElementsByClassName(\"geetest_canvas_fullbg\")[0].style.display=\"inline\";"
driver.execute_script(js)

driver.switch_to.default_content()
screenshot = driver.get_screenshot_as_png()
screenshot = Image.open(BytesIO(screenshot))
screenshot.save("D:\\screen2.png")
print(full_bg.location)
x = full_bg.location['x']
y = full_bg.location['y']
w = full_bg.size['width']
h = full_bg.size['height']
cropImage = screenshot.crop((x,y,x+w,y+h))
cropImage.save("D:\\fullbg.png")

bg_image = Image.open("D:\\screen1.png")
bg_image = bg_image.crop((x,y,x+w,y+h))
bg_image.save("D:\\bg.png")

##拖动滚动条
#slider = driver.find_element_by_class_name("geetest_slider_button")
#ActionChains(driver).click_and_hold(slider).perform()
#for i in range(0,10):
#    ActionChains(driver).move_by_offset(3,0).perform()
#    sleep(0.1)
#ActionChains(driver).release().perform()


print("end")
