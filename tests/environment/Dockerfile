FROM ubuntu:16.04

#We need to force docker to choose the "Y" option to install dependencies of packages
RUN echo "APT::Get::Assume-Yes "true";" >> /etc/apt/apt.conf.d/99allow
RUN echo "APT::Get::allow "true";" >> /etc/apt/apt.conf.d/99allow

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# make sure the package repository is up to date
RUN apt-get -qq update

# These two packages are necessary to run mk-build-deps
RUN apt-get install -y devscripts equivs dpkg-dev

# Make wkhtml control file visible to docker and install dependencies according to it.
ADD ./control /
RUN mk-build-deps --install /control

# Install more dependencies needed to run tests.
RUN apt-get install -y \
python3-nose \
poppler-utils \
imagemagick \
ttf-unifont \
ttf-liberation

# Make visible apt.conf file to docker for the accurate proxy preferences
ADD apt.conf /etc/apt/apt.conf
