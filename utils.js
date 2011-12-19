var escape = require('querystring').escape;

exports.tagFileNameBase = function(tag) {
  return tag.replace(' ', '_') + '.index';
};

exports.tagDescription = function (tag, count) {
  var filename = exports.tagFileNameBase(tag);
  return { name: tag, html: filename + '.html', xml: filename + '.xml', count: count};
};

exports.indexStruct = function (title, posts, all_tags) {
  return {
    title: title,
    date: posts[0].date,
    posts: posts,
    all_tags: all_tags
  };
};

exports.pad0 = function (number, len) {
  var str = number.toString();
  var zeros = '';
  var i;
  for (i = 0; i < len - str.length; ++i) {
    zeros += '0';
  }
  return zeros + str;
};
