;按CtrlAltl一键登录健迅电子病历系统子账号
^!l::
Send, masteruser｛Tab}mastercode{Enter};输入主账号masteruser和密码mastercode
Send, {Tab} ;使光标定位于子账号选择框
Send, ｛Down}{Down} ;按数次下箭头选择自己的子账号
Send, {Tab}{Tab}{Tab} ;使光标定位于密码输入框
Send, aliascode ;输入子账号密码aliascode
Send, {Enter} ;确定
return
