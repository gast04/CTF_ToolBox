import time
import frida
import IPython

print("starting frida hooking script...\n")

js = """
const membase = Module.findBaseAddress('libBMWCrypto.so');
const fstatat = memAddress(membase, '0x0', '0x1631C0');
console.log('Addr: ' + fstatat);
Interceptor.attach(fstatat, {
    onEnter: function (args) {
        console.log('[+] fstatat: ' + Memory.readUtf8String(args[1]));
        Memory.writeUtf8String(args[1], "/empty");
    }
});
"""


liblist = []
imports = []

def on_module(mess, data):
    liblist.append(mess['payload'])

def on_import(mess, data):
    imports.append(mess)

def enumerateModules():
    js_script = open("enumerateModules.js", "r+")
    script = session.create_script(js_script.read())
    script.on('message', on_module)
    script.load()
    print("Done: Enumerating Modules")

def enumerateImports():
    js_script = open("enumerateImports.js", "r+")
    script = session.create_script(js_script.read())
    script.on('message', on_import)
    script.load()
    print("Done: Enumerating Imports")

def interceptor():
    js_script = open("interceptor.js", "r+")
    script = session.create_script(js_script.read())
    script.load()

session = frida.get_usb_device().attach("de.bmw.connected")
#enumerateModules()
#enumerateImports()
#interceptor()

script = session.create_script(js)
script.load()

'''

libBMWCrypto + 0x1631C0 -> encryptFile (5 paramters according to IDA)

'''

#time.sleep(2)
#IPython.embed()
input()

"""
{'name': 'base.odex', 
'base': '0xcc648000', 
'size': 21561344, 
'path': '/data/app/de.bmw.connected-uS0RSKT31NsgnNcnmVJZJA==/oat/x86/base.odex'}

{'name': 'libsqlcipher.so', 
'base': '0xc6a58000', 
'size': 3977216, 
'path': '/data/app/de.bmw.connected-uS0RSKT31NsgnNcnmVJZJA==/lib/x86/libsqlcipher.so'}

{'name': 'libBMWCrypto.so', 
'base': '0xbdd8b000', 
'size': 2424832, 
'path': '/data/app/de.bmw.connected-uS0RSKT31NsgnNcnmVJZJA==/lib/x86/libBMWCrypto.so'}
"""
