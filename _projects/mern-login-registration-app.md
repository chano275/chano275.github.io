---
layout: project-details
title: 'MERN Login/Sign-Up App'
image: /public/assets/images/AuthAppPoster.png
gif: /public/assets/images/AuthAppOptimized960x540.gif
video: /public/assets/videos/AuthApp1080p.m4v
stack: [React, Redux, Bootstrap, Nodejs, MongoDB, Docker, Nginx]
description: Minimalistic, fully responsive, Dockerized and  ready-to-use component for Sessions based Login and Sign-Up   that can be used as a starting point for another project that needs authentication. Uses Cookies
gitrepo: https://github.com/shawn-dsilva/mern-login-signup-component
live: 'https://demos.shawndsilva.com/sessions-auth-app'
---

# Motivation
<br>
This is a template or "starter code" that can be used as a base in other MERN(MongoDB, Express, ReactJS, NodeJS) Projects, Enabling me and other Developers who use this to focus on the core features of their project, rather than bothering with setting up the Frameworks and writing authentication code from scratch

I created this project while learning React, NodeJS, Express, MongoDB and Docker which were all new technologies for me at that point.

It contains a functional ReactJS front-end and a NodeJS backend integrated with MongoDB, Login and Registration functions, with persistence of logins achieved using Sessions, and Fully responsive across Tablet, Mobile and Desktop

This project also has support for protected routes on the React front-end, and support for rate-limiting and input validation at the NodeJS back-end

# Technologies Used
<br>
<img class="svg-std" src="../public/assets/icons/react-original-wordmark.svg">
<img class="svg-std" src="../public/assets/icons/bootstrap-plain-wordmark.svg">
<img class="svg-width" src="../public/assets/icons/Node.js_logo.svg">
<img class="svg-std" src="../public/assets/icons/mongodb-original-wordmark.svg">
<img class="svg-width" src="../public/assets/icons/docker.svg">

# Features

- Login page with success/error messages
- Register page with success/error messages
- Rate-Limiting.
- Input validation
- Protected Profile page route that needs authentication to access
- Persistence achieved using Sessions, with session ID stored on Cookie
- Logout deletes session in database and cookie from browser
- Fully responsive across Desktop, Tablet and Mobile
<br>