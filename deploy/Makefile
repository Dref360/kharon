PROJECT_ID=local
REGION=northamerica-northeast1

.PHONY: deploy
deploy: deploy_be deploy_fe

.PHONY: deploy_be
deploy_be:
	gcloud run deploy kharon-backend --image dref360/kharon-backend:latest --platform managed --region ${REGION} --allow-unauthenticated --port 8000

.PHONY: deploy_fe
deploy_fe:
	gcloud run deploy kharon-frontend --image dref360/kharon-frontend:latest --platform managed --region ${REGION} --allow-unauthenticated