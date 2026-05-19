import { ref } from 'vue'

export function useSequentialReveal<T>(items: T[], duration = 5) {
  const visible = ref<T[]>([])
  const started = ref(false)
  let timers: ReturnType<typeof setTimeout>[] = []

  function start() {
    if (started.value) return
    started.value = true
    const n = items.length
    const totalMs = duration * 1000
    items.forEach((item, i) => {
      // sqrt easing: starts slow, accelerates
      const t = totalMs * Math.sqrt((i + 1) / n)
      timers.push(setTimeout(() => { visible.value.push(item) }, t))
    })
  }

  function reset() {
    timers.forEach(clearTimeout)
    timers = []
    visible.value = []
    started.value = false
  }

  return { visible, start, reset }
}
