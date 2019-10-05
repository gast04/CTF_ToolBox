Interceptor.attach(Module.findExportByName("libsqlcipher.so", "memcpy"), {
    onEnter: function (args) {
        console.log('SRC: ' + hex(args[1]));
        console.log('DST: ' + hex(args[2]));
    }
});