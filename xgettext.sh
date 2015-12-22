#!/bin/bash

find . -iname "*.py" | xargs xgettext --from-code=UTF-8 --default-domain=Macsen

