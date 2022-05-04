# -*- coding=utf-8 -*-
import requests
import logging
import logging.handlers
import time
import json
import sys
import random
from bs4 import BeautifulSoup
import smtplib
import re
from email.mime.text import MIMEText
from email.header import Header
from config import global_config
from bark.bark_pusher import BarkPusher

import traceback


def set_logger(log_file_name, logger):
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        log_file_name, maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_tag_value(tag, key='', index=0):
    if key:
        value = tag[index].get(key)
    else:
        value = tag[index].text
    return value.strip(' \t\r\n')


def response_status(resp):
    if resp.status_code != requests.codes.OK:
        print('Status: %u, Url: %s' % (resp.status_code, resp.url))
        return False
    return True


def validate_cookies(logger, session):
    for flag in range(1, 3):
        try:
            target_url = 'https://order.jd.com/center/list.action'
            payload = {
                'rid': str(int(time.time() * 1000)),
            }
            resp = session.get(url=target_url, params=payload, allow_redirects=False)
            if resp.status_code == requests.codes.OK:
                logger.info('登录成功!')
                return True
            else:
                logger.info('第[%s]次请重新获取cookie...', flag)
                time.sleep(5)
                continue
        except Exception as e:
            logger.info('第[%s]次请重新获取cookie...', flag)
            time.sleep(5)
            continue


def get_user_name(logger, session):
    userName_Url = 'https://passport.jd.com/new/helloService.ashx?callback=jQuery339448&_=' + str(
        int(time.time() * 1000))
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "https://order.jd.com/center/list.action",
        "Connection": "keep-alive"
    }
    resp = session.get(url=userName_Url, allow_redirects=True)
    result_text = resp.text
    result_text = result_text.replace('jQuery339448(', '')
    result_text = result_text.replace(')', '')
    user_name_json = json.loads(result_text)
    logger.info('登录账号名称: ' + user_name_json['nick'])


def cancel_select_cart_item(session):
    url = "https://cart.jd.com/cancelAllItem.action"
    data = {
        't': 0,
        'outSkus': '',
        'random': random.random()
    }
    resp = session.post(url, data=data)
    if resp.status_code != requests.codes.OK:
        print('Status: %u, Url: %s' % (resp.status_code, resp.url))
        return False
    return True


def cart_detail(session, logger, is_output=False):
    url = 'https://cart.jd.com/cart.action'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "https://order.jd.com/center/list.action",
        "Host": "cart.jd.com",
        "Connection": "keep-alive"
    }
    resp = session.get(url, headers=headers)
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
            logger.error("商品%s在购物车中的信息无法解析, 报错信息: %s, 该商品自动忽略", sku_id, e)

    if is_output:
        logger.info('当前购物车信息: %s', cart_detail)
    return cart_detail


def change_item_num_in_cart(sku_id, vender_id, num, p_type, target_id, promo_id, session):
    url = "https://cart.jd.com/changeNum.action"
    data = {
        't': 0,
        'venderId': vender_id,
        'pid': sku_id,
        'pcount': num,
        'ptype': p_type,
        'targetId': target_id,
        'promoID': promo_id,
        'outSkus': '',
        'random': random.random(),
        # 'locationId'
    }
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "https://cart.jd.com/cart",
        "Connection": "keep-alive"
    }
    resp = session.post(url, data=data)
    return json.loads(resp.text)['sortedWebCartResult']['achieveSevenState'] == 2


def add_item_to_cart(sku_id, session, logger):
    url = 'https://cart.jd.com/gate.action'
    payload = {
        'pid': sku_id,
        'pcount': 1,
        'ptype': 1,
    }
    resp = session.get(url=url, params=payload)
    if 'https://cart.jd.com/cart.action' in resp.url:  # 套装商品加入购物车后直接跳转到购物车页面
        result = True
    else:  # 普通商品成功加入购物车后会跳转到提示 "商品已成功加入购物车！" 页面
        soup = BeautifulSoup(resp.text, "html.parser")
        result = bool(soup.select('h3.ftx-02'))  # [<h3 class="ftx-02">商品已成功加入购物车！</h3>]

    if result:
        logger.info('%s 已成功加入购物车', sku_id)
    else:
        logger.error('%s 添加到购物车失败', sku_id)
    return result


def get_checkout_page_detail(session, logger):
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
        resp = session.get(url=url, params=payload, headers=headers)
        if not response_status(resp):
            logger.error('获取订单结算页信息失败')
            return ''

        soup = BeautifulSoup(resp.text, "html.parser")
        risk_control = get_tag_value(soup.select('input#riskControl'), 'value')

        order_detail = {
            'address': soup.find('span', id='sendAddr').text[5:],  # remove '寄送至:  ' from the begin
            'receiver': soup.find('span', id='sendMobile').text[4:],  # remove '收件人:' from the begin
            'total_price': soup.find('span', id='sumPayPriceId').text[1:],  # remove '￥' from the begin
            'items': []
        }

        logger.info("下单信息: %s", order_detail)
        return order_detail
    except requests.exceptions.RequestException as e:
        logger.error('订单结算页面获取异常: %s' % e)
    except Exception as e:
        logger.error('下单页面数据解析异常: %s', e)
    return None


def submit_order(risk_control, session, logger, payment_pwd):
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
        resp = session.post(url=url, data=data, headers=headers)
        resp_json = json.loads(resp.text)

        if resp_json.get('success'):
            logger.info('订单提交成功! 订单号: %s', resp_json.get('orderId'))
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
            logger.info('订单提交失败, 错误码: %s, 返回信息: %s', result_code, message)
            logger.info(resp_json)
            return False
    except Exception as e:
        logger.error(e)
        return False


