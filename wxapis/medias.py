#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    企业微信允许用户上传【临时素材文件】，
    并通过 API 接口获取 `media_id`，
    该 ID 用于在企业内的应用之间共享和发送消息。

    以下是关于如何上传临时素材以及相关要求的详细说明：
        - 获取 `media_id`:
          上传文件后，将获得一个 `media_id`。
          请注意，【该 ID 自发放之日起仅有效三天】，
          并可在同一企业内各应用间共享。

        - 上传文件:
          使用 `multipart/form-data` 类型的 POST 请求来上传文件。

        - 包含信息: 提交的 `form-data` 中，
          媒体文件标识应附带 `filename`（文件展示名称）
          和 `content-type`（媒体类型）等信息。

          (
              `filename` 说明:
              此字段决定使用该 `media_id` 发送消息时【展示给接收者的文件名】。
          )

    为了确保系统处理效率和稳定性，遵守以下关于不同类型媒体文件的大小限制：
        - 图片 (image): 最大支持 10 MB，
          格式限制为 JPG 或 PNG。

        - 语音 (voice): 最大支持 2 MB，
          播放时间不超过 60 秒，仅支持 AMR 格式。

        - 视频 (video): 最大支持 10 MB，
          仅支持 MP4 格式。

        - 普通文件 (file): 最大支持 20 MB。

        (
            企业微信作为一个专业的企业通讯和工作协同平台，
            提供一套完整的 API 接口供开发者使用，
            包括发送媒体文件到应用中。

            按照描述，上传媒体文件是一个两步骤的过程：
            首先上传媒体文件获取到一个媒体文件 ID，
            然后再使用这个 ID 来发送消息。

            这个过程看似繁琐，但实际上有其合理性和必要性：
                - 安全性：通过 API 接口上传文件意味着需要进行身份验证。
                  这样可以确保只有授权的用户或系统能够上传文件，
                  防止恶意内容或病毒代码被传播。

                - 效率：将媒体文件上传与发送消息分成两个步骤可以提高效率。
                  一旦媒体文件被上传并获得一个 ID，
                  在后续的通讯中可以重复使用这个 ID 而无需重新上传相同的文件。

                - 可靠性：通过预先上传到服务器，并在服务器上进行管理，
                  可以确保当发送消息时不会因为网络问题或文件大小导致发送失败。

                - 灵活性：获取媒体 ID 之后可以对其进行多种操作。
                  除发送消息，
                  还可能用在其他需要引用该媒体资源的场景。

                - 性能优化：对于大型企业来说，可能会有大量的文件传输需求。
                  分开处理上传和发送可以避免服务在高负载时出现瓶颈。

                - 一致性：企业微信可能希望维持 API 接口设计上的一致性。
                  许多其他类似平台也是采用类似模式处理复杂对象
                  （如图片、视频等）的处理和引用。

                - 服务端管理：通过这种方法，
                  企业微信平台能够更好地对媒体资源进行管理
                  （例如格式转换、压缩、备份等），提高用户使用时的体验。

            尽管如此，从开发者角度看待整个流程可能确实觉得
            比直接将文件作为请求附件发送更加复杂。

            但从长远角度看待系统设计、运营维护以及用户使用经验时，
            则这些步骤都是为确保整个生态系统长期稳定、安全且易于管理。
        )

    企业微信上传临时素材官方文档：
    https://developer.work.weixin.qq.com/document/path/90253。

    注意：本脚本中出现的 "py"，如无特殊说明，则指代 "Python"。
