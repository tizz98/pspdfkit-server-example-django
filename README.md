# PSPDFKit Server Example – Django

This example shows how to integrate PSPDFKit Server and
[PSPDFKit for Web](https://pspdfkit.com/web/) into a Django app.

You need to have an activation key for PSPDFKit Server - if you don't have one just
[request a trial](https://pspdfkit.com/try/).

## Getting Started with Docker

We recommend you use Docker to get all components up and running quickly.

The provided `docker-compose.yml` and `Dockerfile` will allow you to edit the example app on your
host and it will live-reload.

```sh
$ git clone git@github.com:tizz98/pspdfkit-server-example-django.git
$ cd pspdfkit-server-example-django
$ PSPDFKIT_ACTIVATION_KEY=<YOUR_ACTIVATION_KEY> docker-compose up
```

Make sure to replace `<YOUR_ACTIVATION_KEY>` with your PSPDFKit Server activation key. You only have
to provide the activation key once, after that the server will remain activated until you reset it.

The example app is now running on <http://localhost:8000>. You can access PSPDFKit Server's
dashboard at <http://localhost:5000/dashboard> using `dashboard` // `secret`.

Login using any user name and upload a PDF, then click on the cover image to see PSPDFKit Web in
action.

You can also selectively share PDFs with other users you have created.

### Resetting the server

You can reset the server by first tearing down its containers and volumes and then recreating them.

```sh
$ docker-compose down --volumes
$ PSPDFKIT_ACTIVATION_KEY=<YOUR_ACTIVATION_KEY> docker-compose up
```

## Running the example locally

You can also run the example app directly on your machine, outside of a Docker container.

### Prerequisites

* Python 3.5.3 or newer (The sample is a Django 2.0 app)
* [PSPDFKit Server](https://pspdfkit.com/guides/web/current/server-backed/setting-up-pspdfkit-server/)
  running on [http://localhost:5000](http://localhost:5000) with the default configuration

### Getting Started

```sh
$ git clone git@github.com:tizz98/pspdfkit-server-example-django.git
$ cd pspdfkit-server-example-django
$ pipenv install
$ ./manage.py migrate
$ ./manage.py runserver
```

The example app is now running on <http://localhost:8000>.

Login using any user name and upload a PDF, then click on the cover image to see PSPDFKit Web in
action.

You can also selectively share PDFs with other users you have created.

You can quit the running containers with Ctrl-C.

If you want to test PSPDFKit for Web on different devices in your local network, you need
to edit the `PSPDFKIT_SERVER_EXTERNAL_URL` environment variable in the `docker-compose.yml` and set it to an address that's reachable from your device.
