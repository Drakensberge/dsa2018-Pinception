# Deep learning on a Raspberry Pi

This repo contains the code and notes on running Inception net on a Raspberry Pi 3B. You also need a Raspberry PI motion sensor and a camera.

It was used to deploy a camera trap in the Dedan Kimathi University Nature Reserve at Data Science Africa 2018 in Nyeri, Kenya. Many Thanks to Ciira Maina for hosting us and for his hard work here!

Also Jan Jongboom and Gen-Tao Chiang provided invaluable hardware and software support.

## 1: Setup

This work is base on this tutorial:
[Wine detector on MXnet](https://mxnet.incubator.apache.org/versions/master/tutorials/embedded/wine_detector.html
). That's pretty cool but wine is far less exciting than detecting wildlife.

### Raspbian

First you need Raspbian. We use Stretch-lite because we want to save space: 
[Instructions](https://www.raspberrypi.org/documentation/installation/installing-images/
). BE CAREFUL HERE - if you mess up you can wipe your hard drive.

You need to be able to issue commands to the Pi. You're kinda on your own here. It depends on the hardware you have available (Ideally a power supply, ethernet internet and an HDMI screen and USB keyboard). [This](http://blog.cudmore.io/post/2017/11/22/raspian-stretch/) might work for you. 

### Camera module
You'll need one of [these](https://www.raspberrypi.org/products/camera-module-v2/).

Installing it is [easy](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera).

### OpenCV
Installing this sucks. It take ages to download on a shaky internet line and even longer ages to compile, and even then it will probably fail a few times, and run out of memory.

[This guide](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) *mostly* works.

**Notes:**

* Expanding the file system is a good idea, but cloning the image afterwards seems awkward. Beware if you need to duplicate this.
* Those time estimates are super optimistic - they assume you have very fast internet
* You can skip the virtualenv stuff (but it will come back to bite you if you have version issues between numpy, openCV and MXnet)
* You don't need the contrib stuff
* That Cmake command didn't work for me. Use `cmake -DENABLE_PRECOMPILED_HEADERS=OFF ` as suggested [here](https://github.com/opencv/opencv/issues/6517)
* Make EXTRA SURE of the numpy version in the output of cmake
* That swap size hint is SUPER IMPORTANT -DO IT.
* Once you're done, CHANGE IT BACK TO `CONF_SWAPSIZE=100`
* You can try `make -j4`, but keep an eye on memory while you kill 2-4 hours. 

### MXnet

This part really sucks. Here is the [guide](https://mxnet.incubator.apache.org/install/index.html)

**Notes**

* DO NOT USE THE LATEST VERSION - IT DOES NOT WORK WITH PRETRAINED MODELS AND NOONE SEEMS TO CARE
* The older version does work `git clone --recursive https://github.com/apache/incubator-mxnet.gitmxnet --branch 1.0.0` 
* Do the swap thing, remember to put it back after
* BE VERY CAREFUL WITH THE BINDINGS FOR PYTHON. If you used virtualenv, make sure you pip install in the correct environment. Failure here will ruin your day.


## 2: Fixup

You are now ready to go back to the main [guide](https://mxnet.incubator.apache.org/versions/master/tutorials/embedded/wine_detector.html).

Unfortunately, there are many typos.

Use the code in this repo instead of theirs, which is broken. Do they even test this stuff? I mean they forgot to `import time`, seriously?

The code in this repo is ugly, and needs love, but has been tested and it should work. You should clone it, download it or scp it onto your Pi.

Before you get there, you will have to change `Inception_BN-0039.params` to whatever the new number is. 

Also make a copy of the `Inception_BN-0039.params` replacing the underscore with a dash.

Also make a copy of the `Inception_BN-0039.symbols` replacing the underscore with a dash.

## 3: Startup

If you made it this far (I only did because it was late and I had a deadline and 50 students I couldn't disappoint), you rock.

everything should now work. You just need to 
`mkdir pictures`
and 
`mkdir predictions` and then run `python run_models.py`

It's best to run it with `screen` so that it runs in the background. 
 
It helps if your motion sensor and camera are pointed at the same thing :)

## Parting thoughts

This is really version 0. It's just the barebones to get started. There are a LOT of things that can be done to improve this shaky first attempt:

* Transfer learning: retrain the network on the classes you care about
* Pre-process images: the camera is super wide angle, this biases the prediction toward scenes rather than particular objects. Just crop out the middle of the image
* Two motion sensors: fewer false positives by only predicting when both trigger
* Better models (like YOLO for example)
* Remove dependency on OpenCV and MXNet - both are a total pain to install on a Pi.
* Your ideas!