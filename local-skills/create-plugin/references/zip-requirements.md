# Component and archive requirements

When adding or editing plugin components, follow the rules below for those
components and the manifest format in use. Parse JSON and YAML as data to catch
syntax errors and wrong types. Use the plugin's chosen creation or update workflow.

When submitting a ZIP or tar.gz, also follow the archive layout below.
Check the final archive after edits, including hidden files and intended components.

## Archive layout

When submitting an archive, include one plugin, either directly at the archive
root or inside one enclosing directory with no unrelated siblings. Exclude
marketplaces and extra wrappers. Write the archive outside the directory being
packaged.
Use the layout in [plugin packages](plugin-packages.md) for new packages:

```text
my-plugin/
  plugin.json
  skills/my-workflow/SKILL.md
  mcp.json
  assets/
```

Include only the component directories and files the plugin uses.

## Manifests and components

A complete plugin needs at least one usable skill, MCP server, or connected app.
Portable ingestion can skip invalid skills or MCP servers. Inspect
returned component diagnostics when present; verify expected skills and
connections after saving, even when the tool succeeds.

| File or field | Rule |
| --- | --- |
| Root `plugin.json` | A UTF-8 JSON object with `$schema` exactly `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`. A root manifest without this declaration is not recognized as this format. |
| `name` | Required string, at most 64 characters. Use lowercase letters, digits, dots, or hyphens; start and end with a letter or digit; avoid `--` and `..`. Prefer kebab-case. Preserve it on updates. |
| `version` | Use strict SemVer for new packages, such as `0.1.0`. Follow the existing version scheme when updating. |
| Optional root metadata | When supplied, `description`, `version`, `homepage`, `repository`, and `license` are strings; `author` is an object; `keywords` is an array of strings. Omit unused fields instead of supplying `null`. |
| OpenAI metadata | Put `interface`, app declarations, and other OpenAI settings inside `extensions.com.openai`, an object. Do not put them at the portable manifest's top level. |
| `interface` text | Supplied `displayName`, `shortDescription`, `longDescription`, `developerName`, and `category` must be nonblank strings. Omit unused portable fields to use their defaults. |
| `interface.capabilities` | An array of nonblank strings, including `[]` when none apply. A string or object is invalid. |
| URLs and colors | Supplied interface URL fields must use absolute HTTPS URLs. Colors use six-digit `#RRGGBB`. |

## Skills and optional agent metadata

Portable skills belong at `skills/<skill-name>/SKILL.md`, one directory below
`skills/`. Hidden directories and deeper nesting do not provide portable skills.
Each file must be UTF-8, no larger than 1 MiB, and start with YAML frontmatter:

```markdown
---
name: my-workflow
description: Use when the user needs this specific workflow.
---

Instructions for the workflow.
```

Use nonblank strings for both fields and unique skill names across the package.
Quote YAML strings containing syntax such as `: ` or `#` when needed.
Keep supporting files and their references inside the plugin.

`agents/openai.yaml` is optional. If present, it must be a UTF-8 YAML object.

| Optional setting | Rule |
| --- | --- |
| `interface` | If supplied as an object, include nonblank `display_name` and `short_description`. Optional `default_prompt` is one nonblank string; `brand_color` uses `#RRGGBB`. Plugin camelCase fields do not substitute for these snake_case fields. |
| `policy.allow_implicit_invocation` | Use a YAML boolean, `true` or `false`, or omit it. `null` is accepted and leaves the default enabled. Strings such as `"false"`, objects, and arrays are invalid. Preserve the user's intended invocation policy. |
| `policy.products` | If supplied, an array using supported values `CHAT`, `CODEX`, and `HERMES`, or `null`. Do not add product restrictions unless requested. |
| Other policy fields | Do not add them. `policy` accepts only `products` and `allow_implicit_invocation`. |
| `dependencies` | If supplied, an object whose only supported field is `tools`. |

## MCP configuration

Portable `mcp.json` needs its own schema declaration and a server-name-to-object map:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "workflow-api": {"type": "streamable-http", "url": "https://mcp.example.com/mcp"}
  }
}
```

Put OpenAI connection options under each server's `extensions.com.openai`:

| Option | Rule |
| --- | --- |
| `auth.type` | One of `none`, `oauth`, `mixed`, or `api_key`. Auth configuration applies only to remote servers. |
| OAuth `auth.client` | An object with `mode` equal to `provided`, `dcr`, or `cimd`. `provided` requires nonblank `clientId`; optional `tokenEndpointAuthMethod` is `none`, `client_secret_post`, `client_secret_basic`, or `private_key_jwt`. `dcr` and `cimd` accept only `mode`. Do not use `useCimd` or place client fields directly under `auth`. |
| OAuth scopes | `baseScopes`, `defaultScopes`, and `oidcScopesSupported` are arrays of nonblank strings. `oidcEnabled` is a boolean. Supplied OAuth endpoint fields must be absolute HTTP(S) URLs without credentials or fragments. |
| API-key auth | `headerScheme` is `bearer`, `basic`, or `custom_header`. `headerName` is required for `custom_header` and omitted otherwise; it must be a valid HTTP header name other than `Host`. Describe credential handling here; do not package credentials. |
| `tunnelId` | Use the verified `tunnel_` ID followed by exactly 32 lowercase letters or digits. It requires a remote server and cannot coexist with `url` or `server_url`. |
| `urlTemplates` | If used, provide a nonempty array of unique HTTPS templates. Each needs a `{name}` placeholder, with unique names beginning with a letter and containing only letters, digits, or underscores. Do not put this option at plugin level. |

Portable servers accept transport fields and `extensions`. Do not put auth,
legacy `server_url`, or arbitrary extra fields directly in the server. Portable
packages use root `mcp.json`; legacy `.mcp.json` alone does not replace it. Preserve
existing compatibility files without assuming the configurations merge.

## App references

For account plugins with an existing app dependency, declare
`extensions.com.openai.apps: "./.app.json"` and include root `.app.json`:

```json
{"apps": {"app-key": {"id": "<verified-app-id>"}}}
```

Copy the actual app ID from discovery. Valid prefixes are `asdk_app_`,
`connector_`, or `templated_apps_`, followed by a letter or digit and then only
letters, digits, `_`, or `-`. A plugin ID, URL, display name, or invented prefix
is not an app ID.
