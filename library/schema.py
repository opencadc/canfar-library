"""JSON Schema for CANFAR Library manifest files."""

from __future__ import annotations

from typing import List, Optional, Literal

from pydantic import AnyUrl, BaseModel, ConfigDict, Field


Platform = Literal[
    "linux/amd64",
    "linux/arm64",
    "linux/arm/v7",
    "linux/arm/v6",
    "linux/arm/v5",
    "windows/amd64",
]


class Maintainer(BaseModel):
    """Details about the maintainer of the image."""

    name: str = Field(..., title="Name", description="Name of the maintainer.")
    email: str = Field(
        ...,
        title="Email",
        description="Contact email.",
    )
    github: Optional[str] = Field(
        None,
        title="GitHub Username",
        description="GitHub Username.",
    )
    gitlab: Optional[str] = Field(
        None,
        title="GitLab Username",
        description="GitLab Username.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class Git(BaseModel):
    """Repository information for the image build source."""

    repo: AnyUrl = Field(
        ...,
        title="Repository",
        description="Git repository.",
        examples=["https://github.com/opencadc/canfar-library"],
    )
    tag: str = Field(
        ...,
        title="Git Tag Reference",
        description="git tag",
        examples=["refs/tags/v1.0.0", "v1.0.0"],
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class Build(BaseModel):
    """Configuration for building the container image."""

    path: str = Field(
        ".",
        title="Path",
        description="Directory containing the Dockerfile.",
        examples=[".", "images/base"],
    )
    dockerfile: str = Field(
        "Dockerfile",
        title="Dockerfile",
        description="Dockerfile.",
        examples=["Dockerfile", "base.Dockerfile"],
    )
    context: str = Field(
        ".",
        title="Build Context",
        description="Build context relative to path.",
        examples=[".", "../"],
    )
    builder: str = Field(
        "buildkit",
        title="Build Backend",
        description="Builder backend used for this entry.",
        examples=["buildkit"],
    )
    platforms: list[Platform] = Field(
        default=["linux/amd64"],
        title="Target Platforms",
        description="Target platforms.",
        examples=[["linux/amd64"], ["linux/amd64", "linux/arm64"]],
    )
    tags: List[str] = Field(
        ...,
        title="Container Image Tags",
        description="Image tags.",
        examples=["latest", "1.0.0"],
    )
    args: Optional[dict[str, str]] = Field(
        None,
        title="Build Args",
        description="Build-time variables.",
        examples=[{"FOO": "bar"}],
    )
    annotations: Optional[dict[str, str]] = Field(
        None,
        title="Image Annotations",
        description="Annotations for the image.",
        examples=[{"canfar.image.type": "base"}],
    )
    labels: Optional[dict[str, str]] = Field(
        None,
        title="Image Labels",
        description="Labels for the image.",
        examples=[
            {
                "org.opencontainers.image.title": "CANFAR Base Image",
                "org.opencontainers.image.description": "Base image for CANFAR Science Platform",
            }
        ],
    )
    target: Optional[str] = Field(
        None,
        title="Build Target",
        description="Target stage to build.",
        examples=["runtime"],
    )

    test: Optional[str] = Field(
        None,
        title="Test Command",
        description="Test cmd to verify the image.",
        examples=["bash -c 'echo hello world'", "bash -c ./test.sh"],
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class Metadata(BaseModel):
    """
    Metadata for the image.
    """

    identifier: str = Field(..., description="Unique science identifier for the image.")
    project: str = Field(..., description="SRCnet Project name for the image.")


class Manifest(BaseModel):
    """CANFAR Container Library Schema."""

    name: str = Field(..., description="Image name.", examples=["astroml"])
    maintainers: List[Maintainer] = Field(
        ...,
        title="Maintainers",
        description="Image maintainers.",
    )
    git: Git = Field(..., title="Git Info", description="Image repository.")
    build: Build = Field(..., title="Build Info", description="Image build info.")
    metadata: Metadata = Field(..., title="Metadata", description="Image metadata.")

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://raw.githubusercontent.com/opencadc/canfar-library/main/.spec.json",
            "title": "CANFAR Container Library Schema",
            "description": "Schema to capture ownership, build source, intent, and identity for library artifacts.",
        },
    )


if __name__ == "__main__":
    # Emit the JSON Schema that downstream tools can consume.
    import json

    print(json.dumps(Manifest.model_json_schema(), indent=2))
