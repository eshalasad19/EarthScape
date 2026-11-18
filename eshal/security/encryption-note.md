# Encryption Note

HDFS encryption zones need Hadoop KMS (Key Management Server). KMS is not supported in our Windows single-node setup, so HDFS encryption zones are not enabled.

## What protects the data instead
- HDFS permissions and ACLs (see `hdfs-permissions-commands.md`)
- MongoDB authentication and role-based access (created by Alizah)

## Limitation
HDFS runs in simple authentication mode, so access is controlled by user name only. In a production deployment, Kerberos and HDFS encryption zones (with KMS) would be used.

This is also listed in the project assumptions (`docs/assumptions.md`).