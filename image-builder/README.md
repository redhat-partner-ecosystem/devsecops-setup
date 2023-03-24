## Build the image locall

```shell
podman build -t devsecops-config/gitops-cli .
```

Run the image with an interactive shell:

```shell
podman run --name gitops --rm -i -t devsecops-config/gitops-cli bash
```
