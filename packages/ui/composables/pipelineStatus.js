import { computed, ref, watch } from 'vue';

/** クリックで回る順序も兼ねる */
export const PIPELINE_STATUSES = ['pending', 'running', 'done', 'failed'];

/**
 * steps / current / failedAt から各手順の状態を決め、クリックでの上書きを提供する。
 *
 * - failedAt 指定時: それより前は done、それ自身は failed、以降は pending
 * - current 指定時: それより前は done、それ自身は running、以降は pending
 * - どちらも未指定: steps 側の status をそのまま使う
 *
 * @param props steps / current / failedAt / interactive を持つ props オブジェクト
 */
export function usePipelineStatuses(props) {
  const normalized = computed(() =>
    props.steps.map((step) =>
      typeof step === 'string' ? { label: step } : { ...step },
    ),
  );

  const base = computed(() =>
    normalized.value.map((step, index) => {
      if (props.failedAt !== null && props.failedAt !== undefined) {
        if (index < props.failedAt) return 'done';
        if (index === props.failedAt) return 'failed';
        return 'pending';
      }
      if (props.current === null || props.current === undefined) {
        return PIPELINE_STATUSES.includes(step.status) ? step.status : 'pending';
      }
      if (index < props.current) return 'done';
      if (index === props.current) return 'running';
      return 'pending';
    }),
  );

  // クリックで上書きした状態。current / failedAt / steps が変わったら破棄する
  const overrides = ref({});
  watch(
    () => [props.current, props.failedAt, props.steps],
    () => {
      overrides.value = {};
    },
    { deep: true },
  );

  const resolved = computed(() =>
    normalized.value.map((step, index) => ({
      ...step,
      status: overrides.value[index] ?? base.value[index],
    })),
  );

  const cycle = (index) => {
    if (!props.interactive) return;
    const next =
      (PIPELINE_STATUSES.indexOf(resolved.value[index].status) + 1) %
      PIPELINE_STATUSES.length;
    overrides.value = { ...overrides.value, [index]: PIPELINE_STATUSES[next] };
  };

  return { resolved, cycle };
}
