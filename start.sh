#!/bin/bash
daphne -b 0.0.0.0 -p ${PORT:-8000} nitkigali.asgi:application