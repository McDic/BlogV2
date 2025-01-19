---
title: Blog Architecture
alternative_titles:
  - Architecture
  - Blog Architecture
---

# Blog Architecture

This article introduces how my blog works.

!!! warning

    This blog is being maintained by me alone,
    and everything is subject to change without any explicit notice.

---

## The goal

- I want my blogs looks clean and nice.
- I don't want to operate a blog with my own server, nor spending too much money on using 3rd party services.
- I don't want to distract readers with unnecessary ugly ads in a page.
- I don't want to use outdated or EoL-reached techs like [Ruby Sass](https://sass-lang.com/ruby-sass/).

Therefore I migrated my [old blog](https://github.com/McDic/BlogV1) to the new one.

---

## Core frameworks

[MkDocs](https://www.mkdocs.org/) is a core engine used to build this blog.
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) is an another layer built on top of MkDocs, which helps a lot on building static web page without too much effort.
It was a pretty nice choice, because

- I don't wanted to invest my time on HTML, Typescript, and CSS stuffs too heavily to create nice looking stuffs.
- Python is the most familar programming language for me.
- The framework is actively being maintained.

Most of theme in this blog is provided by those frameworks.
I customized several stuffs that `mkdocs-material` is not currently providing,
but I think that's a relatively smaller work compared to this whole infrastructure.

!!! info

    If `mkdocs-material` becomes inactive, I may migrate this blog to another framework at that time.

---

## Hosting

I use [Github Pages](https://pages.github.com/) to publish my static web pages on Github.
I am already spending money monthly on AWS, Youtube Premium, Linkedin Premium, etc.
I don't wanted to add more 30~40 USD/month eater for non-profit blog.

I have my own domain(`mcdic.net` as you see) with [AWS Route 53](https://aws.amazon.com/route53).
I have some number of subdomains under `mcdic.net` and this blog uses `blog.mcdic.net`.

---

## Comment section

I use [utteranc.es](https://utteranc.es) to build comment system with Github Issues.
Since I use public Github repo to publish my blog,
and it was easy to [override comment parts of HTML](https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/) in `mkdocs-material`,
it was trivial to add this.
There are several alternatives like [Giscus](https://github.com/giscus/giscus) so you can check and compare.

---

## Custom MKDocs plugin

I made [my own custom MKDocs plugin](https://github.com/McDic/BlogV2/tree/master/custom_plugin_blog) to customize following behaviors.
Note that I got rid of [built-in blog plugin](https://squidfunk.github.io/mkdocs-material/plugins/blog/) because there were several big issues on the whole structure, [refer here](https://github.com/squidfunk/mkdocs-material/issues/6647) if you are interested.

- Series
    - `Prev` and `Next` buttons will lead to prev/next articles in same series.
- Metadata of blog posts
    - Git dates
        - Automatically [fetches from the git](https://stackoverflow.com/questions/11533199/how-to-find-the-commit-in-which-a-given-file-was-added) system.
    - Post Views
        - Calculate the metadata from either custom data folder or GA4 API and embedded it.
        (Previously I used Javascript async fetch, but I got rid of it.)
    - Edit history
        - Provides Github commit URL of the post file.
- Post sorting
    - Sorts the blog posts by created date(Look `Archives` tab),
    [recently updated date](../sorted/recent), and [views](../sorted/most_viewed).

---

## Views on posts

Since my blog is a set of static web pages, it was a bit tricky to add views.
I use [Google Analytics](https://analytics.google.com/) to get views, unique users and more of my blog.
So I decided to run [cronjob via Github Actions](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) to periodically [fetch GA4 data with Python](https://github.com/googleapis/google-cloud-python/tree/main/packages/google-analytics-data),
then [customized the blog post HTML section](https://squidfunk.github.io/mkdocs-material/customization/#extending-the-theme) and [my own plugin](#custom-mkdocs-plugin).

So I failed to make my billing completely zero.
However I think this is still feasible, considering I am providing user statistics on my blog posts.

!!! warning

    I changed some posts paths and titles several times,
    and I am aggregating them by summation,
    which might be inaccurate in some cases.

---

## Soundcloud music player

I embedded [Soundcloud Widget API](https://developers.soundcloud.com/docs/api/html5-widget) on the header with some modifications.
I wrote some simple Javascript code to implement random music player.
For music sources, please [refer here](https://soundcloud.com/minsung-kim-mcdic/sets/blog-background-musics).

---

If there is anything you wonder, please ask in comments.
