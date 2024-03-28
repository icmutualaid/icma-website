This is the source code for our collective's website.

# Status

Automated tests: ![linter](https://github.com/icmutualaid/icma-website/actions/workflows/python-app.yml/badge.svg)

The site is not yet ready for the public. We expect to go live sometime in April 2024.

# Roadmap

We've stolen some basic blogging features from [the Flask tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/).

We should improve upon these features by swapping out the plain text blog interface with a feature-rich WYSIWYG like CKEditor.

We need to customize the website's appearance, audit it for accessibility, deploy it on our webserver, and get the blog up and running.

Then, we'll decide on wiki software and implement it. We'll either include that software in this project or host it separately and include a link.

# Contribution and Workflow

If you are an ICMA member, ask someone on the IT committee to add your GitHub account as an owner of the organization, or if you have the [@icma-admin](https://github.com/icma-admin) GitHub credentials, do it yourself on [the organization's Members page](https://github.com/orgs/icmutualaid/people).

Follow [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) (create pull requests with individual fixes and features). Make your git commits using your own GitHub account, **not** the [@icma-admin](https://github.com/icma-admin) account.

If you are not an ICMA member and you're curious, [contact us](https://github.com/icmutualaid).

To manually run tests: `coverage run -m pytest`

# Technical

Also see [our project wiki](https://github.com/icmutualaid/icma-website/wiki/) for more information.

## Installation

See [the Installation page on our project wiki](https://github.com/icmutualaid/icma-website/wiki/Installation) for detailed instructions.

# About Our Organization

We are the Iowa City Mutual Aid collective.

Check our profile [@icmutualaid](https://github.com/icmutualaid) if you want to get in contact.

## Our Mission

We work to meet the survival needs of people whom our systems continue to fail.

We do this because the conditions in which we are made to live are unjust. Our local, state, and national governments all continue to neglect crises and leave people behind.

We must work toward liberation by meeting needs that are unmet by the capitalist class who control the wealth and the state.

# The Project and Our Principles

## We are resourceful.

The purpose of this project is to eliminate overhead costs. Every dollar spent on a website builder is one less dollar spent on propane.

We will choose wisely which services to take on ourselves, because this is all for nothing if the collective has to hire a developer to rescue our project.

## We cannot be beheaded.

The project can never rest on one or two people's shoulders. Other members and other collectives must be able to continue our work. We must:

- Write code that is easy to read, maintain, extend, and test.
- Build a project that is easy to install and migrate.
- Maintain excellent documentation.
- Train each other on maintenance and operations.
- Keep an archive with regular backups.
- Keep the project free, open source, and discoverable.

## We leave no one behind.

Inaccessible is never "good enough for now." Our site will always be easy to parse with accessibility and translation software. Our specific goal is for the production site to always be fully WCAG 2.1 AA compliant.

## We share our skills.

To that end, we will collaborate on development and operations.
