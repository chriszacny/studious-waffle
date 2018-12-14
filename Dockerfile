FROM python:3.7-alpine3.8
LABEL maintainer="zacny"
COPY requirements.txt /requirements.txt
RUN apk update
RUN apk add gcc linux-headers musl-dev libffi-dev openssl-dev make
RUN pip install -r requirements.txt
COPY f5_version_num_gt_eq.py /
RUN mkdir -p /test/units/modules
COPY test/units/modules/test_f5_version_num_gt_eq.py /test/units/modules/
COPY testmod.yml /
COPY args.json /
RUN mkdir -p /root/.ansible/plugins/modules
COPY f5_version_num_gt_eq.py /root/.ansible/plugins/modules
ENV PYTHONPATH="${PYTHONPATH}:/"
ENTRYPOINT ["/bin/sh"]
