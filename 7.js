// import file and arrange as an array of arrays of arrays:
    // each entry of the outermost array is an array:
        // its first entry is the command line, an array:
            // its 0th entry is either 'cd' or 'ls'
            // its 1st entry only exists if the former is 'ls' 
        // its remaining entries only exist if the command is 'ls' (not 'cd')
        // each remaining entry is a line returned from the computer, split by spaces:
            // if it represents a directory, then this array looks like ['dir', directoryName]
            // if it represents a file, then this array looks like [fileSize, fileName]

const fs = require('fs');

const file = fs.readFileSync('7.txt').toString()

const lines = file.split('$ ').filter(elt => elt)

let commands1 = [];

lines.forEach(line => commands1.push(line.split('\n').filter(elt => elt)))

let commands = [];

commands1.forEach(arr => {
    let subArr = [];
    arr.forEach(line => subArr.push(line.split(' ')))
    commands.push(subArr)
});



// console.log(commands.slice(0,5))







// define constructor for the rooted tree-like structure

function Directory(name, parent = null) {
    this.name = name;
    this.subdirectories = {}; // key-value pairs are names and directories (recursively)
    this.parent = parent;
    this.files = {}; // key-value pairs are names and sizes
}


// initialize root directory and pointer to current directory

const root = new Directory('root');

let pointer = root;


// read a single array: a command line followed by the results

function read(arr) {
    const command = arr[0][0];
    // change directory
    if (command === 'cd') {
        const target = arr[0][1]
        if (target === '/') {
            pointer = root;
        } else if (target === '..') {
            pointer = pointer.parent;
        } else {
            // assume that anytime we change to a subdirectory, we've already seen it through an ls command
            pointer = pointer.subdirectories[target];
        }
    }
    // list contents
    if (command === 'ls') {
        const contents = arr.slice(1,)
        contents.forEach(line => {
            if (line[0] === 'dir') {
                console.log('adding the new directory', line[1], 'and pointer is:', pointer)
                pointer.subdirectories[line[1]] = new Directory(line[1], pointer);
            } else {
                pointer.files[line[1]] = Number(line[0]);
            }
        })
    }
}


for (let i=0; i < 3; i++) {
    read(commands[i]);
    console.log(`after reading commands[${i}], root is:`, root, '\nand pointer is:', pointer)
}







