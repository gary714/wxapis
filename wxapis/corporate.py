#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    企业微信【内部应用开发】概述：
        企业微信提供通讯录管理、客户联系、身份验证、应用管理、消息推送、素材管理、OA、
        效率工具、企业支付、企业互联、会话内容存档、电子发票、家校沟通、家校应用、
        政民沟通等 API，企业可以使用这些 API，为企业接入更多个性化的办公应用。

    简易教程：
        https://developer.work.weixin.qq.com/document/path/90487

    注意：本脚本中出现的 "py"，如无特殊说明，则指代 "Python"。
"""
import sys
from pathlib import Path
from diskcache import Cache

# `__all__` 是一个特殊的列表
# 它定义当从模块执行 `from module import *` 时应该导入哪些属性
# 如果定义了 `__all__`，只有在这个列表中的属性才会被导入
# 如果没有定义 `__all__`，那么默认导入模块中不以下划线开头的所有属性
__all__ = [
    "CorpApis"
]
cache = Cache(directory=".cache/")
# 将当前运行的 py 文件所在的上两级目录加入到 py 的【系统路径】中
# 使得在这个【根目录】下的【模块】和【包】可以被当前文件所引用
current_file_path = Path(__file__).absolute()
# 移动到上两级目录以获取【根路径】
root_path = current_file_path.parent.parent
# 将【根路径】作为【系统路径】加入 `sys.path`
sys.path.append(str(root_path))

# 在 py 代码中，`PEP 8` 是一个【编码风格指南】
# 其中 `E402` 错误意味着【模块级别的导入语句没有出现在文件的顶部】
# 对于某个特定的行，可以在该行末尾添加一个特殊的注释
# 来告诉 linter 忽略 `E402` 错误
# 即使用 `# noqa: E402` 告诉代码检查工具忽略此行上的 `E402` 错误
from wxapis.abstract import AbstractApis  # noqa: E402
from wxapis import WXWORK_GET_ACCESS_TOKEN  # noqa: E402

ACCESS_TOKEN_EXPIRE_TIME = 7000


class CorpApis(AbstractApis):
    def __init__(self, **kwargs):
        """
            初始化企业微信 API 接口类。

            该类负责管理企业微信 API 所需的认证信息，
            并在实例化时自动获取访问令牌。

        corpid (str): 每个【服务商】同时也是一个企业微信的【企业】，
        都有【唯一】的 `corpid`。
        获取此信息可在企业微信【管理后台】的 "我的企业" － "企业 ID" 查看。
        agentid (str): `agentid` 是指定应用在企业中的唯一标识 ID，
        通过此标识区分不同的应用。
        获取方法为：在【管理后台】 -> "应用与小程序" -> "应用"，
        选择对应的自建或者官方发布的应用，其详情页将显示该应用的 `agentid`。
        secret (str): `secret` 是企业应用里面用于保障数据安全的 "钥匙"，
        每一个应用都有一个独立的访问密钥，为了保证数据的安全，
        `secret` 务必不能泄漏。`secret` 查看方法：
        在【管理后台】 -> "应用管理" -> "应用" -> "自建"，
        点进某个应用，即可看到。
        """
        super().__init__()
        required_params = [
            "corpid",
            "agentid",
            "secret"
        ]
        missing_params = [
            param
            for param in required_params
            if param not in kwargs
        ]
        if missing_params:
            raise TypeError(
                f"\033[31m类实例化时缺少了以下必需的参数："
                f"\"{', '.join(missing_params)}\"。\033[0m"
            )
        self._corpid = kwargs.get("corpid")
        self._agentid = kwargs.get("agentid")
        self._secret = kwargs.get("secret")
        self._cached_token_key = \
            f"token_{self._corpid}_{self._agentid}"
        # 在初始化时自动获取 `token`
        # 即在初始化时自动执行函数以获得 `token` 并缓存
        self.get_token()

    def get_token(self) -> str:
        """
            获取当前【有效】的【访问令牌】。

            该方法负责从缓存中获取访问令牌，
            如果缓存中没有或令牌过期，
            会自动向微信服务器请求新的令牌并更新缓存。

        :return: 返回获取到的有效访问令牌。
        """
        access_token = cache.get(self._cached_token_key)
        if access_token:
            return access_token
        resp = self.httpReq(
            api=WXWORK_GET_ACCESS_TOKEN,
            params={
                # 企业 ID
                "corpid": self._corpid,
                # 应用的凭证密钥，注意应用需要是启用状态
                "corpsecret": self._secret,
            }
        )
        err_code = resp.get("errcode")
        # 注意：此处不能使用 `if err_code` 进行判断
        # 由于调用成功时 `err_code` 的值为 `0`
        # 如果直接使用 `if err_code` 进行判断
        # 则变成 `if 0`，那么它的结果只能是 `False`
        if err_code == 0:
            cache.set(
                self._cached_token_key,
                resp.get("access_token"),
                expire=ACCESS_TOKEN_EXPIRE_TIME
            )
            return access_token
