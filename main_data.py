from libraries import *


def get_main_data(url, spreadsheet_id):
    start_time = time.time()
    browser = create_browser()

    for item in range(0, 1009, 24):
        if item == 1008:
            item = 1000
        print("\tITEM: " + str(item))
        browser.get(url + f"{item}/")
        if item == 0:
            sleep(10)
        else:
            sleep(3.5)

        category = url.split('/')
        data = get_data(browser, category[3])
        print("\tDATA: " + str(len(data)))
        add_data(data, spreadsheet_id)

    print("\n\tSpent time on the script execution: " + str(time.time() - start_time))
    sleep(10)
    browser.close()
    browser.quit()

def create_browser():
    browser = uc.Chrome(use_subprocess=True)
    browser.maximize_window()
    return browser

def send_command(driver, cmd, params):
    post_url = driver.command_executor._url + '/session/{0:s}/chromium/send_command_and_get_result'.format(
        driver.session_id)
    response = driver.command_executor._request('POST', post_url, json.dumps({'cmd': cmd, 'params': params}))
    if ('status' in response) and response['status']:
        raise Exception(response.get('value'))

def get_data(browser, category):
    data = []

    for human in browser.find_elements(by=By.CLASS_NAME, value="result"):
        name = human.find_element(by=By.CLASS_NAME, value="col-sm-7 > a > h3").text
        location = ""
        direct = human.find_element(by=By.CLASS_NAME, value="img-avatar.align-top.m-3 > div > a").get_attribute("href")
        photo = human.find_element(by=By.CLASS_NAME, value="img-avatar.align-top.m-3 > div > a > img").get_attribute("src")
        description = human.find_element(by=By.CLASS_NAME, value="about").text

        media = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        for social in human.find_elements(by=By.CSS_SELECTOR, value="div.result-container.col-sm-7 > div.float-right.profile-social > a"):
            match social.get_attribute("data-type"):
                case "website": column = 0
                case "amazon": column = 1
                case "twitter": column = 2
                case "tiktok": column = 3
                case "instagram": column = 4
                case "twitch": column = 5
                case "discord": column = 6
                case "etsy": column = 7
                case "facbook": column = 8
                case "youtube": column = 9
                case "snapchat": column = 10
                case "pinterest": column = 11
                case "fansly": column = 12
                case "pornhub": column = 13
                case "patreon": column = 14
                case _: column = 15

            action = ActionChains(browser)
            for _ in range(3):
                hover = action.move_to_element(social)
                hover.perform()
                if social.get_attribute("href") == None:
                    continue

                if media[column] == "":
                    media[column] = social.get_attribute("href")
                else:
                    media[column] = media[column] + "\n" + social.get_attribute("href")
                break

        data.append([
            category, name, location, direct, photo, description, *media
        ])

    return data

def add_data(values, spreadsheet_id):
    gs = GoogleSheet(spreadsheet_id)
    range = "free onlyfans!A1"
    gs.appendRangeValues(range, values)


