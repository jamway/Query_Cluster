ENV_DEPLOY="project_id"
docker build --build-arg envtype=$ENV_DEPLOY -t doc2vec ./
docker tag doc2vec gcr.io/$ENV_DEPLOY/doc2vec:test
docker push gcr.io/$ENV_DEPLOY/doc2vec:test
