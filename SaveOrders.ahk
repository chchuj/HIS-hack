;按Ctrl+F2保存健迅HIS医生工作站系统医嘱
^F2::
Send, {F2} ;保存
WinWaitActive, 用户确认 ;等保存的窗口弹出
Send, 12345 ;录入者工号
Send, {Enter} ；光标移动到下一格
Send, 54321 ;录入者密码
Send, {Enter}
return
