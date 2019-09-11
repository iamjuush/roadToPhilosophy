#!/usr/bin/env bash

faas-cli build -f stack.dev.yml && faas-cli deploy -f stack.dev.yml
