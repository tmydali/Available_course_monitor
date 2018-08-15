# Available_course_monitor
*Line介面版本*

## 概要
+ 這個版本以Line帳號作為輸入輸出介面
+ 使用gunicorn架設於heroku上，可同時處理多人的請求
+ 伺服器架設於:https://dashboard.heroku.com/apps/lin-course-monitor
+ 根據使用者的輸入，區分為五種狀況來回復訊息
  1. 課程尚有餘額
  1. 課程目前沒有餘額
  1. 查無此課程
  1. 輸入格式錯誤
  1. 系統錯誤
+ 待改進的部分
  - 使用者無法反悔已監控的課程
  - webhook伺服器偶爾會無回應而timeout
  - 尚無機制記錄使用者的使用狀況
  
## 內容
#### Pipfile
專案所處的虛擬環境中，需要使用的package (用pipenv打包)

#### Pipfile.lock
上述package的詳細資料，如版本等 (與Pipfile一起產生)

#### Procfile
告訴heroku要執行哪些程式

#### app.py
由Line官方提供的示範程式修改而成
使用flask建立的框架，主要差別在機器人回復訊息時必須使用push物件，而非示範程式中的reply
LineBot針對python的文件：https://github.com/line/line-bot-sdk-python
需先至Line Developers 申請企業帳號，得到兩組密鑰後填入程式中指定位置，以環境變數的方式較為安全
- handle_message(event)
  篩選使用者輸入的訊息是否符合格式，符合則將訊息傳入monitor模組
  
### CourseMonitor
#### __init__
#### monitor
監控課程的主要程式，由單機版crawler.ipynb衍生而來
#### sender
#### websiteParser
    
