const parser = require("../NTNU-Lectures/jblecture/renpy.js")

tests = [ "'xxyyx'", '"This is the new lecture style"', '"""A\nmultiline\nstring"""', "'''Another\r\ntest'''" ]
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
