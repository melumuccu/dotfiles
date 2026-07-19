#!/usr/bin/env node

import { createInstallationToken } from "./github-agent-lib.mjs";

const args = process.argv.slice(2);

if (args.includes("--help") || args.includes("-h")) {
	console.log(`Usage:
  node .agents/credentials/github/scripts/github-agent-token.mjs [--json]

Options:
  --json  Print the full GitHub installation token response.`);
	process.exit(0);
}

const token = await createInstallationToken();

if (args.includes("--json")) {
	console.log(JSON.stringify(token, null, 2));
} else {
	console.log(token.token);
}
