FROM jjanzic/docker-python3-opencv:latest

# for mediapipe
RUN apt-get -qq update && \
    apt-get -qq install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6

RUN pip3 install mediapipe

# for aiortc
# RUN apt-get -qq install -y --no-install-recommends \
#     libavdevice-dev \
#     libavfilter-dev \
#     libopus-dev \
#     libvpx-dev \
#     pkg-config \
#     libopencv-dev 

# for example app
RUN pip3 install aiortc
RUN pip3 install vidgear[asyncio]

EXPOSE 8080:8080 

COPY ./orion /app/orion

ENV PYTHONPATH "${PYTHONPATH}:/app/orion"

WORKDIR /app

CMD ["-m", "orion.web.server"]

ENTRYPOINT [ "python3" ]