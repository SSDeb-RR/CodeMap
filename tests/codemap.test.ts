import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

const cli = path.resolve("scripts/codemap.ts");

function fixture() {
  const root = mkdtempSync(path.join(tmpdir(), "codemap-test-"));
  mkdirSync(path.join(root, "src"));
  writeFileSync(path.join(root, "package.json"), '{"name":"fixture"}\n');
  writeFileSync(path.join(root, "src", "a.ts"), 'export { value } from "./b";\n');
  writeFileSync(path.join(root, "src", "b.ts"), 'export const value = import("./c");\n');
  writeFileSync(path.join(root, "src", "c.ts"), 'const other = require("missing-package");\n');
  writeFileSync(path.join(root, "src", "pkg.py"), 'from .util import helper\n');
  writeFileSync(path.join(root, "src", "util.py"), 'from .missing import helper\n');
  return root;
}

test("mixed repositories produce deterministic validated output", () => {
  const root = fixture();
  const one = path.join(root, "one");
  const two = path.join(root, "two");
  execFileSync("node", [cli, root, "--out", one]);
  execFileSync("node", [cli, root, "--out", two]);
  const first = JSON.parse(readFileSync(path.join(one, "graph.json"), "utf8"));
  const second = JSON.parse(readFileSync(path.join(two, "graph.json"), "utf8"));
  assert.equal(first.schemaVersion, 5);
  assert.deepEqual(first.files, second.files);
  assert.deepEqual(first.edges, second.edges);
  assert.ok(first.files.some((file: { language: string }) => file.language === "python"));
  assert.ok(first.edges.some((edge: { source: string; target: string }) => edge.source.endsWith("a.ts") && edge.target.endsWith("b.ts")));
  assert.ok(first.coverage.imports.unresolved.some((item: { language: string }) => item.language === "python"));
  assert.match(readFileSync(path.join(one, "index.html"), "utf8"), /CodeMap/);
});

test("unsupported-only repositories fail clearly", () => {
  const root = mkdtempSync(path.join(tmpdir(), "codemap-unsupported-"));
  writeFileSync(path.join(root, "main.go"), "package main\n");
  assert.throws(() => execFileSync("node", [cli, root], { stdio: "pipe" }), /No supported source files/);
});
