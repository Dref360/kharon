<p align="center">
   <img src="docs/logo.png", width="40%">
</p>

# Shared Science

⚠️ Under Construction! ⚠️

**Reverse Proxy Server with Google Auth**

---

## Overview

   This project solves the problem of sharing Docker based applications with other people in your organization. This way, you can safely create

Shared Science is a FastAPI-based reverse proxy server with Google Authentication. It allows you to secure your applications by requiring users to authenticate via their Google accounts before accessing web servers spawned on different architecture.

## Features

- [ ] **Reverse Proxy:** Directs incoming requests to the appropriate backend services.
- [x] **Google Authentication:** Users must log in with their Google accounts to access protected resources.
- [x] **FastAPI:** Utilizes the FastAPI framework for efficient and fast development.
- [ ] **Job Scheduler:** Interface with a variety of job scheduling.
  - [ ] **Docker:** Local Cluster
  - [ ] **GKE:** Google Kubernetes Engine

### Recipes

- [ ] **Gradio App:** Launch your own gradio app protected behind a Google Login.
- [ ] **Azimuth:** Collaborate securely on improving your dataset or model using [Azimuth](github.com/ServiceNow/azimuth).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Dref360/shared-science.git
   ```

2. Install the required dependencies:

   ```bash
   poetry install
   ```

## Configuration

1. Create a Google Cloud Platform (GCP) project and set up the OAuth 2.0 credentials.

2. Create a copy of `.env.default` named `.env` with your GCP credentials and other configuration settings.
   1. Do the same in `webapp/.env`

## Usage

1. Start the FastAPI server:

   ```bash
   poetry run uvicorn shared_science.app:app --reload
   ```

2. Access the reverse proxy at `http://localhost:8000` and follow the Google Authentication flow.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Please make sure to follow the project's code of conduct.

## License

This project is licensed under the Apache V2 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI: https://fastapi.tiangolo.com/

Thank you for using Shared Science!
