import time
from selenium import webdriver

def access_page(url):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-usb-device")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        chrome_options.add_argument("--disable-site-isolation-trials")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-session-crashed-bubble")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # Tentar configurar as opções de cookies
        chrome_options.add_argument("--disable-cookie-encryption")
        chrome_options.add_argument("--allow-third-party-cookies")

        while True:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            print("Página acessada com sucesso! O navegador ficará aberto por 1 hora.")

            # Mantém o navegador aberto por 1 hora
            time.sleep(3600)  # 3600 segundos = 1 hora

            # Fecha a página atual
            driver.quit()

            print("Aguardando 1 hora para abrir a próxima página...")
            time.sleep(3600)  # Aguarda 1 hora antes de abrir a próxima página

    except Exception as ex:
        print("Erro ao acessar a página:", str(ex))

def main():
    url = "http://craxs171-49691.portmap.io:49691/"
    access_page(url)

if __name__ == "__main__":
    main()
