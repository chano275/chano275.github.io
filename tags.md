---
layout: page
title: Tags
permalink: /tags/
---
<p>
    {% for tag in site.tags %}
    <a class="tags" href="/tags/{{ tag[0] }}/">
       {{tag[0]}}
    </a>
    {% endfor %}
</p>
<br>
<h1 class="page-title"> <i class="fas fa-folder-open"></i>  Categories  </h1>
{% for category in site.categories %}
<span id="{{category[0]}}" class="categories-main">{{ category[0] | replace: "-"," " }}</span>
{% for post in category[1] %}
<li style="list-style-type: none;"> {{ post.date | date: "%B %-d, %Y" }}<h3 class="archive" ><a href="{{ post.url }}">{{ post.title }}</a></h3></li><br>
{% endfor %}
{% endfor %}