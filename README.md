# Scraper for Company SQL Server

This repository contains code dedicated to scraping data from the company's SQL server. The main purpose of this code is to automate the retrieval of reports in Excel format and load the data into pandas DataFrames for further analysis.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
  - [itemlistscraper](#itemlistscraper)
  - [codedatescraper](#codedatescraper)
  - [Helper Functions](#helper-functions)
    - [configure_options](#configure_options)
    - [get_latest_file_path](#get_latest_file_path)
    - [wait_for_file_download](#wait_for_file_download)
- [Contributing](#contributing)
- [License](#license)

## Overview

The code in this repository automates the process of accessing reports on the company's SQL server, downloading the reports in Excel format, and loading the data into pandas DataFrames. This automation is achieved using Selenium WebDriver to interact with the web interface of the SQL server.

## Installation

To use this code, you need to have Python installed along with the following libraries:

- pandas
- selenium

You can install the required libraries using pip:

```sh
pip install pandas selenium
```
