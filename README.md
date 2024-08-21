# 2023 Video Ingest Automation Testing

== Description ==

This repository is an example of automation testing for a real-world service that interacts with various AWS components (SQS, S3, RDS), databases, classic API. The project was entirely built from scratch by domanina using Python and Pytest.

----
== Key Features ==

* '''Comprehensive Testing''': The tests cover both traditional API testing and interactions with AWS services and databases.
* '''Pytest + Python''': Utilizes Pytest framework, providing a robust and scalable testing environment.
* '''Allure Reporting''': Integrated with Allure to generate detailed and visually appealing test reports.

----
== Getting Started ==

=== Prerequisites ===

Ensure that you have the following installed:

* Python 3.9
* AWS CLI configured with appropriate permissions
* Allure (for generating reports)

=== Installation ===

1. Clone the repository:

2. Install the required Python packages:

   `pip install -r requirements.txt`

----
== Running Tests ==

To execute the tests, use the following commands:

=== Basic Test Run ===

Run all tests with verbose output:

`pytest -v ./tests`

or simply:

`pytest -v`

=== Running with Allure Reports ===

To generate Allure reports:

`pytest -v --alluredir=allure-results`

To view the generated reports:

`allure serve allure-results`