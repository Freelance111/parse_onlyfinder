from libraries import *
import pickle

def main():
    browser = create_browser()
    browser.get("https://onlyfans.com/")
    sleep(10)
    for cookie in pickle.load(open(f"cookies", "rb")):
        browser.add_cookie(cookie)


    sleep(60)
def create_browser():
    browser = uc.Chrome(use_subprocess=True)
    browser.maximize_window()
    return browser

if __name__ == '__main__':
    main()