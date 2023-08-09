# 2023_ingest_aws

Example of automation test repo with tests based on a real service(work with db, AWS(sqs,s3,ec2,rds, API). Created by domanina from scratch
---
Pytest+python
---

run:
`pytest -v ./tests`

run:
`pytest -v`


Allure
---

run with Allure reports:

`pytest -v --alluredir=allure-results`

start Allure:

`allure serve allure-results`