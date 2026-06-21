#!/usr/bin/env bash
set -euo pipefail

from_ref="${PRE_COMMIT_FROM_REF:-}"
to_ref="${PRE_COMMIT_TO_REF:-HEAD}"
zero_ref="0000000000000000000000000000000000000000"

if [[ -z "${from_ref}" || -z "${to_ref}" ]]; then
  exec mise exec -- gitleaks git --redact --verbose .
fi

if [[ "${from_ref}" == "${zero_ref}" ]]; then
  log_opts="--all ${to_ref}"
else
  log_opts="--all ${from_ref}..${to_ref}"
fi

exec mise exec -- gitleaks git --redact --verbose --log-opts="${log_opts}" .
