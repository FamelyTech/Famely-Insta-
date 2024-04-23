# Jalodei

Scrapes data off of an instagram channel by just visting the relative url
`/insta/<user_handle>`

## Deploy

The helm repo is the 'kubernetes' folder. If you make any changes to the template:
`helm package kubernetes/jalodei`.

To deploy, first build the container with changes (if you have new deps use Dockerfile.builder):
Always build in the root of the repo to consider the `.dockerignore` constraints.

```bash
docker build -t registry.digitalocean.com/nano-registry/jalodei -f docker/Dockerfile .
docker push registry.digitalocean.com/nano-registry/jalodei
```

If you have authorization issues, pass ownership of the docker folder to your user
e.g. `sudo chown -R netopaas .docker`

You can just scale to 0 and then more to the deployment to update the image.

But if you changed other things you'll have to upgrade the chart:
djprod is 1 for staging and 2 for prod.

It is important that you have a secret in the value `miscSecrets` which contains
most of the secrets referenced in the environment of `deployment.yaml`
and `job-migrations.yaml`.



```bash
REPO=jalodei
SUFFIX=stage
helm uninstall $REPO-$SUFFIX
helm upgrade --install $REPO-$SUFFIX --force $REPO-0.1.0.tgz \
    --set nameOverride=$REPO-$SUFFIX \
    --set djprod=2 \
    --set rdsExternal=private-db-postgresql-nyc1-38696-do-user-6091934-0.b.db.ondigitalocean.com \
    --set dbSecret=jalodei-db \
    --set miscSecrets=jalodei-secrets \
    --set dbName=jalodei \
    --set dbPort=25060 \
    --set deleteDB=true
```

Add the `--install` if the chart is not up.
