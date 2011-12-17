# Makeblog, Rebuilt

This is (new/will be) version of Makeblog. Some assumptions:

- Abandon own parser and use existing Markdown parser.
- Reuse, reuse, reuse! (components, programs, Unix commands, etc.)
- Don't force site rebuilding when only static data is changed (styles, images, etc.)
- Create actual script `makeblog` -- ideally it will only invoke make with appropriate configuration loaded (from current dir) and Makefile (from makeblog's dir).
- If that fails or will be annoying to use, configuration should be simple: create Makefile in your site's dir, set and export some variables and include Makefile from makeblogs dir.