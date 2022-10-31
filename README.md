================================PREREQUISITES===============================
Ensure that the file at /boot/config.txt contains these three lines:
              dtoverlay=hifiberry-dac
              gpio=25=op,dh
              dtparam=audio=off

 You need to install software and libraries as follows:
              sudo apt-get update
      sudo apt-get upgrade
      sudo reboot

      # optionally install netdata to see how pressed your CPU will be
      # sudo apt-get install netdata && \
          sudo sed -i '/bind socket/d' /etc/netdata/netdata.conf && \
          sudo systemctl restart netdata
      # netdata now accessible via http://<rpi-ip>:19999

              sudo apt-get install -y python3-rpi.gpio python3-spidev python3-pip python3-pil python3-numpy mpg123
      pip install -r requirements.txt 
      sudo cargo install librespot

      # download latest spotifyd armv6 release
      # TODO: Automate finding latest version
      curl -O https://github.com/Spotifyd/spotifyd/releases/download/v0.3.3/spotifyd-linux-armv6-slim.tar.gz && \
      tar xf spotifyd-linux-armv6-slim.tar.gz

 The code below also assumes that you have
      - a font file at /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf

=========================END OF PREREQUISITES===============================
