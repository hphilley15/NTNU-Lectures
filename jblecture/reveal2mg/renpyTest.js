const parser = require("./renpy.js")

tests = [   "'xxyyx cvcvc xxx'", 
            '  \n"This is the new lecture style"  \n', 
            '"""A\nmultiline\nstring"""', 
            "'''Another\r\ntest'''" ]
for(var i = 0; i < tests.length; i++ ) {
    try{
        console.log("Trying to parse |" + tests[i] + "|");
        parser.parse(tests[i]);
        console.log('Success');
    }
    catch(err) {
        console.log('Syntax Error');
        console.log(err);
        throw( err );
    }
} 

tests = [ 
"label test:\n" +
"       \"My message is clear!\"",
"label test2:\n" +
"   \"bob\" \"Hello\"\n" +
"  \t \"marry\" \"Hello Bob\"\n"
]

for(var i = 0; i < tests.length; i++ ) {
    try{
        console.log("Trying to parse |" + tests[i] + "|");
        parser.parse(tests[i]);
        console.log('Success');
    }
    catch(err) {
        console.log('Syntax Error');
        console.log(err);
        throw( err );
    }
} 
