# Deployment Procedure

Our app is fairly simple.

<img width="1406" alt="shapes at 24-08-11 13 09 29" src="https://github.com/user-attachments/assets/c3ff07a5-20c1-4dd2-b6cd-6db6178f57aa">


* Frontend
    * Cloud Run
    * ENV VAR:
        * REACT_APP_GOOGLE_CLIENT_ID
        * REACT_APP_BACKEND_URL
* Backend
    * Cloud Run
    * ENV VAR:
        * GOOGLE_CLIENT_ID
        * GOOGLE_CLIENT_SECRET

**Notes**
- The SQL Database is not permanent. This needs to be fixed.
    - We could mount a GCloud volume [Link](https://cloud.google.com/run/docs/configuring/services/cloud-storage-volume-mounts#gcloud)
