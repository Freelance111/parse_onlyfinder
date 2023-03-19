from libraries import *

def get_additional_data(spreadsheet_id):
    start_time = time.time()
    browser = create_browser()

    try:
        gs = GoogleSheet(spreadsheet_id)
        ran = "free onlyfans!D2:D10000"
        urls = gs.getData(ran)
        if urls is None: return

        for index, url in enumerate(urls):
            if url is None: continue
            if len(url[0].split('/')) > 4: continue
            browser.get(*url)
            if index == 0: sleep(5)
            sleep(7)
            try:
                more_info = browser.find_element(by=By.CLASS_NAME, value="link-trunc")
                browser.execute_script("arguments[0].click();", more_info)

                location, site, amazon = get_data(browser)
                print(str(*url) + " --- " + str(location) + ' | ' + str(site) + ' | ' + str(amazon))

                raw = int(urls.index(url)) + 2
                add_data(location, site, amazon, raw, gs)
            except NoSuchElementException as ex:
                if len(browser.find_elements(by=By.NAME, value="email")) > 0:
                    print("Проблема с входом возникла на url номер --- " + str(index+1))
                    browser.close()
                    browser.quit()
                    browser = create_browser()
    except TypeError:
        pass
    except Exception as ex:
        print(ex)
    finally:
        print("\n\tSpent time on the script execution: " + str(time.time() - start_time))
        sleep(10)
        browser.close()
        browser.quit()

def create_browser():
    options = uc.ChromeOptions()
    options.add_argument('"--disable-notifications"')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = uc.Chrome(use_subprocess=True, options=options)
    browser.maximize_window()
    ua = UserAgent()
    user_agent = ua.random
    send_command(browser, 'Network.setUserAgentOverride', {'userAgent': user_agent})
    return browser

def send_command(driver, cmd, params):
    post_url = driver.command_executor._url + '/session/{0:s}/chromium/send_command_and_get_result'.format(
        driver.session_id)
    response = driver.command_executor._request('POST', post_url, json.dumps({'cmd': cmd, 'params': params}))
    if ('status' in response) and response['status']:
        raise Exception(response.get('value'))

def get_data(browser):
    location = None
    site = None
    amazon = None

    tmp = browser.find_element(by=By.CLASS_NAME, value='g-truncated-text')
    for index, div in enumerate(tmp.find_elements(by=By.CLASS_NAME, value='b-user-info__detail')):
        if index == 0:
            try:
                location = div.find_element(by=By.TAG_NAME, value='p').text
                continue
            except NoSuchElementException:
                pass

        try:
            link = div.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        except NoSuchElementException:
            continue
        link = link.replace("https://onlyfans.com/away?url=", "")
        if link:
            list_link = link.split('/')
            if "amazon" in list_link[2]:
                amazon = link
            elif "instagram" in list_link[2]:
                pass
            elif "onlyfans" in list_link[2]:
                pass
            else:
                site = link

    return location, site, amazon

def add_data(location, site, amazon, raw, gs):
    data = [
        {'range': f"free onlyfans!C{raw}", 'values': [[location]]},
        {'range': f"free onlyfans!G{raw}", 'values': [[site]]},
        {'range': f"free onlyfans!H{raw}", 'values': [[amazon]]}
    ]
    gs.batchUpdateRangeValues(data)

