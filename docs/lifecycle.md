# Image Lifecycle

Let's walk through the full lifecycle of a library image from start to finish to help you understand how the library works and how you can contribute to it.

## Image Request

To request a new image be added to the library, you need to open a new issue in this repository. Please select the "Request New Image" template and fill out the form. We will review your request and get back to you as soon as possible.
In the request issue, you will be asked to provide the following information:

1. Contact information for the upstream maintainers
2. Whether the image source code is available under an [OSI Approved License](https://opensource.org/licenses)?
3. Is the software astronomy related and of interest to the community?
4. Link to the associated manifest pull request to be reviewed and merged once the request is approved
5. Link to the upstream `Dockerfile` to be reviewed for best practices, security, and optimization. (Performed on the manifest pull request)
6. Is the image based on an existing library image (for example, `base` or `python`)? If not, why not?
7. The manifest pull request passes all tests including static analysis, linting, and functional testing.

## Image Manifest

The image manifest is a YAML file that describes the image's source, build configuration, metadata, and other information. The manifest is written in YAML and is validated against the [Library's JSON schema](https://github.com/opencadc/canfar-library/blob/main/.spec.json) to ensure correctness.

```yaml
name: base
maintainers:
  - name: Shiny Brar
    email: shiny.brar@nrc-cnrc.gc.ca
    github: shinybrar
git:
  repo: https://github.com/opencadc/canfar-library
  tag: v0.1.0
build:
  path: images/base
  dockerfile: Dockerfile
  context: .
  platforms:
    - linux/amd64
    - linux/arm64
  tags:
    - latest
  labels:
    org.opencontainers.image.title: "CANFAR Base Image"
    org.opencontainers.image.description: "Base image for CANFAR Science Platform"
    org.opencontainers.image.vendor: "Canadian Astronomy Data Centre"
    org.opencontainers.image.source: "https://github.com/opencadc/canfar-library"
    org.opencontainers.image.licenses: "AGPL-3.0"
  annotations:
    canfar.image.type: "base"
  test: uv --version
metadata:
  identifier: canfar-base
  project: canfar
```

## How are library images updated?

1. A change gets committed to the relevant image source Git repository, for example a new version release or a bug fix.
2. A PR to the relevant image manifest (`manifests/XXXX.yaml`) is opened in this repository to update relevant fields, typically `git.tag`, `build.tags`, and `metadata` fields, etc.
3. The library automation detects the change and updates the PR with a full diff of the actual `Dockerfile` changes upstream.
4. The library automation runs a basic build test on `linux/amd64` to ensure the image builds successfully and executes `build.test` if provided.
5. Once the PR is approved and merged, the library automation builds the image for all the platforms specified in the manifest.
6. The build process generates provenance information about the build and image contents.
7. The image is pushed to the `images.canfar.net/library/<image>:<tag>` and signed using [cosign](https://github.com/sigstore/cosign).
8. The image is available for use downstream.
