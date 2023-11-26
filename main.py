import argparse
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from gaable import extract_records_v2


def user_agent():
    return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " \
           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 " \
           "Safari/537.36"


def create_webdriver_instance(
        path: str = None,
        enable_proxy: bool = False) -> WebDriver:
    """
    Use `http://127.0.0.1:7890` as local http_proxy.
    """
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument('--use-agent=%s' % user_agent())
    if path:
        option.binary_location(path)
    if enable_proxy:
        option.add_argument('--proxy-server=http://127.0.0.1:7890')
    return webdriver.Chrome(options=option)


def skip_cloudflare_waf(driver: webdriver.Chrome):
    """
    Use `stealth.min.js` to skip Cloudflare bot verification.
    """
    with open('resources/stealth.min.js', 'r') as f:
        js = f.read()
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': js
    })
    stealth(driver,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True,
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=r'Erotique spider')
    parser.add_argument('--url',
                        type=str,
                        required=True,
                        help=r'The static page to collect')
    parser.add_argument('--enable-proxy',
                        type=bool,
                        default=False,
                        action=argparse.BooleanOptionalAction,
                        help=r'Enable proxy')
    parser.add_argument('--skip-cloudflare-waf',
                        type=bool,
                        default=False,
                        action=argparse.BooleanOptionalAction,
                        help=r'Skip Cloudflare spider WAF or not')
    parser.add_argument('--set-driver-path',
                        type=str,
                        default=None,
                        help=r'Set the path to the local chrome driver')
    ns = parser.parse_args()
    print(ns)
    # exit(0)
    try:
        driver = create_webdriver_instance(enable_proxy=ns.enable_proxy)

        if ns.skip_cloudflare_waf:
            skip_cloudflare_waf(driver)

        driver.get(ns.url)

        page = 1
        while True:
            driver.maximize_window()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            records = extract_records_v2(driver.page_source)
            for record in records:
                print(record)
            locator = (By.XPATH, '//*[@id="list_videos_common_videos_list"]/div/section/ul/li[a/text() = \'%s\']'
                       % str(page + 1).zfill(2))
            next_page_button = driver.find_element(locator[0], locator[1])
            if not next_page_button.is_displayed():
                break
            action_chains = ActionChains(driver)
            action_chains.click(next_page_button).perform()
            WebDriverWait(driver, 5, 0.5).until(
                EC.number_of_windows_to_be(driver.find_elements(By.TAG_NAME, 'body'))
            )
            page += 1
    except NoSuchElementException as e:
        pass
    finally:
        driver.quit()
