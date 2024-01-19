---
no_comments: true
---

# Post Format

This article explains the format of articles in this website.

!!! migrated "Notice on migrated posts"

    Some blog posts here are migrated from other web sources written by me,
    and some of them may not strictly respect the following format.

!!! warning

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

- Last updated date and created date of an article.
- A number of [active users](https://support.google.com/analytics/answer/12253918?hl=en#:~:text=is%20populated%20automatically.-,Active%20users,engagement_time_msec%20parameter%20from%20a%20website) visited this page since the beginning of the blog.
  This is different from total views.
  Since I am not using realtime data, this metadata is not available if the data is not available from GA4 yet.

!!! disclaimer

    The "number of active users" statistics is analyzed anonymously and
    I do not provide any personalized information(who visited here, etc) on this blog,
    since I do not intend to provide it and also I have no way to get it from GA4 API.

---

## Admonitions

I use [built-in admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/?h=admon#supported-types) featured by `mkdocs-material`.
For typical admonitions, I use `note`, `info`, and `quote` types in most cases
and occasionally use `warning` and `danger` types.
However, I customized some following stuffs, thanks for [CSS animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations/Using_CSS_animations).

!!! disclaimer

!!! migrated

!!! references

!!! caption

!!! copyright

!!! formula

---

## Resources

Almost all custom icons here are provided by [SVG Repo](https://www.svgrepo.com/).

---

## References

I try to use official links as possible as I can.
If I fail to find good enough reference in a reasonable time,
I may reference some lower quality articles like [namu.wiki](https://namu.wiki).
