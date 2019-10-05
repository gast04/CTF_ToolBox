




/*
Interceptor.attach(Module.findExportByName("libcrypto.so", "somefunction"), {
    onEnter: function () {
	//var keySize = args[2].toInt32();
        //var keyDump = Memory.readByteArray(args[1], keySize);
        //console.log('HMAC Key found at ' + args[1]);
        //console.log('HMAC Key size = ' + keySize);
        //console.log(hexdump(keyDump, { offset: 0, length: keySize, header: false, ansi: false }));  
	  
	send("called");
    }
});
*/

/*
Interceptor.attach(Module.findExportByName("libcrypto.so", "somefunction"), {
    onEnter: function () {
	//var keySize = args[2].toInt32();
        //var keyDump = Memory.readByteArray(args[1], keySize);
        //console.log('HMAC Key found at ' + args[1]);
        //console.log('HMAC Key size = ' + keySize);
        //console.log(hexdump(keyDump, { offset: 0, length: keySize, header: false, ansi: false }));  
	  
	send("called");
    }
});
*/