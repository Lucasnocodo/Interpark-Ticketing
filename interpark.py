from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException, UnexpectedAlertPresentException, \
    ElementClickInterceptedException, NoAlertPresentException, ElementNotInteractableException
from tkinter import *
import numpy
import time, datetime
import cv2 as cv
from pytesseract import image_to_string
import os
from selenium.webdriver.support.ui import Select

opt = webdriver.ChromeOptions()
opt.add_argument('window-size=800,600')
driver = webdriver.Chrome(executable_path=os.getcwd() + "\\es\\chromedriver.exe", options=opt)
wait = WebDriverWait(driver, 10)
url = "https://www.globalinterpark.com/user/signin"
driver.get(url)


def login_go():
    # driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    driver.find_element(By.ID, 'memEmail').send_keys(id_entry.get())
    driver.find_element(By.ID, 'memPass').send_keys(pw_entry.get())
    driver.find_element(By.ID, 'sign_in').click()


def link_go():
    driver.get('https://www.globalinterpark.com/detail/edetail?prdNo=' + showcode_entry.get() + '&dispNo=01003')  


def link_test():
    driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + showcode_entry.get())
    driver.switch_to.frame(driver.find_element_by_id('ifrmBookStep'))
    driver.execute_script("document.querySelectorAll('.calCont').forEach(function(a) {a.remove()})")


def seat_macro():
    driver.switch_to.default_content()
    seat1_frame = driver.find_element_by_name("ifrmSeat")
    driver.switch_to.frame(seat1_frame)
    seat2_frame = driver.find_element_by_name("ifrmSeatDetail")
    driver.switch_to.frame(seat2_frame)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')))
    seats = driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')
    print(len(seats))
    vip_list = []
    vip2_list = []
    vip3_list = []
    for i in seats:
        if "B블록2열" in i.get_attribute("title"):
            vip_list.append(i)
        elif "B블록3열" in i.get_attribute("title"):
            vip2_list.append(i)
        elif "B블록4열" in i.get_attribute("title"):
            vip3_list.append(i)
    print("2열 : ", len(vip_list))
    print("3열 : ", len(vip2_list))
    print("4열 : ", len(vip3_list))
    shot = 0
    shot1 = 0
    shot2 = 0
    shot3 = 0
    for x in range(0, len(vip_list) + len(vip2_list) + len(vip3_list)):
        try:
            print("2열")
            vip_list[x].click()
            shot += 1
            shot1 += 1
        except:
            try:
                print("3열")
                if x == 1 and shot2 == 0:
                    x = 0
                elif x == 1 and shot2 == 1:
                    x = 1
                elif x == 2 and shot2 == 0:
                    x = 0
                elif x == 2 and shot2 == 1:
                    x = 1
                elif x == 2 and shot2 == 2:
                    x = 2

                vip2_list[x].click()
                shot += 1
                shot2 += 1
            except:
                try:
                    print("4열")
                    if x == 1 and shot3 == 0:
                        x = 0
                    elif x == 1 and shot3 == 1:
                        x = 1
                    elif x == 2 and shot3 == 0:
                        x = 0
                    elif x == 2 and shot3 == 1:
                        x = 1
                    elif x == 2 and shot3 == 2:
                        x = 2
                    elif x == 3 and shot3 == 0:
                        x = 0
                    elif x == 3 and shot3 == 1:
                        x = 1
                    elif x == 3 and shot3 == 2:
                        x = 2
                    elif x == 3 and shot3 == 3:
                        x = 3
                    vip3_list[x].click()
                    shot += 1
                    shot3 += 1
                except:
                    print("예외")
                    break
        if shot == int(ticket_entry.get()):
            print("종료")
            break
        # elif shot >= ) and :

    print("종료 종료")

