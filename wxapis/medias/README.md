# 企业微信媒体文件管理工具
> * 本文档旨在介绍如何使用媒体文件管理工具来获取企业微信中的媒体文件 `ID` 以及如何通过企业微信 `API` 发送媒体消息。

## 获取媒体 Media ID 指南

### 执行生成 Media ID 操作
* 若要生成特定类型媒体文件（比如图片或者文档）的 `Media ID`，请执行以下代码并替换相应参数：

    ```shell script
    from wxapis.medias import UploadWXMedias

    wx = UploadWXMedias(
        corpid="",
        agentid="",
        secret=""
    )
    media_id = wx.upload(
        media="test.txt",
        media_type="file"
    )
    print(media_id)
    ```

* 执行成功后，系统会输出如下所示的 `Media ID`：

    ```shell script
    3jqst_sDaeMmFqsUtNC95PtsT5UNMPk9x-yCKdDKs_sQXt8QUrwHi1XcQzJ19yJT5
    ```

## 向企业微信应用发送媒体文件指南

### 查看 smsg 命令帮助信息

* 若要了解如何使用 `smsg` 发送消息，请运行以下命令获取帮助信息：

    ```shell script
    # `smsg` 命令是安装完 `wxapis` 包后自动加载到系统路径中的命令工具
    smsg --help
    ```

* 您将看到如下用法说明：

    ```
    usage: smsg [-h] -c CORPID -s SECRET -i AGENTID -m MESSAGE [-a FIELD] [-f {json,yaml}]
            [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

    发送企业微信内部应用消息。
    
    optional arguments:
      -h, --help            显示此帮助信息并退出。
      -c CORPID, --corpid CORPID
                            企业微信的企业 id。可以在企业微信管理后台获取此 id。此选项为必须选项。
      -s SECRET, --secret SECRET
                            与企业微信内应用关联的 secret。secret 用于验证身份并加密通讯过程，可在企业微信管理后台找到。此选项为必须选项。
      -i AGENTID, --agentid AGENTID
                            企业微信内应用的 agent id，代表了应用实体，在企业微信中唯一标识一个应用。请确保传入正确的 agent id。此选项为必须选项。
      -m MESSAGE, --message MESSAGE
                            要发送给企业微信应用的消息文本内容。此选项为必须选项。
      -a FIELD, --field FIELD
                            消息体字段，格式为 "k=v"，添加或覆盖参数 `message` 中字段的值，例如 "-a text.content=xxx"。此选 项为可选选项。
      -f {json,yaml}, --format {json,yaml}
                            定义参数 `message` 文本内容的解析格式，默认为 "json"。此选项为可选选项。
      -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                            设置输出日志级别，默认为 "INFO"，在命令行传入时不区分大小写，比如传入 "DEBUG" 和传入 "debug" 一 样。此选项为可选选项。
    ```

### 执行发送消息操作

* 若要向指定用户发送携带已获取 `Media ID` 的图片或者其他类型文件，请按以下示例替换相应参数，并执行命令：

    ```shell script
    smsg --corpid "" 
    --agentid "" \
    --secret "" \
    --message '{\"touser\": \"\", \"agentid\": , \"msgtype\": \"image\", \"image\": {\"media_id\": \"\"}}'
    ```

* 成功发送后系统会返回结果数据类似于以下格式：

    ```
    INFO:root:发送消息[{'touser': '', 'agentid': , 'msgtype': 'image', 'image': {'media_id': ''}}]。
    INFO:root:任务执行："True"。
    ```
