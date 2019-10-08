from selenium import webdriver
from time import sleep
from selenium.webdriver import support
#from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import random
import msvcrt

class bilibili_login():     
    def __init__(self,accout,password):
        self.driver = webdriver.Chrome()
        self.accout = accout
        self.password = password
        self.url = "https://passport.bilibili.com/login"
        self.driver.get("https://passport.bilibili.com/login")
        self.driver.maximize_window()
        #sleep(0.5)

        m_username = self.driver.find_element_by_id("login-username")
        m_username.clear()
        m_username.send_keys(accout)
        #sleep(0.5)

        m_password = self.driver.find_element_by_id("login-passwd")
        m_password.clear()
        m_password.send_keys(password)
        #sleep(0.5)

        m_login = self.driver.find_element_by_class_name("btn-login")
        m_login.click()
        sleep(1.5)

    def getImage(self):
        slice = self.driver.find_element_by_class_name("geetest_canvas_slice")
        js = "document.getElementsByClassName(\"geetest_canvas_slice\")[0].style.display=\"none\";"
        self.driver.execute_script(js)
        
        self.driver.switch_to.default_content()
        bg_screenshot = self.driver.get_screenshot_as_png()
        bg_screenshot = Image.open(BytesIO(bg_screenshot))
        bg_screenshot.save("D:\\picture_data\\bg_screenshot.png")

        full_bg = self.driver.find_element_by_class_name("geetest_canvas_fullbg")
        js = "document.getElementsByClassName(\"geetest_canvas_fullbg\")[0].style.display=\"inline\";"
        self.driver.execute_script(js)

        self.driver.switch_to.default_content()
        fullbg_screenshot = self.driver.get_screenshot_as_png()
        fullbg_screenshot = Image.open(BytesIO(fullbg_screenshot))
        fullbg_screenshot.save("D:\\picture_data\\fullbg_screenshot.png")

        x = full_bg.location['x']
        y = full_bg.location['y']
        w = full_bg.size['width']
        h = full_bg.size['height']
       
        fullbg_image = fullbg_screenshot.crop((x,y,x+w,y+h))
        fullbg_image.save("D:\\picture_data\\fullbg.png")
        
        bg_image = bg_screenshot.crop((x,y,x+w,y+h))
        bg_image.save("D:\\picture_data\\bg.png")

        js = "document.getElementsByClassName(\"geetest_canvas_fullbg\")[0].style.display=\"none\";"
        self.driver.execute_script(js)
        js = "document.getElementsByClassName(\"geetest_canvas_slice\")[0].style.display=\"block\";"

        self.driver.execute_script(js)

        return fullbg_image, bg_image
    def get_left_distance(self,fullbg,bg,threshold = 30):
        #该方法获得数据不准确，已经弃用
        left1 = 0
        left2 = 0
        find_left1 = False
        find_left2 = False
        
        for i in range ( 1 ,fullbg.size[0]):
            for j in range( 1,fullbg.size[1]):
                if not self.is_pixel_equal(fullbg,bg,i,j,threshold):
                    left1 = i
                    find_left1 = True
                    break
            if(find_left1):
                break

        for j in range ( 1 ,fullbg.size[1]):
            for i in range( 1,fullbg.size[0]):
                if not self.is_pixel_equal(fullbg,bg,i,j,threshold):
                    left2 = i
                    find_left2 = True
                    break  
            if find_left2 :
                break
        if left1 >left2:
            return left1
        else:
            return left2

    def get_right_distance(self,fullbg,bg,threshold = 30):
        #该方法获得数据不准确，已经弃用
        right1 = 0
        right2 = 0
       
        find_right1 = False
        find_right2 = False
        for i in range (1,fullbg.size[0]):
            for j in range(1,fullbg.size[1]):
                if not self.is_pixel_equal(fullbg,bg,fullbg.size[0]-i,j,threshold):
                    right1 = fullbg.size[0]-i
                    find_right1 = True
                    break
            if(find_right1):
                break

        for j in range (1,fullbg.size[1]):
            for i in range(1,fullbg.size[0]):
                if not self.is_pixel_equal(fullbg,bg,fullbg.size[0]-i,j,threshold):
                    right2 = fullbg.size[0]-i
                    find_right2 = True
                    break
        if right1> right2 :
            return right2
        else:
            return right1
    def get_left_distance_use_line(self,fullbg,bg,threshold = 30):
        #获得准确的左边界
        for i in range ( 1 ,fullbg.size[0]):
            diffent_pixel_num = 0
            for j in range( 1,fullbg.size[1]):              
                if not self.is_pixel_equal(fullbg,bg,i,j,threshold):
                    diffent_pixel_num +=1
            if(diffent_pixel_num >25):
                return i
        
    def nothing(self):
        print("nothing")
    
    
    def get_right_distance_use_line(self,fullbg,bg,threshold = 30):
        #获得准确的右边界
        for i in range ( 1 ,fullbg.size[0]):
            diffent_pixel_num = 0
            for j in range( 1,fullbg.size[1]):
                if not self.is_pixel_equal(fullbg,bg,fullbg.size[0]-i,j,threshold):
                    diffent_pixel_num +=1
            if(diffent_pixel_num >25):
                return fullbg.size[0]-i
        
    def is_pixel_equal(self, img1, img2, x, y,threshold = 30):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        
        if (abs(pix1 - pix2) < threshold):
        #if (abs(pix1[0] - pix2[0]) < threshold and abs(pix1[1] - pix2[1]) < threshold and abs(pix1[2] - pix2[2]) < threshold):
            return True
        else:
            return False
    
    def moveslider(self):
        #拖动滚动条
        #该方法由于匀速移动，被网站认定为机器人从而吞掉验证码，故已弃用
        slider = self.driver.find_element_by_class_name("geetest_slider_button")
        slider_width =  slider.size["width"]
        move_distance = self.get_left_distance() + (slider_width/2)

        ActionChains(self.driver).click_and_hold(slider).perform()
        current_move = 0
        each_step = 3
        while (current_move < move_distance):
            ActionChains(self.driver).move_by_offset(each_step,0).perform()
            current_move +=each_step
            sleep(0.1)
        
        ActionChains(self.driver).release().perform()

        ActionChains(self.driver).drag_and

    def super_move_slider(self, move_distance):
        #高级拖动
        
        slider = self.driver.find_element_by_class_name("geetest_slider_button")
        
        #print("slidersize:",slider.size)
        #slider_width =  slider.size["width"]
        #offset = -3
        #move_distance =  left_distance+ slider_width/2-10

        
        ActionChains(self.driver).click_and_hold(slider).perform()
        current_move = 0
        
        while (current_move < move_distance):
            #if(move_distance - current_move < 5):
            #    each_step = random.uniform(0.8,1.2)
            #else:
            each_step = random.uniform(5,8)
            ActionChains(self.driver).move_by_offset(each_step,random.uniform(-2,2)).perform()
            current_move +=each_step
            sleep(0.05)
        while(current_move >move_distance ):
            each_step = random.uniform(1.0,2.0)
            ActionChains(self.driver).move_by_offset(-each_step,random.uniform(-2,2)).perform()
            current_move -=each_step
            sleep(0.1)
        #print("current_move:",current_move)
        style =  slider.get_attribute("style")
        #print("slider属性",style)
        ActionChains(self.driver).release().perform()
    def png2gray(self,image_path):
        Image.open(image_path)
        gray =  Image.open(image_path).convert('L')
        #gray.show()
        return gray
    def png2gray_use_img(self,img):
        gray =img.convert('L')     
        return gray
    def refresh_page(self):
        self.driver.refresh()
        m_username = self.driver.find_element_by_id("login-username")
        m_username.clear()
        m_username.send_keys(self.accout)
        #sleep(0.5)
        
        m_password = self.driver.find_element_by_id("login-passwd")
        m_password.clear()
        m_password.send_keys(self.password)
        #sleep(0.5)

        m_login = self.driver.find_element_by_class_name("btn-login")
        m_login.click()
        sleep(1.5)

    def mark_image(self,left_distance,right_distance,bg):
        #对找到的缺口边界进行白边标记
        mark_bg = bg
        for i in range(1,mark_bg.size[1]):
            mark_bg.putpixel((left_distance,i),(255))
            mark_bg.putpixel((right_distance,i),(255))       
        return mark_bg
    def process(self):
        #程序处理流程
        while(True):
            fullbg, bg =  self.getImage()           
            fullbg = self.png2gray_use_img(fullbg)
            bg = self.png2gray_use_img(bg)
            fullbg.save("D:\\picture_data\\fullbg_gray.png")
            bg.save("D:\\picture_data\\bg_gray.png")         
            left_distance =  self.get_left_distance_use_line(fullbg,bg,5)
            right_distance =  self.get_right_distance_use_line(fullbg,bg,5)
            #print("10(use line):",left_distance,right_distance)
            mark_bg = self.mark_image(left_distance,right_distance,bg)
            mark_bg.save("D:\\picture_data\\mark_bg.png")           
            move_distance = (left_distance+right_distance)/2 -18 #有一定的偏移量
            self.super_move_slider(move_distance)

            sleep(1)
            try:
                """
                找"geetest_fail"元素，找到则表示位置不正确，刷新页面
                """
                self.driver.find_element_by_class_name("geetest_fail")
                print ("not in a suitable position.")                
                input()#没有移动到正确位置，暂时挂起，等待键盘输入任意数继续运行
                self.refresh_page()
            except NoSuchElementException:
                """
                没有找到"geetest_fail"元素，表示验证码被吞或者成功，若成功则结束程序，若失败则继续
                """
                sleep(1.5)
                if self.driver.current_url == self.url :
                    print(self.driver.current_url)
                    print("geetest was eaten.")
                    sleep(3)
                else:
                    print("ohohohohohohhhhhhh! sucess login! congratulations!")
                    return
            
        return
if __name__ == '__main__':
    print('开始验证')
    m_login =  bilibili_login("your_username","your_password")
    m_login.process()
    print('end')