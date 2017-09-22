#!
# -*- coding:utf-8 -*-


import itchat
from itchat.content import *
from qqbot import _bot as bot


# 一般聊天
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # msg.user.send('%s: %s' % (msg.type, msg.text))
    user = msg.fromUserName
    print(user)
    nickname = itchat.search_friends(name=user)
    print(nickname)
    if nickname != []:
        user = nickname[0].NickName
    bot.SendTo(g, '来自 %s 的消息:\n%s' % (user, msg.text))


# 群聊
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        user = msg.fromUserName[2:]
        nickname = itchat.search_friends(name=user)
        if nickname != []:
            user = nickname[0].NickName
        bot.SendTo(g, '群聊被 %s @:\n%s' % (user, msg.text))
    else:
        bot.SendTo(g, '有新的群聊消息')


# 下载文件
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    itchat.send('@%s@%s' % (typeSymbol, msg.fileName), toUserName='filehelper')
    bot.SendTo(g, '收到 %s 类型文件,在微信端文件助手查看' % msg.type)


# 加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!——From WeQQChat Robot')
    bot.SendTo(g, '添加新好友')


if __name__ == "__main__":
    # 命令行扫码登录QQ， 之前登陆过有缓存可改为['-q', 'QQ号']直接登录
    # 更多命令查看源码或者在Login（）中故意输入一个错误的参数查看返回的帮助文档
    bot.Login(['-cq'])
    # 命令行扫码登录微信
    itchat.auto_login(enableCmdQR=True)

    # 在客户端显示登陆成功
    itchat.send('成功开启服务——From WeQQChat Robot', toUserName='filehelper')
    g = bot.List('group', '微信个人号助手')[0]
    bot.SendTo(g, '成功开启服务——From WeQQChat Robot')

    itchat.run()
