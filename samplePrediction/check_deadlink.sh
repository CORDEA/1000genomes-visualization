#!/bin/sh
/usr/bin/find $dir -name '*.html' -mtime +1 -exec /usr/bin/rm {} \;
