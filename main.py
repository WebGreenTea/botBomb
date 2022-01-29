#from math import trunc
#from numpy.lib.utils import who
import pyautogui as bot
import time
from datetime import datetime
import logging
import codecs
import re
import win32api
import threading
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image,ImageChops,ImageDraw
import requests
import random
import subprocess
import sys
import os
import hashlib,binascii
import configparser as cf
#from songline import Sendline


class Sline():
    def __init__(self,token):
        self.token = token

    #ข้อความ
    def sendtext(self,message):
        payload = {'message':message}
        self._lineNotify(payload)

    #รูปภาพ
    def sendPic(self,path,mess=" "):
        payload = {'message': mess}
        self._lineNotify(payload,img=open(path,'rb'))

    #ส่งแจ้งเตือน
    def _lineNotify(self,payload,img=None):
        url = 'https://notify-api.line.me/api/notify'
        token = self.token
        headers = {'Authorization':'Bearer '+token}
        if(img):
            img = {'imageFile': img}
        return requests.post(url, headers=headers , data = payload, files=img)

class cap():
    def __init__(self,maxAcc):
        self.root = Tk()
        self.root.geometry('200x200+100+100')        
        self.root.overrideredirect(True)
        self.root.config(bg = '#add123')
        self.root.wm_attributes('-transparentcolor','#add123')
        self.root.attributes('-topmost',True)
        self.screen = []
        self.currAcc = 1
        self.maxAcc = maxAcc
        pass

    def start(self):
        borderbuttom = Frame(self.root,highlightbackground='red',highlightthickness=10)
        borderbuttom.pack(side=TOP,fill=X)

        borderleft = Frame(self.root,highlightbackground='red',highlightthickness=10)
        borderleft.pack(side=LEFT,fill=Y)

        borderright = Frame(self.root,highlightbackground='red',highlightthickness=10)
        borderright.pack(side=RIGHT,fill=Y)

        borderbuttom = Frame(self.root,highlightbackground='red',highlightthickness=10)
        borderbuttom.pack(side=BOTTOM,fill=X)

        #title_bar = Frame(root,relief='raised')
        #title_bar.pack(anchor='nw')
        img = Image.open("simg/h.png")
        img = img.resize((30,30))
        img = ImageTk.PhotoImage(img)
        title_label = Label(self.root,image=img)
        title_label.pack(anchor='nw')
        title_label.bind("<B1-Motion>",self.move_app)

        self.select = Button(self.root,text=f"Get position\n{self.currAcc}/{self.maxAcc}", font=('tahoma',20),command=self.click,bg='green',fg='white')
        self.select.pack(expand = True)
        #select['text'] = "test"
        Button(self.root,text='exit',command=self.root.destroy).pack()

        img2 = Image.open("simg/resize.png")
        img2 = img2.resize((30,30))
        img2 = ImageTk.PhotoImage(img2)
        resi =  Label(self.root,image=img2)
        resi.place(relx=1.0, rely=1.0, anchor="se")
        resi.bind("<B1-Motion>", self.OnMotion)
        self.root.mainloop()
        return self.screen

    def click(self):
        
        
        box = (self.root.winfo_x(),self.root.winfo_y(),self.root.winfo_width(),self.root.winfo_height())
        self.screen.append(box)
        print(box)
        self.currAcc+=1
        self.select['text'] = f"Get position\n{self.currAcc}/{self.maxAcc}"
        if(self.currAcc > self.maxAcc):
            self.root.destroy()
        #print(self.root.winfo_x(), self.root.winfo_y())
        #print(self.root.winfo_width(),self.root.winfo_height())

    def move_app(self,e):
        self.root.geometry(f'+{e.x_root}+{e.y_root}')
        pass

    def OnMotion(self,event):
        x1 = self.root.winfo_pointerx()
        y1 = self.root.winfo_pointery()
        x0 = self.root.winfo_rootx()
        y0 = self.root.winfo_rooty()
        if(x1 >= x0+50 and y1 >= y0+50):
            self.root.geometry("%sx%s" % ((x1-x0),(y1-y0)))
        return

HWID = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

file = codecs.open('lineToken.txt','r','utf8')
token = ''
try:
    token = file.readline()
except:
    token = ''
if(len(token) != 43):
    token = ''
file.close()

SONGLINE = False
try:
    if(len(token) == 43):
        LINE = Sline(token)
        SONGLINE = True
