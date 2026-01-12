"""JSON Schema for CANFAR Library manifest files."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional, Any

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, model_validator


class Architecture(str, Enum):
    """Container Architectures."""

    AMD64 = "amd64"
    ARM32V5 = "arm32v5"
    ARM32V6 = "arm32v6"
    ARM32V7 = "arm32v7"
    ARM64V8 = "arm64v8"
    WINDOWS_AMD64 = "windows-amd64"


class Builder(str, Enum):
    """Docker build backends."""

    BUILDKIT = "buildkit"
    CLASSIC = "classic"
    OCI_IMPORT = "oci-import"


class Maintainer(BaseModel):
    """Build Maintainer Information."""

    name: str = Field(..., title="Name", description="Full name of the maintainer.")
    email: str = Field(
        ...,
        title="Email",
        description="Contact email, required for traceability.",
    )
    github: Optional[str] = Field(
        None,
        title="Maintainer Github",
        description="Github handle without the leading '@'.",
    )
    gitlab: Optional[str] = Field(
        None,
        title="Maintainer Gitlab",
        description="GitLab handle without the leading '@'.",
    )

    model_config = ConfigDict(extra="forbid")


class Git(BaseModel):
    """Git repository which contains build source."""

    repo: AnyUrl = Field(
        ...,
        title="Repository",
        description="Git repository which contains the Dockerfile.",
    )
    fetch: str = Field(
        "refs/heads/main",
        title="Fetch",
        description="Reference to fetch before resolving commits.",
        examples=["refs/heads/main", "refs/tags/v1.0.0"],
    )
    sha: Optional[str] = Field(
        None,
        title="Git Commit SHA",
        description="Commit SHA to checkout for builds.",
    )
    tag: Optional[str] = Field(
        None,
        title="Git Tag",
        description="Tag to checkout for builds.",
    )

    @model_validator(mode="before")
    @classmethod
    def _sanitize_checkout(cls, data: Any) -> Any:
        """Check git config.

        Raises:
            ValueError: If neither sha nor tag is provided.
            ValueError: If both sha and tag are provided.

        Returns:
            Any: The sanitized data.
        """
        if data.get("sha") is None and data.get("tag") is None:
            raise ValueError("Either sha or tag must be provided.")
        if data.get("sha") is not None and data.get("tag") is not None:
            raise ValueError("Only one of sha or tag may be provided.")
        return data

    model_config = ConfigDict(extra="forbid")


class Build(BaseModel):
    """Build information."""

    path: str = Field(
        ".",
        title="Path",
        description="Path to the directory containing the Dockerfile; defaults to the root of the repository.",
    )
    dockerfile: str = Field(
        "Dockerfile",
        title="Dockerfile",
        description="Name of the Dockerfile relative to the path.",
        examples=["Dockerfile", "Dockerfile-alternate"],
    )
    context: str = Field(
        ".",
        title="Build Context",
        description="Build context path relative to the Dockerfile.",
        examples=[".", "../"],
    )
    builder: str = Field(
        Builder.BUILDKIT,
        title="Build Backend",
        description="Builder backend used for this entry.",
        examples=[Builder.BUILDKIT, Builder.CLASSIC, Builder.OCI_IMPORT],
    )
    platforms: list[Architecture] = Field(
        default=[Architecture.AMD64],
        title="Image Platforms",
        description="Set target platforms for the build.",
    )
    tags: List[str] = Field(
        ..., title="Image Tags", description="Tags produced by this build entry."
    )
    args: Optional[dict[str, str]] = Field(
        None,
        title="Build Args",
        description="Set build-time variables for the build.",
    )
    annotations: Optional[dict[str, str]] = Field(
        None,
        title="Image Annotations",
        description="Add annotation to the container image.",
    )
    labels: Optional[dict[str, str]] = Field(
        None,
        title="Image Labels",
        description="Add metadata to the container image.",
    )
    target: Optional[str] = Field(
        None,
        title="Build Target",
        description="Set the target build stage to build.",
    )

    test: Optional[Run] = Field(
        None,
        title="Image Test Command",
        description="Command to run in the created container to verify the image is working.",
    )

    model_config = ConfigDict(extra="forbid")


class Metadata(BaseModel):
    """
    Metadata for the image.
    """

    identifier: str = Field(..., description="Unique science identifier for the image.")
    project: str = Field(..., description="SRCnet Project name for the image.")


class Run(BaseModel):
    """
    Test information for the image.
    """

    cmd: Optional[str] = Field(
        None,
        title="Testing Command",
        description="Command to run in the created container to verify the image is working."
        " The command is run with `docker run --rm -it <image> <cmd>`, where image is populated automatically from the build process."
        " If the command returns a non-zero exit code, the test is considered to have failed.",
        examples=["bash -c 'echo hello world'"],
    )


class Manifest(BaseModel):
    """
    Manifest information.
    """

    version: float = Field(
        0.2, title="Version", description="Library manifest version."
    )
    name: str = Field(..., description="Name of the image.", examples=["astroml"])
    maintainers: List[Maintainer] = Field(
        ...,
        title="Maintainers",
        description="List of maintainers responsible for the image.",
    )
    git: Git = Field(
        ..., title="Git Info", description="Repository information for the image."
    )
    build: Build = Field(
        ..., title="Build Info", description="Build information for the image."
    )
    metadata: Metadata = Field(
        ..., title="Metadata", description="Metadata for the image."
    )


if __name__ == "__main__":
    # Emit the JSON Schema that downstream tools can consume.
    import json

    print(json.dumps(Manifest.model_json_schema(), indent=2))
