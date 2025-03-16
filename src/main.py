#! /usr/bin/env python
import subprocess

# Play the movie in full screen (volume of 20 seems to match text to speech volume of 10)
subprocess.call(["mpv", "--fs", "--loop=inf", "/home/pi/io_badge/img/test_optimized.mp4"])