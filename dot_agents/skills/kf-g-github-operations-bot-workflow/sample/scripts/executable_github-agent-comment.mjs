#!/usr/bin/env node

import {
	getOption,
	githubRequest,
	parseRepository,
	readMarkedBody
} from "./github-agent-lib.mjs";

const args = process.argv.slice(2);

if (args.includes("--help") || args.includes("-h")) {
	console.log(`Usage:
  node .agents/credentials/github/scripts/github-agent-comment.mjs OWNER/REPO ISSUE_OR_PR_NUMBER BODY_FILE

Arguments:
  OWNER/REPO           Target repository.
  ISSUE_OR_PR_NUMBER  Issue or PR number.
  BODY_FILE           Markdown file to post as the comment body.`);
	process.exit(0);
}

const repoOption = getOption(args, "--repo");
const numberOption = getOption(args, "--number");
const bodyFileOption = getOption(args, "--body-file");
const repoValue = repoOption ?? args.shift();
const numberValue = numberOption ?? args.shift();
const bodyFile = bodyFileOption ?? args.shift();

if (!repoValue || !numberValue || !bodyFile || args.length > 0) {
	throw new Error("Usage: github-agent-comment.mjs OWNER/REPO ISSUE_OR_PR_NUMBER BODY_FILE");
}

const { owner, repo } = parseRepository(repoValue);
const issueNumber = Number.parseInt(numberValue, 10);

if (!Number.isInteger(issueNumber) || issueNumber <= 0) {
	throw new Error("ISSUE_OR_PR_NUMBER must be a positive integer.");
}

const body = await readMarkedBody(bodyFile);
const comment = await githubRequest(`/repos/${owner}/${repo}/issues/${issueNumber}/comments`, {
	method: "POST",
	body: JSON.stringify({ body })
});

console.log(comment.html_url);
