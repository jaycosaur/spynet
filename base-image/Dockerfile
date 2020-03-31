FROM balenalib/raspberrypi4-64-python:3.7.6

RUN apt-get update && apt-get install -y --no-install-recommends

RUN apt-get install -y build-essential cmake unzip pkg-config

RUN apt-get install -y libjpeg-dev libpng-dev libtiff-dev

RUN apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

RUN apt-get install -y libxvidcore-dev libx264-dev

RUN apt-get install -y libgtk-3-dev libcanberra-gtk*

RUN apt-get install -y libatlas-base-dev gfortran python3-dev

RUN apt-get install -y wget

RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip

RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip

RUN unzip opencv.zip && unzip opencv_contrib.zip
RUN mv opencv-4.0.0 opencv 
RUN mv opencv_contrib-4.0.0 opencv_contrib

RUN python3 -m pip install numpy
RUN cd opencv && mkdir build && cd build

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

RUN make -j4

RUN make install

RUN ldconfig

