<p align="center">
    <img alt="Plone Logo" width="200px" src="https://raw.githubusercontent.com/plone/.github/main/plone-logo.png">
</p>

<h1 align="center">
  Plone Distribution: Intranet
</h1>

[![Built with Cookiecutter Plone Starter](https://img.shields.io/badge/built%20with-Cookiecutter%20Plone%20Distribution-0083be.svg?logo=cookiecutter)](https://github.com/collective/cookiecutter-plone-distribution/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Code Analysis](https://github.com/collective/collective.ploneintranet/actions/workflows/code-analysis.yml/badge.svg)](https://github.com/collective/collective.ploneintranet/actions/workflows/code-analysis.yml)
[![Tests](https://github.com/collective/collective.ploneintranet/actions/workflows/tests.yml/badge.svg)](https://github.com/collective/collective.ploneintranet/actions/workflows/tests.yml)


## Why use Plone for an Intranet?

1. **Security**: Plone is widely known for its strong security. It is engineered with a focus on security at the core, which makes it an ideal choice for intranets that often require a high degree of security. The default configurations of Plone are inherently secure and regularly audited, which reduces the risk of common vulnerabilities.

2. **Content Management**: Plone provides powerful content management features. It allows users to create, manage, and publish content with ease. It also supports versioning, which means changes to the content can be tracked and reverted if necessary.

3. **User Management and Permissions**: Plone offers comprehensive user management with fine-grained permission control. This allows administrators to have precise control over who can view, edit, or publish content in different parts of the intranet.

4. **Customizability and Scalability**: Plone is highly customizable and can be scaled to fit the needs of both small and large organizations. This makes it a versatile solution that can grow with the organization.

5. **Workflow Management**: Plone supports the creation of complex workflow scenarios. This means you can implement approval processes, drafting states, and more, helping you ensure quality and oversight on your intranet content.

6. **Multilingual Support**: Plone has built-in support for multiple languages. This is particularly beneficial for multinational corporations or organizations with a diverse user base who need their intranet content in several languages.

7. **Integration Capabilities**: Plone can integrate with a wide variety of other systems, including databases, authentication systems, and other third-party services. This flexibility allows you to incorporate the intranet into your existing IT environment seamlessly.

8. **Open Source**: Finally, Plone is open source, which means you have the freedom to modify and adapt it to your specific needs. Moreover, it's backed by an active community that continuously works on updates, patches, and improvements.

## Features

This package provides a new Plone Distribution called "Plone Intranet (Volto UI)" that creates a simple Intranet.

The Intranet will require users to authenticate before being able to view any content.

### Authentication Options

During site creation, you could choose one of the available authentication methods:

* **Plone**: Default authentication method where users are created and stored in the Intranet database.
* **GitHub**: Setup OAuth2 authentication with GitHub.
* **Google**: Setup OAuth2 authentication with Google.

### Example content

The "Plone Intranet (Volto UI)" comes with the following content:

* **/images/**: Image bank with faceted navigation for images.
* **/news/**: Listing of News Items available on the Intranet.

## Using

## Docker Image

In your computer, create a new folder (i.e. `Intranet`) and copy the example [docker-compose.yml](./docker-compose.yml) into it:

```shell
mkdir Intranet
cd Intranet
curl https://raw.githubusercontent.com/collective/collective.ploneintranet/main/docker-compose.yml --output docker-compose.yml
```

Then start the stack with:

```shell
docker compose up -d
```

This command starts three containers:

* webserver: A Traefik router that acts as an ingress to this stack.
* frontend: Volto frontend for the intranet.
* backend: The Plone Intranet backend.

### Create the Intranet

To create the Plone site on the backend, visit the url: [http://intranet-admin.localhost](http://intranet-admin.localhost) and add a new Plone Intranet.

Please, keep the site_id as **Plone**, as the frontend container expects that value.

To test the GitHub authentication use the following values:

* consumer_key: **ee86d42b5c4bc4987818**
* consumer_secret: **6f3a390401470b26c847e0d7832bacec7f214a1c**

## In an existing Plone project

Add **collective.ploneintranet** as a dependency of your project.

## Contribute

- [Issue Tracker](https://github.com/collective/collective.ploneintranet/issues)
- [Source Code](https://github.com/collective/collective.ploneintranet/)

## License

The project is licensed under GPLv2.
