1.  Regenerate only affected tag listings.

2.  Auto-generate apply_mustache.mk-like file for every mustache
    template or parametrize apply_mustache.mk file for this task.

3.  Allow custom pre- and post-blog generation targets. like:
    blog: $(PRE_MAKEBLOG) .... $(POST_MAKEBLOG)