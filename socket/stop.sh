#!/bin/bash

echo "stop scripts..."
ps -ef | grep "python vndirect.py" | grep -v grep | awk '{print $2}' | xargs kill
echo "done"