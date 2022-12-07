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




// define constructor for the rooted tree-like structure

function Directory() {
    this.subdirectories = {}; // key-value pairs are names and directories
    this.files = {}; // key-value pairs are names and sizes
    this.size; // initialized to undefined, will later be computed recursively
}




// initialize root directory and pointer (which records the array of directories running from the root and ending with the working directory)

const root = new Directory();

let pointer = [root];




// read a single array: a command line followed by the returned results

function read(arr) {
    const command = arr[0][0];
    // change directory
    if (command === 'cd') {
        const target = arr[0][1]
        if (target === '/') {
            pointer = [root];
        } else if (target === '..') {
            pointer.pop();
        } else {
            pointer.push(pointer[pointer.length-1].subdirectories[target]);
        }
    }
    // list contents
    if (command === 'ls') {
        const contents = arr.slice(1,)
        contents.forEach(line => {
            if (line[0] === 'dir') {
                // console.log('adding the new directory', line[1], 'and pointer is:', pointer)
                pointer[pointer.length-1].subdirectories[line[1]] = new Directory();
            } else {
                pointer[pointer.length-1].files[line[1]] = Number(line[0]);
            }
        })
    }
}


// read the commands

commands.forEach(command => read(command));


// compute sizes

function size(dir) {
    let output = Object.values(dir.files).reduce((a,b) => a+b, 0);
    Object.values(dir.subdirectories).forEach(subdirectory => {
        size(subdirectory);
        output += subdirectory.size;
    })
    dir.size = output;
}

size(root);

console.log('size of root is:', root.size) // 45349983 (around  45 million)

let sum1 = 0;

function sumDirSizesUnder100k(dir) {
    if (dir.size < 100000) sum1 += dir.size;
    Object.values(dir.subdirectories).forEach(subdirectory => {
        sumDirSizesUnder100k(subdirectory);
    })
}

sumDirSizesUnder100k(root)

console.log('sum for part 1 is:', sum1);



// for part 2

const totalDiskSpace = 70000000; // 70 million
const spaceNeeded = 30000000; // 30 million
const spaceNow = totalDiskSpace - root.size; // 24650017 (around 24 million)
const toDelete = spaceNeeded - spaceNow; // 5349983 (around 5 million)

let answer = root.size;

function findSmallestDirSizeToDelete(dir) {
    if (dir.size >= toDelete) {
        if (dir.size <= answer) answer = dir.size;
        Object.keys(dir.subdirectories).forEach(subdirectoryName => {
            findSmallestDirSizeToDelete(dir.subdirectories[subdirectoryName]);
        });
    }
}

findSmallestDirSizeToDelete(root)

console.log('answer to part 2 is:', answer);