except:
    pass

def CK():
    key = ''
    try:
        file = codecs.open('key.txt','r','utf8')
        key = file.readline()
    except:
        print('Failed to read key')
        sys.exit()
    file.close()
    
    salt = b'1334#bomb_byWGT'
    hwid = bytes(HWID, 'utf-8')
    key = bytes(key, 'utf-8')

    enC = hashlib.pbkdf2_hmac('sha256',hwid,salt,100000)
    enC = binascii.hexlify(enC)
    if(enC != key):
        print('Invalid Key')
        os.system("pause")
        sys.exit()
        
CK()
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

# our first handler is a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler_format = '%(asctime)s | %(message)s'
console_handler.setFormatter(logging.Formatter(console_handler_format))
logger.addHandler(console_handler)

# the second handler is a file handler
file_handler = logging.FileHandler('botLog.log')
file_handler.setLevel(logging.DEBUG)
file_handler_format = '%(asctime)s | %(levelname)s | %(lineno)d: %(message)s'
file_handler.setFormatter(logging.Formatter(file_handler_format))
logger.addHandler(file_handler)
file = codecs.open('config.txt','r','utf8')

logger.debug('loading config... ')
i = 0
configchecklist = ['mouseMoveSpeed','refreshMap','looplimit','delayMainloop','loginlimit','confidence','numOfAcc','zoom']
config = []
for line in file:
    if(re.split('=|#',line)[0] == ''):
        continue
    data = re.split('=|#',line)[1]
    try:
        data = float(data)
        logger.debug(f'{configchecklist[i]} = {data}')
        config.append(data)
    except:
        logger.error('config failed')
        break
    i+=1

file.close()
#waitlogin = 8 #เวลา(วินาที)ที่รอโหลดเข้าเกม


mouseMoveSpeed = config[0] #ความเร็วการเคลื่อนเม้า ปรับน้อยเร็ว ปรับมากช้า !แนะนำที่ 0.3!
refreshMap = int(config[1]) #เวลา(นาที) ที่จะคอยคลิกออกจาก map แล้วเข้าใหม่ เพื่อทำให้ตัวละครกระจายตัว,แก้ตัวละครที่บัคไม่ยอมวางระเบิด และลดโอกาสเกิด unknow

looplimit = int(config[2]) #จำนวนรอบสูงสุดที่ระบบจะวนหาปุ่มในกรณีที่หาปุ่มไม่เจอ
delayMainloop = config[3] #หน่วงเวลาในการวนตรวจสอบหน้าจอ ถ้าใส่ค่า 0 คือ จะวนเร็วสุดเท่าที่ทำได้ แต่ถ้าใส่ค่าอื่น เช่น 2 ก็คือจะวนช้าลงจากเดิม 2 วินาที 
loginlimit = int(config[4]) #เวลา(วินาที) ที่จะรอหลอดโหลดเข้าเกม หากโหลดนานกว่าที่กำหนดไว้ จะรีหน้าแล้วล็อกอินใหม่
confidence = config[5]
numOfAcc = int(config[6])
zoom = int(config[7])


character = []
timetowakeup = []

file = codecs.open('config_acc.txt','r','utf8')
logger.debug('loading account config... ')
IDconfigCheckList = ['character','timetowakeup']
IDconfig = []
i = 0
#p = 0
for line in file:
    #print(i)
    if((i+1)>(3*numOfAcc)):
        break

    if(re.split('=|#',line)[0] == ''):
        i+=1
        continue
    #print(line)
    #print(re.split('=|#',line))
    
    data = re.split('=|#',line)
    try:
        if(data[0] == 'character'):
            character.append(int(data[1]))
            logger.debug(f'character : {int(data[1])}')
        elif(data[0] == 'timetowakeup'):
            timetowakeup.append(int(data[1]))
            logger.debug(f'timetowakeup : {int(data[1])}')
    except:
        logger.error('config failed')
        break
    i+=1
file.close()
if(i+1 < (3*numOfAcc)):
    logger.error('!! ERROR !! please check config_acc.txt')
    quit()


#print(character)
#print(timetowakeup)

def getscreensize():
    moniter = win32api.EnumDisplayMonitors()
    #print(moniter)


    left = min([mon[2][0] for mon in moniter])
    top = min([mon[2][1] for mon in moniter])

    width = max([mon[2][2] for mon in moniter])-left
    height = max([mon[2][3] for mon in moniter])-top

    return (left,top,width,height)


