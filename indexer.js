// Takes json list of page descriptions and put an index together.

var makeblog = require('./utils');
var fs = require('fs');

var main_index_path = process.argv[2];
var existing_index;

var tmpdir = process.argv[3];

var input_paths = process.argv.slice(4);
var jsons = [];

var throwErr = function (err) { if (err) throw err; }

var genAll = function () {
  // Only documents with date are considered posts.
  jsons = jsons.filter(function (val) { return val && val.date; });

  // Don't change anything if there are no new/updated posts.
  if (jsons.length > 0) {
    
    var new_posts_paths = jsons.reduce(function (aggregate, value) {
      aggregate[value.json] = true;
      return aggregate;
    }, {});

    var posts = (existing_index.posts || []).
      filter(function (val) {
        return !new_posts_paths[val.json];
      }).
      concat(jsons).
      sort(function (a, b) {
        return a.date.str === b.date.str ? 0
          : a.date.str < b.date.str ? 1 : -1;
      });

    var tags = {};
    posts.forEach(function (post) {
      if (post.tags) post.tags.forEach(function (tag) {
        if (!tags[tag.name]) { tags[tag.name] = []; }
        tags[tag.name].push(post);
      });
    });
    
    var changed_tags = {};
    jsons.forEach(function (val) {
      if (val.tags) val.tags.forEach(function (tag) {
        changed_tags[tag.name] = true;
      });
    });

    var all_tags = [];
    for (var tag in tags) {
      if (tags.hasOwnProperty(tag)) {
        all_tags.push(makeblog.tagDescription(tag, tags[tag].length));
      }
    }
    
    all_tags.sort(function (tagDesc1, tagDesc2) {
      return tagDesc1.count == tagDesc2.count
        ? (tagDesc1.name == tagDesc2.name ? 0 : tagDesc1.name > tagDesc2.name ? 1 : -1)
      : tagDesc1.count > tagDesc2.count ? -1 : 1;
    });

    fs.writeFile(
      main_index_path,
      JSON.stringify(makeblog.indexStruct(undefined, posts, all_tags)),
      throwErr
    );
    
    for (var tag in changed_tags) {
      if (tags.hasOwnProperty(tag)) {
        fs.writeFile(
          tmpdir + '/' + makeblog.tagFileNameBase(tag) + '.index.json',
          JSON.stringify(makeblog.indexStruct('Tag: ' + tag, tags[tag], all_tags)),
          throwErr
        );
      }
    }
  }
};

var tryGenAll = function () {
  if (jsons.length == input_paths.length && existing_index) {
    genAll();
  }
}

fs.stat(main_index_path, function (err, info) {
  if (err || !info.isFile()) {
    console.error('Recreating index.');
    existing_index = {};
    tryGenAll();
  } else {
    fs.readFile(main_index_path, 'utf8', function (err, text) {
      if (err) throw err;
      existing_index = JSON.parse(text);
      tryGenAll();
    });
  }
});

var push = function (err, text) {
  if (err) throw err;
  jsons.push(JSON.parse(text));
  tryGenAll();
}


input_paths.forEach(function (path) {
  fs.readFile(path, 'utf8', push);
});
