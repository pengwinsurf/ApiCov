#!/bin/bash
git tag -f "$1"
git push origin "$1" --force
