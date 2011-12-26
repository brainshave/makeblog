3.  Allow custom pre- and post-blog generation targets. like:
    blog: $(PRE_MAKEBLOG) .... $(POST_MAKEBLOG)

4.  Flush all_tags to separate file, but update it only when it's
    contents changed.