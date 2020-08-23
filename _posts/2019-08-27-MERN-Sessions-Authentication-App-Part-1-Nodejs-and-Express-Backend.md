---
layout: post
title: 'MERN Sessions-Based Login and Registration App Part One : Node.JS, Express and MongDB REST API Backend'
categories: [Web-Development]
tags : [Nodejs, Express, MongoDB, REST-API, Backend]
excerpt_separator: <!--more-->
description: This is the first part in a three part series about building a full stack MERN( MongoDB, Express, React, NodeJS ) based Authentication Web App using Sessions & Cookies.
image: /public/assets/images/jXAvz9h.png
---

{{ page.description }}
In this part we will setup our Nodejs and MongoDB based REST API backend
<!--more-->

# What is a REST API ?
We have two parts of our app, one is the Nodejs based server in this post, and the other is the Reactjs based client which will be covered in future posts, both of these programs need to communicate with each other to fulfil our goal of user authentication, this is where REST comes in, REST is a specification that defines the communication between two different web programs should be done using HTTP requests like GET, POST, UPDATE, DELETE etc and with the data encoded in the JSON( JavaScript Object Notation ) format, this enables smooth communication between web programs written even in different languages, as long as data is sent and received according to the REST specification.


# How to maintain a persistent Login across refreshes?
Once your user has logged in to your website, you want to make sure that he doesn't have to log back in again and again everytime he accesses your website in a certain time period, to accomplish this persistence of user login, there are three main methods.<br>
The most popular among these three today is using a JWT token to store user data in the browser's
LocalStorage upon a successful login, and pass it to the server with each request manually by the clients side code.<br>
The second method is using a Cookie to store user data, and this is automatically attached to each request made to the server by the web browser<br>
The third method, and in my opinion the most secure, and the topic of this tutorial series, is using  **Sessions** based authentication.
Sessions based authentication means that upon a successful login, a "session" entry containting the user data is created in the Database or an In-Memory Store like Redis on the Server, while a cookie with an expiry date, containing a sessionID to this session entry is sent to the client, this cookie is then automatically sent with each request, which is accepted by the server if it is not expired, and access is granted as a logged in user

# How will this be accomplished using our Nodejs, Express and MongoDB stack?

We will be using a middleware called `express-sessions` for this purpose, this package allows us
to configure a secure cookie which will contain the session id, and provide us a `session` object in our `req` which we can use to interact with the session, and methods like `session.destroy()` to destroy our session if the user log's out for example.

# Tutorial

## Basic Server Setup

first we need to make a folder for our project, i called mine `mern-login-signup-component` but you can name it whatever you want.
```
mkdir mern-login-signup-component
```
```
cd mern-login-signup-component
```
Next we need to start a nodejs project using
```
npm init
```
choose the "starting point" of the app as `server.js`fill in the details it asks you for or just go along with the defaults
<br>

Now we create our directories
```
mkdir routes models config
```
and our `server.js` file
```
touch server.js
```
`config` just contains two files called `config.js` and `database.js`, you can simply copy these over from my github repo of this project, these files are just boilerplate for the variables and MongoURI from our `.env` file containing our environment variables.
<br>
Now open `server.js` in a text editor of your choice, and enter the following
<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/server.js</span>
</div>

```js
const express = require("express");
const app = express();
const session = require("express-session");
const MongoDBStore = require("connect-mongodb-session")(session);
const router = express.Router();
const mongoose = require("mongoose");

// Constants
const {
  HOST,
  PORT,
  SESS_SECRET,
  NODE_ENV,
  IS_PROD,
  COOKIE_NAME
} = require("./config/config");
const { MongoURI } = require("./config/database");
const MAX_AGE = 1000 * 60 * 60 * 3; // Three hours
```

The first `consts` are our packages being imported for us to use in our app, like the `express` package.
Next is the `express-session` package, and the `connect-mongodb-session` package that allows MongoDB to be used as a session store in the `express-sessions` middleware.
Then we import the express Router that is responsible for `GET` `POST` etc routes to our server
and lastly mongoose that is the ORM wrapper for our MongoDB database <br>

The next constants are our ENV variables and MongoURI that are imported from our `.env` file using JavaScript destructuring( these are the `{}` around the constants)
lastly we have a `MAX_AGE` constant that will be passed to our `express-sessions` init function, this will control the expiry date of the session cookie, in this case it will expire after 3 hours of being sent.<br>

## Middleware Setup

Next up is the setup of our middleware packages

