import datetime
import os

from pinkhat.iacparsers.utils.certificate.certificate_validator import CertificateValidator
from pinkhat.iacparsers.utils.graph_builder.graph_core import GraphCore

certificate_data = {
    "github.com": {
        "version": "v3",
        "serial_number": "4e28f786b66c1a3b942cd2c40eb742a5",
        "issuer": "C=GB,ST=Greater Manchester,L=Salford,O=Sectigo Limited,"
        "CN=Sectigo ECC Domain Validation Secure Server CA",
        "subject": "CN=github.com",
        "signature_algorithm": "ecdsa-with-SHA256",
        "signature_hash_algorithm": "sha256",
        "signature": "3045022100aeed8c70faf478dc1c58db83118d1afeb1b35d17d"
        "1ae6fba5df65e4b385865ec02201ab84d41010a06a9bfbc6f02d44a755762fdbe26dfa5327a3d6083226c89eb00",
        "not_before_utc": datetime.datetime(
            2024, 3, 7, 0, 0, tzinfo=datetime.timezone.utc
        ),
        "not_after_utc": datetime.datetime(
            2025, 3, 7, 23, 59, 59, tzinfo=datetime.timezone.utc
        ),
        "extensions": {
            "authorityKeyIdentifier": {
                "authority_cert_issuer": None,
                "authority_cert_serial_number": None,
                "key_identifier": "f6850a3b1186e1047d0eaa0b2cd2eecc647b7bae",
                "critical": False,
            },
            "subjectKeyIdentifier": {
                "digest": "3b683f343af54734caefa64e3d9abd5e6e7acc9f",
                "key_identifier": "3b683f343af54734caefa64e3d9abd5e6e7acc9f",
                "critical": False,
            },
            "keyUsage": {
                "content_commitment": False,
                "crl_sign": False,
                "data_encipherment": False,
                "decipher_only": None,
                "digital_signature": True,
                "encipher_only": None,
                "key_agreement": False,
                "key_cert_sign": False,
                "key_encipherment": False,
                "critical": True,
            },
            "basicConstraints": {"ca": False, "path_length": None, "critical": True},
            "extendedKeyUsage": {
                "serverAuth": "1.3.6.1.5.5.7.3.1",
                "clientAuth": "1.3.6.1.5.5.7.3.2",
                "critical": False,
            },
            "certificatePolicies": {
                "policies": [
                    {
                        "policy_identifier": "1.3.6.1.4.1.6449.1.2.2.7",
                        "policy_qualifiers": ["https://sectigo.com/CPS"],
                    },
                    {
                        "policy_identifier": "2.23.140.1.2.1",
                        "policy_qualifiers": None,
                    },
                ],
                "critical": False,
            },
            "authorityInfoAccess": {
                "authority_information": [
                    {
                        "access_method": "caIssuers",
                        "access_location": "http://crt.sectigo.com/SectigoECCDomainValidationSecureServerCA.crt",
                    },
                    {
                        "access_method": "OCSP",
                        "access_location": "http://ocsp.sectigo.com",
                    },
                ],
                "critical": False,
            },
            "signedCertificateTimestampList": {"critical": False},
            "subjectAltName": {
                "subject_alternative_name": [
                    {"dns": "github.com"},
                    {"dns": "www.github.com"},
                ],
                "critical": False,
            },
        },
        "public_key": {
            "algorithm": "ECC",
            "size": 256,
            "pub": "04044efc7a3d5dd918d6a87d9808233949169974dbd398e046e94a72231506e28"
            "1dd91dec6f09dca888244710c05f157a1985691054ca2034ba3f956db5e57de91",
        },
    },
    "GB,Greater Manchester,Salford,Sectigo Limited,Sectigo ECC Domain Validation Secure Server CA": {
        "version": "v3",
        "serial_number": "f3644e6b6e0050237e0946bd7be1f51d",
        "issuer": "C=US,ST=New Jersey,L=Jersey City,O=The USERTRUST Network,CN=USERTrust ECC Certification Authority",
        "subject": "CN=Sectigo ECC Domain Validation Secure Server CA,"
        "O=Sectigo Limited,L=Salford,ST=Greater Manchester,C=GB",
        "signature_algorithm": "ecdsa-with-SHA384",
        "signature_hash_algorithm": "sha384",
        "signature": "306502304be7c7715cb15c096d9a42605f73e9f0d626d4b551546c712d1c8560"
        "4d28f14da6f0ca76b74a45efa8024af68d4fae6e023100e0e1792af65e1700ee8"
        "cfd1e679d19d32196b77de13a0a15b665fbf3a7145cea9ef3a17231ef0a510211070a99cf1f98",
        "not_before_utc": datetime.datetime(
            2018, 11, 2, 0, 0, tzinfo=datetime.timezone.utc
        ),
        "not_after_utc": datetime.datetime(
            2030, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc
        ),
        "extensions": {
            "authorityKeyIdentifier": {
                "authority_cert_issuer": None,
                "authority_cert_serial_number": None,
                "key_identifier": "3ae10986d4cf19c29676744976dce035c663639a",
                "critical": False,
            },
            "subjectKeyIdentifier": {
                "digest": "f6850a3b1186e1047d0eaa0b2cd2eecc647b7bae",
                "key_identifier": "f6850a3b1186e1047d0eaa0b2cd2eecc647b7bae",
                "critical": False,
            },
            "keyUsage": {
                "content_commitment": False,
                "crl_sign": True,
                "data_encipherment": False,
                "decipher_only": None,
                "digital_signature": True,
                "encipher_only": None,
                "key_agreement": False,
                "key_cert_sign": True,
                "key_encipherment": False,
                "critical": True,
            },
            "basicConstraints": {"ca": True, "path_length": 0, "critical": True},
            "extendedKeyUsage": {
                "serverAuth": "1.3.6.1.5.5.7.3.1",
                "clientAuth": "1.3.6.1.5.5.7.3.2",
                "critical": False,
            },
            "certificatePolicies": {
                "policies": [
                    {"policy_identifier": "2.5.29.32.0", "policy_qualifiers": None},
                    {
                        "policy_identifier": "2.23.140.1.2.1",
                        "policy_qualifiers": None,
                    },
                ],
                "critical": False,
            },
            "cRLDistributionPoints": {
                "crl_distribution_points": [
                    {
                        "full_name": [
                            "http://crl.usertrust.com/USERTrustECCCertificationAuthority.crl"
                        ],
                        "crl_issuer": None,
                        "reasons": None,
                        "relative_name": None,
                    }
                ],
                "critical": False,
            },
            "authorityInfoAccess": {
                "authority_information": [
                    {
                        "access_method": "caIssuers",
                        "access_location": "http://crt.usertrust.com/USERTrustECCAddTrustCA.crt",
                    },
                    {
                        "access_method": "OCSP",
                        "access_location": "http://ocsp.usertrust.com",
                    },
                ],
                "critical": False,
            },
        },
        "public_key": {
            "algorithm": "ECC",
            "size": 256,
            "pub": "04791893ca9f6d9e6c57002305370b5f0f585ac4de7f55a3e91ed6"
            "d9250a88a0204a1d7a4f05308a6349138c64210795fd3a35e14ace90f018f73daf68a6fbd448",
        },
    },
    "US,New Jersey,Jersey City,The USERTRUST Network,USERTrust ECC Certification Authority": {
        "version": "v3",
        "serial_number": "5c8b99c55a94c5d27156decd8980cc26",
        "issuer": "C=US,ST=New Jersey,L=Jersey City,O=The USERTRUST Network,CN=USERTrust ECC Certification Authority",
        "subject": "CN=USERTrust ECC Certification Authority,O=The USERTRUST Network,L=Jersey City,ST=New Jersey,C=US",
        "signature_algorithm": "ecdsa-with-SHA384",
        "signature_hash_algorithm": "sha384",
        "signature": "306502303667a11608dce49700411d4ebee16301cf3baa421164a09d94390"
        "211795c7b1dfa64b9ee1642b3bf8ac209c4ece4b14d023100e92a61478c524"
        "a4b4e1870f6d644d66ef583ba6d58bd24d95648eaefc4a24681886a3a46d1a99b4dc961dad15d576a18",
        "not_before_utc": datetime.datetime(
            2010, 2, 1, 0, 0, tzinfo=datetime.timezone.utc
        ),
        "not_after_utc": datetime.datetime(
            2038, 1, 18, 23, 59, 59, tzinfo=datetime.timezone.utc
        ),
        "extensions": {
            "subjectKeyIdentifier": {
                "digest": "3ae10986d4cf19c29676744976dce035c663639a",
                "key_identifier": "3ae10986d4cf19c29676744976dce035c663639a",
                "critical": False,
            },
            "keyUsage": {
                "content_commitment": False,
                "crl_sign": True,
                "data_encipherment": False,
                "decipher_only": None,
                "digital_signature": False,
                "encipher_only": None,
                "key_agreement": False,
                "key_cert_sign": True,
                "key_encipherment": False,
                "critical": True,
            },
            "basicConstraints": {"ca": True, "path_length": None, "critical": True},
        },
        "public_key": {
            "algorithm": "ECC",
            "size": 384,
            "pub": "041aac545aa9f96823e77ad5246f53c65ad84babc6d5b6d1e67371aedd9c"
            "d60c61fddba08903b80514ec57ceee5d3fe221b3cef7d48a79e0a3837e2d9"
            "7d061c4f199dc259163ab7f30a3b470e2c7a1339cf3bf2e5c53b15fb37d327f8a34e37979",
        },
    },
}


def test_certificate_validator():
    test_file_name = "github.crt"
    test_file_path = os.path.join("tests", "certificate", "test_files", test_file_name)
    graph_builder = GraphCore()
    certificate_validator = CertificateValidator(
        certificate_path=test_file_path, graph_builder=graph_builder
    )
    certificate_validator.load_certificate_data()
    objects = graph_builder.get_objects()
    assert len(certificate_data) == len(objects)
    for object_name, object_value in objects.items():
        assert certificate_data.get(object_name) == object_value.object
