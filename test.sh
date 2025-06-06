#!/bin/bash

sed -i '' "/param channelname=/c\\
param channelname=default
" .input.in
