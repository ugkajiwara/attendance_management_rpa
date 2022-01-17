#github用

# chrome ver 97.*
# coding: UTF-8

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

notices = []

# WebDriver のオプションを設定する
options = webdriver.ChromeOptions()
options.add_argument('--headless')

print('connectiong to remote browser...')
driver = webdriver.Chrome(options=options)

###ここからデータを取ってくるページ#######################################################

driver.get('＃＃ログインページのURL＃＃')
print(driver.current_url + 'に接続しています...')

# ID,pass入力
driver.find_element(By.NAME,'login_name').send_keys('＃＃ログインID＃＃')
driver.find_element(By.NAME,'password').send_keys('＃＃ログインパスワード＃＃')
driver.find_element(By.CSS_SELECTOR,"[type='submit']").send_keys(Keys.ENTER)

print('HPログイン中...')
sleep(1)
date = input('取得したい日付を入力してください（例）20220101:')
driver.get('＃＃打刻データを取得するページのURL＃＃?date=' + date)
print(date + 'の実績管理に移動中...')
sleep(1)

soup = BeautifulSoup(driver.page_source, "lxml")

#名前
names = soup.select("#attend-table td:nth-child(1)")

#出勤時間
attend_times = soup.select("#attend-table td:nth-child(2)")

#退勤時間
leave_times = soup.select("#attend-table td:nth-child(3)")

#休憩時間
break_times = soup.select("#attend-table td:nth-child(4)")

#ヘルプ店舗
help_stores = soup.select("#attend-table td:nth-child(5)")

###ここからAirShift#######################################################

driver.get('＃＃AirShiftログインページのURL＃＃')
print(driver.current_url + 'に接続しています')

#AirShiftにログイン
driver.find_element(By.ID, "account").send_keys('＃＃ログインID＃＃')
driver.find_element(By.ID, "password").send_keys('＃＃ログインパスワード＃＃')
driver.find_element(By.CSS_SELECTOR,"[type='submit']").send_keys(Keys.ENTER)
sleep(1)

#店舗選択
driver.find_elements(By.XPATH,'//a')[1].click()

sleep(1)

driver.get('＃＃データを入力するページのURL＃＃' + date)
driver.find_element(By.CLASS_NAME,'label___1541MBG8').click()

sleep(1)

soup = BeautifulSoup(driver.page_source, "lxml")

#名前
airshift_names = soup.select(".staffName___31nIRozl")

