from datetime import datetime

from selenium_options import get_chromedriver, user_agent_list
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import choice
import time
from .serializers import ProductSerializer
import telegram_bot

MAX_ERRORS_COUNT_FOR_PRODUCT = 10

def parse_product(products_count):
    global driver
    driver = get_chromedriver(choice(user_agent_list))
    products_list = []
    last_error_product = 0
    number_of_attempts_for_product = 0
    while len(products_list) < products_count:
        len_products_list = len(products_list)
        if last_error_product == len_products_list:
            number_of_attempts_for_product += 1
            # Если количество ошибок в процессе парсинга одного товара больше лимита
            # Прекращаем парсинг, записываем успешные товары, отправляем уведомление об ошибке
            if number_of_attempts_for_product > MAX_ERRORS_COUNT_FOR_PRODUCT:
                telegram_bot.send_notification_about_errors(len_products_list)
                break
        else:
            last_error_product = len_products_list

        # Запускаем сбор информации товаров, пропуская те, что уже есть в products_list
        products_list = select_info_about_products(len_products_list, products_count, products_list)

    if len(products_list) == products_count:
        telegram_bot.send_notification_about_success(products_count)
    driver.quit()
    save_products(products_list)


def save_products(products_list):
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    for i in range(len(products_list)):
        products_list[i]['recording_time'] = current_time
        if ProductSerializer(data=products_list[i], many=False).is_valid() is False:
            print(products_list[i])

    if len(products_list) == 1:
        serializer = ProductSerializer(data=products_list[0], many=False)
    else:
        serializer = ProductSerializer(data=products_list, many=True)
    if serializer.is_valid():
        serializer.save()


def select_info_about_products(start, end, products_list):
    # Определяем page в зависимости от того сколько продуктов уже есть в products_list
    page = ((start + 1) // 37) + 1
    url = f'https://www.ozon.ru/seller/proffi-1/products/?miniapp=seller_1&page={page}'
    driver.get(url=url)
    bypass_protection()

    for product_id in range(start + 1, end + 1):
        print(product_id)
        # Останавливаем цикл если прошли все товары на странице
        if page != (product_id // 37) + 1:
            break

        product_id = product_id - 36 * (page - 1)
        # Пробуем взять информацию о продукте
        try:
            products_list = product_processing(products_list, product_id)
        # В случае какой-либо ошибки останавливаем цикл
        except Exception as ex:
            print(ex)
            break

    return products_list


def product_processing(products_list, product_id):
    open_product(product_id)
    product_info = get_product_info()
    products_list.append(product_info)
    driver.back()
    return products_list


def bypass_protection():
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    while True:
        time.sleep(1)
        try:
            reload_button = driver.find_element(By.CSS_SELECTOR, "#reload-button")
            reload_button.click()
            break

        except NoSuchElementException:
            try:
                driver.find_element(By.CSS_SELECTOR, f"#paginatorContent > div > div > div:nth-child(1)")
                break
            except:
                pass


def open_product(product_id):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print(1)
    time.sleep(1)
    product = driver.find_element(By.CSS_SELECTOR, f"#paginatorContent > div > div > div:nth-child({product_id})")
    print(2)
    driver.execute_script("arguments[0].scrollIntoView(true);", product)
    print(3)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    product = driver.find_element(By.CSS_SELECTOR, f"#paginatorContent > div > div > div:nth-child({product_id})")
    print(4)
    product.click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print(5)


def get_price():
    price = driver.find_element(By.CSS_SELECTOR,
                                "#layoutPage > div.b2 > div.container.b6 > div.y6k.zk1 > div.y6k.zk2.kz.zk > div.y6k.zk2.kz.kz0 > div > div > div.lz2 > div > div > div.wl0 > div.wl3.wl8 > div > div.w6l > span.w4l.lw5.w8l").text[
            :-2]
    price = str(price).replace('\u2009', '')
    return price


def get_product_info():
    image = driver.find_element(By.CSS_SELECTOR,
                                "#layoutPage > div.b2 > div.container.b6 > div.y6k.zk1 > div.y6k.zk2.k1z > div.d8 > div.d2.c4 > div > div > div > div > div > div.kx7 > div.v3j.ky1 > div > img")
    print('img', bool(image))

    try:
        discount = driver.find_element(By.CSS_SELECTOR,
                                       "#layoutPage > div.b2 > div.container.b6 > div.y6k.zk1 > div.y6k.zk2.k1z > div.d8 > div.d2.c4 > div > div > div > div > div > div.kx7 > div.kx8 > div > div > div > div > div > div > div").text[
                   1:-1]
        print('discount', bool(discount))
    except:
        discount = None

    price = get_price()
    print('price', bool(price))

    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#section-description > div > div > div > div")))
        description = driver.find_element(By.CSS_SELECTOR, "#section-description > div > div > div > div").text
    except:
        description = ''

    print('description', bool(description))

    name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div[1]/h1").text

    print('name', bool(name))

    product_info = {
        "name": name,
        "price": int(price),
        "description": description,
        "image_url": image.get_attribute("src"),
        "discount": discount,
        'link': driver.current_url
    }
    print(product_info)
    return product_info



