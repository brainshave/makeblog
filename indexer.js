// Takes json list of page descriptions and put an index together.

var makeblog = require('./utils');
var fs = require('fs');
var escape = require('querystring').escape;

makeblog.readAllStdin(function(text) {
  var posts = text.split('\n').
    filter(function (line) {
      // Get rid of empty lines.
      return line;
    }).
    map(function (line) {
      return JSON.parse(line);
    }).
    filter(function (val) {
      // Only documents with date are considered posts.
      return val && val.date;
    }).
    sort(function (a, b) {
      return a.date === b.date ? 0
        : a.date < b.date ? 1 : -1;
    });

  var tags = {};
  posts.forEach(function (post, i) {
    post.tags && post.tags.forEach(function (tag) {
      if (!tags[tag]) { tags[tag] = []; }
      tags[tag].push(post);
    });
  });

  var tag_list = [];
  for (var tag in tags) {
    if (tags.hasOwnProperty(tag)) {
      var filename = makeblog.tagFileNameBase(tag);
      tag_list.push({ name: tag, html: filename + '.html', xml: filename + '.xml'});
    }
  }
  
  process.stdout.write(JSON.stringify({ posts: posts, date: posts[0].date, tags: tag_list }));

  // First argument tells where to put indexes for tags (optional).
  if (process.argv.length > 2) {
    var tmpdir = process.argv[2];

    for (var tag in tags) {
      if (tags.hasOwnProperty(tag)) {
        fs.writeFile(tmpdir + '/' + escape(tag) + '.index.json', JSON.stringify({ title: 'Tag: ' + tag, date: tags[tag][0].date, posts: tags[tag], tags: tag_list }), function (err) {
          if (err) throw err;
        });
      }
    }
  }
});
