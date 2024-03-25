![linter](https://github.com/icmutualaid/icma-website/actions/workflows/python-app.yml/badge.svg)

# About Our Organization

We are IC Mutual Aid. 

We work to meet the survival needs of people whom our systems continue to fail.

We do this because the conditions in which we are made to live are unjust. Our local, state, and national governments all continue to neglect crises and leave people behind.

We must work toward liberation by meeting needs that are unmet by the capitalist class who control the wealth and the state.

You may contact us via email (see our profile [@icmutualaid](https://github.com/icmutualaid)) or on our social media platforms:

- Instagram: [@icmutualaid](https://www.instagram.com/icmutualaid)
- Twitter: [@icmutualaid](https://twitter.com/icmutualaid)

# About Our Project

This project will hold the code for our collective's website.

## Status

The site is not yet ready for the public. We expect to go live sometime in April 2024.

## Roadmap

Currently, we're following along with [the Flask tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/)!

Then, we'll customize the website's appearance, audit it for accessibility, deploy it on our webserver, and get the blog up and running.

Then, we'll decide on wiki software and implement it. We'll either include that software in this project or host it separately and include a link.

## Contributing

If you are an ICMA member, ask someone on the IT committee to add your GitHub account as a contributor on the project, or if you have the [@icmutualaid](https://github.com/icmutualaid) GitHub credentials, do it yourself on [this project's Settings page](https://github.com/icmutualaid/icma-website/settings/).

Please make your git commits using your own GitHub account, **not** the [@icmutualaid](https://github.com/icmutualaid) account.

If you are not an ICMA member, how did you find this page? Contact us if you're curious!

### Installation

1. `git clone https://github.com/icmutualaid/icma-website.git`
2. create a python venv (in vscode, `Python > Create Environment…`) and install dependencies from requirements.txt (vscode will prompt; otherwise, `python3 -m pip3 install requirements.txt`)
3. initialize the db: `flask --app blog init-db`
4. start the webserver: `flask --app blog init-db`

## Technical Specifications

### Features

The project should support these basic groups of stories:

1. As a server admin, I need to manage website admin accounts.
2. As a website admin, I need to create and manage blog posts on the website.
3. As a member of the public, I need to create and manage a wiki account.
4. As a wiki user, I need to do wiki stuff.
5. As a website admin, I need to do wiki admin stuff.
6. As a member of the public, I need to see contact info and social accounts.

### File Structure

Here is an outline of the file structure you'll see while working on the project:

```
icma-website/
  blog/              source code for the app
  instance/            contains the website's db (git ignored)
  .gitignore           instructs your git client to ignore certain files when committing
```

The `instance/` directory will appear when you run the project. This won't and shouldn't be added to your commits.

Other junk like `.venv/`, `__pycache__/`, and `.git/` will also appear as you work on the project. They won't and shouldn't be added to your commits.

## Mission

### We are resourceful.

The purpose of this project is to eliminate overhead costs. Every dollar spent on a website builder is one less dollar spent on propane.

We will choose wisely which services to take on ourselves, because this is all for nothing if the collective has to hire a developer to rescue our project.

### We cannot be beheaded.

The project can never rest on one or two people's shoulders. Other members and other collectives must be able to continue our work. We must:

- Write code that is easy to read, maintain, extend, and test.
- Build a project that is easy to install and migrate.
- Maintain excellent documentation.
- Train each other on maintenance and operations.
- Keep an archive with regular backups.
- Keep the project free, open source, and discoverable.

### We leave no one behind.

Inaccessible is never "good enough for now." Our site will always be easy to parse with accessibility and translation software.

### We share our skills.

To that end, we will collaborate on development and operations.