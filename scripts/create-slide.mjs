import { mkdirSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const name = process.argv[2];

if (!name) {
  console.error("Error: スライド名を指定してください。\n  例: pnpm new-slide my-talk");
  process.exit(1);
}

const slideDir = join("packages", "slides", name);

if (existsSync(slideDir)) {
  console.error(`Error: ${slideDir} は既に存在します。`);
  process.exit(1);
}

mkdirSync(slideDir, { recursive: true });

const packageJson = {
  name: `@slides/${name}`,
  type: "module",
  private: true,
  scripts: {
    dev: "slidev",
    build: "slidev build",
    export: "slidev export",
  },
  dependencies: {
    "@slidev/cli": "^52.1.0",
    "@slidev/theme-default": "latest",
    "@slidev/theme-seriph": "latest",
  },
};

writeFileSync(
  join(slideDir, "package.json"),
  JSON.stringify(packageJson, null, 2) + "\n",
);

const slidesContent = `---
title: ${name}
mdc: true
drawings:
  persist: false
transition: slide-left
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

# タイトル

---

# ページ2
`;

writeFileSync(join(slideDir, "slides.md"), slidesContent);

console.log(`\n${slideDir} を作成しました!\n`);
console.log("次のステップ:");
console.log(`  cd ${slideDir} && pnpm install && pnpm dev\n`);
