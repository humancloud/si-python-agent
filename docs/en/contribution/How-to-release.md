# Apache StackInsights Python Release Guide

This documentation guides the release manager to release the StackInsights Python in the Apache Way, and also helps people to check the release for vote.

## Prerequisites

1. Close (if finished, or move to next milestone otherwise) all issues in the current milestone from [stackinsights-python](https://github.com/apache/stackinsights-python/milestones) and [stackinsights](https://github.com/apache/stackinsights/milestones), create a new milestone if needed.
2. Update CHANGELOG.md and `version` in `pyproject.toml`.

## Add your GPG public key to Apache SVN

1. Log in [id.apache.org](https://id.apache.org/) and submit your key fingerprint.

2. Add your GPG public key into [StackInsights GPG KEYS](https://dist.apache.org/repos/dist/release/stackinsights/KEYS) file, **you can do this only if you are a PMC member**.  You can ask a PMC member for help. **DO NOT override the existed `KEYS` file content, only append your key at the end of the file.**


## Build and sign the source code package

```shell
export VERSION=<the version to release>

git clone --recurse-submodules git@github.com:apache/stackinsights-python && cd stackinsights-python
git tag -a "v$VERSION" -m "Release Apache StackInsights-Python $VERSION"
git push --tags

make clean && make release
```

## Upload to Apache SVN

```bash
svn co https://dist.apache.org/repos/dist/dev/stackinsights/python release/stackinsights/python
mkdir -p release/stackinsights/python/"$VERSION"
cp stackinsights*.tgz release/stackinsights/python/"$VERSION"
cp stackinsights*.tgz.asc release/stackinsights/python/"$VERSION"
cp stackinsights-python*.tgz.sha512 release/stackinsights/python/"$VERSION"

cd release/stackinsights && svn add python/$VERSION && svn commit python -m "Draft Apache StackInsights-Python release $VERSION"
```

## Make the internal announcement

First, generate a sha512sum for the source code package generated in last step:

```bash
sha512sum release/stackinsights/python/"$VERSION"/stackinsights-python-src-"$VERSION".tgz
``` 

Send an announcement email to dev@ mailing list, **please check all links before sending the email**, the same as below.

```text
Subject: [ANNOUNCEMENT] Apache StackInsights Python $VERSION test build available

Content:

The test build of Apache StackInsights Python $VERSION is now available.

We welcome any comments you may have, and will take all feedback into
account if a quality vote is called for this build.

Release notes:

 * https://github.com/apache/stackinsights-python/blob/v$VERSION/CHANGELOG.md

Release Candidate:

 * https://dist.apache.org/repos/dist/dev/stackinsights/python/$VERSION
 * sha512 checksums
   - sha512xxxxyyyzzz stackinsights-python-src-x.x.x.tgz

Release Tag :

 * (Git Tag) v$VERSION

Release Commit Hash :

 * https://github.com/apache/stackinsights-python/tree/<Git Commit Hash>

Keys to verify the Release Candidate :

 * http://pgp.mit.edu:11371/pks/lookup?op=get&search=0x8BD99F552D9F33D7 corresponding to kezhenxu94@apache.org

Guide to build the release from source :

 * https://github.com/apache/stackinsights-python/blob/master/CONTRIBUTING.md#compiling-and-building

A vote regarding the quality of this test build will be initiated
within the next couple of days.
```

## Wait at least 48 hours for test responses

Any PMC, committer or contributor can test features for releasing, and feedback.
Based on that, PMC will decide whether to start a vote or not.

## Call for vote in dev@ mailing list

Call for vote in `dev@stackinsights.apache.org`.

```text
Subject: [VOTE] Release Apache StackInsights Python version $VERSION

Content:

Hi the StackInsights Community:
This is a call for vote to release Apache StackInsights Python version $VERSION.

Release notes:

 * https://github.com/apache/stackinsights-python/blob/v$VERSION/CHANGELOG.md

Release Candidate:

 * https://dist.apache.org/repos/dist/dev/stackinsights/python/$VERSION
 * sha512 checksums
   - sha512xxxxyyyzzz stackinsights-python-src-x.x.x.tgz

Release Tag :

 * (Git Tag) v$VERSION

Release Commit Hash :

 * https://github.com/apache/stackinsights-python/tree/<Git Commit Hash>

Keys to verify the Release Candidate :

 * https://dist.apache.org/repos/dist/release/stackinsights/KEYS

Guide to build the release from source :

 * https://github.com/apache/stackinsights-python/blob/master/CONTRIBUTING.md#compiling-and-building

Voting will start now and will remain open for at least 72 hours, all PMC members are required to give their votes.

[ ] +1 Release this package.
[ ] +0 No opinion.
[ ] -1 Do not release this package because....

Thanks.

[1] https://github.com/apache/stackinsights/blob/master/docs/en/guides/How-to-release.md#vote-check
```

## Vote Check

All PMC members and committers should check these before voting +1:

1. Features test.
1. All artifacts in staging repository are published with `.asc`, `.md5`, and `sha` files.
1. Source codes and distribution packages (`stackinsights-python-src-$VERSION.tgz`)
are in `https://dist.apache.org/repos/dist/dev/stackinsights/python/$VERSION` with `.asc`, `.sha512`.
1. `LICENSE` and `NOTICE` are in source codes and distribution package.
1. Check `shasum -c stackinsights-python-src-$VERSION.tgz.sha512`.
1. Check `gpg --verify stackinsights-python-src-$VERSION.tgz.asc stackinsights-python-src-$VERSION.tgz`.
1. Build distribution from source code package by following this [the build guide](#build-and-sign-the-source-code-package).
1. Licenses check, `make license`.

Vote result should follow these:

1. PMC vote is +1 binding, all others is +1 no binding.

1. Within 72 hours, you get at least 3 (+1 binding), and have more +1 than -1. Vote pass. 

1. **Send the closing vote mail to announce the result**.  When count the binding and no binding votes, please list the names of voters. An example like this:

   ```
   [RESULT][VOTE] Release Apache StackInsights Python version $VERSION
   
   72+ hours passed, we’ve got ($NUMBER) +1 bindings (and ... +1 non-bindings):
   
   (list names)
   +1 bindings:
   xxx
   ...
   
   +1 non-bindings:
   xxx
   ...
    
   Thank you for voting, I’ll continue the release process.
   ```

## Publish release

1. Move source codes tar balls and distributions to `https://dist.apache.org/repos/dist/release/stackinsights/`, **you can do this only if you are a PMC member**.

    ```shell
    svn mv https://dist.apache.org/repos/dist/dev/stackinsights/python/"$VERSION" https://dist.apache.org/repos/dist/release/stackinsights/python/"$VERSION"
    ```
    
2. Refer to the previous [PR](https://github.com/apache/stackinsights-website/pull/571), update news and links on the website. There are several files need to modify.


### Publish PyPI package

After the official ASF release, we publish the packaged wheel to the PyPI index.

1. Make sure the final upload is correct by using the test PyPI index `make upload-test`.
2. Upload the final artifacts by running `make upload`.

### Publish Docker images

After the release on GitHub, a GitHub Action will be triggered to build Docker images based on the latest code.

**Important** We announce the new release by drafting one on [Github release page](https://github.com/apache/stackinsights-python/releases), following the previous convention.

An automation via GitHub Actions will automatically trigger upon the mentioned release event to build and upload Docker images to DockerHub.

See [How-to-release-docker](./How-to-release-docker.md) for a detailed description of manual release.

4. Send ANNOUNCEMENT email to `dev@stackinsights.apache.org` and `announce@apache.org`, the sender should use his/her Apache email account. 

    ```
    Subject: [ANNOUNCEMENT] Apache StackInsights Python $VERSION Released

    Content:

    Hi the StackInsights Community

    On behalf of the StackInsights Team, I’m glad to announce that StackInsights Python $VERSION is now released.

    StackInsights Python: The Python Agent for Apache StackInsights provides the native tracing/metrics/logging/profiling abilities for Python projects.

    StackInsights: APM (application performance monitor) tool for distributed systems, especially designed for microservices, cloud native and container-based (Docker, Kubernetes, Mesos) architectures.

    Download Links: http://stackinsights.apache.org/downloads/

    Release Notes : https://github.com/apache/stackinsights-python/blob/v$VERSION/CHANGELOG.md

    Website: http://stackinsights.apache.org/
    
    StackInsights Python Resources:
    - Issue: https://github.com/apache/stackinsights/issues
        - Mailing list: dev@stackinsights.apache.org
        - Documents: https://github.com/apache/stackinsights-python/blob/v$VERSION/README.md
    
    The Apache StackInsights Team
    ```
