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
### /
#### Pipfile
專案所處的虛擬環境中，需要使用的package (用pipenv打包)

#### Pipfile.lock
上述package的詳細資料，如版本等 (與Pipfile一起產生)

#### Procfile
告訴heroku要執行哪些程式

#### app.py
webhook主要運作程式，由Line官方提供的示範程式修改而成
使用flask建立的框架，主要差別在機器人回復訊息時必須使用push物件，而非示範程式中的reply
LineBot針對python的文件：https://github.com/line/line-bot-sdk-python
需先至Line Developers 申請企業帳號，得到兩組密鑰後填入程式中指定位置，以環境變數的方式較為安全
+ handle_message(event)
  篩選使用者輸入的訊息是否符合格式，符合則將訊息傳入monitor模組，`event`物件由webhook取得
  
### /CourseMonitor
#### \_\_init\_\_.py
#### websiteParser.py
解析html網站
+ get_site(url)
  - *url*：待解析的html網址
  模組使用BeautifulSoup4
+ Department_list()
  解析成大課程查詢首頁後，將系所代碼及其對應的課程網址存入字典，形式為 `{系所代碼 : 網址}` ，回傳字典
+ Course_list(DeptNo, dept_dict)
  - *DeptNo*：系所代碼，由`event.message.text`取得
  - *dept_dict*：系所代碼與其對應網址，由`Department_list()`取得
  
  解析指定系所的課程網站，最後以`{課程代碼 : [課程中文名稱, 課程餘額]}`字典的形式儲存，回傳字典
#### sender.py
由Line官方示範程式中獨立出來，以便其他module呼叫，用來送出訊息至Line用戶
+ message_sender(to, text)
  - *to*：傳訊對象ID，由`event.sourse.user_id`取得
  - *text*：欲傳送的訊息
  
  示範程式中使用`reply()`方法，但此方法必須在收到訊息後數秒內回覆，故無法滿足監控需求，改用`push()`方法
#### monitor.py
監控課程的主要程式，由單機版crawler.ipynb衍生而來
+ multithrd(userID, DeptNo, CrsNo, dept)
  - *userID*：使用者專用ID，由U開頭的33碼組成，藉由webhook傳進的`event.sourse.user_id`取得
  - *DeptNo*：系所代碼，由`event.message.text`取得
  - *CrsNo* ：科目代碼，由`event.message.text`取得
  - *dept*  ：所有系所課程列表的網址，由websiteParser.py中的`Department_list()`取得，每一次接收到訊息後新建一個執行續，來獨立執行    `checkCourse()`
+ checkCourse(userID, DeptNo, CrsNo, dept)
  - *參數同上*
  
  呼叫`Course_list()`來取出所指定的系所課程清單，首先查詢所指定的課程代碼是否存在，不存在則呼叫`sender()`傳回訊息提醒使用者重新輸入，存在則進入判斷，課程若有餘額則傳回有餘額的訊息，沒有則傳回無餘額的訊息，並且固定時間抓資料，直到有餘額為止
    
