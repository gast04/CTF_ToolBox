import frida
import sys
import time

def on_message(mess, data):
    print(mess) #['payload']
    #print mess, data

# attach to process
sess = frida.attach("sample")

# binary is not PIE
func_addr = 0x401136
#func_addr = 0x1149

# open and load js script from file
js_script = open("inst.js", "r+")
script = sess.create_script(js_script.read() % func_addr)

script.on('message', on_message)
script.load()

time.sleep(100) # to keep script alive