def item_removed(sku_id, logger, session):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "http://trade.jd.com/shopping/order/getOrderInfo.action",
        "Connection": "keep-alive",
        'Host': 'item.jd.com',
    }
    url = 'https://item.jd.com/{}.html'.format(sku_id)
    page = session.get(url=url, headers=headers)

    if "刷新太频繁了" in page.text:
        # 刷新太频繁
        logger.info("[{}]刷新太频繁".format(sku_id))
        return True
    if "class=\"btn-special1 btn-lg btn-disable\" style=\"\">抢购</a>" in page.text:
        # 按钮灰了，买不了了，抢没了
        logger.info("[{}]已经抢空".format(sku_id))
        return True
    if '该商品已下柜' in page.text:
        logger.info("[{}]商品已下柜".format(sku_id))
        return True
    return False


def buy_good(sku_id, session, logger, payment_pwd):
    for count in range(1, 5):
        logger.info('第[%s/%s]次尝试提交订单', count, 5)
        cancel_select_cart_item(session)
        cart = cart_detail(session, logger)
        if sku_id not in cart:
            if not add_item_to_cart(sku_id, session, logger):
                continue
            cart_detail(session, logger, True)

        risk_control = get_checkout_page_detail(session, logger)
        if len(risk_control) > 0:
            if submit_order(risk_control, session, logger, payment_pwd):
                return True
        logger.info('等待%ss', 3)
        time.sleep(3)
    else:
        logger.info('执行结束, 提交订单失败！')
        return False


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


def send_bark(bark_keys, send_title, send_content):
    if bark_keys is None or len(bark_keys) == 0:
        return

    server_ip = global_config.getRaw("messenger", "bark_server_ip")
    server_port = int(global_config.getRaw("messenger", "bark_server_port"))
    pusher = BarkPusher(server_ip, server_port, bark_keys)
    pusher.push_msg_content(send_title, send_content, "jd_sec_kill")


def notify(sku_id, buy_result, custom_content=None):
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
    send_to = global_config.getRaw("messenger", "mails").split(",")
    send_mail(send_to, send_title, send_content)
    # 发bark
    bark_keys = global_config.getRaw("messenger", "bark_keys").split(",")
    send_bark(bark_keys, send_title, send_content)


random_max = 0
random_min = 0
range_arr = global_config.getRaw("config", "loop_interval_random_time_range").split(",")
if range_arr is not None and len(range_arr) == 2:
    random_min = int(range_arr[0])
    random_max = int(range_arr[1])


def wait_some_time(logger):
    if random_min > 0 and random_max > 0:
        wait_time = random.randint(random_min, random_max)
    else:
        wait_time = int(global_config.getRaw("config", "loop_interval"))
    logger.info("Monitor.loop.wait.%d..." % wait_time)
    time.sleep(wait_time)


def main(cookies_string, url):
    session = requests.session()
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Connection": "keep-alive"
    }

    log_file_name = global_config.getRaw('config', 'log_name')
    logger = logging.getLogger()
    set_logger(log_file_name, logger)

    manual_cookies = {}
    for item in cookies_string.split(';'):
        # 用=号分割.
        name, value = item.strip().split('=', 1)
        manual_cookies[name] = value

    # print(manual_cookies)
    cookies_jar = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None, overwrite=True)
    session.cookies = cookies_jar

    payment_pwd = ''
    flag = 1
    while True:
        try:
            if flag == 1:
                validate_cookies(logger, session)
                get_user_name(logger, session)
            check_session = requests.Session()
            check_session.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/79.0.3945.130 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                          "application/signed-exchange;v=b3",
                "Connection": "keep-alive"
            }
            logger.info('第' + str(flag) + '次 查询...')
            flag += 1

            url = global_config.get("config", "goods_urls").split(";")

            for i in url:
                if i is None or len(i) == 0:
                    continue
                # 商品url
                sku_id = i.split('skuIds=')[1].split('&')[0]
                response = check_session.get(i)

                if response.text.find('无货') > 0:
                    logger.info('[%s]商品无货.', sku_id)
                elif response.text.find('可配货') > 0:
                    logger.info('[%s]商品等待配货.', sku_id)
                else:
                    if not item_removed(sku_id, logger, session):
                        logger.info('[%s]商品有货啦! 马上下单...', sku_id)
                        buy_result = buy_good(sku_id, session, logger, payment_pwd)

                        if bool(global_config.getRaw('messenger', 'enable')):
                            notify(sku_id, buy_result)
                        if buy_result:
                            sys.exit(1)

                    else:
                        logger.info('[%s]商品有货, 但已下架.', sku_id)

            # 循环间隔时间
            wait_some_time(logger)

            if flag % 20 == 0:
                logger.info('校验是否还在登录...')
                validate_cookies(logger, session)
        except Exception as e:
            print(traceback.format_exc())
            time.sleep(10)


if __name__ == '__main__':
    cookies_string = global_config.getRaw("config", "cookies")
    if cookies_string is None or len(cookies_string) == 0:
        print("ERROR: Missing cookie.")

    goods_urls = global_config.getRaw("config", "goods_urls").split(",")

    try:
        main(cookies_string, goods_urls)
    except Exception as e:
        notify(0, False, custom_content=e)
