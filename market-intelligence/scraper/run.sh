#!/usr/bin/env bash
# Quick launcher for Houston Business Scraper CLI
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$DIR:$PYTHONPATH"
exec python3 -m houston_biz "$@"
