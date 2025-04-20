# FastAPI Vercel

Deploy a [FastAPI] app as a [Vercel] Serverless Function.

This repo deploys the [FastAPI PDF unlocker Service] to demonstrate how a FastAPI app can be deployed using the Vercel 
[Asynchronous Server Gateway Interface (ASGI)].

**_View the live demo at: [https://fastapi-zeit-now.paul121.now.sh/?name=GithubUser](https://fastapi-zeit-now.paul121.now.sh/?name=GithubUser)_**
- OpenAPI Docs: [https://fastapi-zeit-now.paul121.now.sh/docs](https://fastapi-zeit-now.paul121.now.sh/docs)
- Try the API endpoints [/?name=Name](https://fastapi-zeit-now.paul121.now.sh/?name=Name), [/users](https://fastapi-zeit-now.paul121.now.sh/users), [/items](https://fastapi-zeit-now.paul121.now.sh/items)

Notes about this deployment:
- FastAPI is configured to return a `Cache-Control` header set to `no-cache` for all responses. Because
static caching is automatic with Vercel, this ensures the Vercel CDN doesn't cache anything for the purposes of this 
example. More on caching [here](https://vercel.com/docs/edge-network/caching).
- This repo contains a sample sqlite database that has a few predefined `users` and `items` to demonstrate returning data
from a database.
  - **Note** Due to the nature of a serverless deploy, the sqlite file cannot be written to so any 
*POST requests attempting to modify the DB will fail.*
  - In a production deploy, the FastAPI app would connect to a 
database hosted elsewhere.

This is merely an example of integration with Vercel. I'm not currently deploying any FastAPI apps in this way, but would
like to consider it a possibility. **_Any thoughts, concerns or ideas for benchmarking are welcome!!_**

## Background

After learning about [Zappa] I was inspired to learn more about hosting FastAPI as a server-less function:
> Zappa makes it super easy to build and deploy server-less, event-driven Python applications (including, but not limited to, WSGI web apps) on AWS Lambda + API Gateway. Think of it as "serverless" web hosting for your Python apps. That means infinite scaling, zero downtime, zero maintenance - and at a fraction of the cost of your current deployments!

The problem is that Zappa only works with WSGI Python apps such as Flask and Django, not ASGI.

Google Cloud Run and AWS Elastic Beanstalk are other alternatives, but don't support ASGI either.

I came across [Mangum] which is similar to Zappa, except it supports ASGI apps. While this would likely work with 
FastAPI (or most any ASGI Python app) it also seems to make some decisions about how you structure your app. And it 
still requires quite a bit of configuration with AWS to get everything working. (more in this [issue](https://github.com/tiangolo/fastapi/issues/812))

[Vercel] makes this all a bit easier. Develop locally with `vercel dev` and deploy with `vercel --prod`.

## Configuration

With [Vercel], we just need to configure a few things in `vercel.json`, run `vercel --prod` and FastAPI is deployed.

*See Vercel Docs on [Configuration](https://vercel.com/docs/project-configuration)*

### Requirements

Define `pip install` requirements in a `requirements.txt` file.

### Routing

Looking into this, the hardest thing to configure was [Vercel Routes]: 
> By default, routing is defined by the filesystem of your deployment. For example, if a user makes a request to /123.png, and your vercel.json file does not contain any routes with a valid src matching that path, it will fallback to the filesystem and serve /123.png if it exists.

This makes great sense for most serverless apps, but doesn't work so well with FastAPI when one function needs to 
respond to multiple routes (figured out in this [issue](https://github.com/zeit/now/issues/3729#issuecomment-582114686)).

I couldn't get `rewrite` to work, but did have success routing all requests to one FastAPI function:
```json
  "routes": [
    { "src": "/(.*)", "dest": "app/main.py" }
  ]
```

### Defining Functions

By default Vercel also looks for Python apps in an `index.py` file at the root or in the `/api` directory. This is can be
configured by adding a `build` configuration to `vercel.json`:
```json
  "builds": [
    { "src": "/app/main.py", "use": "@vercel/python" }
  ]
```


[FastAPI]: https://fastapi.tiangolo.com
[FastAPI SQL Databases Tutorial]:https://fastapi.tiangolo.com/tutorial/sql-databases/#review-all-the-files
[Vercel]: https://vercel.com
[Asynchronous Server Gateway Interface (ASGI)]: https://vercel.com/docs/runtimes#advanced-usage/advanced-python-usage/asynchronous-server-gateway-interface
[Vercel Routes]: https://vercel.com/docs/project-configuration#project/routes
[Zappa]: https://github.com/Miserlou/Zappa
[Mangum]: https://github.com/erm/mangum
