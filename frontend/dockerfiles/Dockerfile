# syntax=docker/dockerfile:1
ARG VOLTO_VERSION
FROM plone/frontend-builder:${VOLTO_VERSION} as builder

# Copy jsconfig.json configuration
COPY --chown=node:node jsconfig.json /app/

# We copy here to install all addons (package.json)
COPY --chown=node:node src/addons/ /app/src/addons/

RUN <<EOT
    /setupAddon
    yarn install --network-timeout 1000000
    yarn build
    rm -rf cache omelette .yarn/cache
EOT

FROM plone/frontend-prod-config:${VOLTO_VERSION}

LABEL maintainer="Plone Collective <collective@plone.org>" \
      org.label-schema.name="ghcr.io/collective/plone-intranet-backend" \
      org.label-schema.description="Plone Intranet distribtuion frontend." \
      org.label-schema.vendor="Plone Foundation"

COPY --from=builder /app/ /app/
