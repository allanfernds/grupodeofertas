from selenium import webdriver
from selenium.webdriver.common.by import By
from telegram_message import enviar_mensagem_com_imagem
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from short_url import encurtar_url
import time


# Função para obter informações do produto
from selenium.common.exceptions import NoSuchElementException


def obter_titulo_e_imagem(driver):
    try:
        title = driver.find_element(
            By.XPATH, '//*[@id="__next"]/div/main/section[2]/div[2]/h1'
        ).text
        image_url = driver.find_element(
            By.XPATH, '//*[@id="__next"]/div/main/section[3]/div/div/div/div[2]/img'
        ).get_attribute("src")
        return title, image_url
    except NoSuchElementException:
        return None, None


def obter_old_price(driver):
    old_price_xpaths = [
        '//*[@id="__next"]/div/main/section[4]/div[4]/div/div/div/p[1]',
        '//*[@id="__next"]/div/main/section[4]/div[5]/div/div/div/p[1]',
        '//*[@id="__next"]/div/main/section[4]/div[6]/div[1]/div/div/p',
        '//*[@id="__next"]/div/main/section[4]/div[5]/div[1]/div/div/p[1]',
        '//*[@id="__next"]/div/main/section[4]/div[6]/div/div/div/p',
    ]
    for xpath in old_price_xpaths:
        try:
            old_price_element = driver.find_element(By.XPATH, xpath)
            old_price = old_price_element.text

            if old_price:
                return old_price
        except NoSuchElementException as e:
            print(f"Exception while trying xpath {xpath}: {e}")
    return None


def obter_discount_price(driver):
    discount_price_xpaths = [
        '//*[@id="__next"]/div/main/section[4]/div[4]/div/div/div/div/p',
        '//*[@id="__next"]/div/main/section[4]/div[4]/div/div/div/div/p[2]',
        '//*[@id="__next"]/div/main/section[4]/div[5]/div[1]/div/div/div/p',
    ]
    for xpath in discount_price_xpaths:
        try:
            discount_price_element = driver.find_element(By.XPATH, xpath)
            discount_price = discount_price_element.text

            if discount_price:
                return discount_price
        except NoSuchElementException as e:
            print(f"Exception while trying xpath {xpath}: {e}")
    return None


def obter_installment_value(driver):
    installment_value_xpaths = [
        '//*[@id="__next"]/div/main/section[4]/div[4]/div/div/div/p[2]',
        '//*[@id="__next"]/div/main/section[4]/div[4]/div/div/div/div/p[2]',
        '//*[@id="__next"]/div/main/section[4]/div[5]/div[1]/div/div/p[2]',
    ]
    for xpath in installment_value_xpaths:
        try:
            installment_value_element = driver.find_element(By.XPATH, xpath)
            installment_value = installment_value_element.text

            if installment_value:
                return installment_value
        except NoSuchElementException as e:
            print(f"Exception while trying xpath {xpath}: {e}")
    return None


def obter_informacoes_produto(driver, product_link):
    try:
        driver.get(product_link)
        title, image_url = obter_titulo_e_imagem(driver)
        old_price = obter_old_price(driver)
        discount_price = obter_discount_price(driver)
        installment_value = obter_installment_value(driver)
        return title, image_url, old_price, discount_price, installment_value
    except Exception as e:
        print(f"Erro ao obter informações do produto: {e}")
        return None, None, None, None, None


# Função para montar a mensagem----------------------------------------------------------------
def montar_mensagem(
    product_title, old_price, discount_price, installment_value, current_url, group_link
):
    try:
        # Construir a parte da mensagem relacionada ao preço
        price_message = ""
        if old_price:
            price_message += f"de: {old_price}\n\n"
        if discount_price:
            price_message += f"por apenas {discount_price} no PIX\n"
        if installment_value:
            price_message += f"{installment_value}\n"

        # Construir a mensagem completa
        message = (
            f"{product_title}\n\n\n"
            f"{price_message}\n"
            f"Link do produto: {current_url}\n\n"
            f"Link do grupo de ofertas: {group_link}\n"
        )

        return message

    except Exception as e:
        print(f"Erro ao montar mensagem: {e}")
        return None


def pesquisar_links_e_enviar_mensagens(driver, product_links, group_link):
    for product_link in product_links:
        try:
            (
                product_title,
                image_url,
                old_price,
                discount_price,
                installment_value,
            ) = obter_informacoes_produto(driver, product_link)

            if product_title is not None:
                current_url = encurtar_url(driver.current_url)
                message = montar_mensagem(
                    product_title,
                    old_price,
                    discount_price,
                    installment_value,
                    current_url,
                    group_link,
                )
                enviar_mensagem_com_imagem(message, image_url)

            time.sleep(7)

        except Exception as e:
            print(f"Erro ao pesquisar o link {product_link}: {e}")



chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


group_link = "https://t.me/+yHMWypDzEJs2YWEx"


product_links = [
    "https://divulgador.magalu.com/USAl68Vr",
    "https://divulgador.magalu.com/7FwfoTSp",
    "https://divulgador.magalu.com/FUnD995O",
    "https://divulgador.magalu.com/9MvoiXzo",
    "https://divulgador.magalu.com/xnol5WsW",
    "https://divulgador.magalu.com/ngR8JoV1",
    "https://divulgador.magalu.com/R=lKaBzI",

]

pesquisar_links_e_enviar_mensagens(driver, product_links, group_link)


driver.quit()
