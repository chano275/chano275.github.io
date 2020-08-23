---
layout: project-details
title: "ListWala"
image: /public/assets/images/ListWalaPoster.png
gif: /public/assets/images/ListWalaOptimized.gif
video: /public/assets/videos/ListWala1080p.m4v

stack: [React, Redux, Bootstrap, Nodejs, MongoDB, Docker, Nginx]
description: A Fully Free & Open Source, Dockerized To-Do List and Project Management web app, supporting user authentication, routing, descriptions, status changes and checklists and deletions, Fully responsive across Desktop, Tablet and Mobile.
gitrepo: https://github.com/shawn-dsilva/list-wala
live: "https://demos.shawndsilva.com/list-wala"
---

# Motivation
<br>
ListWala is an Open Source To-Do List and Project management app, I created this project to strenghten my understanding of MERN based Full Stack Web Apps, especially React, Redux and how they both work together.

This project started out as a simple To-Do List App, but later on I added features that also made it useful for minimal project management, for example a "roadmap" of sorts for any new coding project I am developing with what specific features need to be developed etc.

With this Project, I also learnt How to Deploy my web apps to live servers using Docker, which I have documented in this [Blog Post here](http://shawndsilva.com/blog/systems-administration-and-devops/Hosting-Multiple-Full-Stack-Web-Projects-On-One-VPS-Using-Nginx-And-Docker.html)

# Technologies Used
<br>
<img class="svg-std" src="../public/assets/icons/react-original-wordmark.svg">
<img class="svg-width" src="../public/assets/icons/redux-notext.svg">
<img class="svg-std" src="../public/assets/icons/bootstrap-plain-wordmark.svg">
<img class="svg-width" src="../public/assets/icons/Node.js_logo.svg">
<img class="svg-std" src="../public/assets/icons/mongodb-original-wordmark.svg">
<img class="svg-width" src="../public/assets/icons/docker.svg">

# Features

- Login page with success/error messages
- Register page with success/error messages
- Protected List page route that needs authentication to access
- Persistence achieved using Sessions, with session ID stored on Cookie
- Logout deletes session in database and cookie from browser
- Create Lists containing ToDo items.
- ToDo items have editable descriptions, checklists and status
- Status can be changed to Done, In Progress or back to Not Started
- Lists and ToDo items can be Deleted
- Fully responsive across Desktop, Tablet and Mobile
<br>
