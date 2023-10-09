FROM registry.access.redhat.com/ubi8/python-39

USER 0
ADD python .
RUN chown -R 1001:0 ./
USER 1001

RUN pip install -U "ml-metadata==1.14.0"

CMD tail -f /dev/null