def captcha():
    driver.switch_to.default_content()
    seat1_frame = driver.find_element_by_id("ifrmSeat")
    driver.switch_to.frame(seat1_frame)
    image = driver.find_element_by_id('imgCaptcha')
    image = image.screenshot_as_png
    with open(os.getcwd() + "\\captcha.png", "wb") as file:
        file.write(image)
    image = cv.imread(os.getcwd() + "\\captcha.png")
    # Set a threshold value for the image, and save
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 91, 1)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel, iterations=1)

    cnts = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv.contourArea(c)
        if area < 50:
            cv.drawContours(image, [c], -1, (0, 0, 0), -1)
    kernel2 = numpy.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv.filter2D(image, -1, kernel2)
    result = 255 - image
    captcha_text = image_to_string(result)
    print(captcha_text)
    driver.switch_to.default_content()
    driver.switch_to.frame(seat1_frame)
    driver.find_element_by_class_name('validationTxt').click()
    driver.find_element_by_id('txtCaptcha').send_keys(captcha_text)
    if driver.find_element_by_xpath('//*[@id="divRecaptcha"]/div[1]/div[3]/div').is_displayed() == 1:
        driver.execute_script('fnCapchaRefresh()')
        captcha()
    while 1:
        global wait
        try:
            if driver.find_element_by_xpath('//*[@id="divRecaptcha"]/div[1]/div[3]/div').is_displayed() == 1:
                driver.execute_script('fnCapchaRefresh()')
                captcha()
            wait = WebDriverWait(driver, 0)
            go2()
        except:
            driver.execute_script('fnCapchaRefresh()')
            captcha()
            wait = WebDriverWait(driver, 0)
            go2()


def date_select():
    # 날짜
    while True:
        driver.switch_to.frame(driver.find_element(By.ID, 'play_date'))
        if int(calender_entry.get()) == 0:
            pass
        elif int(calender_entry.get()) >= 1:
            for i in range(1, int(calender_entry.get()) + 1):
                driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/span[3]").click()
        try:
            driver.find_element_by_xpath('(//*[@id="CellPlayDate"])' + "[" + date_entry.get() + "]").click()
            break
        except NoSuchElementException:
            link_go()
            go()
            break
        except NoSuchElementException:
            link_go()
            go()
            break
    # 회차
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + round_entry.get() + ']/a'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_id('LargeNextBtnImage').click()


def seat_again():
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("ifrmSeat"))
    driver.execute_script('$("ifrmSeatDetail").contentWindow.location.reload();')
    driver.execute_script('fnInitSeat();')
    seat_macro()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("ifrmSeat"))
    driver.find_element_by_id('NextStepImage').click()


def go2():
    seat_macro()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("ifrmSeat"))
    driver.find_element_by_id('NextStepImage').click()
    print("이선좌")
    while True:
        try:
            seat_again()
            print("가")
        except UnexpectedAlertPresentException:
            print("나")
        except NoSuchElementException:
            break
        except ElementNotInteractableException:
            break
def go():
    # 等待并定位 iframe
    wait = WebDriverWait(driver, 30)
    iframe_element = wait.until(EC.presence_of_element_located((By.ID, "product_detail_area")))

    # 切换到 iframe
    driver.switch_to.frame(iframe_element)
    code_time.delete(0, END)
    start_time = time.time()
    driver.switch_to.frame(driver.find_element(By.ID, 'product_detail_area'))
    try:
        date_select_element = driver.find_element(By.ID, "play_date")
    except NoSuchElementException:
        print("Element with ID 'play_date' not found")
    date_select = Select(date_select_element)
    date_value = date_entry
    try:
        date_select.select_by_value(date_value)
    except NoSuchElementException:
        print(f"No option found with value {date_value}")
    # try:
    #     print("A")
    #     driver.find_element(By., 'play_date').click()
    #     date_select()
    #     try:
    #         print("B")
    #         captcha()
    #     except NoSuchElementException:
    #         print("C")
    #         go2()
    # except NoSuchElementException:
    #     print("D")
    #     date_select()
    #     try:
    #         print("E")
    #         captcha()
    #     except NoSuchElementException:
    #         print("F")
    #         go2()
    # except UnexpectedAlertPresentException:
    #     all_go()
    finally:
        code_time.insert(0, "%s 초" % round((time.time() - start_time), 3))


def all_go():
    global wait
    wait = WebDriverWait(driver, 10)
    link_go()
    go()


def credit():
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="YYMMDD"]'))).send_keys(birth_entry.get())
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    bank2 = bank_var.get()
    kakao2 = kakao_var.get()
    if bank2 == 1:
        bank()
    elif kakao2 == 1:
        kakao()


