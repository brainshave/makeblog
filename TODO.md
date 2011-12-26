3.  Allow custom pre- and post-blog generation targets. like:
    blog: $(PRE_MAKEBLOG) .... $(POST_MAKEBLOG)

4.  all_tags field in indexes is one that actually should be updated
    on every index page. Consider updating them when there is a new
    tag, tag was deleted or counts have changed.