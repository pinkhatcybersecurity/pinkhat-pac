from ipaddress import IPv4Address, IPv6Address, IPv6Network, IPv4Network
from pathlib import Path
from typing import Any

from cryptography import x509
from cryptography.hazmat.bindings._rust import ObjectIdentifier
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.dh import DHPublicKey
from cryptography.hazmat.primitives.asymmetric.dsa import DSAPublicKey
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
from cryptography.hazmat.primitives.asymmetric.x448 import X448PublicKey
from cryptography.x509 import (
    Extensions,
    Extension,
    ExtendedKeyUsage,
    AuthorityInformationAccess,
    PrecertificateSignedCertificateTimestamps,
    PolicyInformation,
    CertificatePolicies,
    UserNotice,
    SubjectAlternativeName,
    DNSName,
    DirectoryName,
    IPAddress,
    OtherName,
    RFC822Name,
    RegisteredID,
    UniformResourceIdentifier,
    Name,
    CRLDistributionPoints,
    DistributionPoint,
)
from loguru import logger

from pinkhat.iacparsers.utils.graph_builder.graph_core import GraphCore


class CertificateValidator:
    """
    Certificate description:
    https://www.rfc-editor.org/rfc/rfc5280
    https://learn.microsoft.com/en-us/azure/iot-hub/reference-x509-certificates
    """

    KEY_TYPE_ALGORITHM_MAPPING = {
        EllipticCurvePublicKey: "ECC",
        RSAPublicKey: "RSA",
        DHPublicKey: "DH",
        DSAPublicKey: "DSA",
        X448PublicKey: "X448",
        Ed448PublicKey: "ED448",
        X25519PublicKey: "X25519",
        Ed25519PublicKey: "ED25519",
    }
    KEY_SUBJECT_ALTERNATIVE_NAME = {
        DNSName: "dns",
        DirectoryName: "directory",
        IPAddress: "ip_address",
        OtherName: "other",
        RFC822Name: "rfc822",
        RegisteredID: "registered_id",
        UniformResourceIdentifier: "uniform_resource_identifier",
    }

    def __init__(self, certificate_path: str, graph_builder: GraphCore):
        self._certificate_path = certificate_path
        self._graph_builder = graph_builder

    def _load_certificate_from_file(self) -> list[x509.Certificate]:
        try:
            child = Path(self._certificate_path)
            if child.is_file():
                suffix = child.suffix.lower()
                if suffix in [".pem", ".crt"]:
                    return self._load_pem_x509_certificate(child=child)
                elif suffix == ".der":
                    return self._load_der_x509_certificate(child=child)
        except Exception as e:
            logger.error(str(e))

    @staticmethod
    def _load_pem_x509_certificate(child: Path) -> list[x509.Certificate]:
        with child.open("rb") as file:
            return x509.load_pem_x509_certificates(file.read())

    @staticmethod
    def _load_der_x509_certificate(child: Path) -> list[x509.Certificate]:
        with child.open("rb") as file:
            return [x509.load_der_x509_certificate(file.read())]

    def load_certificate_data(self):
        cert: x509.Certificate
        for cert in self._load_certificate_from_file():
            self._graph_builder.add_graph_object(
                name=",".join([s.value for s in cert.subject]),
                link="certificate",
                child_name=(
                    ",".join([s.value for s in cert.issuer])
                    if cert.subject != cert.issuer
                    else None
                ),
                object_in_graph=self._generate_certificate_data(cert=cert),
            )

    def _generate_certificate_data(self, cert: x509.Certificate) -> dict:
        public_key = cert.public_key()
        return {
            "version": cert.version.name,
            "serial_number": f"{cert.serial_number:x}",
            "issuer": ",".join([rdn.rfc4514_string() for rdn in cert.issuer.rdns]),
            "subject": cert.subject.rfc4514_string(),
            "signature_algorithm": cert.signature_algorithm_oid._name,
            "signature_hash_algorithm": cert.signature_hash_algorithm.name,
            "signature": cert.signature.hex(),
            "not_before_utc": cert.not_valid_before_utc,
            "not_after_utc": cert.not_valid_after_utc,
            "extensions": self._parse_extensions(extensions=cert.extensions),
            "public_key": {
                "algorithm": self._get_public_key_algorithm_type(public_key),
                "size": public_key.key_size,
                "pub": self._get_public_key(public_key=public_key),
            },
        }

    def _parse_extensions(self, extensions: Extensions):
        extension: Extension
        return {
            extension.oid._name: self._get_extension_properties(extension)
            for extension in extensions
        }

    def _get_extension_properties(self, extension: Extension):
        values = {}
        if isinstance(extension.value, ExtendedKeyUsage):
            values = {
                usage._name: usage.dotted_string for usage in extension.value._usages
            }
        elif isinstance(extension.value, AuthorityInformationAccess):
            values["authority_information"] = [
                {
                    "access_method": description.access_method._name,
                    "access_location": description.access_location.value,
                }
                for description in extension.value._descriptions
            ]
        elif isinstance(extension.value, CertificatePolicies):
            policy: PolicyInformation
            values["policies"] = [
                {
                    "policy_identifier": policy.policy_identifier.dotted_string,
                    "policy_qualifiers": (
                        [
                            self._parse_policy_qualifier(qualifier=qualifier)
                            for qualifier in policy.policy_qualifiers
                        ]
                        if policy.policy_qualifiers
                        else None
                    ),
                }
                for policy in extension.value._policies
            ]
        elif isinstance(extension.value, SubjectAlternativeName):
            values["subject_alternative_name"] = [
                {
                    self.KEY_SUBJECT_ALTERNATIVE_NAME.get(
                        type(san)
                    ): self._get_subject_alternative_name_value(value=san.value)
                }
                for san in extension.value
            ]
        elif isinstance(extension.value, CRLDistributionPoints):
            distribution_point: DistributionPoint
            values["crl_distribution_points"] = [
                {
                    "full_name": (
                        [full_name.value for full_name in distribution_point.full_name]
                        if distribution_point.full_name
                        else None
                    ),
                    "crl_issuer": (
                        [
                            crl_issuer.value
                            for crl_issuer in distribution_point.crl_issuer
                        ]
                        if distribution_point.crl_issuer
                        else None
                    ),
                    "reasons": distribution_point.reasons,
                    "relative_name": (
                        distribution_point.relative_name.rfc4514_string()
                        if distribution_point.relative_name
                        else None
                    ),
                }
                for distribution_point in extension.value
            ]
        elif isinstance(extension.value, PrecertificateSignedCertificateTimestamps):
            properties = self._get_properties(
                extension.value._signed_certificate_timestamps
            )
            values = {
                prop: self._get_value(
                    extension.value._signed_certificate_timestamps, prop
                )
                for prop in properties
            }
        else:
            properties = self._get_properties(extension.value)
            values = {
                prop: self._get_value(extension.value, prop) for prop in properties
            }
        values["critical"] = extension.critical
        return values

    @staticmethod
    def _get_properties(extension):
        return [
            prop
            for prop in dir(extension)
            if isinstance(getattr(extension.__class__, prop, None), property)
        ]

    def _parse_policy_qualifier(self, qualifier: str | UserNotice) -> dict | str | None:
        if not qualifier:
            return
        if str == type(qualifier):
            return qualifier
        qualifier: UserNotice
        notice_reference = qualifier.notice_reference
        if notice_reference:
            properties = self._get_properties(extension=notice_reference)
            notice_reference = {
                prop: self._get_value(notice_reference, prop) for prop in properties
            }
        return {
            "explicit_text": qualifier.explicit_text,
            "notice_reference": notice_reference,
        }

    @staticmethod
    def _get_subject_alternative_name_value(value):
        if str == type(value):
            return value
        elif Name == type(value):
            return value.rfc4514_string()
        elif type(value) in [IPv4Address, IPv6Address, IPv4Network, IPv6Network]:
            return str(value)
        elif bytes == type(value):
            return value.hex()
        elif ObjectIdentifier == type(value):
            return value.dotted_string

    @staticmethod
    def _get_value(value: Any, prop):
        try:
            tmp_value = getattr(value, prop)
            if bytes == type(tmp_value):
                return tmp_value.hex()
            return tmp_value
        except ValueError as e:
            logger.debug(str(e))

    def _get_public_key_algorithm_type(self, public_key):
        """
        Check the type of the public key
        """
        for class_name, algorithm_name in self.KEY_TYPE_ALGORITHM_MAPPING.items():
            if isinstance(public_key, class_name):
                return algorithm_name
        return "Unknown"

    @staticmethod
    def _get_public_key(public_key):
        if isinstance(public_key, RSAPublicKey):
            return public_key.public_bytes(
                serialization.Encoding.DER,
                serialization.PublicFormat.PKCS1,
            ).hex()
        elif isinstance(public_key, EllipticCurvePublicKey):
            return public_key.public_bytes(
                serialization.Encoding.X962,
                serialization.PublicFormat.UncompressedPoint,
            ).hex()
        else:
            return public_key.public_bytes(
                serialization.Encoding.DER,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            ).hex()
