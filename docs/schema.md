---
hide: 
    - toc
---

# CANFAR Library Manifest

Schema to capture ownership, build source, intent, and identity for library artifacts.

### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Description | Examples |
| -------- | ---- | -------- | --------------- | ----------- | -------- |
| name | `string` | ✅ | string | Image name. | ```astroml``` |
| maintainers | `array` | ✅ | [Maintainer](#maintainer) | Image maintainers. |  |
| git | `object` | ✅ | [Git](#git) | Image repository. |  |
| build | `object` | ✅ | [Build](#build) | Image build info. |  |
| metadata | `object` | ✅ | [Metadata](#metadata) | Image metadata. |  |


---

# Definitions

## Build

Configuration for building the container image.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Default | Description | Examples |
| -------- | ---- | -------- | --------------- | ------- | ----------- | -------- |
| tags | `array` | ✅ | string |  | Image tags. | ```latest```, ```1.0.0``` |
| path | `string` |  | string | `"."` | Directory containing the Dockerfile. | ```.```, ```images/base``` |
| dockerfile | `string` |  | string | `"Dockerfile"` | Dockerfile. | ```Dockerfile```, ```base.Dockerfile``` |
| context | `string` |  | string | `"."` | Build context relative to path. | ```.```, ```../``` |
| builder | `string` |  | string | `"buildkit"` | Builder backend used for this entry. | ```buildkit``` |
| platforms | `array` |  | `linux/amd64` `linux/arm64` `linux/arm/v7` `linux/arm/v6` `linux/arm/v5` `windows/amd64` | `["linux/amd64"]` | Target platforms. | ```['linux/amd64']```, ```['linux/amd64', 'linux/arm64']``` |
| args | `object` or `null` |  | object | `null` | Build-time variables. | ```{'FOO': 'bar'}``` |
| annotations | `object` or `null` |  | object | `null` | Annotations for the image. | ```{'canfar.image.type': 'base'}``` |
| labels | `object` or `null` |  | object | `null` | Labels for the image. | ```{'org.opencontainers.image.description': 'Base image for CANFAR Science Platform', 'org.opencontainers.image.title': 'CANFAR Base Image'}``` |
| target | `string` or `null` |  | string | `null` | Target stage to build. | ```runtime``` |
| test | `string` or `null` |  | string | `null` | Test cmd to verify the image. | ```bash -c 'echo hello world'```, ```bash -c ./test.sh``` |

## Git

Repository information for the image build source.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Description | Examples |
| -------- | ---- | -------- | --------------- | ----------- | -------- |
| repo | `string` | ✅ | Format: [`uri`](https://json-schema.org/understanding-json-schema/reference/string#built-in-formats) | git repo | ```https://github.com/opencadc/canfar-library``` |
| tag | `string` | ✅ | string | git tag | ```refs/tags/v1.0.0```, ```v1.0.0``` |

## Maintainer

Details about the maintainer of the image.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| name | `string` | ✅ | string |  | Name of the maintainer. |
| email | `string` | ✅ | string |  | Contact email. |
| github | `string` or `null` |  | string | `null` | Github Username. |
| gitlab | `string` or `null` |  | string | `null` | Gitlab Username. |

## Metadata

Metadata for the image.

#### Type: `object`

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| identifier | `string` | ✅ | string | Unique science identifier for the image. |
| project | `string` | ✅ | string | SRCnet Project name for the image. |