x = 0 #実績管理側の配列番号
for name in names: #namesを回す処理
    i = 1 #airshift側の配列番号

    name = str(name).replace('<td>','')
    name = str(name).replace('</td>','')
    name = str(name).replace('　',' ')

    help_store = help_stores[x]
    help_store = str(help_store).replace('<td>','')
    help_store = str(help_store).replace('</td>','')
    help_store = str(help_store).replace( '\n' , '' )
    if help_store != '': #ヘルプ店舗の場合スキップ
        x += 1
        print('別店舗ヘルプのため'+ name +'の入力をスキップします')
        continue

    for airshift_name in airshift_names: #nameに合致するairshift_nameを探す
        
        airshift_name = str(airshift_name).replace('<span class="staffName___31nIRozl">','')
        airshift_name = str(airshift_name).replace('</span>','')
        
        if name == airshift_name: #合致するものが見つかった時の処理

            #airshift側の表示シフト時間
            airshift_shift_path = ".summaryTableWrapper___2eKGavN6 > div tbody tr:nth-child(" + str(i) + ") td:nth-child(1) div" 
            airshift_shift = soup.select(airshift_shift_path)

            #バグるので初期化
            airshift_shift_break_start = ''
            airshift_shift_break_end = ''
            #airshift上の出勤退勤休憩開始終了時間取得処理
            if len(airshift_shift) > 1: #airshift上において休憩がある場合の処理
                airshift_shift[0] = str(airshift_shift[0]).replace('<div>','')
                airshift_shift[0] = str(airshift_shift[0]).replace('</div>','')
                airshift_shift[0] = str(airshift_shift[0]).replace('〜','')
                airshift_shift[0] = str(airshift_shift[0]).replace('<!-- -->','')
                airshift_shift[0] = str(airshift_shift[0]).replace(':','')

                airshift_shift[1] = str(airshift_shift[1]).replace('<div>','')
                airshift_shift[1] = str(airshift_shift[1]).replace('</div>','')
                airshift_shift[1] = str(airshift_shift[1]).replace('〜','')
                airshift_shift[1] = str(airshift_shift[1]).replace('<!-- -->','')
                airshift_shift[1] = str(airshift_shift[1]).replace(':','')

                airshift_shift_start = airshift_shift[0][:4]
                airshift_shift_break_start = airshift_shift[0][4:]
                airshift_shift_break_end = airshift_shift[1][:4]
                airshift_shift_end = airshift_shift[1][4:]

            elif len(airshift_shift) == 1:
                airshift_shift = str(airshift_shift[0]).replace('<div>','')
                airshift_shift = str(airshift_shift).replace('</div>','')
                airshift_shift = str(airshift_shift).replace('〜','')
                airshift_shift = str(airshift_shift).replace('<!-- -->','')
                airshift_shift = str(airshift_shift).replace(':','')

                airshift_shift_start = airshift_shift[:4]
                airshift_shift_end = airshift_shift[4:]

            else: #シフトに入ってないのに、出勤した人
                airshift_shift = ''


          #break_time他加工処理
            attend_time = str(attend_times[x]).replace('<td>','')
            attend_time = str(attend_time).replace('</td>','')
            attend_time = str(attend_time).replace(':','')
           #30分単位変換処理
            if 0 < int(attend_time) % 100 <= 30:
                attend_time = attend_time[:-2]
                attend_time += '30' 
            elif 30 < int(attend_time) % 100:
                attend_time = attend_time[:-2]
                attend_time += '00' 
                attend_time = int(attend_time) + 100
                attend_time = str(attend_time)

            leave_time = str(leave_times[x]).replace('<td>','')
            leave_time = str(leave_time).replace('</td>','')
            leave_time = str(leave_time).replace(':','')

            if leave_time == '': #退勤時間を打刻しわすれた時の処理
                leave_time = str('2400')
                notices.append(airshift_name + 'の退勤時間の打刻がされていないため、ダミーデータで24:00を入力しています')

           #30分単位変換処理
            if 0 <= int(leave_time) % 100 < 30:
                leave_time = leave_time[:-2]
                leave_time += '00' 
            else:
                leave_time = leave_time[:-2]
                leave_time += '30' 


            break_time = str(break_times[x]).replace('<td>','')
            break_time = str(break_time).replace('</td>','')
            break_time = str(break_time).replace(':','')
           #30分単位変換処理
            if break_time != '':
                if 0 < int(break_time) % 100 <= 30:
                    break_time = break_time[:-2]
                    break_time += '30' 
                elif 30 < int(break_time) % 100:
                    break_time = break_time[:-2]
                    break_time += '00' 
                    break_time = int(break_time) + 100
                    break_time = str(break_time)



         #出勤時間入力処理
            start_xpath = "//tbody/tr[position()="+ str(i) +"]/td[position()=6]/div[position()=1]/span/input"
            start = driver.find_element(By.XPATH,start_xpath)

            if  break_time == '' and int(leave_time) - int(attend_time) > 500: #5時間より長く働いた場合
                assumption_attend_time = int(attend_time) - 100
                assumption_attend_time = str(assumption_attend_time)
                start.send_keys(assumption_attend_time)
                print(airshift_name + 'に出勤時間' + assumption_attend_time + 'を入力しました')
            else:
                start.send_keys(attend_time)
                print(airshift_name + 'に出勤時間' + attend_time + 'を入力しました')

            if int(attend_time) != int(airshift_shift_start):
                notices.append(airshift_name + 'の出勤時間のデータに相違があります')

            
         #退勤時間入力処理
            end_xpath = "//tbody/tr[position()="+ str(i) +"]/td[position()=6]/div[position()=2]/span/input"
            end = driver.find_element(By.XPATH,end_xpath)

            if int(leave_time) >= 2400: #2430などの値は不適切と判断されるため
                leave_time_r = int(leave_time) % 2400
                leave_time_r = str(leave_time_r)
                end.send_keys(leave_time_r)

                if int(leave_time_r) != int(airshift_shift_end):
                    notices.append(airshift_name + 'の退勤時間のデータに相違があります')
            else:
                end.send_keys(leave_time)

                if int(leave_time) != int(airshift_shift_end):
                    notices.append(airshift_name + 'の退勤時間のデータに相違があります')

            print(airshift_name + 'に退勤時間' + leave_time + 'を入力しました')


         #休憩時間に関する処理
            #休憩開始時間のフォーム
            b_start_xpath = "//tbody/tr[position()="+ str(i) +"]/td[position()=7]/div/div[position()=1]/span/input"
            b_start = driver.find_element(By.XPATH,b_start_xpath)

            #休憩終了時間のフォーム
            b_end_xpath = "//tbody/tr[position()="+ str(i) +"]/td[position()=7]/div/div[position()=2]/span/input"
            b_end = driver.find_element(By.XPATH,b_end_xpath)

            if break_time != '' and airshift_shift_break_start != '': #シフト上休憩があり、実際に休憩した時
                b_start.send_keys(airshift_shift_break_start)
                print(airshift_name + 'に休憩開始時間' + airshift_shift_break_start + 'を入力しました')
                break_time_end = int(airshift_shift_break_start) + int(break_time)

                if str(break_time_end)[-2:] == '60': #XX60の形になってしまった場合
                    break_time_end = break_time_end[:-2]
                    break_time_end += '00' 
                    break_time_end = int(break_time_end) + 100
                    break_time_end = str(break_time_end)

                b_end.send_keys(break_time_end)
                print(airshift_name + 'に休憩終了時間' + str(break_time_end) + 'を入力しました')

                if int(break_time) != int(airshift_shift_break_end) - int(airshift_shift_break_start):
                    notices.append(airshift_name + 'の休憩した時間のデータに相違があります')

            elif break_time != '' and airshift_shift_break_start == '': #シフト上休憩がなかったが、実際休憩した時
                b_start.send_keys(attend_time)
                print(airshift_name + 'に休憩開始時間' + attend_time + 'を入力しました（仮入力で、出勤時間と休憩開始時間を被らせています）')
                break_time_end = int(attend_time) + int(break_time)

                if str(break_time_end)[-2:] == '60': #XX60の形になってしまった場合
                    break_time_end = break_time_end[:-2]
                    break_time_end += '00' 
                    break_time_end = int(break_time_end) + 100
                    break_time_end = str(break_time_end)

                b_end.send_keys(break_time_end)
                print(airshift_name + 'に休憩終了時間' + str(break_time_end) + 'を入力しました') 

            elif break_time == '' and int(leave_time) - int(attend_time) > 500: #5時間より長く働いた場合
                b_start.send_keys(assumption_attend_time)
                print(airshift_name + 'に休憩開始時間' + assumption_attend_time + 'を入力しました') 
                b_end.send_keys(attend_time)
                print(airshift_name + 'に休憩終了時間' + attend_time + 'を入力しました※５時間より長く働いていてかつ休憩をとっていないため、出勤時間を1時間早め、1時間の休憩をしたことにしました') 
            


            break
        i += 1
    x += 1


button = "//div[@id='centerSpacer']//div[@class='root___F-opJFUK']/div[2]/button"

sleep(1)

driver.find_element(By.XPATH,button).click()
print('実績管理より抽出した勤務時間をairshiftに保存中...')


#エラー・相違があったら配列にぶち込んでループ処理で出力
if notices != []:
    print('！！！注意！確認してください！！！')
    for notice in notices:
        print(notice)

# ブラウザを終了する
driver.close()
driver.quit()

print('処理が正常に完了しました')