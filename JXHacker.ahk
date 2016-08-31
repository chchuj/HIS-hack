;一个改善“健迅医院信息系统”的外挂程序，基于AutoHotKey 1.1.24.01
;项目地址 https://github.com/chchuj/HIS-hack
;欢迎到https://github.com/chchuj/HIS-hack/issues提交反馈
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
;SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
;SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
^!9::
Run, %comspec% /c taskkill /f /im Ditto.exe
Run, %comspec% /c taskkill /f /im wText.exe
return

^!0::
Run, C:\Program Files\Ditto\Ditto.exe
Run, C:\Program Files\AquaDeskperiencechs\Aqua\wText.exe
return

^!2::
Run, C:\Program Files\双开电子病历.exe.lnk
return

;打印病程记录
^!p::
Send,!p{Down}{Down}{Enter}
return

;一键退出HIS全家桶
^!k::
Run, %comspec% /c taskkill /f /im JXC.exe
Run, %comspec% /c taskkill /f /im EMRSysPlantform.exe
return


;一键提交一条病程记录
^!s::
Send, {F3}
Send, {Enter}
Send, {F2}
Send, {F6}
Send, y
Send, 1 ;password
Send, {Enter}
Send, {Enter}
return

;把一段文字拷贝进病例系统
;原作者路人乙小明
;链接：http://www.zhihu.com/question/37702841/answer/73461176
^1::

;clipboard = %clipboard%   ; 把任何复制的文件, HTML 或其他格式的文本转换为纯文本.
txtsrc := clipboard
txtlen := StrLen(txtsrc)
Loop, %txtlen%{

a := SubStr(txtsrc,a_index,1)

SendInput,%a%

}

return
