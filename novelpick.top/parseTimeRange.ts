function parseTimeRange(input: string, ref: Date): { start: string, end: string } {
  const r = (d: Date) => d.toISOString();
  switch(input) {
    case "last 7 days": 
      return { start: r(new Date(ref.getTime() - 7*86400000)), end: r(ref) };
    case "past 24 hours": 
      return { start: r(new Date(ref.getTime() - 86400000)), end: r(ref) };
    case "yesterday": 
      const y = new Date(ref); y.setDate(y.getDate()-1); y.setHours(0,0,0,0);
      return { start: r(y), end: r(new Date(y.getTime()+86399999)) };
    case "this week": 
      const w = new Date(ref); w.setDate(w.getDate()-w.getDay()+1); w.setHours(0,0,0,0);
      return { start: r(w), end: r(ref) };
    case "this month": 
      const m = new Date(ref); m.setDate(1); m.setHours(0,0,0,0);
      return { start: r(m), end: r(ref) };
    case "last 30 minutes": 
      return { start: r(new Date(ref.getTime()-1800000)), end: r(ref) };
    default: 
      throw new Error("Unknown time range: "+input);
  }
}
console.log(JSON.stringify(parseTimeRange("last 7 days", new Date("2026-04-20T12:00:00Z"))));
console.log(JSON.stringify(parseTimeRange("yesterday", new Date("2026-04-20T12:00:00Z"))));
console.log(JSON.stringify(parseTimeRange("this week", new Date("2026-04-20T12:00:00Z"))));
