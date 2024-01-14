---
no_comments: true
slug: format
---

# Post Format

This article explains the format of articles in this website.

!!! info "Notice on migrated posts"

    Some blog posts here are migrated from other web sources written by me,
    and some of them may not strictly respect the following format.

!!! info "Subject to be changed"

    This is my own blog, and some stuffs may be changed without notice.

---

## Titles

For every blog post, it should have exactly one category that is classified as part of series.
The main title format of a blog post would be `{ABBREVIATED SERIES NAME} {NUMBERING}. {POST TITLE}`, and slug should be `{ABBREVIATED SERIES NAME}-{NUMBERING}`.
For every non blog post like this article, it should have no category at all. There is no strict title naming rule on non blog posts.

I use `h1` as main title of a post.
I use `h2` and `h3` as paragraph titles of a post.
Every title provides a permalink for easier reference.
The navigation provided by `mkdocs-material` is available at the right side, if your screen is large enough.

---

## Metadata

Every blog post will provide following metadata;

- A date when this blog post was created.
- A category of this blog post.
- An [estimation of reading time](https://squidfunk.github.io/mkdocs-material/setup/setting-up-a-blog/?h=reading#setting-the-reading-time), automatically calculated by `mkdocs-materials`.
- A number of [active users](https://support.google.com/analytics/answer/12253918?hl=en#:~:text=is%20populated%20automatically.-,Active%20users,engagement_time_msec%20parameter%20from%20a%20website) visited this page since the beginning of the blog.
  This is different from total views.
  Because I am not using realtime data, this metadata is invisible on post page if the data is not available from GA4 yet.

!!! warning "Disclaimer"

    The "number of active users" statistics is analyzed anonymously and
    I do not provide any personalized information(who visited here, etc) on this blog,
    since I do not intend to provide it and also I have no way to get it from GA4 API.

---

## Admonitions

I use [built-in admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/?h=admon#supported-types) featured by `mkdocs-material`.

Most of admonitions would be either `note`, `info`, or `quote` type.
However, I occasionally use `warning` or `danger` type when I write something serious, a disclaimer for an example.

---

## References

I try to use official links as possible as I can.
If I fail to find good enough reference in a reasonable time,
I may reference some lower quality articles like [namu.wiki](https://namu.wiki).
