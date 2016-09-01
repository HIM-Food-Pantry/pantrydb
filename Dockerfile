FROM python:3.6-alpine

ENV INSTALL_PATH=/django/ \
    DJANGO_SETTINGS_MODULE=him_database.settings.production \
    # Secret Key and Database env var's used here for collect static command, replace this varpiable in prod
    SECRET_KEY="u8!7cbl_=e-2o=&513r^*nj)b+yqkd^tb2w^e1b3h93a)h14tv" \
    # syntax: DATABASE_URL=postgres://username:password@127.0.0.1:5432/database
    DATABASE_URL="postgres://postgres:postgrest@postgrest:5432/postgress" \
    LOG_DIR=/him_db/logs \
    ALLOWED_HOSTS='*'

RUN mkdir $INSTALL_PATH /deploy

WORKDIR $INSTALL_PATH

COPY ./requirements/ $INSTALL_PATH/requirements/

RUN apk add --no-cache --virtual .build-deps \
  build-base postgresql-dev libffi-dev \
    && pip3 install -r $INSTALL_PATH/requirements/production.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

COPY ./src $INSTALL_PATH

COPY ./deploy /deploy

COPY ./deploy/vhost.d /etc/nginx/vhost.d

RUN python3 manage.py collectstatic --no-input

EXPOSE 8000

VOLUME ["/deploy", "/django/staticfiles", "/etc/nginx/vhost.d"]

ENTRYPOINT ["/usr/local/bin/python3", "-u", "manage.py"]

CMD ["runserver"]

# CMD ["/usr/local/bin/waitress-serve", "--port=8000" , "him_database.wsgi:application"]