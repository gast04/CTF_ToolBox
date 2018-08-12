
// enumerate over all Modules and get the Name and base address
Process.enumerateModules({
  onMatch: function(module){
    send('Name: ' + module.name + " - " + "Baddr: " + module.base.toString());
  }, 
  onComplete: function(){}
});

// enumerate through all Threads
Process.enumerateThreads({
  onMatch: function(thread){
    send('Module name: ' + thread.state + " - " + "Base Address: " + thread.context.pc);
  }, 
  onComplete: function(){}
});


// create Interceptors to attach to function calls
// functions calls in binary
Interceptor.attach(ptr("%s"), {
  onEnter: function(args) {
    // some basic informations
    //send("BaseAddr:" + Module.findBaseAddress("libc.so.6"));
    //send(Process.arch);
    //send(DebugSymbol.fromName('main'));
    
    // overwrite args
    args[0] = ptr(0); // overwrite sleep argument      
  }, 
  onLeave: function(retval) {
    retval.replace(1234);
  }
});

// intercepting libc function
Interceptor.attach(Module.findExportByName("libc.so.6", "sleep"), {
  onEnter: function(args) {
    send("sleep-arg[0]: " + args[0]);
  }
});

// intercepting libc function
Interceptor.attach(Module.findExportByName("libc.so.6", "printf"), {
    onEnter: function(args) {
      send("printf-arg[0]: " + args[0]);
    }
});

