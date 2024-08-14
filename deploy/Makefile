PROJECT_ID=local
REGION=us-east4

.PHONY: deploy
deploy: deploy_be deploy_fe

.PHONY: deploy_be
deploy_be:
	gcloud beta run deploy kharon-backend \
	--image dref360/kharon-backend:latest \
	--platform managed --region ${REGION} \
	--allow-unauthenticated --port 8000 \
	--add-volume name=KHARON_STORAGE,type=cloud-storage,bucket=kharon_storage \
	--add-volume-mount volume=KHARON_STORAGE,mount-path=/data \
	--set-env-vars "KHARON_STORAGE=/data" \
	--update-secrets=GOOGLE_CLIENT_ID=KHARON_GOOGLE_CLIENT_ID:latest \
	--update-secrets=GOOGLE_CLIENT_SECRET=KHARON_GOOGLE_CLIENT_SECRET:latest \

.PHONY: deploy_fe
deploy_fe:
	cd ../webapp && gcloud app deploy --quiet