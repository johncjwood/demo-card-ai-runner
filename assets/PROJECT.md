**Three Tiered Application for Trading Card Game**

**Get stack up**
sudo snap install docker
docker compose up -d

**Access tools in the stack**
Frontend: http://app.local (protected by Traefik)
REST API: http://app.local/api (protected by Traefik)
Traefik Dashboard: http://traefik.local:8080
PostgreSQL: localhost:5432

**Setup /etc/hosts**
Add to /etc/hosts: 127.0.0.1 app.local traefik.local

**Authentication**
All requests to the frontend (port 4200) now go through Traefik login.
Default users: alice/password, bob/password

**Purpose**
This is an application designed to mimic elements of a normal enterprise application.
Some choices, such as using Angular and having a REST API instead of doing server-side rendering are consistent with that goal.

**Auth**
The first thing one might note is that we are publishing the auth credentials in our setup.
This includes a secret key and usernames / passwords.
This is by design, as our goal was to use an auth service that we could setup and initialize programatically.
We did not want an auth service that needed manual intervention or a persistent docker volume / file share / database to function.
This is obviously not a model for emulation, but rather an standard speedbump for enterprise app development (and potentially one that the system could trip on) - integrating with whatever IDAM and Auth provider is provided by the firm.


