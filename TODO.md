2.  Auto-generate apply_mustache.mk-like file for every mustache
    template or parametrize apply_mustache.mk file for this task.

3.  Allow custom pre- and post-blog generation targets. like:
    blog: $(PRE_MAKEBLOG) .... $(POST_MAKEBLOG)

4.  all_tags field in indexes is one that actually should be updated
    on every index page. Consider updating them when there is a new
    tag, tag was deleted or counts have changed.