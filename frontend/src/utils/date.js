export const formatLocalDate = (date) => {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

export const getDateRange = (timeRange = 'all') => {
  const now = new Date()
  let start_date = ''
  let end_date = ''
  if (timeRange === 'today') {
    const today = formatLocalDate(now)
    start_date = today
    end_date = today
  } else if (timeRange === 'week') {
    const day = now.getDay()
    const diff = now.getDate() - day + (day === 0 ? -6 : 1)
    const monday = new Date(now.getFullYear(), now.getMonth(), diff)
    start_date = formatLocalDate(monday)
    const sunday = new Date(monday.getFullYear(), monday.getMonth(), monday.getDate() + 6)
    end_date = formatLocalDate(sunday)
  }
  return { start_date, end_date }
}

export const getTodayStr = () => formatLocalDate(new Date())

export const getWeekStartStr = () => {
  const now = new Date()
  const day = now.getDay()
  const diff = now.getDate() - day + (day === 0 ? -6 : 1)
  const monday = new Date(now.getFullYear(), now.getMonth(), diff)
  return formatLocalDate(monday)
}
