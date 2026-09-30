/**
 * 吹き出し (ChatMessage) のセリフの組み立て。
 *
 * texts を渡されたときはクリックごとにセリフを差し替え、`...` で囲んだところは
 * インラインコードとして描き分けられるように分割して返す。
 * texts がないときは null を返すので、呼び出し側はスロットをそのまま出せばよい。
 */
import { computed } from 'vue';
import { useSlideContext } from '@slidev/client';

export function useChatParts(props) {
  const { $clicks } = useSlideContext();

  const text = computed(() => {
    const { texts } = props;
    if (!texts?.length) return null;
    // クリックが進みすぎても最後のセリフで止める
    return texts[Math.min(Math.max($clicks.value, 0), texts.length - 1)];
  });

  return computed(() =>
    text.value == null
      ? null
      : text.value
          .split(/(`[^`]+`)/)
          .filter(Boolean)
          .map((part) =>
            part.startsWith('`') && part.endsWith('`')
              ? { code: true, value: part.slice(1, -1) }
              : { code: false, value: part },
          ),
  );
}
