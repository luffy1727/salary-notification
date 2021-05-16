## Project Idea
I used to have a cron job on my laptop that notifies me as soon as my bonuses are transferred into my bank account (the dates of the bonuses varies from month to month. It was distracting, both mentally and physically to go check my bank account every other hour) As I dove deep into the costs and perks of AWS, I found out that first million request of AWS Lambda are actually free. This led me to take my cron job to the clouds.

## Overview
This is a AWS Lambda Cron-job python code, to notify me as soon as my salary/bonuses are transfered into my bank account.

![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)

## To run this on AWS
1) Upload this project to AWS using the upload (or just copy it to the web IDE)
2) Replace the credentials in credentials.json.dist
3)
```bash
cp credentials.json.dist credentials.json
```


## To run this on AWS
1) Upload this project to AWS using the upload (or just copy it to the web IDE)
2) Replace the credentials in credentials.json.dist
3)
```bash
cp credentials.json dist credentials.json
```
4) Set up a CloudWatch trigger to run this code every hour 
```bash
rate(1 hour)
```