<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/server.js</span>
</div>

```js
// Connecting to Database
mongoose
  .connect(MongoURI, {
    useNewUrlParser: true,
    useCreateIndex: true
  })
  .then(() => console.log("MongoDB connected..."))
  .catch((err) => console.log(err));

// setting up connect-mongodb-session store
const mongoDBstore = new MongoDBStore({
  uri: MongoURI,
  collection: "mySessions"
});

// Express Bodyparser
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

// Express-Session
app.use(
  session({
    name: COOKIE_NAME, //name to be put in "key" field in postman etc
    secret: SESS_SECRET,
    resave: true,
    saveUninitialized: false,
    store: mongoDBstore,
    cookie: {
      maxAge: MAX_AGE,
      sameSite: false,
      secure: IS_PROD
    }
  })
);
```

First off we connect to our database via `mongoose`, with these options `useNewUrlParser` and `useCreateIndex`.Next, we setup `connect-mongodb-session`, which will make a new `collection` in our database to store Sessions data, this object will then be passed to `express-sessions` when we set it up, we then use Expess' inbuilt body parsing functionality to read the `body` of HTTP requests and any JSON they may contain.
<br>
Finally, we setup our `session` config, here we can set various options for our sessions cookie, and the full list of options can be found in the `express-session` documentation, we assign the cookie a name and a secret, which can be anything, tell it to use our `MongoDBStor` as its store, give the cookie a max age of 3 hours, `sameSite` to prevent or allow CORS requests, and set `secure`, which allows cookies only to be sent to HTTPS secured servers to depend on whether our app is in development or production mode, if in prod mode, it is set to `true`<br>

<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/server.js</span>
</div>

```js
app.listen(PORT, () => console.log(`Server started on http://${HOST}:${PORT}`));
```

This last line simply starts up our Nodejs server on the specified Port number

## Defining a Mongoose Model for our 'User'

Mongoose is an ORM( Object Relational Mapper) or in simple words a middleware which makes interacting with our MongoDB database from within our program much easier and safer than trying to interact with mongoDB directly<br>
We will now write some code to define a model for our user data, first we `cd` into `models` from our project root directory, and create a new file called `User.js`.<br>
Then we make a new `Schema` by using the `Schema()` method from mongoose, and passing it an object containing the "schema" or format we want our `User` entry in our database to have, we will be passing three fields, name, email and password, which are all strings and all are required, in addition, we will have a `date` field, which will automatically be added by `mongoose` upon saving our `User` into our MongoDB database<br>
lastly we set and export `User` as a mongoose `model`, to be used in the next part of our server, that are the `routes`


<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/models/User.js</span>
</div>


```js
const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true
  },
  password: {
    type: String,
    required: true
  },
  date: {
    type: Date,
    default: Date.now
  }
});

const User = mongoose.model("User", UserSchema);