capApp = cap(numOfAcc)
box = capApp.start()
screensize = box

if(len(screensize) != numOfAcc):
    quit()

    
logger.debug(f'screen size : {screensize}')

print(f'botBomb will start in 3 seconds...')
time.sleep(3)
try:
    if(SONGLINE):
        threading.Thread(target=LINE.sendtext(f'\n-----บอทเริ่มทำงาน-----')).start()
        
except:
    pass

class bombBot():
    def __init__(self):
        #self.dealywaitLogin = 10
        self.character = 15
        self.moveSpeed = 0.3
        self.looplimit = 200
        self.confidence = 0.9
        self.maxloginfreez = 60
        self.screensize = (0,0,1920,1080)
        self.refreshMap = 9
        self.delayMainloop = 2
        self.timetowakeup = 60
        self.mp = None
        self.accNum = 1
        self.picPath = f'pictmp/{self.accNum}.png'
        self.errTxt = '\nมีบางอย่างผิดพลาด\nบอทกำลังทำการ Login ใหม่\nระหว่างนี้ควรตรวจสอบว่าบอทของคุณยังทำงานปกติอยู่หรือไม่'
        #self.zoom = 100
        self.mainpicPath = f'pic/100'

    def setAccnum(self,accNum):
        self.accNum = accNum
        self.picPath = f'pictmp/{self.accNum}.png'

    def savePic(self,region):
        im = bot.screenshot(region=region)
        im.save(self.picPath)

    def moveAndClik(self,pos):
        orPos = bot.position()
        bot.mouseUp(button='left')

        bot.moveTo(pos)
        bot.click(pos)

        bot.moveTo(orPos)


    def antibotDetect(self):
        pos = bot.locateOnScreen(f'{self.mainpicPath}/antibot/are.png',region=self.screensize,confidence=self.confidence)
        if(pos):
            rgbsl = []
            succ = False
            logger.debug('solve captcha !!')
            for i in range(1,4):
                pos = bot.locateOnScreen(f'{self.mainpicPath}/antibot/are.png',region=self.screensize,confidence=self.confidence)
                bot.moveTo(pos,duration=self.moveSpeed)
                if(pos):
                    #bot.moveTo(pos,duration=self.moveSpeed)
                    pos = bot.locateOnScreen(f'{self.mainpicPath}/antibot/yy.png',region=self.screensize,confidence=self.confidence)
                    bot.moveTo(pos,duration=self.moveSpeed)
                    time.sleep(0.3)
                    
                    if(i == 1):
                        sl = bot.position()
                        rgbsl = bot.pixel(sl[0], sl[1])

                    x,y = bot.position()
                    bot.mouseDown(button='left')
                    time.sleep(0.2)
                    if(random.randint(1,2) == 1):
                        y+=(random.randint(1,15))
                    else:
                        y-=(random.randint(1,15))
                    bot.moveTo(x+(random.randint(50,200)),y,duration=self.moveSpeed)
                    time.sleep(0.5)
                    bot.mouseUp(button='left')
                    if(i == 3):
                        time.sleep(1)
                    else:
                        time.sleep(0.3)
                if(not(bot.locateOnScreen(f'{self.mainpicPath}/antibot/are.png',region=self.screensize,confidence=self.confidence)) and (not(bot.locateOnScreen(f'{self.mainpicPath}/antibot/fail.png',region=self.screensize,confidence=self.confidence)))):
                    succ = True
                    break

                if(i+1 == 2 or i+1 == 3):
                    while(1):
                        sl = bot.position()
                        rgbsl2 = bot.pixel(sl[0], sl[1])
                        print(f'{rgbsl} - {rgbsl2}')
                        if(rgbsl == rgbsl2):
                            break
                        else:
                            pos = bot.locateOnScreen(f'{self.mainpicPath}/antibot/yy.png',region=self.screensize,confidence=self.confidence)
                            bot.moveTo(pos,duration=0.1)
                else:
                    sl = bot.position()
                    rgbsl = bot.pixel(sl[0], sl[1])
            if(succ):
                logger.debug(f'[{self.accNum}] captcha solved')
                return True
            else:
                #time.sleep(12)
                logger.error(f'[{self.accNum}] solve captcha failed')
                return False
        else:
            logger.debug(f'[{self.accNum}] captcha not found')
            return True
        
    def findAndClick(self,path,duration,outputTxt):
        pos = bot.locateOnScreen(path,region=self.screensize)
        i = 0
        while(not(pos) and i< self.looplimit):
            logger.warning(f'[{self.accNum}] {outputTxt}: not found ({i}/{self.looplimit})')
            pos = bot.locateOnScreen(path,region=self.screensize,confidence=self.confidence)
            i+=1
            try:
                if(i>=self.looplimit and SONGLINE):
                    threading.Thread(target=LINE.sendtext(f'account {self.accNum}{self.errTxt}')).start()
            except:
                pass
        if(pos):
            logger.debug(f'[{self.accNum}] {outputTxt} -> {pos}')
            
            self.moveAndClik(pos)
            '''bot.moveTo(pos,duration=duration)
            time.sleep(0.3)
            bot.click(pos)'''
            
        return pos
        

    def login(self):
        pos = bot.locateOnScreen(f'{self.mainpicPath}/login/connect.png',region=self.screensize,confidence=self.confidence)
        if(pos):
            #logger.debug(f'[{self.accNum}] logo {pos}')
            #self.moveAndClik(pos)
            #pos = bot.locateOnScreen(f'{self.mainpicPath}/login/connect.png',region=self.screensize,confidence=self.confidence)
            logger.debug(f'[{self.accNum}] connect {pos}')
            self.moveAndClik(pos)
            '''bot.moveTo(pos)
            bot.click(pos)'''
            time.sleep(1)
            solCap = self.antibotDetect()
            if(not(solCap)):
                return False

            #login แบบเก่า 
            '''
            pos = bot.locateOnScreen(f'{self.mainpicPath}/login/metamask1.png',region=self.screensize,confidence=self.confidence)
            if(pos):
                logger.debug(f'[{self.accNum}] metamask {pos}')
                bot.moveTo(pos)
                bot.click(pos)
            else:
                pos = bot.locateOnScreen(f'{self.mainpicPath}/login/metamask2.png',region=self.screensize,confidence=self.confidence)
                if(pos):
                    logger.debug(f'[{self.accNum}] metamask2 {pos}')
                    bot.moveTo(pos)
                    bot.click(pos)
            '''
            time.sleep(3)
            pos = bot.locateOnScreen(f'pic/all/metamask_load.png',confidence=self.confidence)
            while(pos):
                time.sleep(0.5)
                logger.debug(f'[{self.accNum}] metamask is loading')
                pos = bot.locateOnScreen(f'pic/all/metamask_load.png',confidence=self.confidence)
                
            time.sleep(0.5)
            pos = bot.locateOnScreen(f'{self.mainpicPath}/login/auth.png',confidence=self.confidence)
            if(pos):
                while(pos):
                    logger.debug(f'[{self.accNum}] auth {pos}')
                    self.moveAndClik(pos)
                    '''bot.moveTo(pos)
                    bot.click(pos)'''
                    time.sleep(0.7)
                    pos = bot.locateOnScreen(f'{self.mainpicPath}/login/auth.png',confidence=self.confidence)
            else:
                pos = bot.locateOnScreen(f'{self.mainpicPath}/login/autheng.png',confidence=self.confidence)
                if(pos):
                    while(pos):
                        logger.debug(f'[{self.accNum}] auth {pos}')
                        self.moveAndClik(pos)
                        '''bot.moveTo(pos)
                        bot.click(pos)'''
                        time.sleep(0.7)
                        pos = bot.locateOnScreen(f'{self.mainpicPath}/login/autheng.png',confidence=self.confidence)
                else:
                    return False
            #time.sleep(self.dealywaitLogin)
            time.sleep(1)

            print('---------')

            #เช็คว่าหลังจาก connect metamask แล้ว ค้างมั้ย?
            logger.debug(f'[{self.accNum}] freeze checking...')
            pos = bot.locateOnScreen(f'{self.mainpicPath}/login/connect.png',region=self.screensize,confidence=self.confidence)
            if(pos):
                logger.debug(f'[{self.accNum}] found freeze')    
                return False
            #เช็คว่าหลังจาก connect metamask แล้ว เกิด error มั้ย?
            logger.debug(f'[{self.accNum}] login error checking...')
            pos = bot.locateOnScreen(f'{self.mainpicPath}/error/error.png',region=self.screensize,confidence=self.confidence)
            if(pos):
                logger.debug(f'[{self.accNum}] found login error')
                return False
            else:
                pos = bot.locateOnScreen(f'{self.mainpicPath}/error/error2.png',region=self.screensize,confidence=self.confidence)
                if(pos):
                    logger.debug(f'[{self.accNum}] found login error')
                    return False


            pos = bot.locateOnScreen(f'{self.mainpicPath}/login/inlogin.png',region=self.screensize,confidence=self.confidence)
            #time.sleep(2)
            freezLogin = 0
            timetempS = int(int(datetime.now().timestamp()))
            while(pos):#รอโหลด
                logger.debug(f'[{self.accNum}] login {freezLogin}/{self.maxloginfreez} sec')
                time.sleep(0.7)
                freezLogin = int(datetime.now().timestamp()) - timetempS
                pos = bot.locateOnScreen(f'{self.mainpicPath}/login/inlogin.png',region=self.screensize,confidence=self.confidence)
                if(freezLogin > self.maxloginfreez):
                    logger.debug(f'[{self.accNum}] loading too long')
                    return False #โหลดนานไป
                elif(bot.locateOnScreen(f'{self.mainpicPath}/error/error.png',region=self.screensize,confidence=self.confidence)):
                    logger.debug(f'[{self.accNum}] found login error')
                    return False #ระหว่างรอโหลดเกิด error
                elif(bot.locateOnScreen(f'{self.mainpicPath}/error/error2.png',region=self.screensize,confidence=self.confidence)):
                    logger.debug(f'[{self.accNum}] found login error')
                    return False #ระหว่างรอโหลดเกิด error
            time.sleep(0.3)
            if(bot.locateOnScreen(f'{self.mainpicPath}/wakeup/entermap.png',region=self.screensize,confidence=self.confidence)):
                return True
            else:
                return False
        else:
            if(bot.locateOnScreen(f'{self.mainpicPath}/wakeup/entermap.png',region=self.screensize,confidence=self.confidence)):
                return True
            else:
                return False
    
    def wakeup(self):
        if(not(self.findAndClick(path=f'{self.mainpicPath}/wakeup/hero.png',duration=self.moveSpeed,outputTxt='hero menu button'))):
            return False
        time.sleep(0.4)
        solCap = self.antibotDetect()
        if(not(solCap)):
            return False
        i = 1
        while(1):
            pos = bot.locateOnScreen(f'{self.mainpicPath}/wakeup/loading.png',region=self.screensize,confidence=self.confidence)
            time.sleep(0.5)
            logger.debug(f'[{self.accNum}] loading {i}/{self.looplimit}')
            if(not(pos)):
                break
            elif(i == self.looplimit):
                return False
            i+=1
        pos = self.findAndClick(path=f'{self.mainpicPath}/wakeup/menu.png',duration=self.moveSpeed,outputTxt='character menu')
        #pos = bot.locateOnScreen('wakeup/menu.png',confidence=self.confidence)


        
        if(pos):
            if(not(bot.locateOnScreen(f'{self.mainpicPath}/wakeup/notwork.png',region=self.screensize,confidence=self.confidence))):    
                if(not(self.findAndClick(path=f'{self.mainpicPath}/wakeup/workall.png',duration=self.moveSpeed,outputTxt='Wakeup All'))):
                    return False
                #time.sleep(0.3)
            if(not(self.findAndClick(path=f'{self.mainpicPath}/wakeup/exitmenu.png',duration=self.moveSpeed,outputTxt='Exit Hero Menu'))):
                return False
            if(not(self.findAndClick(path=f'{self.mainpicPath}/wakeup/entermap.png',duration=self.moveSpeed,outputTxt='Enter Map'))):
                return False
            else:
                return True
        '''if(pos):
            for i in range(40):
                bot.scroll(-100)
            time.sleep(1)
            character = 1
            notfoundcharac = 1

            while(character <= self.character and notfoundcharac <= int(self.looplimit)):
                logger.debug(f'[{self.accNum}] Work!! character {character}')
                pos = bot.locateOnScreen(f'{self.mainpicPath}/wakeup/work.png',region=self.screensize,confidence=0.99)

                if(not(pos) and notfoundcharac >= 10 and not(bot.locateOnScreen(f'{self.mainpicPath}/wakeup/lag.png',region=self.screensize,confidence=0.90))):
                    break

                if(pos and not(bot.locateOnScreen(f'{self.mainpicPath}/wakeup/lag.png',region=self.screensize,confidence=0.90))):
                    logger.debug(f'[{self.accNum}] Found character {character} in menu')
                    bot.moveTo(pos)#,duration=self.moveSpeed)
                    bot.click(pos)
                    time.sleep(0.05) #ต้องมี    
                    logger.debug(f'[{self.accNum}] character {character} Wakes Up-> {pos}\n')
                    character+=1
                    notfoundcharac = 0
                elif(pos):
                    logger.warning(f'[{self.accNum}] Server Lag !!! {character}')
                    time.sleep(0.3)
                    notfoundcharac+=1
                else:
                    logger.warning(f'[{self.accNum}] not found character {character}')
                    notfoundcharac+=1
                
                if(notfoundcharac > self.looplimit and SONGLINE):
                    try:
                        threading.Thread(target=LINE.sendtext(f'account {self.accNum}{self.errTxt}')).start()
                    except:
                        pass
                    return False
                
            for i in range(self.looplimit):
                time.sleep(0.4)
                if(not(bot.locateOnScreen(f'{self.mainpicPath}/wakeup/work.png',region=self.screensize,confidence=0.99))):
                
                    logger.debug(f'[{self.accNum}] Ready to Exit Menu\n')
                    if(not(self.findAndClick(path=f'{self.mainpicPath}/wakeup/exitmenu.png',duration=self.moveSpeed,outputTxt='Exit Hero Menu'))):
                        return False
                    break
                logger.debug(f'[{self.accNum}] Not! ready to Exit Menu\n')

                if(i==self.looplimit-1 and SONGLINE):
                    try:
                        threading.Thread(target=LINE.sendtext(f'account {self.accNum}{self.errTxt}')).start()
                    except:
                        pass
                    return False
            if(not(self.findAndClick(path=f'{self.mainpicPath}/wakeup/entermap.png',duration=self.moveSpeed,outputTxt='Enter Map'))):
                return False
            else:
                return True
        '''
        return False
    
    def toMainMenu(self):
        return self.findAndClick(path=f'{self.mainpicPath}/tomainmenu/back.png',duration=self.moveSpeed,outputTxt='back to MainMenu')
            
    def newmap(self):
        pos = bot.locateOnScreen(f'{self.mainpicPath}/newmap/newmap.png',region=self.screensize,confidence=self.confidence)
        
        if(pos):
            logger.debug(f'[{self.accNum}] new map -> {pos}')
            self.moveAndClik(pos)
            '''bot.moveTo(pos,duration=self.moveSpeed)
            bot.click(pos)'''
            time.sleep(3)
            solCap = self.antibotDetect()
            if(not(solCap)):
                if(SONGLINE):
                    try:
                        threading.Thread(target=LINE.sendtext(f'account {self.accNum}\nแก้ Captcha ไม่สำเร็จ กำลังทำการ Login ใหม่')).start()
                    except:
                        pass
                return False
            self.capAndSend()
            return True
        else:
            logger.debug(f'[{self.accNum}] new map : not found')
            return True

    def capAndSend(self):
        self.savePic(self.screensize)
        time.sleep(0.5)
        if(SONGLINE):
            try:
                threading.Thread(LINE.sendPic(self.picPath,mess=f'account {self.accNum}\nเปลี่ยน Map แล้ว !!!')).start()
            except:
                pass

    def errorhandling(self):
        if(bot.locateOnScreen(f'{self.mainpicPath}/error/error.png',region=self.screensize,confidence=self.confidence)):
            if(not(self.FixErr())):
                return False
        elif(bot.locateOnScreen(f'{self.mainpicPath}/error/error2.png',region=self.screensize,confidence=self.confidence)):
            if(not(self.FixErr())):
                return False
        else:
            logger.debug(f'[{self.accNum}] ERROR : not found')
        return True
    
    def FixErr(self):
        logger.warning(f'[{self.accNum}] !!found ERROR!!')
        try:
            if(SONGLINE):
                threading.Thread(target=LINE.sendtext(f'account {self.accNum}\nพบ Error ของเซิฟเวอร์ บอทกำลังทำการ Login ใหม่')).start()
        except:
                pass
        f5 = self.F5_()
        if(not(f5)):
            return False
        #else:
        logined = self.login()
        if(not(logined)):
            return False
        else:
            self.entermap()
            try:
                if(SONGLINE):
                    threading.Thread(target=LINE.sendtext(f'account {self.accNum}\nLogin สำเร็จ')).start()
            except:
                pass
            return True

    def RefreshMap(self):
        #self.findAndClick(path='antiunknow/box.png',duration=0.3,outputTxt='setting')
        #pos = bot.locateOnScreen('tomainmenu/back.png',confidence=self.confidence)
        found = self.findAndClick(path=f'{self.mainpicPath}/tomainmenu/back.png',duration=self.moveSpeed,outputTxt='(RefreshMap)Back Menu')
        '''while(not(pos)):
            logger.debug(f'setting {pos}')
            pos = bot.locateOnScreen('antiunknow/box.png')
        logger.debug(f'setting {pos}')'''
        
        #logger.debug(f'RefreshMap: found back botton -> {pos}')
        #bot.moveTo(pos,duration=self.moveSpeed)
        #bot.click(pos)
        if(found):
            time.sleep(0.3)
            found = self.findAndClick(path=f'{self.mainpicPath}/wakeup/entermap.png',duration=self.moveSpeed,outputTxt='(RefreshMap)Enter Map')

        if(found):
            return True
        else:
            return False
        

    def F5_(self):
        pos = self.mp
        self.moveAndClik(pos)
        '''bot.moveTo(pos,duration=self.moveSpeed)
        bot.click(pos)'''
        bot.hotkey('ctrl','f5')
        time.sleep(0.5)
        #time.sleep(10)
        return self.waitRefresh()
        
    def waitRefresh(self):
        '''
        pos = bot.locateOnScreen(f'{self.mainpicPath}/login/logo2.png',region=self.screensize,confidence=self.confidence)
        if(not(pos)):
            pos = bot.locateOnScreen(f'{self.mainpicPath}/login/logo.png',region=self.screensize,confidence=self.confidence)    
        '''
        timetempS = int(int(datetime.now().timestamp()))
        pos = bot.locateOnScreen(f'{self.mainpicPath}/login/connect.png',region=self.screensize,confidence=self.confidence)
        counttime = 0
        while(not(pos) and counttime <= 10):
            counttime = int(datetime.now().timestamp()) - timetempS
            pos = bot.locateOnScreen(f'{self.mainpicPath}/login/connect.png',region=self.screensize,confidence=self.confidence)
            time.sleep(1)
            #print(counttime)
            logger.debug(f'[{self.accNum}] wait for refresh ({counttime}/10 s)')
        if(counttime > 10):
            return False
        else:
            return True
    
    def entermap(self):
        time.sleep(2)
        self.findAndClick(path=f'{self.mainpicPath}/wakeup/entermap.png',duration=self.moveSpeed,outputTxt='Enter Map')

            



