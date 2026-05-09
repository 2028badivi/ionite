# IONITE: TJHSST Club Spot Checker

Powered by Flask + Vercel + Python + Cron Scheduling + Google Sheets + TJHSST Intranet-IONv3 API

Developed by Bhavesh Adivi

This experimental club spot checker is a side-project of mine that checks periodically if a club spot is available. The endpoint uses Flask 3 on Vercel with Serverless Functions using the 
[Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python).

## Demo Flask app with vercel

https://flask-python-template.vercel.app/

## PUBLIC ENDPOINT:

Access to the public IONITE Flask endpoint is currently restricted due to serverless function runtime limitations on the free plan.


## How it Works

This example uses the Web Server Gateway Interface (WSGI) with Flask to enable handling requests on Vercel with Serverless Functions.

I set up a cron job to ping this url occassionally and parse output JSON to send an email directly to my inbox if there is an open spot available for a club that I am interested in attending. Honestly, I made this because one club that I really wanted to go to was very popular and people were signing up quickly so I wanted to be notified ASAP if anyone opened their spot. 

## Running Flask Locally

```bash
npm i -g vercel
vercel dev
```
You should get something like:
Your Flask application is now available at `http://localhost:3000`.