module.exports = User;
```

## Creating our REST API Routes

Create a new file in our `routes` folder called `user.js`, this will be our routes folder, where we handle our login, logout, registration and checking if a session cookie is present.
Start by importing our packages

<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/routes/users.js</span>
</div>

```js
const express = require("express");
const router = express.Router();
const bcrypt = require("bcryptjs");
const User = require("../models/User"); // User model
```
We are using the express Router, to handle our HTTP routes, bcryptjs which will convert the user's password into a hash, which will then be saved in a database, and also to compare the password hashes, lastly we import our User model that we created earlier<br>
The first route we will be starting with is the `register` route

#### Register

<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/routes/users.js</span>
</div>

```js
router.post("/register", (req, res) => {
  const { name, email, password } = req.body;

  // Check required fields
  if (!name || !email || !password) {
    return res.status(400).json({ msg: "Please enter all fields" });
  }
  //Check password length
  if (password.length < 6) {
    return res.status(400).json({ msg: "Password should be atleast 6 characters long" });
  }
}
```
Here in the first line, we use JavaScript destructuring to extract the user, email and password fields from the HTTP request body, and then we do some basic input validation, which sends a descriptive message with the HTTP Status Code of 400( Bad Request ) upon failing, once the input passes these tests, we move on to the next step

<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/routes/users.js</span>
</div>

```js
User.findOne({ email: email }).then((user) => {
    if (user) return res.status(400).json({ msg: "User already exists" });

    //New User created
    const newUser = new User({
      name,
      email,
      password
    });

    //Password hashing
    bcrypt.genSalt(12, (err, salt) =>
      bcrypt.hash(newUser.password, salt, (err, hash) => {
        if (err) throw err;

        newUser.password = hash;
        // Save user
        newUser
          .save()
          .then(
            res.json({
              msg: "Successfully Registered"
            })
          )
          .catch((err) => console.log(err));
      })
    );
  });
```

The `User.findOne({ email: email })` function comes from mongoose, and it checks the database for entries with the `email` field that match the `email` variable containing the field obtained from the request body, if it does, the  the `user` object is set to the database entry, and a HTTP 400 status code along with a message is sent back to the user that the user with that email already is registered.<br>
Otherwise the `user` object is set to null which means no user by that email exists, and so a new user can be registered, we do this by setting the `const newUser` to a new instance of `User` with the fields name, email and body from our request, we next use `bcrypt.genSalt` to generate a salt, which then returns a salt as a callback, we then hash the password using `bcrypt.hash()`, set the password field to the hash, and then save the User object into the database.
<br><br>
We now move on to our `login` route

#### Login

<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/routes/users.js</span>
</div>

```js
router.post("/login", (req, res) => {
  const { email, password } = req.body;

  // basic validation
  if (!email || !password) {
    return res.status(400).json({ msg: "Please enter all fields" });
  }
  //check for existing user
  User.findOne({ email }).then((user) => {
    if (!user) return res.status(400).json({ msg: "User does not exist" });

    // Validate password
    bcrypt.compare(password, user.password).then((isMatch) => {
      if (!isMatch) return res.status(400).json({ msg: "Invalid credentials" });

      const sessUser = { id: user.id, name: user.name, email: user.email };
      req.session.user = sessUser; // Auto saves session data in mongo store

      res.json({ msg: " Logged In Successfully", sessUser }); // sends cookie with sessionID automatically in response
    });
  });
});
```

The logic here proceeds pretty much the same way as our register router, but here if checks to see if a user is not found, but if the email is of an existing user, we drop into `bcrypt.compare()` which compares the hashed password of the user from the database, to a hashed version of the password from the request body, if the passwords do not match an HTTP 400 is sent out, but if the passwords are the same, a `const` `sessUser` is set with an object containing the parameters from the autenticated user from the database.<br>
Then this `sessUser` object is assigned to `req.session.user`, which automatically creates a session for this user in the database, and attaches a cookie to the response, lastly, the response is sent with an HTTP 200, success message and the `sessUser` object itself.<br>

Our last two routes are the `logout` and `authchecker`
<br>

#### Logout

<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/routes/users.js</span>
</div>

```js
router.delete("/logout", (req, res) => {
  req.session.destroy((err) => {
    //delete session data from store, using sessionID in cookie
    if (err) throw err;
    res.clearCookie("session-id"); // clears cookie containing expired sessionID
    res.send("Logged out successfully");
  });
});
```

If the request being sent to the `/logout` route contains a valid cookie, `express-session` automatically attaches a `session` object to the `req` containing the session data, and associated methods, of these, the `destroy()` method deletes the session data from the `mongoDB store`, after which we clear the `cookie` in the response by specifying it's `name`, and we send out a success message in the response

#### AuthChecker

<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/routes/users.js</span>
</div>

```js
router.get("/authchecker", (req, res) => {
  const sessUser = req.session.user;
  if (sessUser) {
    return res.json({ msg: " Authenticated Successfully", sessUser });
  } else {
    return res.status(401).json({ msg: "Unauthorized" });
  }
});
```

This method is meant to be used on the home page of our React app, to check if a user has already logged in by checking for a valid sessions cookie.<br>
As mentioned earlier, if a valid cookie is sent along with the request to this root, a `sessions` object is automatically attached containing the `user` data, if a user is found, a success message and the user data is sent, if not, and HTTP 401 ( Unauthorized ) with a message is sent out.<br>
lastly we export our routes
<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/routes/users.js</span>
</div>

```js
  module.exports = router;
```

## Final touch

<div class="file-display">
  <span><i class="fas fa-folder"></i>  ~/mern-login-signup-component/server.js</span>
</div>

```js
app.use("/api/users", require("./routes/users"));
```
we add this line to our `server.js`, which tells our server to accept our routes coming from the `users.js` file in the `routes` folder on `/api/users`
for example, to register a user we would have to send a POST request to `http://localhost:5000/api/users/register`, with `localhost` and `5000` being  environment variable
<br>
With this we have completed our REST API backend, and in the following posts we will setup our React frontend
<br>
