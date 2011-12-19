// Takes json list of page descriptions and put an index together.

var makeblog = require('./utils');
var fs = require('fs');

var main_index = process.argv[2];
var tmpdir = process.argv[3];

var inputs = process.argv.slice(4);

var jsons = [];

var throwErr = function (err) { if (err) throw err; }

var genAll = function () {
  var posts = jsons.
    filter(function (val) {
      // Only documents with date are considered posts.
      return val && val.date;
    }).
    sort(function (a, b) {
      return a.date.str === b.date.str ? 0
        : a.date.str < b.date.str ? 1 : -1;
    });

  var tags = {};
  posts.forEach(function (post) {
    post.tags && post.tags.forEach(function (tag) {
      if (!tags[tag.name]) { tags[tag.name] = []; }
      tags[tag.name].push(post);
    });
  });

  var all_tags = [];
  for (var tag in tags) {
    if (tags.hasOwnProperty(tag)) {
      all_tags.push(makeblog.tagDescription(tag, tags[tag].length));
    }
  }
  all_tags.sort(function (tagDesc1, tagDesc2) {
    return tagDesc1.count == tagDesc2.count ? 0
      : tagDesc1.count < tagDesc2.count  ? 1 : -1;
  });
  
  fs.writeFile(
    main_index,
    JSON.stringify(makeblog.indexStruct(undefined, posts, all_tags)),
    throwErr
  );

  for (var tag in tags) {
    if (tags.hasOwnProperty(tag)) {
      fs.writeFile(
        tmpdir + '/' + makeblog.tagFileNameBase(tag) + '.json',
        JSON.stringify(makeblog.indexStruct('Tag: ' + tag, tags[tag], all_tags)),
        throwErr
      );
    }
  }
};

var push = function (err, text) {
  if (err) throw err;
  jsons.push(JSON.parse(text));
  if (jsons.length == inputs.length) genAll();
}


inputs.forEach(function (path) {
  fs.readFile(path, 'utf8', push);
});
