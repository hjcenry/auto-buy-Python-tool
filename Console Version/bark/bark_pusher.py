import requests

from bark.time_level import TimeLevel
from bark.sound import SoundType


class BarkPusher(object):

    def __init__(self, server_ip: str, server_port: int, user_keys: list):
        self.server_ip = server_ip
        self.server_port = server_port
        self.user_keys = user_keys

    def push_msg_content(self, title, content, group_name: str):
        self.push_msg(title, content, group_name, None, None, None, None, None, None)

    def push_msg(self, title, content, group_name: str, forward_url: str, badge: int, icon_url: str,
                 sound: SoundType, time_level: TimeLevel, achieve: bool):
        """
        推送消息
        :param title:  标题
        :param content: 内容
        :param group_name: 分组名，通知中心按分组归类
        :param icon_url: 通知icon的url
        :param forward_url: 通知消息点击跳转url
        :param badge: 通知角标数字
        :param sound: 通知音效
        :param time_level: 通知时效性
        :param achieve: 是否归档保存推送，默认保存
        :return:
        """
        if title is None and content is None:
            msg = '没有内容'
        elif title is None:
            msg = self.get_valid_url_param(content)
        else:
            msg = "%s/%s" % (self.get_valid_url_param(title), self.get_valid_url_param(content))

        param = ""
        if achieve is not None and not achieve:
            param = param + "isAchieve=0&"
        if sound is not None:
            param = param + "sound=" + sound + "&"
        if icon_url is not None:
            param = param + "icon=" + icon_url + "&"
        if group_name is not None:
            param = param + "group=" + group_name + "&"
        if time_level is not None:
            param = param + "level=" + time_level + "&"
        if forward_url is not None:
            param = param + "url=" + forward_url + "&"
        if badge is not None:
            param = param + "badge=" + badge + "&"

        for user_key in self.user_keys:
            if user_key is None or user_key == "":
                content
            url = "http://%s:%d/%s/%s?%s" % (self.server_ip, self.server_port, user_key, msg, param)
            resp = requests.get(url)
            # logger.info("PUSH:%s\nRESP:%s" % (url, resp.text))

    def get_valid_url_param(self, check_content: str):
        return check_content.replace("/", " ")
