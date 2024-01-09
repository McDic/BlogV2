# Blog Architecture

This article introduces how my blog works.

---

## The Goal

- I want my blogs looks clean and nice.
- I don't want to operate a blog with my own server, nor spending too much money on using 3rd party services.
- I don't want to distract readers with unnecessary ugly ads in a page.
- I don't want to use outdated or EoL-reached techs like [Ruby Sass](https://sass-lang.com/ruby-sass/).

Therefore I migrated my [old blog](https://github.com/McDic/BlogV1) to the new one.

---

## Core Frameworks

[MkDocs](https://www.mkdocs.org/) is a core engine used to build this blog.
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) is an another layer built on top of MkDocs, which helps a lot on building static web page without too much effort.
It was a pretty nice choice, because

- I don't wanted to invest my time on HTML, Typescript, and CSS stuffs too heavily to create nice looking stuffs.
- Python is the most familar programming language for me.
- The framework is actively being maintained.

Most of theme in this blog is provided by those frameworks.
I customized several stuffs that `mkdocs-material` is not currently providing,
but I think that's a relatively smaller work compared to this whole infrastructure.

If `mkdocs-material` becomes inactive, I may migrate this blog to another framework at that time.

---

## Hosting

I use [Github Pages](https://pages.github.com/) to publish my static web pages on Github.
I am already spending money monthly on AWS, Youtube Premium, Linkedin Premium, etc.
I don't wanted to add more 30~40 USD/month eater for non-profit blog.

I have my own domain(`mcdic.net` as you see) with [AWS Route 53](https://aws.amazon.com/route53).
I have some number of subdomains under `mcdic.net` and this blog uses one of them.

---

## Comment Section

I use [utteranc.es](https://utteranc.es) to build comment system with Github Issues.
Since I use public Github repo to publish my blog,
and it was easy to [override comment parts of HTML](https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/) in `mkdocs-material`,
it was trivial to add this.
There are several alternatives like [Giscus](https://github.com/giscus/giscus) so you can check and compare.

---

## Views on Posts

Since my blog is a set of static web pages, it was a bit tricky to add views.
I use [Google Analytics](https://analytics.google.com/) to get views, unique users and more of my blog.
So I decided to run [cronjob via Github Actions](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) to periodically [fetch GA4 data with Python](https://github.com/googleapis/google-cloud-python/tree/main/packages/google-analytics-data),
then [customized the blog post HTML section](https://squidfunk.github.io/mkdocs-material/customization/#extending-the-theme).

So I failed to make my billing completely zero, but I think this is still feasible, considering I am providing unique user views on my blog posts.

---

If there is anything you wonder, please ask in comments.