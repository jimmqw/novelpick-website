function parseTimeRange(input, ref) {
  const toISO = (d) => d.toISOString();
  // Use local time for boundary calculations
  const toLocalMidnight = (d, daysOffset = 0) => {
    const local = new Date(d);
    local.setDate(local.getDate() + daysOffset);
    local.setHours(0, 0, 0, 0);
    return local;
  };
  const toLocalEnd = (d, daysOffset = 0) => {
    const local = new Date(d);
    local.setDate(local.getDate() + daysOffset);
    local.setHours(23, 59, 59, 999);
    return local;
  };
  switch(input) {
    case "last 7 days": 
      return { start: toISO(toLocalMidnight(ref, -7)), end: toISO(ref) };
    case "past 24 hours": 
      return { start: toISO(new Date(ref.getTime() - 86400000)), end: toISO(ref) };
    case "yesterday": 
      return { start: toISO(toLocalMidnight(ref, -1)), end: toISO(toLocalEnd(ref, -1)) };
    case "this week": 
      const dayOfWeek = ref.getDay();
      const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
      return { start: toISO(toLocalMidnight(ref, mondayOffset)), end: toISO(ref) };
    case "this month": 
      const local = new Date(ref);
      local.setDate(1);
      local.setHours(0, 0, 0, 0);
      return { start: toISO(local), end: toISO(ref) };
    case "last 30 minutes": 
      return { start: toISO(new Date(ref.getTime()-1800000)), end: toISO(ref) };
    default: 
      throw new Error("Unknown time range: "+input);
  }
}
// Test
const ref = new Date("2026-04-20T12:00:00Z");
["last 7 days", "past 24 hours", "yesterday", "this week", "this month", "last 30 minutes"].forEach(t => {
  console.log(t + ": " + JSON.stringify(parseTimeRange(t, ref)));
});
