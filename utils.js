exports.readAllStdin = function(callback) {
  process.stdin.setEncoding('utf8');
  process.stdin.resume();
  var data = [];
  
  process.stdin.on('data', function (chunk) {
    data.push(chunk);
  });
  
  process.stdin.on('end', function () {
    callback(data.join());
  });
};

exports.tagFileNameBase = function(tag) {
  return 'tag-' + escape(tag);
};
