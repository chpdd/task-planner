FROM fluent/fluentd:v1.16.3-1.0

USER root
RUN gem install elasticsearch --no-document --version 8.19.0

RUN gem install fluent-plugin-elasticsearch --no-document --version 6.0.0
RUN gem install fluent-plugin-multi-format-parser --no-document
RUN gem install fluent-plugin-concat --no-document
USER fluent