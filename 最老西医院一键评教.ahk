#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

;以管理员身份运行
If not A_IsAdmin
{
   Run *RunAs "%A_ScriptFullPath%"
   ExitApp
}

;评价带教老师，Ctrl+alt+3
^!3::
Loop, 4
{
    Send, 5{Tab}{Tab}
}
Loop, 6
{
    Send, 10{Tab}{Tab}
}
Send, 20{Tab}{Tab}{Enter}
return

;评价科室，Ctrl+alt+4
^!4::
Loop, 20
{
    Send, 5{Tab}{Tab}
}
return