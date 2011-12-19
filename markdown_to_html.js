var fs = require('fs');
var yaml = require('yamlparser');
var marked = require('marked');
var makeblog = require('./utils');
//var hl = require('highlight').Highlight;

function parse(fragment) {
  //return hl(marked(fragment), false, true);
  return marked(fragment);
}

var input = fs.readFileSync(process.argv[2], 'utf8').split('\n&&&\n');
var data = yaml.eval(input[0]);
if (data.date) data.date = {
  str: data.date.toISOString().substring(0,10),
  day: data.date.getDate(),
  day0: makeblog.pad0(data.date.getDate(), 2),
  month: data.date.getMonth() + 1,
  month0: makeblog.pad0(data.date.getMonth() + 1, 2),
  year: data.date.getFullYear(),
  year0: makeblog.pad0(data.date.getFullYear(), 4),
};

if (data.tags) data.tags = data.tags.map(function(tag) {
  return makeblog.tagDescription(tag);
});

data.intro = parse(input[1]);
data.body = parse(input[2]);
data.markdown = process.argv[2];
data.json = process.argv[3];
data.html = process.argv[4];
fs.writeFileSync(process.argv[3], JSON.stringify(data) + '\n', 'utf8');

