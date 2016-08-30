#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
;SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
;SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
;OneKeyLogOot
^!k::
Run %comspec% /c taskkill /f /im JXC.exe && taskkill /f /im EMRSysPlantform.exe

;提交
^!s::
Send, {F2}
Send, {F6}
Send, y
Send, 1 ;password
Send, {Enter}
Send, {Enter}

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
