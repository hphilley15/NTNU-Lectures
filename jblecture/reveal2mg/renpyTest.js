const parser = require("./renpy.js")

tests = [   "'xxyyx cvcvc xxx'", 
            '"This is the new lecture style"', 
            '"""A\nmultiline\nstring"""', 
            "'''Another\r\ntest'''" ]
for(var i = 0; i < tests.length; i++ ) {
    try{
        parser.parse(tests[i]);
        console.log('Success');
    }
    catch(err) {
        console.log('Syntax Error');
        console.log(err)
    }
} 

tests = [ 
"label test:\n" +
"       \"My message is clear!\"",
]

for(var i = 0; i < tests.length; i++ ) {
    try{
        parser.parse(tests[i]);
        console.log('Success');
    }
    catch(err) {
        console.log('Syntax Error');
        console.log(err)
    }
} 
