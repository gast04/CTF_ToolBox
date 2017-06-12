

import frida, sys

app_name = "com.example.niskurt_win10.myapplication"

def on_message(message, data):
    print(message)

jscode = """
Java.perform(function () {
    // Function to hook is defined here
    var activity = Java.use('java.lang.String');

    // print all functions of object
    var proto = Object.getPrototypeOf(activity)
    var funcs = Object.getOwnPropertyNames(proto)
    send(funcs)

    for( var i = 0; i < funcs.length; i++){
        send(funcs[i].toString())
    }

    // create hook on function call, [C is a char array
    activity.copyValueOf.overload('[C').implementation = function (v1) {
        send('hook:' + v1);
        return "";
    };

});"""

# send the JS-script and execute it
process = frida.get_usb_device().attach(app_name)
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running Frida Example')
script.load()
sys.stdin.read()
