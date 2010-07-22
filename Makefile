# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# Makefile that makes it all happen

blog: blog_main

# Append to this variable to compile your targets in blog:
ALL_TARGETS := 

# Include rules from all makefiles in "makefiles" dir:
include makefiles/*.mk

blog_main: output $(ALL_TARGETS)

output: 
	mkdir output
clean:
	rm -rf $(ALL_TARGETS)
