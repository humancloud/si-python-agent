#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

ARG BASE_PYTHON_IMAGE
ARG BUILDER_PYTHON_IMAGE
FROM ${BASE_PYTHON_IMAGE} AS base

FROM ${BUILDER_PYTHON_IMAGE} AS builder
RUN apt-get update && apt-get install -y make
RUN pip install --upgrade pip
RUN pip install poetry
COPY ./ /tmp/
RUN make -C /tmp package
RUN pip wheel psutil -w /tmp/dist/

FROM ${BASE_PYTHON_IMAGE} AS final
COPY --from=builder /tmp/dist/*.whl /tmp/
RUN pip install --upgrade pip
RUN pip install /tmp/psutil*.whl /tmp/humancloud_stackinsights*.whl
RUN rm /tmp/humancloud_stackinsights*.whl /tmp/psutil*.whl
# So that the agent can be auto-started when the container is started
ENTRYPOINT ["sw-python"]
