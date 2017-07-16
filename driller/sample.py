import driller               

d = driller.Driller("simple_test", "abcd", "\xff"*65535, "whatever~")             
inp = d.drill()              
inp 

