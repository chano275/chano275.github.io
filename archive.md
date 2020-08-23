---
layout: page
title: Blog Archive
permalink: /blog/
---

<section class="archive-post-list">
{% for post in site.posts %}
       {% assign year = post.date | date: "%Y" %}
       {% if year != postYear %}
           <h2>{{ year }}</h2>
           {% assign postYear = year %}
       {% endif %}
       <br>
       <li style="list-style-type: none;">{{ post.date | date: "%B %-d, %Y" }}<h3 class="archive" ><a href="{{ post.url }}">{{ post.title }}</a></h3></li>
   {% endfor %}


</section>