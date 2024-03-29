.. MediaGoblin Documentation

   Written in 2011, 2012, 2014, 2015 by MediaGoblin contributors

   To the extent possible under law, the author(s) have dedicated all
   copyright and related and neighboring rights to this software to
   the public domain worldwide. This software is distributed without
   any warranty.

   You should have received a copy of the CC0 Public Domain
   Dedication along with this software. If not, see
   <http://creativecommons.org/publicdomain/zero/1.0/>.

.. _media-types-chapter:

====================
Media Types
====================

In the future, there will be all sorts of media types you can enable,
but in the meanwhile there are six additional media types: video, audio,
raw image, ASCII art, STL/3D models, PDF and Document.

First, you should probably read ":doc:`configuration`" to make sure
you know how to modify the MediaGoblin config file.

Enabling Media Types
====================

.. note::
    Media types are now plugins

Media types are enabled in your MediaGoblin configuration file.

Most media types require **additional dependencies** that you will have to install. You
will find descriptions on how to satisfy the requirements of each media type
below.

To enable a media type, add the the media type under the ``[plugins]`` section
in you ``mediagoblin.ini``. For example, if your system supported image
and video media types, then it would look like this::

    [plugins]
    [[mediagoblin.media_types.image]]
    [[mediagoblin.media_types.video]]

Note that after enabling new media types, you must run dbupdate. If you have
deployed MediaGoblin as an unprivileged user as described in
":doc:`production-deployments`", you'll first need to switch to this account::

    sudo su mediagoblin --shell=/bin/bash
    $ cd /srv/mediagoblin.example.org/mediagoblin

Now run dbupdate::

    $ ./bin/gmg dbupdate

If you are running an active site, depending on your server
configuration, you may need to stop it first (and it's certainly a
good idea to restart it after the update).


How does MediaGoblin decide which media type to use for a file?
===============================================================

MediaGoblin has two methods for finding the right media type for an uploaded
file. One is based on the file extension of the uploaded file; every media type
maintains a list of supported file extensions. The second is based on a sniffing
handler, where every media type may inspect the uploaded file and tell if it
will accept it.

The file-extension-based approach is used before the sniffing-based approach,
if the file-extension-based approach finds a match, the sniffing-based approach
will be skipped as it uses far more processing power.

Configuring Media Types
=======================

Each media type has a ``config_spec.ini`` file with configurable
options and comments explaining their intended side effect. For
instance the ``video`` media type configuration can be found in
``mediagoblin/media_types/video/config_spec.ini``.


Audio
=====

To enable audio, install the GStreamer and python-gstreamer bindings (as well
as whatever GStreamer plugins you want, good/bad/ugly):

.. code-block:: bash

    # Debian and co.
    sudo apt install python3-gst-1.0 gstreamer1.0-plugins-{base,bad,good,ugly} \
    gstreamer1.0-libav

    # Fedora and co.
    sudo dnf install gstreamer1-plugins-{base,bad-free,good,ugly-free}

.. note::

   MediaGoblin previously generated spectrograms for uploaded audio. This
   feature has been removed due to incompatibility with Python 3. We may
   consider re-adding this feature in the future.

Add ``[[mediagoblin.media_types.audio]]`` under the ``[plugins]`` section in your
``mediagoblin.ini`` and update MediaGoblin::

    $ ./bin/gmg dbupdate

Restart MediaGoblin (and Celery if applicable). You should now be able to upload
and listen to audio files!


Video
=====

To enable video, first install GStreamer and the python-gstreamer
bindings (as well as whatever GStreamer extensions you want,
good/bad/ugly):

.. code-block:: bash

    # Debian and co.
    sudo apt install python3-gi gstreamer1.0-tools gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-{good,bad,ugly} \
    gstreamer1.0-libav python3-gst-1.0

.. note::

   We unfortunately do not have working installation instructions for Fedora and
   co. Some incomplete information is available on the `Hacking Howto wiki page <http://wiki.mediagoblin.org/HackingHowto#Fedora_.2F_RedHat.28.3F.29_.2F_CentOS>`_
    
