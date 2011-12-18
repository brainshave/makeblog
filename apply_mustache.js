var mu = require('mu2');
var makeblog = require('./utils');

makeblog.readAllStdin(function (text) {
  data = JSON.parse(text);
  mu.compile(process.argv[2], function (err, obj) {
    if (err) throw err;
    mu.render(obj, data).on('data', function (chunk) {
      process.stdout.write(chunk);
    });
  });
});
