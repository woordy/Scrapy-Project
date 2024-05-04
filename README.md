# Scrapy with Splash Data Scraper

## Overview
This project showcases a web scraping solution using the Scrapy framework paired with Splash for handling dynamic content rendered with JavaScript. 

## Features
- **Dynamic content handling**: Utilizes Splash to render JavaScript-generated content on the webpage.
- **Custom logging**: Configures a custom logging setup that logs events into a file named with the current timestamp.
- **Error handling**: Robust error handling to manage HTTP errors and log them for review.


## Setup
### Requirements
- Python 3.6+
- Scrapy 2.4+
- Scrapy-Splash

### Key Components
- **Dockerfile and docker-compose.yml**: Define the Docker containers for the Scrapy and Splash setup.
- **requirements.txt**: Specifies all necessary Python dependencies.
- **scrapyproject/**: Contains all necessary modules and files for the Scrapy operations.
  - **database/**: Includes the database connection and ORM model definitions.
  - **spiders/**: Houses the `hospital_spider.py` Scrapy spider for data scraping.
  - **items.py, middlewares.py, pipelines.py, settings.py**: Define the project's data structures, middleware, item pipelines, and settings, respectively.


## Setup and Installation

### Using Docker
Ensure Docker is installed on your machine. If not, download and install Docker from [Docker's official site](https://www.docker.com/products/docker-desktop).

To set up the project environment:

1. **Build and run the containers in detached mode**:
   ```bash
   docker-compose up -d




