
Quick Tutorial to start and use Frida:
(https://www.frida.re/docs/android/)

download latest frida server version:
(take care frida client version and server version have to match!)

download from: https://github.com/frida/frida/releases
(android_x86 version could get started in genymotion simulator)


with the following adb commands, start the server:
./adb push /pathToFile/frida_server /data/local/tmp/    # copy file
./adb shell "chmod 755 /data/local/tmp/frida_server"    # make executable
./adb shell "/data/local/tmp/frida_server &"            # start server


to test if the server runs enter:
  frida-ps -U   # lists all running processes


connect to an running app with "frida -U pid"
(it has no documentation but a code/command completion with tab
https://www.frida.re/docs/frida-cli/)


The provided test exploit works with Genymotion, Android 7.1.0 device,
and frida version 10.0.12 (client and server)
everything is provided in the files folder.