'''bomb = []
thread = []
#add bot list
for i in range(1,numOfAcc+1):
    bomb.append(bombBot())

for i in range(numOfAcc):
    bomb[i].character = character[i]
    bomb[i].timetowakeup = timetowakeup[i]
    bomb[i].moveSpeed = mouseMoveSpeed
    bomb[i].looplimit = looplimit
    bomb[i].maxloginfreez = loginlimit
    bomb[i].confidence = confidence
    bomb[i].screensize = screensize[i]
    bomb[i].refreshMap = refreshMap
    bomb[i].delayMainloop = delayMainloop
    threading.Thread(target=bomb[i].begin).start()
    time.sleep(5)
    print('--------------------------------------------------------------------------------------')
    
 
'''



'''mybot = bombBot()

mybot.character = character
mybot.moveSpeed = mouseMoveSpeed
mybot.looplimit = looplimit
mybot.maxloginfreez = loginlimit
mybot.confidence = confidence
mybot.screensize = screensize'''
picPathMain = f'pic/{zoom}'
mybot = []
firstwake = []
for i in range(numOfAcc):
    mybot.append(bombBot())

for i in range(numOfAcc):
    mybot[i].character = character[i]
    mybot[i].timetowakeup = timetowakeup[i]
    mybot[i].moveSpeed = mouseMoveSpeed
    mybot[i].looplimit = looplimit
    mybot[i].maxloginfreez = loginlimit
    mybot[i].confidence = confidence
    mybot[i].screensize = screensize[i]
    mybot[i].refreshMap = refreshMap
    mybot[i].delayMainloop = delayMainloop
    #mybot[i].accNum = i+1
    mybot[i].setAccnum(i+1)
    mybot[i].mainpicPath = picPathMain
    firstwake.append(1)

