import { createSign } from "node:crypto";
import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { basename, dirname, isAbsolute, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptsDir = dirname(fileURLToPath(import.meta.url));
const credentialsDir = dirname(scriptsDir);
const envPath = join(credentialsDir, ".env");

export const agentMarker = "<!-- ai-agent-melumuccu:v1 -->";

export async function createInstallationToken() {
	const config = await loadConfig();
	const jwt = await createAppJwt(config);
	const apiUrl = config.apiUrl;
	const response = await fetch(
		`${apiUrl}/app/installations/${config.installationId}/access_tokens`,
		{
			method: "POST",
			headers: {
				accept: "application/vnd.github+json",
				authorization: `Bearer ${jwt}`,
				"content-type": "application/json",
				"x-github-api-version": "2022-11-28"
			}
		}
	);

	if (!response.ok) {
		throw new Error(await formatGitHubError(response));
	}

	return response.json();
}

export async function githubRequest(path, init = {}) {
	const token = await createInstallationToken();
	const config = await loadConfig();
	const response = await fetch(`${config.apiUrl}${path}`, {
		...init,
		headers: {
			accept: "application/vnd.github+json",
			authorization: `Bearer ${token.token}`,
			"content-type": "application/json",
			"x-github-api-version": "2022-11-28",
			...init.headers
		}
	});

	if (!response.ok) {
		throw new Error(await formatGitHubError(response));
	}

	return response.json();
}

export function parseRepository(value) {
	const [owner, repo, extra] = value.split("/");

	if (!owner || !repo || extra) {
		throw new Error("Repository must be OWNER/REPO.");
	}

	return { owner, repo };
}

export async function readMarkedBody(filePath) {
	const body = (await readFile(filePath, "utf8")).trimEnd();

	if (body.includes(agentMarker)) {
		return body;
	}

	return `${agentMarker}\n\n${body}`;
}

export function getOption(args, name) {
	const index = args.indexOf(name);

	if (index === -1) {
		return undefined;
	}

	const value = args[index + 1];

	if (!value || value.startsWith("--")) {
		throw new Error(`${name} requires a value.`);
	}

	args.splice(index, 2);
	return value;
}

async function loadConfig() {
	const env = await loadDotEnv();
	const readEnv = (name) => process.env[name] ?? env[name];
	const clientId =
		readEnv("AI_AGENT_GITHUB_CLIENT_ID") ??
		readEnv("AI_AGENT_GITHUB_APP_ID");
	const installationId =
		readEnv("AI_AGENT_GITHUB_INSTALLATION_ID");
	const privateKeyPath =
		readEnv("AI_AGENT_GITHUB_PRIVATE_KEY_PATH");
	const apiUrl = (readEnv("AI_AGENT_GITHUB_API_URL") ?? "https://api.github.com").replace(
		/\/$/,
		""
	);

	const missing = [
		["AI_AGENT_GITHUB_CLIENT_ID or AI_AGENT_GITHUB_APP_ID", clientId],
		["AI_AGENT_GITHUB_INSTALLATION_ID", installationId],
		["AI_AGENT_GITHUB_PRIVATE_KEY_PATH", privateKeyPath]
	]
		.filter(([, value]) => !value)
		.map(([name]) => name);

	if (missing.length > 0) {
		throw new Error(`Missing required env: ${missing.join(", ")}`);
	}

	const resolvedPrivateKeyPath = resolveCredentialPath(privateKeyPath);

	if (!existsSync(resolvedPrivateKeyPath)) {
		throw new Error(`Private key file not found: ${resolvedPrivateKeyPath}`);
	}

	return {
		apiUrl,
		clientId,
		installationId,
		privateKeyPath: resolvedPrivateKeyPath
	};
}

async function loadDotEnv() {
	if (!existsSync(envPath)) {
		return {};
	}

	const contents = await readFile(envPath, "utf8");
	const env = {};

	for (const line of contents.split(/\r?\n/)) {
		const trimmed = line.trim();

		if (!trimmed || trimmed.startsWith("#")) {
			continue;
		}

		const match = /^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/.exec(trimmed);

		if (!match) {
			continue;
		}

		env[match[1]] = unquoteEnvValue(match[2].trim());
	}

	return env;
}

function unquoteEnvValue(value) {
	if (
		(value.startsWith('"') && value.endsWith('"')) ||
		(value.startsWith("'") && value.endsWith("'"))
	) {
		return value.slice(1, -1);
	}

	return value;
}

function resolveCredentialPath(value) {
	if (isAbsolute(value)) {
		return value;
	}

	const candidates = [
		resolve(process.cwd(), value),
		resolve(credentialsDir, value),
		resolve(credentialsDir, basename(value))
	];

	for (const candidate of candidates) {
		if (existsSync(candidate)) {
			return candidate;
		}
	}

	return candidates[0];
}

async function createAppJwt(config) {
	const privateKey = await readFile(config.privateKeyPath, "utf8");
	const now = Math.floor(Date.now() / 1000);
	const header = base64UrlJson({ alg: "RS256", typ: "JWT" });
	const payload = base64UrlJson({
		iat: now - 60,
		exp: now + 540,
		iss: config.clientId
	});
	const signingInput = `${header}.${payload}`;
	const signer = createSign("RSA-SHA256");
	signer.update(signingInput);
	signer.end();

	return `${signingInput}.${signer.sign(privateKey, "base64url")}`;
}

function base64UrlJson(value) {
	return Buffer.from(JSON.stringify(value)).toString("base64url");
}

async function formatGitHubError(response) {
	const text = await response.text();
	return `GitHub API request failed: ${response.status} ${response.statusText}\n${text}`;
}
