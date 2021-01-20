from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests
import pandas as pd
import selenium
import datetime

# url の初期値設定（ログイン／社員プロファイル）
login_url = 'https://salesdemo.successfactors.eu/login?company=SFPART033321'
profile_url = 'https://salesdemo.successfactors.eu/xi/ui/pages/empfile/liveprofile.xhtml?selected_user={}'

login_user = '9990001'
login_pw = 'test02'

# 処理日のセット
today_date = str(datetime.date.today())

# アップロードパス指定／ファイル名指定
import_file_path = './input.xlsx'                  # 読込みファイルパス
export_file_path = './output/'                     # 出力ファイルパス
excel_sheet_name = 'data'                          # 編集したいシート名
file_name = 'output_{0}.xls'.format(today_date)    # ファイル名生成

# クロームドライバーの実行ファイルパス指定
chrome_path = r'C:\Users\i0150\Desktop\driver\chromedriver'

# 各種オプション設定
options = Options()
# options.add_argument('--headless')                 # headlessモードを使用する
options.add_argument('--incognito')                # シークレットモードモードを使用する
options.add_argument('--disable-gpu')              # headlessモードで暫定的に必要なフラグ(そのうち不要になる)
options.add_argument('--disable-extensions')       # すべての拡張機能を無効にする。ユーザースクリプトも無効にする
options.add_argument('--proxy-server="direct://"') # Proxy経由ではなく直接接続する
options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
# options.add_argument('--start-maximized')          # 起動時にウィンドウを最大化する

# driver 関数の呼び出し
driver = webdriver.Chrome(executable_path = chrome_path, options=options)

# ログイン画面へのアクセス
driver.get(login_url)
driver.implicitly_wait(10)

# ログインユーザーID／PWセット
user_name = driver.find_element_by_id('__input1-inner')
user_name.send_keys(login_user)
password = driver.find_element_by_id('__input2-inner')
password.send_keys(login_pw)
login_btn = driver.find_element_by_id('__button2-inner')
login_btn.click()


# ファイル読込み処理
df = pd.read_excel(import_file_path, sheet_name = excel_sheet_name)

# 処理対象ユーザーのセット
menbers = df['uid'].unique()

index = 0
# ユーザー毎プロファイルアクセス
for menber in menbers:
    driver.implicitly_wait(3)
    target_user = menber
    target_user_profile = profile_url.format(target_user)

    # 対象ユーザーの社員プロファイル表示
    driver.get(target_user_profile)

    # bs4 による要素取得
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 職務情報タブをクリック
    sleep(5)
    menu_tab_select = driver.find_element_by_css_selector('#__xmlview0--objectPage-anchBar-__section1-__xmlview0--objectPage-1-anchor-BDI-content')
    menu_tab_select.click()

    # スクショを撮る
    file_name = "スクショ_{0}_{1}.png".format(today_date, menber)
    driver.save_screenshot("./screen_shot/" + file_name)

    # 処理対象者
    print(menber)    
    index += 1
    sleep(1)  

driver.quit()

print('処理対象人数：' + str(index))