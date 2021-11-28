#!/bin/bash

voice2json -p /home/pi/.local/share/voice2json/en-us_kaldi-zamia/ transcribe-stream --exit-count 1 | voice2json -p /home/pi/.local/share/voice2json/en-us_kaldi-zamia/ recognize-intent | \
  while read -r intent_json;
  do
    intent_name="$(echo "${intent_json}" | jq -r .intent.name)"
    echo "Command: "${intent_name}""
  done
