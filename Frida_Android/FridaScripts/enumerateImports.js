Module.enumerateImports("libsqlcipher.so",{
    onMatch: function(imp){
        send(imp);
    }, onComplete:function(){}
})
