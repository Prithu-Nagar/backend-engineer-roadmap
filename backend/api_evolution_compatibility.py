"""
Day 66 — API Evolution and Compatibility

A framework-neutral example showing how an API can evolve from a stable v1
contract to a richer v2 contract while keeping compatibility decisions explicit.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UserProfile:
    user_id: int
    display_name: str
    email: str
    active: bool


class ApiVersionError(ValueError):
    """Raised when an unsupported API version is requested."""


class UserApiV1:
    """Stable legacy response contract."""

    @staticmethod
    def serialize(profile: UserProfile) -> dict[str, object]:
        return {
            "id": profile.user_id,
            "name": profile.display_name,
            "email": profile.email,
        }


class UserApiV2:
    """New response contract that adds explicit account status."""

    @staticmethod
    def serialize(profile: UserProfile) -> dict[str, object]:
        return {
            "id": profile.user_id,
            "display_name": profile.display_name,
            "email": profile.email,
            "status": "active" if profile.active else "inactive",
        }


class UserApiCompatibilityLayer:
    """Keeps version selection and deprecation policy at the API boundary."""

    SUPPORTED_VERSIONS = frozenset({"v1", "v2"})
    DEPRECATED_VERSIONS = frozenset({"v1"})

    def serialize(
        self,
        version: str,
        profile: UserProfile,
    ) -> tuple[dict[str, object], dict[str, str]]:
        normalized = version.strip().lower()
        if normalized not in self.SUPPORTED_VERSIONS:
            raise ApiVersionError(f"unsupported API version: {version}")

        headers: dict[str, str] = {}
        if normalized in self.DEPRECATED_VERSIONS:
            headers["Deprecation"] = "true"
            headers["Sunset"] = "2027-01-01"
            headers["Link"] = '</api/v2/users>; rel="successor-version"'

        if normalized == "v1":
            return UserApiV1.serialize(profile), headers
        return UserApiV2.serialize(profile), headers


def main() -> None:
    profile = UserProfile(
        user_id=42,
        display_name="Asha",
        email="asha@example.com",
        active=True,
    )
    api = UserApiCompatibilityLayer()

    v1_response, v1_headers = api.serialize("v1", profile)
    v2_response, v2_headers = api.serialize("v2", profile)

    print("v1:", v1_response, v1_headers)
    print("v2:", v2_response, v2_headers)


if __name__ == "__main__":
    main()
