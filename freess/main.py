
import re
import requests
import threading

from v2ray import SS
from v2ray import Trojan
from v2ray import Vmess
from utils import bs64_decode
from utils import bs64_encode
from utils import get_server_location
from utils import update_github_file


def get_subscription():
    url = "https://raw.githubusercontent.com/freefq/free/master/v2"
    proxies = {
        "http": "127.0.0.1:6666",
        "https": "127.0.0.1:6666",
    }
    proxies = proxies if proxy else {}
    response = requests.get(url=url, proxies=proxies).text
    return bs64_decode(response).strip().split("\n")


def change_ss_remark(ss: SS):
    ss.config["remark"] = get_server_location(ss.config["server"])
    new_links.append(ss.shared_link)


def change_trojan_remark(trojan: Trojan):
    trojan.config["remark"] = get_server_location(trojan.config["server"])
    new_links.append(trojan.shared_link)


def change_vmess_remark(vmess: Vmess):
    vmess.config["ps"] = get_server_location(vmess.config["add"])
    new_links.append(vmess.shared_link)


def change_remark():
    orig_links = get_subscription()
    rex = re.compile(r"www\.\d+\.xyz")  # 跳过XF那些地址
    tasks = []
    for link in orig_links:
        ser_type, ser_conf = link.split("://")
        if ser_type == "freess":
            ss = SS(link)
            tasks.append(threading.Thread(target=change_ss_remark, args=(ss,)))
        elif ser_type == "trojan":
            trojan = Trojan(link)
            tasks.append(threading.Thread(target=change_trojan_remark, args=(trojan,)))
        elif ser_type == "vmess":
            vmess = Vmess(link)
            if not rex.search(vmess.config["host"]):
                tasks.append(threading.Thread(target=change_vmess_remark, args=(vmess,)))

    [t.start() for t in tasks]
    [t.join() for t in tasks]


def save_to_file(s, file_name):
    with open(file_name, encoding="utf-8", mode="w") as f:
        f.write(bs64_encode(s))
    print("文件保存成功")


def sort_name(s):
    return s.split("#")[1] if "#" in s else s


if __name__ == "__main__":
    token = input()
    proxy = False  # 本地测试用代理
    new_links = []
    change_remark()
    new_links.sort(key=sort_name)
    url = "https://api.github.com/repos/JinggeLiang/ss/contents/v2"
    update_github_file(token, url, bs64_encode("\n".join(l for l in new_links)))
