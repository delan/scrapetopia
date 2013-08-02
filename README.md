Scrapetopia
===========

Preparation
-----------

Install Python 2.7, pip and a C compiler. Windows users would be far better off
using cygwin, though it may work with native Python and exactly MSVC++ 2008.

If you don't have pip, install it with `easy_install pip`.

Then install dependencies with `pip install -r requirements.txt`.

Finally, run `setup.py` to create the database and other directories.

Fetching lecture metadata
-------------------------

Run `getallmeta.py` to fetch lecture information.

There is no official list of units, and no indication of the highest ID, so by
default it tries 0 to 9999, which appears to be sufficient because the highest
ID that exists within this range is 5151.

Extracting the media file list
------------------------------

Run `getlist.py` to dump all media file URLs from the database.

The list of files will be at `data/list.txt`. Don't try to feed it into a
typical download manager like JDownloader, it won't handle it nicely because
there can be over 100000 files.

Downloading media files
-----------------------

Run `getmedia.py` to download media files.

It supports retrying and continuing partial downloads, so feel free to ^C at any
time. If you restart the downloader, it'll go through and ping all of the files
to make sure they exist and are the right size.

Files that are definitely done will automatically go into `data/done.txt`, and
you can remove these from the main list by running `scalpel.sh`. Running this is
optional but makes restarts faster because the list is shortened.

Backing up media files
----------------------

You can run `backup.py` with the main and backup directories supplied as
arguments to copy the media files to another location. The need to copy a
particular file is determined by a quick check of file sizes, as matching file
contents exactly would be very slow.

Hosting the web-based browser
-----------------------------

Run `web.py` to start the application.

Install nginx and use the provided `nginx.conf`, changing the `alias` path on
line 15 to point to the `data/media` directory.

Start nginx and the interface will be available on port 8653.
