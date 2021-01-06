
import json

from utils import (
    bs64_decode,
    bs64_encode,
    get_unicode,
    url_encode,
)


class Vmess:
    def __init__(self, subs):
        self.subs = subs
        self._config = {}

        self._get_vmess_config()

    @property
    def shared_link(self):
        """
        :return: vmess配置链接
        vmess://eyd2JzogJzInLCAncHMnOiAnXHU3ZjhlXHU1NmZkXHU2NWU3XHU5MAXxXHU1YzcxJywgJ2FkZCc6
                ICcxNTQuODQuMS46MTAnLCAncG9ydCc8ICc0NDMnLCAnaWQnOiAnNGUyZmM2ZTctNTZlNi00YTAy
                LTk5MTItYWZjNzU5M2NjOTllJywgJ2FpZCc6ICc2NCcsICduZXQnOiAnd3MnLCAndHlwZSc6ICdk
                dGxzJywgJ2hvc3Q1OiAnd3d3LjA5MjE5NzYzNTQueHl6JywgJ3BhdGgnOiAnL2Zvb3RlcnMnLCAn
                dGxzJzogJ3Rscyd9
        """
        return "vmess://" + bs64_encode(get_unicode(str(self._config).replace("'", '"')))

    @property
    def config(self):
        """
        :return: 服务器配置dict
                 {'v': '2', 'ps': 'US', 'add': '154.*.*.110', 'port': '443',
                  'id': '4e2fc6e7-56e6-4a02-9912-afc7593cc99e', 'aid': '64', 'net': 'ws',
                  'type': 'dtls', 'host': 'www.***.com', 'path': '/freess', 'tls': 'tls'}
        """
        return self._config

    @config.setter
    def config(self, v):
        #  修改dict用不上这个方法
        pass

    def _get_vmess_config(self):
        """
        通过分享链接获取Vmess配置
        """
        config = bs64_decode(self.subs[8:])  # vmess://...
        self._config = json.loads(config)


class SS:
    def __init__(self, subs):
        self.subs = subs
        self._config = {}

        self._get_ss_config()

    @property
    def shared_link(self):
        """
        :return: 配置链接
        freess://YWVzLTI1Ni1nY206cGFzc3dvcmQxMjM=@84.*.*.160:4666#%E7%BE%8E%E5%9B%BD%E6%97%A7%E9%87%91%E5%B1%B1
        """
        ss = "freess://"
        ss += bs64_encode(self.config["encryption"] + ":" + self.config["password"])
        ss += "@" + self.config["server"]
        ss += ":" + self.config["port"]
        ss += "#" + url_encode(self.config["remark"])
        return ss

    @property
    def config(self):
        """
        :return: 服务器配置dict
                 {'server': '84.*.*.160',
                  'port': '4666',
                  'encryption': 'aes-256-gcm',
                  'password': 'password123',
                  'remark': '%E7%BE%8E%E5%9B%BD%E6%97%A7%E9%87%91%E5%B1%B1'}
        """
        return self._config

    @config.setter
    def config(self, v):
        #  修改dict用不上这个方法
        pass

    def _get_ss_config(self):
        server, port = self.subs.split("@")[1].split("#")[0].split(":")
        encryption, password = bs64_decode(self.subs.split("@")[0][5:]).split(":")
        remark = self.subs.split("@")[1].split("#")[1]
        self._config = {
            "server": server,
            "port": port,
            "encryption": encryption,
            "password": password,
            "remark": remark
        }


class Trojan:
    def __init__(self, subs):
        self.subs = subs
        self._config = {}

        self._get_trojan_config()

    @property
    def shared_link(self):
        """
        :return: 配置链接
        trojan://0f137e0f-05ed-4729-8315-30970a73d4eb@xibun.cf:443#github.com/
                remark
        """
        trojan = "trojan://"
        trojan += self._config["password"]
        trojan += "@" + self._config["server"]
        trojan += ":" + self._config["port"]
        trojan += "#" + url_encode(self._config["remark"])
        return trojan

    @property
    def config(self):
        """
        :return: 服务器配置dict
        """
        return self._config

    @config.setter
    def config(self, v):
        #  修改dict用不上这个方法
        pass

    def _get_trojan_config(self):
        server, port = self.subs.split("@")[1].split("#")[0].split(":")
        password = self.subs.split("@")[0].split("//")[1]
        remark = self.subs.split("#")[1]
        self._config = {
            "server": server,
            "port": port,
            "password": password,
            "remark": remark
        }
