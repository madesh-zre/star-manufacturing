# Star Manufacturing

A responsive manufacturing company website built to present services, capabilities and consultation enquiries.

## Features

- Responsive single-page website
- Company branding and hero section
- Navigation between website sections
- Manufacturing feature cards
- Industries and About sections
- Customer consultation form
- Python backend for handling enquiries
- Local registration storage

## Technologies Used

- HTML5
- CSS3
- JavaScript
- Python

## Project Structure

- index.html - Main website
- css/styles.css - Website styling
- js/app.js - Frontend functionality
- server.py - Python backend
- assets/ - Images and icons
- tests/ - Backend tests

## Requirements

Python 3.10 or later.

No external Python dependencies are required.

## Run the Project

1. Open the project folder in PowerShell.
2. Run:

   py server.py

3. Open your browser and visit:

   http://127.0.0.1:8765/

## Run Backend Tests

Run:

   py -m unittest discover -s tests -v

## Data Privacy

Customer registration records and environment secrets are excluded from Git using .gitignore.

## Deployment

The production deployment must provide a working frontend and backend API over HTTPS.

The consultation form must return genuine success or error responses.

## Project Status

Local website and backend functionality have been tested in Chrome and Firefox.
