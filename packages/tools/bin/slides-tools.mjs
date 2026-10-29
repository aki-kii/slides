#!/usr/bin/env node
// TypeScript のまま動かすため、tsx を読み込んでから CLI 本体を呼ぶ
import { register } from 'tsx/esm/api';

register();
await import('../src/cli.ts');