"""
from diskcache import Cache
import requests
import sys
import hashlib
import os
from pathlib import Path

# `__all__` 是一个特殊的列表
# 它定义当从模块执行 `from module import *` 时应该导入哪些属性
# 如果定义了 `__all__`，只有在这个列表中的属性才会被导入
# 如果没有定义 `__all__`，那么默认导入模块中不以下划线开头的所有属性
__all__ = [
    "UploadWXMedias"
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
from wxapis import WXWORK_API_BASE_URL  # noqa: E402
from wxapis.corporate import CorpApis  # noqa: E402

# 企业微信 API 中支持上传的媒体文件类型
MEDIA_TYPES = [
    "file",
    "image",
    "voice",
    "video"
]


class UploadWXMedias:
    def __init__(self, **kwargs):
        """
            初始化 `UploadWXMedias` 类的实例，
            用于上传媒体文件到企业微信。

            参数:
                - `corpid` (str): 企业微信的 `corpid`。

                - `agentid` (str): 企业微信的 `agentid`。

                - `secret` (str): 企业微信应用的凭证密钥。

        :param kwargs:
        """
        self._corpid = kwargs.get("corpid")
        self._agentid = kwargs.get("agentid")
        self._secret = kwargs.get("secret")
        self._api = None

    @property
    def __api(self) -> CorpApis:
        """
            返回 `CorpApis` 的实例，
            如果之前未创建，则首先创建它。

        :return: 返回一个 `CorpApis` 的实例，
        用于与企业微信 API 进行交互。
        """
        if not self._api:
            api = CorpApis(
                corpid=self._corpid,
                agentid=self._agentid,
                secret=self._secret
            )
            self._api = api
        return self._api

    @staticmethod
    def __hash_the_file(media: str):
        """
            计算并返回指定媒体文件内容的 SHA-256 哈希值。

            此函数设计用于验证文件的内容完整性，
            确保文件内容在传输或存储过程中未被篡改。

            通过计算文件的哈希值，可以用于比对文件是否保持不变，
            这在文件缓存管理中非常有用。

            例如，在将文件名作为缓存键时可能出现同名不同内容的情况，
            使用哈希值作为键则可以避免这一问题。

        :param media: 要进行哈希计算的文件路径。
        :return: 文件内容的 SHA-256 哈希值（十六进制形式）。
        """
        # 使用上下文管理器 `with` 安全打开要上传的文件
        # `mode` 设置为 "rb" 表示以二进制形式读取
        # `buffering` 设置缓冲区大小 10000000 `bytes`
        # 计算文件内容的哈希值作为缓存键
        with open(
                file=media,
                mode="rb",
                buffering=10000000
        ) as f_obj:
            file_content = f_obj.read()
            file_hash = hashlib.sha256(
                file_content
            ).hexdigest()
            f_obj.flush()
        return file_hash

    def upload(self, media_type: str, media: str) \
            -> dict or None:
        """
            上传指定类型的媒体文件到企业微信，并返回上传结果。

            首先，函数会计算文件内容的哈希值来检查是否已存在缓存的媒体 ID。

            如果存在，则直接返回缓存的媒体 ID。

            否则，函数会构建企业微信的上传 API URL，
            读取文件内容并通过 POST 请求将其发送至企业微信服务器。

            请求成功并且服务器返回媒体 ID 时，
            该 ID 将被缓存在本地，并设置三天的过期时间。

        :param media_type: 要上传文件的类型
        （如 "image"、"video" 等）。
        :param media: 本地文件路径，用于读取要上传的文件内容。
        :return: 如果上传成功，返回包含媒体 ID 的响应字典；
        如果失败或已有缓存，则可能返回 None 或已缓存的结果。
        """
        file_hash = self.__hash_the_file(
            media=media
        )
        # 检查是否已经有缓存
        cached_media_id = cache.get(file_hash)
        if cached_media_id:
            return cached_media_id
        if media_type not in MEDIA_TYPES:
            raise TypeError(
                f"\"{media_type}\" 不是一个有效的媒介类型。"
                f"有效的媒介类型包括 \"{','.join(MEDIA_TYPES)}\"。"
            )
        # 没有缓存，则上传文件并保存新的 `media_id` 到缓存
        media_url = f"{WXWORK_API_BASE_URL}/cgi-bin/media/upload?" \
                    f"access_token={self.__api.get_token()}" \
                    f"&type={media_type}"
        # 重新打开文件，因为之前已经读取过一次
        with open(file=media, mode="rb") as f_obj_second_time:
            # 发起 HTTP POST 请求至构建好的 `media_url` 地址
            # 在 `headers` 中声明内容类型和字符集
            # 在 `files` 中定义表单字段
            resp = requests.post(
                url=media_url,
                headers={
                    "Content-Type": "multipart/form-data",
                    "Charset": "utf-8"
                },
                files={
                    # `(media, f_obj, "", {})`:
                    # 是一个元组
                    # 其中包含要上传文件的路径、打开文件对象
                    # 空字符串表示 MIME 类型
                    # 空字典提供额外选项或头部信息
                    "type_": (
                        os.path.basename(media),
                        f_obj_second_time,
                        "",
                        {}
                    )
                }
            )
            f_obj_second_time.flush()
            if resp.status_code == 200 and "media_id" in resp.json():
                media_id = resp.json().get("media_id")
                # 将新获取到的 `media_id` 添加到缓存中
                # 并设置三天过期时间（以秒为单位）
                cache.set(
                    file_hash,
                    media_id,
                    expire=2 * 24 * 60 * 60 + 23 * 60 * 60
                )
                return media_id
