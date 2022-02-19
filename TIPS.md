# in playsound.py,you should change it like this

def winCommand(*command):
        bufLen = 600
        buf = c_buffer(bufLen)
        #command = ' '.join(command).encode('utf-16')
        command = ' '.join(command)
        errorCode = int(windll.winmm.mciSendStringW(command, buf, bufLen - 1, 0))  # use widestring version of the function
        if errorCode:
            errorBuffer = c_buffer(bufLen)
            windll.winmm.mciGetErrorStringW(errorCode, errorBuffer, bufLen - 1)  # use widestring version of the function
            exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
            #                    '\n        ' + command.decode('utf-16') +
                                '\n        ' + command +
                                '\n    ' + errorBuffer.raw.decode('utf-16').rstrip('\0'))
            logger.error(exceptionMessage)
            raise PlaysoundException(exceptionMessage)
        return buf.value