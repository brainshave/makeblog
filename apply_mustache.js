var fs = require('fs');
var mu = require('mu2');
var makeblog = require('./utils');

var layout = process.argv[2];
var input = process.argv[3];
var output = process.argv[4];


mu.compile(layout, function (err, obj) {
  if (err) throw err;
  fs.readFile(input, 'utf8', function (err, text) {
    if (err) throw err;
    data = JSON.parse(text);
    mu.render(obj, data).pipe(fs.createWriteStream(output, { encoding: 'utf8' }));
  });
});
