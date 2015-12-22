#!/bin/bash
find . -path ./client/modules -prune -o -iname "*.py" -print | xargs xgettext --from-code=UTF-8 --default-domain=Macsen

