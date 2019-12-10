import msvcrt, sys, os
print('password: ', end='', flush=True)

li = []

while 1:
    ch = msvcrt.getch()
    #回车
    if ch == b'\r':
        msvcrt.putch(b'\n')
        print('输入的密码是：%s' % b''.join(li).decode())
        break
    #退格
    elif ch == b'\x08':
        if li:
            li.pop()
            msvcrt.putch(b'\b')
            msvcrt.putch(b' ')
            msvcrt.putch(b'\b')
    #Esc
    elif ch == b'\x1b':
        break
    else:
        li.append(ch)
        msvcrt.putch(b'*')

os.system('pause')
