import { defineShikiSetup } from '@slidev/types';

/*
 * コードブロックの配色。
 * このデッキはライトモードで映すが、コードブロックだけは暗い地に置くので、
 * light / dark どちらにも暗いテーマ (vitesse-dark) を指定して固定する。
 * 地の色は style.css で --shiki-dark-bg (= #121212) を参照している。
 */
export default defineShikiSetup(() => {
  return {
    themes: {
      dark: 'vitesse-dark',
      light: 'vitesse-dark',
    },
  };
});
