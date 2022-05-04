# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qsswindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import json
import logging
import logging.handlers
import os
import pickle
import random
import re
import smtplib
import sys
import time
from email.header import Header
from email.mime.text import MIMEText

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup

from bark.bark_pusher import BarkPusher
from config import global_config

LOG_FILENAME = global_config.getRaw("config", "log_name")


class Ui_QSSWindow(object):
    def setupUi(self, QSSWindow):
        QSSWindow.setObjectName("QSSWindow")
        QSSWindow.resize(1950, 1450)
        self.centralwidget = QtWidgets.QWidget(QSSWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.goods = QtWidgets.QHBoxLayout()
        self.goods.setObjectName("goods")
        self.labelGoods = QtWidgets.QLabel(self.groupBox)
        self.labelGoods.setObjectName("labelGoods")
        self.goods.addWidget(self.labelGoods)
        self.inputGoods = QtWidgets.QLineEdit(self.groupBox)
        self.inputGoods.setObjectName("inputGoods")
        self.goods.addWidget(self.inputGoods)
        self.verticalLayout.addLayout(self.goods)
        self.area = QtWidgets.QHBoxLayout()
        self.area.setObjectName("area")
        self.labelArea = QtWidgets.QLabel(self.groupBox)
        self.labelArea.setObjectName("labelArea")
        self.area.addWidget(self.labelArea)
        self.inputArea = QtWidgets.QLineEdit(self.groupBox)
        self.inputArea.setObjectName("inputArea")
        self.area.addWidget(self.inputArea)

        # 邮箱
        self.labelMail = QtWidgets.QLabel(self.groupBox)
        self.labelMail.setObjectName("labelMail")
        self.area.addWidget(self.labelMail)
        self.inputMail = QtWidgets.QLineEdit(self.groupBox)
        self.inputMail.setObjectName("inputMail")
        self.area.addWidget(self.inputMail)

        # Bark Key
        self.labelBark = QtWidgets.QLabel(self.groupBox)
        self.labelBark.setObjectName("labelBark")
        self.area.addWidget(self.labelBark)
        self.inputBark = QtWidgets.QLineEdit(self.groupBox)
        self.inputBark.setObjectName("inputBark")
        self.area.addWidget(self.inputBark)

        # 抢购数量
        self.labelNum = QtWidgets.QLabel(self.groupBox)
        self.labelNum.setObjectName("labelNum")
        self.area.addWidget(self.labelNum)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.area.addWidget(self.comboBox)

        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.area.addWidget(self.checkBox)

        self.checkEnableNoticeBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkEnableNoticeBox.setObjectName("checkEnableNoticeBox")
        self.area.addWidget(self.checkEnableNoticeBox)

        self.verticalLayout.addLayout(self.area)
        self.speedLayout = QtWidgets.QHBoxLayout()
        self.speedLayout.setObjectName("speedLayout")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setProperty("value", 50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickInterval(0)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.speedLayout.addWidget(self.horizontalSlider)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.speedLayout.addWidget(self.progressBar)

        self.verticalLayout.addLayout(self.speedLayout)
        self.text_edit = QtWidgets.QTextEdit(self.groupBox)
        self.text_edit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.text_edit)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setObjectName("buttonLayout")
        self.loginBtn = QtWidgets.QPushButton(self.groupBox)
        self.loginBtn.setStyleSheet("")
        self.loginBtn.setObjectName("loginBtn")
        self.button_layout.addWidget(self.loginBtn)
        self.start_btn = QtWidgets.QPushButton(self.groupBox)
        self.start_btn.setStyleSheet("")
        self.start_btn.setObjectName("startBtn")
        self.button_layout.addWidget(self.start_btn)
        self.stop_btn = QtWidgets.QPushButton(self.groupBox)
        self.stop_btn.setStyleSheet("")
        self.stop_btn.setObjectName("stopBtn")
        self.button_layout.addWidget(self.stop_btn)
        self.verticalLayout.addLayout(self.button_layout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tab, "")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")

        self.labelAboutMe = QtWidgets.QLabel(self.tab_1)
        # self.labelAboutMe.setGeometry(QtCore.QRect(50, 30, 280, 180))
        self.labelAboutMe.setObjectName("labelAboutMe")

        self.tabWidget.addTab(self.tab_1, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        QSSWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(QSSWindow)
        self.statusbar.setObjectName("statusbar")
        QSSWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(QSSWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 25))
        self.menubar.setObjectName("menubar")
        self.file = QtWidgets.QMenu(self.menubar)
        self.file.setObjectName("file")
        self.edit = QtWidgets.QMenu(self.menubar)
        self.edit.setObjectName("edit")
        QSSWindow.setMenuBar(self.menubar)
        self.file.addSeparator()
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.edit.menuAction())

        self.re_translate_ui(QSSWindow)
        self.tabWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(QSSWindow)

    def re_translate_ui(self, QSSWindow):
        _translate = QtCore.QCoreApplication.translate
        QSSWindow.setWindowTitle(_translate("QSSWindow", "MainWindow"))
        self.tabWidget.setToolTip(_translate("QSSWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.tabWidget.setWhatsThis(_translate("QSSWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.groupBox.setTitle(_translate("QSSWindow", "让我抢一个A7M4吧！！！"))
        self.labelGoods.setText(_translate("QSSWindow", "请输入商品ID(以逗号间隔):"))
        self.labelArea.setText(_translate("QSSWindow", "请输入收件地区编码:"))
        self.labelMail.setText(_translate("QSSWindow", "通知邮箱:"))
        self.labelBark.setText(_translate("QSSWindow", "Bark秘钥:"))
        self.labelNum.setText(_translate("QSSWindow", "购买数量:"))
        self.loginBtn.setText(_translate("QSSWindow", "扫码登录"))
        self.start_btn.setText(_translate("QSSWindow", "开始监控(可自动登录)"))
        self.stop_btn.setText(_translate("QSSWindow", "停止监控"))
        self.checkBox.setText(_translate("QSSWindow", "是否自动忽略下架商品"))
        self.checkEnableNoticeBox.setText(_translate("QSSWindow", "是否开启通知"))

        self.labelAboutMe.setText(_translate("QSSWindow",
                                             '<h1>使用指南</h1> <a href="https://github.com/ZhangYikaii/auto-buy-Python-tool">请点击这里跳转</a> <h3>战疫情, 加油!</h3> <h4>欢迎在GitHub上加星. 谢谢!</h4> <h3>Tips: 登录一次之后本地会保存登录信息, 重启软件之后仍然可以记住账号登录信息</h3> <h3>只需点击"开始监控"就可以自动登录, 不必重复扫码哦</h3>'))
        self.labelAboutMe.setOpenExternalLinks(True)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("QSSWindow", "Console"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("QSSWindow", "指南"))

        self.file.setTitle(_translate("QSSWindow", "文件"))
        self.edit.setTitle(_translate("QSSWindow", "编辑"))


class Autobuy(QtWidgets.QMainWindow, Ui_QSSWindow):
    def __init__(self):
        super().__init__()
        self.sess = requests.Session()
        self.sess.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "https://order.jd.com/center/list.action",
            "Connection": "keep-alive"
        }

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "https://cart.jd.com/cart.action",
            "Connection": "keep-alive"
        }

        self.speed = 5000
        self.is_monitor_sold_out = True
        self.is_monitor_enable_notice = bool(global_config.getRaw("messenger", "enable"))

        # self.isLogin = False
        self.cookies_string = ''
        self.cookies = {}
        self.sku_id_string = ''
        self.sku_id = []
        self.cont = 1
        self.timer = QTimer(self)
        self.logger = logging.getLogger()
        self.load_qss()
        self.setupUi(self)
        self.connect_sign()
        self.init_data()

        self.checkEnableNoticeBox.setChecked(self.is_monitor_enable_notice)
        # self.show()

    def load_qss(self):
        file = 'window.qss'
        with open(file, 'rt', encoding='utf8') as f:
            style_sheet = f.read()
        self.setStyleSheet(style_sheet)
        f.close()

    def set_logger(self, logFileName=LOG_FILENAME):
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = logging.handlers.RotatingFileHandler(
            logFileName, maxBytes=10485760, backupCount=5, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def init_data(self):
        self.inputGoods.setText(global_config.getRaw("config", "skuIds"))
        self.inputArea.setText(global_config.getRaw("config", "area"))
        self.inputMail.setText(global_config.getRaw("messenger", "mails"))
        self.inputBark.setText(global_config.getRaw("messenger", "bark_keys"))
        self.comboBox.addItems(['1', '2', '3'])
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setMinimum(0)
        self.set_progress_bar()

        self.set_logger()

        if len(self.cookies_string) != 0:
            manual_cookies = {}
            for item in self.cookies_string.split(';'):
                # 用=号分割.
                name, value = item.strip().split('=', 1)
                manual_cookies[name] = value
            self.cookies = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None, overwrite=True)
            self.sess.cookies = self.cookies

    def connect_sign(self):
        self.horizontalSlider.valueChanged.connect(self.set_progress_bar)
        self.horizontalSlider.valueChanged[int].connect(self.set_speed)

        self.loginBtn.clicked.connect(self.login_by_qr)
        self.start_btn.clicked.connect(self.monitor_connect)
        self.stop_btn.clicked.connect(self.stop_connect)

    def stop_connect(self):
        self.update_state_text("已停止监控.")
        self.timer.stop()

    def stop_now(self):
        self.update_state_text("已停止监控.")
        self.timer.stop()

    def set_speed(self, val):
        # self.updateStateText("设置抢购速度: %d" % val)
        if val > 85:
            self.speed = 500
        elif val > 60:
            self.speed = 9000 - val * 100
        else:
            self.speed = 10000 - val * 100

    def set_progress_bar(self):
        self.progressBar.setValue(self.horizontalSlider.value())

    def check_login(self):
        self.update_state_text('正在验证登录状态...')
        for flag in range(1, 3):
            try:
                target_url = 'https://order.jd.com/center/list.action'
                payload = {
                    'rid': str(int(time.time() * 1000)),
                }
                resp = self.sess.get(url=target_url, params=payload, allow_redirects=False)
                if resp.status_code == requests.codes.OK:
                    self.update_state_text('登录成功!')
                    return True
                else:
                    self.update_state_text('第 %s 次再尝试验证cookie...' % flag)
                    self.update_state_text('正在尝试从历史讯息中恢复...')
                    with open('cookie', 'rb') as f:
                        cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
                    # print(cookies)
                    self.sess.cookies = cookies
                    continue
            except Exception as e:
                self.update_state_text(str(e))
                self.update_state_text('第 %s 次再尝试验证cookie...' % flag)
                continue
        self.update_state_text('请登录!')
        return False

    def login_by_qr(self):
        # jd login by QR code
        try:
            self.update_state_text('请您打开京东手机客户端或微信扫一扫, 准备扫码登录')

            urls = (
                'https://passport.jd.com/new/login.aspx',
                'https://qr.m.jd.com/show',
                'https://qr.m.jd.com/check',
                'https://passport.jd.com/uc/qrCodeTicketValidation'
            )
            # step 1: open login page
            response = self.sess.get(
                urls[0],
                headers=self.headers
            )
            if response.status_code != requests.codes.OK:
                self.update_state_text(f'获取登录页失败: {response.status_code}')
                # self.isLogin = False
                return False
            # update cookies
            self.cookies.update(response.cookies)
            self.sess.cookies = response.cookies

            # step 2: get QR image
            response = self.sess.get(
                urls[1],
                headers=self.headers,
                cookies=self.cookies,
                params={
                    'appid': 133,
                    'size': 147,
                    't': int(time.time() * 1000),
                }
            )
            if response.status_code != requests.codes.OK:
                self.update_state_text(f'获取二维码失败: {response.status_code}')
                # self.isLogin = False
                return False

            # update cookies
            self.cookies.update(response.cookies)
            self.sess.cookies = response.cookies

            # save QR code
            image_file = 'qr.png'
            with open(image_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

            # scan QR code with phone
            if os.name == "nt":
                # for windows
                os.system('start ' + image_file)
            else:
                if os.uname()[0] == "Linux":
                    # for linux platform
                    os.system("eog " + image_file)
                else:
                    # for Mac platform
                    os.system("open " + image_file)

            # step 3: check scan result
            self.headers['Host'] = 'qr.m.jd.com'
            self.headers['Referer'] = 'https://passport.jd.com/new/login.aspx'

            # check if QR code scanned
            qr_ticket = None
            retry_times = 1000  # 尝试1000次
            while retry_times:
                retry_times -= 1
                response = self.sess.get(
                    urls[2],
                    headers=self.headers,
                    cookies=self.cookies,
                    params={
                        'callback': 'jQuery%d' % random.randint(1000000, 9999999),
                        'appid': 133,
                        'token': self.cookies['wlfstk_smdl'],
                        '_': int(time.time() * 1000)
                    }
                )
                if response.status_code != requests.codes.OK:
                    continue
                rs = json.loads(re.search(r'{.*?}', response.text, re.S).group())
                if rs['code'] == 200:
                    self.update_state_text(f"{rs['ticket']}(Response Code: {rs['code']})")
                    qr_ticket = rs['ticket']
                    break
                else:
                    self.update_state_text(f"{rs['msg']}(Response Code: {rs['code']})")
                    time.sleep(2)

            if not qr_ticket:
                self.update_state_text("ERROR: 二维码登录失败.")
                # self.isLogin = False
                return False

            # step 4: validate scan result
            self.headers['Host'] = 'passport.jd.com'
            self.headers['Referer'] = 'https://passport.jd.com/new/login.aspx'
            response = requests.get(
                urls[3],
                headers=self.headers,
                cookies=self.cookies,
                params={'t': qr_ticket},
            )
            if response.status_code != requests.codes.OK:
                self.update_state_text(f"二维码登录校验失败: {response.status_code}")
                # self.isLogin = False
                return False

            # 京东有时会认为当前登录有危险, 需要手动验证
            # url: https://safe.jd.com/dangerousVerify/index.action?username=...
            res = json.loads(response.text)
            if not response.headers.get('p3p'):
                if 'url' in res:
                    self.update_state_text(f"请进行手动安全验证: {res['url']}")
                    # self.isLogin = False
                    return False
                else:
                    self.update_state_text('登录失败, ERROR message: ' + res)
                    # self.isLogin = False
                    return False

            # login succeed
            self.headers['P3P'] = response.headers.get('P3P')
            self.cookies.update(response.cookies)
            self.sess.cookies = response.cookies

            # save cookie
            with open('cookie', 'wb') as f:
                pickle.dump(self.cookies, f)

            self.update_state_text("登录成功!")
            # self.isLogin = True
            self.get_user_name()
            return True

        except Exception as e:
            # self.isLogin = False
            self.update_state_text('ERROR message: ' + str(e))
            raise

    def get_user_name(self):
        userName_Url = 'https://passport.jd.com/new/helloService.ashx?callback=jQuery339448&_=' + str(
            int(time.time() * 1000))

        resp = self.sess.get(url=userName_Url, allow_redirects=True)
        result_text = resp.text
        result_text = result_text.replace('jQuery339448(', '')
        result_text = result_text.replace(')', '')
        user_name_json = json.loads(result_text)
        self.update_state_text('账号名称: ' + user_name_json['nick'])

    def check_stock(self):
        url = 'https://c0.3.cn/stocks'

        callback = 'jQuery' + str(random.randint(1000000, 9999999))

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "https://cart.jd.com/cart.action",
            "Connection": "keep-alive",
        }

        payload = {
            'type': 'getstocks',
            'skuIds': self.sku_id_string,
            'area': self.area_id,
            'callback': callback,
            '_': int(time.time() * 1000),
        }
        resp = self.sess.get(url=url, params=payload, headers=headers)
        resp_text = resp.text.replace(callback + '(', '').replace(')', '')
        resp_json = json.loads(resp_text)
        in_stock_sku_id = []
        no_has_sku_id = []
        abnormal_skuid = []

        sold_out = 0
        alloca = 0
        for i in self.sku_id:
            try:
                if resp_json[i]['StockStateName'] == '无货':
                    no_has_sku_id.append(i)
                    sold_out += 1
                elif resp_json[i]['StockStateName'] == '可配货':
                    no_has_sku_id.append(i)
                    alloca += 1
                else:
                    in_stock_sku_id.append(i)

            except Exception as e:
                abnormal_skuid.append(i)

        if sold_out != 0:
            self.update_state_text('监控的 %d 个商品无货.' % sold_out)
        if alloca != 0:
            self.update_state_text('监控的 %d 个商品所在地区暂无货, 未来可能配货.' % alloca)
        if len(abnormal_skuid) > 0:
            self.update_state_text('WARNING: %s 编号商品查询异常.' % ','.join(abnormal_skuid))
        return in_stock_sku_id

    def is_sold_out(self, sku_id):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "http://trade.jd.com/shopping/order/getOrderInfo.action",
            "Connection": "keep-alive",
            'Host': 'item.jd.com',
        }
        url = 'https://item.jd.com/{}.html'.format(sku_id)
        page = requests.get(url=url, headers=headers)

        page_text = page.text

        if "class=\"btn-special1 btn-lg btn-disable\" style=\"\">抢购</a>" in page_text:
            # 按钮灰了，买不了了
            return True
        if '该商品已下柜' in page.text:
            return True
        return False

    def select_all(self):
        url = "https://cart.jd.com/selectAllItem.action"
        data = {
            't': 0,
            'outSkus': '',
            'random': random.random()
        }
        resp = self.sess.post(url, data=data)
        if resp.status_code != requests.codes.OK:
            self.update_state_text('全选购物车商品出错! status_code: %u, URL: %s' % (resp.status_code, resp.url))
            return False
        self.update_state_text('全选购物车商品成功.')
        return True

    def cart_detail(self, is_output=False):
        url = 'https://cart.jd.com/cart.action'
        resp = self.sess.get(url, headers=self.headers)
        soup = BeautifulSoup(resp.text, "html.parser")

        cart_detail = dict()
        for item in soup.find_all(class_='item-item'):
            sku_id = item['skuid']  # 商品id
            try:
                # 例如: ['increment', '8888', '100001071956', '1', '13', '0', '50067652554']
                # ['increment', '8888', '100002404322', '2', '1', '0']
                item_attr_list = item.find(class_='increment')['id'].split('_')
                p_type = item_attr_list[4]
                promo_id = target_id = item_attr_list[-1] if len(item_attr_list) == 7 else 0

                def get_tag_value(tag, key='', index=0):
                    if key:
                        value = tag[index].get(key)
                    else:
                        value = tag[index].text
                    return value.strip(' \t\r\n')

                cart_detail[sku_id] = {
                    'name': get_tag_value(item.select('div.p-name a')),  # 商品名称
                    'verder_id': item['venderid'],  # 商家id
                    'count': int(item['num']),  # 数量
                    'unit_price': get_tag_value(item.select('div.p-price strong'))[1:],  # 单价
                    'total_price': get_tag_value(item.select('div.p-sum strong'))[1:],  # 总价
                    'is_selected': 'item-selected' in item['class'],  # 商品是否被勾选
                    'p_type': p_type,
                    'target_id': target_id,
                    'promo_id': promo_id
                }
            except Exception as e:
                self.update_state_text("ERROR: 商品%s在购物车中的信息无法解析, 报错信息: %s, 该商品自动忽略.", sku_id, e)

        if is_output:
            self.update_state_text('当前购物车信息: %s.' % cart_detail)
        return cart_detail

    def add_item_to_cart(self, sku_id):
        url = 'https://cart.jd.com/gate.action'
        addNum = self.comboBox.currentIndex() + 1
        payload = {
            'pid': sku_id,
            'pcount': addNum,
            'ptype': 1
        }
        resp = self.sess.get(url=url, params=payload)
        if 'https://cart.jd.com/cart.action' in resp.url:  # 套装商品加入购物车后直接跳转到购物车页面
            result = True
        else:  # 普通商品成功加入购物车后会跳转到提示 "商品已成功加入购物车！" 页面
            soup = BeautifulSoup(resp.text, "html.parser")
            result = bool(soup.select('h3.ftx-02'))  # [<h3 class="ftx-02">商品已成功加入购物车！</h3>]

        if result:
            self.update_state_text('%s 编号商品已成功加入购物车, 数量: %d.' % (sku_id, addNum))
        else:
            self.update_state_text('ERROR: %s 编号商品添加到购物车失败.' % sku_id)

    def response_status(self, resp):
        if resp.status_code != requests.codes.OK:
            self.update_state_text('Status: %u, Url: %s' % (resp.status_code, resp.url))
            return False
        return True

    def get_check_out_page_detail(self):
        url = 'http://trade.jd.com/shopping/order/getOrderInfo.action'
        # url = 'https://cart.jd.com/gotoOrder.action'
        payload = {
            'rid': str(int(time.time() * 1000)),
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "https://cart.jd.com/cart.action",
            "Connection": "keep-alive",
            'Host': 'trade.jd.com',
        }
        try:
            resp = self.sess.get(url=url, params=payload, headers=headers)

            if not self.response_status(resp):
                self.update_state_text('ERROR: 获取订单结算页信息失败.')
                return None
            soup = BeautifulSoup(resp.text, "html.parser")

            order_detail = {
                'address': soup.find('span', id='sendAddr').text[5:],
                'receiver': soup.find('span', id='sendMobile').text[4:],
                'total_price': soup.find('span', id='sumPayPriceId').text[1:],
                'items': []
            }

            self.update_state_text("下单信息: %s" % order_detail)
            return order_detail
        except requests.exceptions.RequestException as e:
            self.update_state_text('订单结算页面获取异常, ERROR message: %s.' % e)
        except Exception as e:
            self.update_state_text('下单页面数据解析异常, ERROR message: %s.' % e)
        return None

    def submit_order(self, risk_control, payment_pwd):
        url = 'https://trade.jd.com/shopping/order/submitOrder.action'
        # js function of submit order is included in https://trade.jd.com/shopping/misc/js/order.js?r=2018070403091

        # overseaPurchaseCookies:
        # vendorRemarks: []
        # submitOrderParam.sopNotPutInvoice: false
        # submitOrderParam.trackID: TestTrackId
        # submitOrderParam.ignorePriceChange: 0
        # submitOrderParam.btSupport: 0
        # riskControl:
        # submitOrderParam.isBestCoupon: 1
        # submitOrderParam.jxj: 1
        # submitOrderParam.trackId:

        data = {
            'overseaPurchaseCookies': '',
            'vendorRemarks': '[]',
            'submitOrderParam.sopNotPutInvoice': 'false',
            'submitOrderParam.trackID': 'TestTrackId',
            'submitOrderParam.ignorePriceChange': '0',
            'submitOrderParam.btSupport': '0',
            'riskControl': risk_control,
            'submitOrderParam.isBestCoupon': 1,
            'submitOrderParam.jxj': 1,
            'submitOrderParam.trackId': '9643cbd55bbbe103eef18a213e069eb0',  # Todo: need to get trackId
            # 'submitOrderParam.eid': eid,
            # 'submitOrderParam.fp': fp,
            'submitOrderParam.needCheck': 1,
        }

        def encrypt_payment_pwd(paymentPwd):
            return ''.join(['u3' + x for x in paymentPwd])

        if len(payment_pwd) > 0:
            data['submitOrderParam.payPassword'] = encrypt_payment_pwd(payment_pwd)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "http://trade.jd.com/shopping/order/getOrderInfo.action",
            "Connection": "keep-alive",
            'Host': 'trade.jd.com',
        }

        try:
            resp = self.sess.post(url=url, data=data, headers=headers)
            resp_json = json.loads(resp.text)

            if resp_json.get('success'):
                self.update_state_text('订单提交成功! 订单号: %s' % resp_json.get('orderId'))
                return True
            else:
                message, result_code = resp_json.get('message'), resp_json.get('resultCode')
                if result_code == 0:
                    # self._save_invoice()
                    message = message + '(下单商品可能为第三方商品, 将切换为普通发票进行尝试)'
                elif result_code == 60077:
                    message = message + '(可能是购物车为空或未勾选购物车中商品)'
                elif result_code == 60123:
                    message = message + '(未配置支付密码)'
                self.update_state_text('订单提交失败, 错误码: %s, 返回信息: %s.' % (result_code, message))
                self.update_state_text(resp_json)
                return False
        except Exception as e:
            self.update_state_text("ERROR: " + str(e))
            return False

    def cancel_select_cart_item(self):
        url = "https://cart.jd.com/cancelAllItem.action"
        data = {
            't': 0,
            'outSkus': '',
            'random': random.random()
        }
        resp = self.sess.post(url, data=data)
        if resp.status_code != requests.codes.OK:
            self.update_state_text(
                'cancelSelectCartItem() function WARNING: %u, Url: %s' % (resp.status_code, resp.url))
            return False
        return True

    def buy_goods(self, sku_id, retry_times):
        for i in range(1, retry_times):
            self.update_state_text('第 %d/%d 次尝试提交订单...' % (i, retry_times))
            self.cancel_select_cart_item()
            cart = self.cart_detail()
            if sku_id not in cart:
                self.add_item_to_cart(sku_id)
                self.cart_detail(True)

            risk_control = self.get_check_out_page_detail()
            if risk_control is not None:
                if self.submit_order(risk_control, ''):
                    return True
            time.sleep(1)
        else:
            self.update_state_text('执行结束，提交订单失败.')
            return False

    def monitor_connect(self):
        if not self.check_login():
            return False
        self.sku_id_string = self.inputGoods.text()
        pattern = re.compile(",|，")
        self.sku_id = pattern.split(self.sku_id_string)

        self.area_id = self.inputArea.text()

        self.timer.timeout.connect(self.monitor_main)
        self.update_state_text("当前轮询速度为 %f 秒/次." % (self.speed / 1000))

        # 自动忽略并删除下架商品
        if self.checkBox.isChecked():
            self.is_monitor_sold_out = False
            self.update_state_text('当前模式将为您自动忽略并删除下架商品.')
        else:
            self.is_monitor_sold_out = True
            self.update_state_text('当前模式将为您保持监控下架商品, 若其上架则立即抢购.')

        # 是否开启通知
        if self.checkEnableNoticeBox.isChecked():
            self.is_monitor_enable_notice = True
            self.update_state_text('开启下单成功通知.')
        else:
            self.is_monitor_enable_notice = False
            self.update_state_text('关闭下单成功通知.')

        self.timer.start(self.speed)  # 设置计时间隔并启动
        return True

    @staticmethod
    def send_mail(send_to, send_title, send_content):
        if send_to is None or len(send_to) == 0:
            return

        for mail in send_to:
            if mail is None or len(mail) == 0:
                return
            mail_re = re.compile('^\w{1,15}@\w{1,10}\.(com|cn|net)$')
            if not re.search(mail_re, mail):
                return

            send_from = global_config.getRaw('mail_from', 'account')
            smtp_server = global_config.getRaw('mail_from', 'smtp_server')
            smtp_server_port = int(global_config.getRaw('mail_from', 'smtp_server_port'))
            send_password = global_config.getRaw('mail_from', 'password')

            msg = MIMEText(send_content, 'plain', 'utf-8')
            msg['From'] = Header(send_from)
            msg['To'] = Header(mail)
            msg['Subject'] = Header(send_title)

            server = smtplib.SMTP_SSL(host=smtp_server)
            server.connect(smtp_server, smtp_server_port)
            server.login(send_from, send_password)
            server.sendmail(send_from, mail, msg.as_string())
            server.quit()

    @staticmethod
    def send_bark(bark_keys, send_title, send_content):
        if bark_keys is None or len(bark_keys) == 0:
            return

        server_ip = global_config.getRaw("messenger", "bark_server_ip")
        server_port = int(global_config.getRaw("messenger", "bark_server_port"))
        pusher = BarkPusher(server_ip, server_port, bark_keys.split(","))
        pusher.push_msg_content(send_title, send_content, "jd_sec_kill")

    def remove_item(self):
        url = "https://cart.jd.com/batchRemoveSkusFromCart.action"
        data = {
            't': 0,
            'null': '',
            'outSkus': '',
            'random': random.random(),
            'locationId': '19-1607-4773-0'
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.37",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://cart.jd.com/cart.action",
            "Host": "cart.jd.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://cart.jd.com",
            "Connection": "keep-alive"
        }

        resp = self.sess.post(url, data=data, headers=headers)
        if resp.status_code != requests.codes.OK:
            self.update_state_text('清空购物车勾选商品出错. status_code: %u, URL: %s.' % (resp.status_code, resp.url))
            return False

        self.update_state_text('清空购物车勾选商品成功!')
        return True

    def notify(self, sku_id, buy_result, custom_content=None):
        if custom_content is not None:
            send_title = "通知!"
            send_content = custom_content
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Referer": "http://trade.jd.com/shopping/order/getOrderInfo.action",
                "Connection": "keep-alive",
                'Host': 'item.jd.com',
            }
            url = 'https://item.jd.com/{}.html'.format(sku_id)
            page = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")
            goods_title = soup.find("title").text

            if buy_result:
                send_title = '抢购成功！' + goods_title
                send_content = '您抢购的 ' + goods_title + ' (' + url + ') 商品已下单, 请在尽快付款.'
            else:
                send_title = '抢购失败！' + goods_title
                send_content = '您抢购的 ' + goods_title + ' (' + url + ') 商品抢购失败.'

        # 发邮件
        self.send_mail(self.inputMail.text(), send_title, send_content)
        # 发bark
        self.send_bark(self.inputBark.text(), send_title, send_content)

    def monitor_main(self):
        try:
            check_session = requests.Session()
            check_session.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/75.0.3770.100 Safari/531.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                          "application/signed-exchange;v=b3",
                "Connection": "keep-alive"
            }
            self.update_state_text('第 ' + str(self.cont) + ' 次查询:')
            self.cont += 1
            in_stock_sku_id = self.check_stock()
            sold_out_num = 0

            retry_times = global_config.getRaw("config", "buy_retry_times")
            if retry_times is not None:
                retry_times = 5

            for skuId in in_stock_sku_id:
                if not self.is_sold_out(skuId):
                    self.update_state_text('%s 编号商品有货啦! 马上下单.' % skuId)
                    buy_result = self.buy_goods(skuId, retry_times)
                    if self.is_monitor_enable_notice:
                        self.notify(skuId, buy_result)
                    self.stop_now()

                else:
                    if not self.is_monitor_sold_out:
                        self.update_state_text('%s 编号商品已下架或抢空.' % skuId)
                        self.sku_id.remove(skuId)
                        id_beg = self.sku_id_string.find(str(skuId))
                        id_end = id_beg + len(str(skuId))
                        self.sku_id_string = self.sku_id_string[0:id_beg] + self.sku_id_string[id_end + 1:]
                        self.inputGoods.setText(self.sku_id_string)
                        self.update_state_text('已将 %s 编号的下架商品清除, 并更新了商品编号输入框.' % skuId)
                        self.select_all()
                        self.remove_item()
                    else:
                        sold_out_num += 1
            if sold_out_num != 0:
                self.update_state_text('监控的 %d 个商品已下架, 但当前模式保持监控.' % sold_out_num)

            if self.cont % 300 == 0:
                self.check_login()
        except Exception as e:
            import traceback
            self.update_state_text(traceback.format_exc())

    def update_state_text(self, state_text):
        # print(stateText)
        self.logger.info(state_text)
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.insertPlainText(f'{time.ctime()} > ' + state_text + '\n')


def main():
    app = QApplication(sys.argv)
    auto_buy = Autobuy()
    auto_buy.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
