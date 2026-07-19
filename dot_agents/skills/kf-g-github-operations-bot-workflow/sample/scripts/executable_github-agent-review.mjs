#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import {
	getOption,
	githubRequest,
	parseRepository,
	readMarkedBody
} from "./github-agent-lib.mjs";

const args = process.argv.slice(2);

if (args.includes("--help") || args.includes("-h")) {
	console.log(`Usage:
  node .agents/credentials/github/scripts/github-agent-review.mjs OWNER/REPO PR_NUMBER BODY_FILE [--event COMMENT] [--comments-file comments.json]

Arguments:
  OWNER/REPO       Target repository.
  PR_NUMBER        Pull request number.
  BODY_FILE        Markdown file to post as the review body.

Options:
  --event          COMMENT, APPROVE, or REQUEST_CHANGES. Default: COMMENT.
  --comments-file  JSON array for inline review comments.`);
	process.exit(0);
}

const repoOption = getOption(args, "--repo");
const numberOption = getOption(args, "--number");
const bodyFileOption = getOption(args, "--body-file");
const event = getOption(args, "--event") ?? "COMMENT";
const commentsFile = getOption(args, "--comments-file");
const repoValue = repoOption ?? args.shift();
const numberValue = numberOption ?? args.shift();
const bodyFile = bodyFileOption ?? args.shift();

if (!repoValue || !numberValue || !bodyFile || args.length > 0) {
	throw new Error("Usage: github-agent-review.mjs OWNER/REPO PR_NUMBER BODY_FILE");
}

if (!["COMMENT", "APPROVE", "REQUEST_CHANGES"].includes(event)) {
	throw new Error("--event must be COMMENT, APPROVE, or REQUEST_CHANGES.");
}

const { owner, repo } = parseRepository(repoValue);
const pullNumber = Number.parseInt(numberValue, 10);

if (!Number.isInteger(pullNumber) || pullNumber <= 0) {
	throw new Error("PR_NUMBER must be a positive integer.");
}

const body = await readMarkedBody(bodyFile);
const payload = { body, event };

if (commentsFile) {
	const comments = JSON.parse(await readFile(commentsFile, "utf8"));

	if (!Array.isArray(comments)) {
		throw new Error("--comments-file must contain a JSON array.");
	}

	payload.comments = comments;
}

const review = await githubRequest(`/repos/${owner}/${repo}/pulls/${pullNumber}/reviews`, {
	method: "POST",
	body: JSON.stringify(payload)
});

console.log(review.html_url);
