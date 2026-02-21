---
layout: default
---
# The Daily Brief
Navigating the Global Digital Economy.

### Latest Briefings:

{% for post in site.posts %}
* [{{ post.title }}]({{ site.baseurl }}{{ post.url }}) - *{{ post.date | date: "%B %d, %Y" }}*
{% endfor %}