Add ``[[mediagoblin.media_types.video]]`` under the ``[plugins]`` section in
your ``mediagoblin.ini`` and restart MediaGoblin.

Run::

    $ ./bin/gmg dbupdate

Restart MediaGoblin (and Celery if applicable). Now you should be able to submit
videos, and MediaGoblin should transcode them.

.. note::

   You will likely need to increase the ``client_max_body_size`` setting in
   Nginx to upload larger videos.
   
   You almost certainly want to separate Celery from the normal
   paste process or your users will probably find that their connections
   time out as the video transcodes.  To set that up, check out the
   ":doc:`production-deployments`" section of this manual.


Raw image
=========

To enable raw image you need to install pyexiv2::

    # Debian and co.
    sudo apt install python3-pyexiv2

Add ``[[mediagoblin.media_types.raw_image]]`` under the ``[plugins]``
section in your ``mediagoblin.ini`` and restart MediaGoblin.

Run::

    $ ./bin/gmg dbupdate

Restart MediaGoblin (and Celery if applicable). Now you should be able to submit
raw images, and MediaGoblin should extract the JPEG preview from them.


ASCII art
=========

To enable ASCII art support, first install the
`chardet <http://pypi.python.org/pypi/chardet>`_
library, which is necessary for creating thumbnails of ASCII art::

    $ ./bin/easy_install chardet


Next, modify your ``mediagoblin.ini``.  In the ``[plugins]`` section, add
``[[mediagoblin.media_types.ascii]]``.

Run::

    $ ./bin/gmg dbupdate

Restart MediaGoblin (and Celery if applicable). Now any .txt file you uploaded
will be processed as ASCII art!


STL / 3D model support
======================

To enable the "STL" 3D model support plugin, first make sure you have
a recent `Blender <http://blender.org>`_ installed and available on
your execution path.  This feature has been tested with Blender 2.63.
It may work on some earlier versions, but that is not guaranteed (and
is surely not to work prior to Blender 2.5X).

Add ``[[mediagoblin.media_types.stl]]`` under the ``[plugins]`` section in your
``mediagoblin.ini`` and restart MediaGoblin.

Run::

    $ ./bin/gmg dbupdate

Restart MediaGoblin (and Celery if applicable). You should now be able to upload
.obj and .stl files and MediaGoblin will be able to present them to your wide
audience of admirers!


PDF and Document
================

To enable the "PDF and Document" support plugin, you need:

1. pdftocairo and pdfinfo for PDF only support.

2. unoconv with headless support to support converting LibreOffice supported
   documents as well, such as doc/ppt/xls/odf/odg/odp and more.
   For the full list see mediagoblin/media_types/pdf/processing.py,
   unoconv_supported.

All executables must be on your execution path.

To install this on Fedora::

    sudo dnf install poppler-utils unoconv libreoffice-headless

Note: You can leave out unoconv and libreoffice-headless if you want only PDF
support. This will result in a much smaller list of dependencies.

pdf.js relies on git submodules, so be sure you have fetched them::

    $ git submodule init
    $ git submodule update

This feature has been tested on Fedora with:
 poppler-utils-0.20.2-9.fc18.x86_64
 unoconv-0.5-2.fc18.noarch
 libreoffice-headless-3.6.5.2-8.fc18.x86_64

It may work on some earlier versions, but that is not guaranteed.

Add ``[[mediagoblin.media_types.pdf]]`` under the ``[plugins]`` section in your
``mediagoblin.ini`` and restart MediaGoblin.

Run::

    $ ./bin/gmg dbupdate


Blog (HIGHLY EXPERIMENTAL)
==========================

MediaGoblin has a blog media type, which you might notice by looking
through the docs!  However, it is *highly experimental*.  We have not
security reviewed this, and it acts in a way that is not like normal
blogs (the blog posts are themselves media types!).

So you can play with this, but it is not necessarily recommended yet
for production use! :)
