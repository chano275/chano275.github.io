---
layout: post
title: 'How to Migrate or Copy MongoDB documents to another Server'
categories: [Systems-Administration-and-DevOps,]
tags : [mongodb, database, linux]
description: I recently installed Kubuntu 18.04 on my desktop PC, after doing a wipe-and-reinstall of my Windows 10 installation on the SSD.Altough most of my code is backed up either locally or on Github my MongoDB documents are not, because i never found it necessary.
excerpt_separator: <!--more-->
---
{{page.description}}

<!--more-->
The current version of my chat app needs some filler data so as to test certain functionality, and so i decided to migrate MongoDB documents from my
laptop to my Kubuntu install on the desktop, this will be accomplished through native MongoDB utilities for backup and restore, and Secure Copy or `scp`
to copy files from Laptop to Desktop over the network through SSH

## Setup
- The Receiver PC running `openssh-server` , installable on Ubuntu/Debian based systems by
```
    sudo apt install openssh-server
```
- The Sender PC having `ssh` installed, this should be default on most installations of Ubuntu
- Both sender and receiver should have MongoDB installed, for obvious reasons :P
- Both sender and receiver should have `ifconfig` tool from `net-tools` package on Ubuntu or Debian for finding out the IP address of both systems
```
    sudo apt install net-tools
```

## Migrations
- On your sender PC and receiver PC, make a directory called `mongobackups` in your home folder or any other location
    ```
    mkdir ~/mongobackups
    ```
- Again on the sender PC, backup your mongoDB documents to the `mongobackups` folder, `yourdb` here is just the name of your MongoDB collection
    ```
    sudo mongodump --db yourdb --out ~/mongobackups/`date +"%d-%m-%y"`
    ```
    This `date +"%d-%m-%y"`  creates a folder with the current date stamp, inside this folder there will be `.bson` files containing your documents

- Make sure `openssh-server` is installed on the receiver PC,and run `ifconfig` to find the IP address of your receiver PC, in my case it is 192.168.2.3


- On the Sender PC `scp` the `mongobackups` folder to the `mongobackups` on the receiver PC like so.Replace `shawn` with your username of your receiver PC
```
    scp -r ~/mongobackups/  shawn@192.168.2.3:~/mongobackups
```
You will be prompted for your password.

- On the Receiver pc now your restore your backups using `mongorestore`, `06-01-19` and `yourdb` are just placeholders,enter your own datestamp folder and collection name instead
```
    sudo mongorestore --db yourdb --drop ~/mongobackups/06-01-19/yourdb/
```

<br>
You should now be able to use your MongoDB documents in your webapp now.