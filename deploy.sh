#!/usr/bin/env bash
git add -f .secrets && eb deploy --staged --profile=eb-prac && git reset HEAD .secrets