def bank():
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22004"]/td/input'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BankCode"]/option[7]'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="LargeNextBtnImage"]').click()


def kakao():
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22084"]/td/input'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="LargeNextBtnImage"]').click()


def clock_time():
    clock = time.strftime('%X')
    time_label.config(text=clock)
    time_label.after(1, clock_time)


def full_auto():
    time2 = 0
    while True:
        time1 = time.strftime('%X')
        if time1 != time2:
            print(time1)
        elif time1 == full_entry.get():
            all_go()
            break
        time2 = time.strftime('%X')



dp = Tk()
main_frame = Frame(dp)
dp.geometry('300x450')
dp.title("인터파크 티켓팅 프로그램")
main_frame.pack()

id_label = Label(main_frame, text="帳號")
id_label.grid(row=1, column=0)

id_entry = Entry(main_frame)
id_entry.grid(row=1, column=1)

pw_label = Label(main_frame, text="密碼")
pw_label.grid(row=2, column=0)

pw_entry = Entry(main_frame)
pw_entry.grid(row=2, column=1)

login_button = Button(main_frame, text="登入", command=login_go, height=2)
login_button.grid(row=3, column=1)

showcode_label = Label(main_frame, text="演唱會編號")
showcode_label.grid(row=4, column=0)

showcode_entry = Entry(main_frame)
showcode_entry.grid(row=4, column=1)

calendar_label = Label(main_frame, text="日歷")
calendar_label.grid(row=5, column=0)

calender_entry = Entry(main_frame)
calender_entry.grid(row=5, column=1)

date_label = Label(main_frame, text="日期")
date_label.grid(row=6, column=0)

date_entry = Entry(main_frame)
date_entry.grid(row=6, column=1)

round_label = Label(main_frame, text="場次")
round_label.grid(row=7, column=0)

round_entry = Entry(main_frame)
round_entry.grid(row=7, column=1)

ticket_label = Label(main_frame, text="票數")
ticket_label.grid(row=8, column=0)

ticket_entry = Entry(main_frame)
ticket_entry.grid(row=8, column=1)

link_button = Button(main_frame, text="直接連結", command=link_go, height=2)
link_button.grid(row=9, column=0, sticky=E)

all_button = Button(main_frame, text='開始', command=all_go, height=2)
all_button.grid(row=9, column=1, sticky=W + E)

chair_button = Button(main_frame, text="座位", command=go2, height=2)
chair_button.grid(row=9, column=2, sticky=W)

start_button = Button(main_frame, text="直接選座", command=go, height=2)
start_button.grid(row=10, column=0, sticky=E)

credit_button = Button(main_frame, text="付款", command=credit, height=2)
credit_button.grid(row=10, column=1, sticky=W + E)

captcha_button = Button(main_frame, text='驗證碼', command=captcha, height=2)
captcha_button.grid(row=10, column=2, sticky=W)

bank_var = IntVar(value=0)
bank_check = Checkbutton(main_frame, text='無銀行帳戶轉帳', variable=bank_var)
bank_check.grid(row=9, column=3)

kakao_var = IntVar(value=0)
kakao_check = Checkbutton(main_frame, text='KakaoPay', variable=kakao_var)
kakao_check.grid(row=10, column=3)

credit2_button = Button(main_frame, text="自動預訂", command=full_auto, height=2)
credit2_button.grid(row=12, column=1, sticky=N)

full_label = Label(main_frame, text="預訂時間")
full_label.grid(row=13, column=0)

full_entry = Entry(main_frame)
full_entry.grid(row=13, column=1)

time_label = Label(main_frame, height=2)
time_label.grid(row=14, column=1)

birth_label = Label(main_frame, text='生日')
birth_label.grid(row=15, column=0)

birth_entry = Entry(main_frame)
birth_entry.grid(row=15, column=1)

code_label = Label(main_frame, text='所需時間')
code_label.grid(row=16, column=0)

code_time = Entry(main_frame)
code_time.grid(row=16, column=1)

full_time = (datetime.datetime.combine(datetime.date(1, 1, 1), datetime.datetime.now().time()) + datetime.timedelta(
    seconds=20)).time()

clock_time()
dp.mainloop()
