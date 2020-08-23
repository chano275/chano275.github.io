---
layout: page
title: My Projects
permalink: /projects/
---

<section id="projects">



<div class="all-projects-container">
    {% for project in site.projects  %}


     <div data-aos="fade-up"  class="all-projects-item">
          <img class="post-image" src="{{project.image}}"/>
          <div class="all-projects-content">
          <h1 class="project-title">
              {{ project.title | truncate:75 | strip_html }}
          </h1>

            <p>
          {{ project.description  | strip_html }}
        </p>
          <br>
                    <div class="link-tag-container">

        <a class="link-tags blu" href="{{project.live}}">
          <i class="fas fa-desktop"></i> Live Demo </a>

        <a class="link-tags blk" href="{{project.gitrepo}}">
          <i class="fab fa-github"></i> View Code</a>

        <a class="link-tags det" href="{{project.url}}">
          <i class="fa fa-plus"></i> More Details</a>
      </div>
        </div>



        </div>
    {% endfor %}
</div>

</section>