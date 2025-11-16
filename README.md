# IONITE: TJHSST CLUB SPOT CHECKER

Powered by Flask + Vercel + Google Sheets + TJHSST INTRANET-ION API

This experimental club spot checker is a side-project of mine that checks periodically if a club spot is available. The endpoint uses Flask 3 on Vercel with Serverless Functions using the Python Runtime.
[Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python).

## Demo Flask app with vercel

https://flask-python-template.vercel.app/

## PUBLIC ENDPOINT:

Access to the public IONITE Flask endpoint is currently restricted.


## How it Works

This example uses the Web Server Gateway Interface (WSGI) with Flask to enable handling requests on Vercel with Serverless Functions.

## Running Flask Locally

```bash
npm i -g vercel
vercel dev
```
You should get something like:
Your Flask application is now available at `http://localhost:3000`.