state = []
stateRefreshMap = []

timetemp = []
login = []
#pos = []
cappic = []

for i in range(numOfAcc):
    
    state.append(0)
    stateRefreshMap.append(0)
    cappic.append(0)
    timetemp.append(int(int(datetime.now().timestamp())/60))
    login.append(0)
    mp = bot.locateOnScreen(f'{picPathMain}/mainpos/MP1.png',region=mybot[i].screensize,confidence=mybot[i].confidence)
    if(not(mp)):
        mp = bot.locateOnScreen(f'{picPathMain}/mainpos/MP2.png',region=mybot[i].screensize,confidence=mybot[i].confidence)
        login[i] = 1
        firstwake[i] = 2
    if(mp):
        orPos = bot.position()
        bot.moveTo(mp,duration=mouseMoveSpeed)
        bot.moveTo(orPos)
        print(f'mainpoint {mp}')
        print(bot.center(mp))
        mybot[i].mp = bot.center(mp)
    else:
        logger.error('fail to find mainpos')
        quit()
    print('setup complate')

'''for i in range(numOfAcc):
    #mybot[i].login()
    mybot[i].wakeup()'''



while(1):
    try:
        for i in range(numOfAcc):
            if(login[i]):
                login[i] = 0
                f5 = mybot[i].F5_()
                if(not(f5)):
                    login[i] = 1
                    continue
                elif(not(mybot[i].login())):
                    login[i] = 1
                    continue
                else:
                    mybot[i].entermap()
                    try:
                        if(SONGLINE):
                            threading.Thread(target=LINE.sendtext(f'account {mybot[i].accNum}\nLogin สำเร็จ')).start()
                    except:
                        pass
                    if(cappic[i]):
                        mybot[i].capAndSend()
                        cappic[i] = 0
            Cnewmap = mybot[i].newmap()#check new map 
            if(not(Cnewmap)):
                login[i] = 1
                cappic[i] = 1
                print('\n')
                continue
            #errfixd,pos[i] = mybot[i].errorhandling()
            errfixd = mybot[i].errorhandling()
            if(not(errfixd)):#check error and handling
                login[i] = 1
                continue
            
            now = int(int(datetime.now().timestamp())/60)
            #now = int(int(datetime.now().timestamp()))#test
            current_time = now-timetemp[i]
            logger.debug(f'[{mybot[i].accNum}] ({state[i]}) cooldown for wakeup: {current_time}/{mybot[i].timetowakeup} min')
            logger.debug(f'[{mybot[i].accNum}] ({stateRefreshMap[i]}) cooldown for Refresh Map: {current_time %mybot[i].refreshMap}/{mybot[i].refreshMap} min')

            if(current_time %mybot[i].refreshMap == 0 and stateRefreshMap[i]):
                refesh = mybot[i].RefreshMap()#anti unknow
                stateRefreshMap[i] = 0
                if(not(refesh)):
                    login[i] = 1
                    print('\n')
                    continue
            elif(current_time %mybot[i].refreshMap != 0):
                stateRefreshMap[i] = 1
                

            if((current_time >= mybot[i].timetowakeup and state[i]) or firstwake[i]):
                
                if(firstwake[i] == 2 or firstwake[i] == 0):
                    if(not(mybot[i].toMainMenu())):
                        login[i] = 1
                        print('\n')
                        continue
                firstwake[i] = 2
                CK()
                wake = mybot[i].wakeup()
                if(wake):
                    state[i] = 0
                    timetemp[i] = int(int(datetime.now().timestamp())/60)
                #timetemp = int(int(datetime.now().timestamp()))#test
                else:
                    login[i] = 1
                    print('\n')
                    continue
                firstwake[i] = 0

            elif(current_time >= mybot[i].timetowakeup):
                state[i] = 0
            elif(current_time < mybot[i].timetowakeup):
                state[i] = 1

            #logger.debug(f'({wakeup}) wait for wakeup when {timetowakeup} min')
            print('\n')
    except:
        pass
    
    time.sleep(delayMainloop)
