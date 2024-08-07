# Deployment Procedure

Our app is fairly simple.

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