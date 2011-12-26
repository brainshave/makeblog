# Makeblog — The Advertising

Makeblog is yet-simple and **fast** static site generator.

Features:

1. Markdown for content source.
2. Mustache for layouts.
3. Make for recreating only what really changed.
4. Fast: works well with multiple make jobs (`make -jX`).
5. Fast, p.2: uses node.js for scripts.
6. Generated and static files lives in one directory.

# Flow

Here is how it works:

1. `src/*.md` files are parsed to `tmp/*.json` files (HTML with some metadata).
2. `tmp/*.index.json` files are generated for main list and each tag.
3. `tmp/*.<layout-name>.json` files are parsed using layouts from `layouts` directory to files in main site's directory with suffixes dependent on suffix in layouts name. If layouts have versions with different suffixes, Each input file will be generated in both versions.

Illustrated:

    /   == SOURCE PART BEGINS ==
    |
    +-- layouts/
    |   +-- post.html          Example layout for post. You can add as many
    |   |                      layouts as you wish.
    |   +-- index.html         These are layouts for one only makeblog-specific
    |   +-- index.xml          pages: indexes are lists of all posts and for each tag.
    |
    +-- src/
    |   +-- hello.post.md      Input markdown files, they're parsed to json
    |   +-- goodbye.post.md    files in tmp directory. 
    |
    |       | | | | | | | | | | | | | |
    |   == EVERYTHING BELOW IS GENERATED ==
    |       | | | | | | | | | | | | | |
    |       V V V V V V V V V V V V V V
    |
    +-- tmp/
    |   +-- hello.post.json    Layout is choosen by suffix ("post").
    |   +-- goodbye.post.json
    |   +-- index.index.json   Index and files for each tag are automatically
    |   +-- tag1.index.json    created by makeblog. For each *.index.json 
    |                          file two files will be spit: one with html
    |                          and one with xml suffix because "index" layout
    +-- hello.html      \      have two versions.
    +-- goodbye.html     \     
    +-- index.html        ---  Generated files. Layout's name is cut from
    +-- index.xml         ---  file name.
    +-- tag1.html        /     
    +-- tag1.xml        /

# Requirements

1. GNU make (not tested with anything else).
2. node.js with packages: mu2, marked, yamlparser.
    
# Installation & Example

1. Clone makeblog somewhere.
2. Create a Makefile with nothing more than `include <path-to-makeblog>/Makefile` in your site's directory.
3. Put some layouts in layouts directory for example post.html
4. Put some input files in src directory.
5. Run `make` inside your site's directory.

# Input Files Format

    title: Title
    date: 2012-01-01
    tags: [a,b,c]
    + any metadata you'd like (all in YAML format)

    &&&

    Abstract, introduction, etc (Markdown format)

    &&&

    Main article body (Markdown)

# Data Available In Regular Layouts

- **title**
- **intro** - introduction part
- **body**
- **date**
  - **str** - YYYY-MM-DD
  - **day**, **month**, **year**
  - **day0**, **month0**, **year0** - padded with zeros
- **tags** - tags from header, each one has:
  - **name** - tag name
  - **basename** - basename of file (without extension)
- **basename** - basename of output file (without extension and layout name)
- **json** - path to json half-baked file
- **markdown** - path to original markdown file
- + everything you put in YAML header

# Data Available In Indexes Layouts

- **title** - name of or undefined for main index
- **date** - date of freshest post for this index
- **posts** - collection of posts with structure as in earlier list, sorted by date, descending
- **all_tags** - list of tags sorted by item count in descending order, each one has:
  - **name** - tag name
  - **basename** - basename of file (whithout extension)
  - **count** - number of posts tagged by this tag

# COPYING & Disclaimer

Copywrong 2010-2012 Szymon Witamborski, MIT License.