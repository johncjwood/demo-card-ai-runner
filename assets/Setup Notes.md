**Running the stack**
docker compose down -v && docker compose up --build -d

**Access Points**
- Frontend: http://localhost
- REST API: http://localhost:3001/api
- PostgreSQL: localhost:5432

**Issues w/ Architecture**
When building this test app, there were some tradeoffs made between what was ideal enterprise software proxy and what would be easy to deploy and takedown. 

One of those tradeoffs was the question of Auth.
I wanted to run an auth service like authentik or tinyauth, but either the auth services rely on some persistent infrastructure such as a database (which, normally would exist and be owned by another team), or there were some unseen complexities.
A 3rd party solution is also out-of-bounds for an open source project, so we chose a non-ideal solution of rolling our own auth. Please don't do this in your own project. 