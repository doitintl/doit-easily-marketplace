FROM gcr.io/cloud-marketplace-tools/k8s/deployer_envsubst/onbuild

COPY manifest/* /data/manifest/
COPY schema.yaml /data/
COPY apptest/deployer /data-test/

ARG REGISTRY
ARG TAG
RUN cat /data-test/schema.yaml \
    | env -i "REGISTRY=$REGISTRY" "TAG=$TAG" envsubst \
    > /data-test/schema.yaml.new \
    && mv /data-test/schema.yaml.new /data-test/schema.yaml