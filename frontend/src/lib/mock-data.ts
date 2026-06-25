export const agents = [
  { id: "1", name: "CEO Agent", type: "CEO", status: "working", efficiency: "98%", tasksCompleted: 145 },
  { id: "2", name: "Marketing Agent", type: "MARKETING", status: "idle", efficiency: "92%", tasksCompleted: 890 },
  { id: "3", name: "Sales Agent", type: "SALES", status: "working", efficiency: "95%", tasksCompleted: 432 },
  { id: "4", name: "CS Agent", type: "CS", status: "idle", efficiency: "97%", tasksCompleted: 1205 },
  { id: "5", name: "Ops Agent", type: "OPS", status: "sleeping", efficiency: "94%", tasksCompleted: 231 },
  { id: "6", name: "Reputation Agent", type: "REPUTATION", status: "idle", efficiency: "91%", tasksCompleted: 567 },
  { id: "7", name: "Finance Agent", type: "FINANCE", status: "working", efficiency: "99%", tasksCompleted: 89 },
];

export const leads = [
  { id: "1", customerName: "John Doe", status: "new", source: "Google Ads", phone: "555-0101", summary: "Broken HVAC unit" },
  { id: "2", customerName: "Jane Smith", status: "qualifying", source: "LSA", phone: "555-0102", summary: "Need new roof estimate" },
  { id: "3", customerName: "Bob Johnson", status: "booked", source: "Website", phone: "555-0103", summary: "Leaking faucet" },
  { id: "4", customerName: "Alice Williams", status: "dead", source: "Referral", phone: "555-0104", summary: "Window cleaning" },
];

export const jobs = [
  { id: "1", customerName: "Bob Johnson", techName: "Dave", scheduledAt: "2024-06-17 10:00", status: "scheduled", description: "Leaking faucet repair" },
  { id: "2", customerName: "Charlie Brown", techName: "Mike", scheduledAt: "2024-06-17 11:30", status: "in_progress", description: "AC Maintenance" },
  { id: "3", customerName: "Eva Green", techName: "Dave", scheduledAt: "2024-06-16 14:00", status: "completed", description: "Electrical Panel Upgrade" },
];

export const invoices = [
  { id: "INV-001", customerName: "Eva Green", amount: 1250.00, status: "paid", dueAt: "2024-06-16" },
  { id: "INV-002", customerName: "Frank Castle", amount: 450.00, status: "sent", dueAt: "2024-06-20" },
  { id: "INV-003", customerName: "Grace Hopper", amount: 89.99, status: "draft", dueAt: "2024-06-25" },
];

export const conversations = [
  { id: "1", customerName: "John Doe", lastMessage: "Can you help me with my HVAC?", time: "2m ago", unread: true },
  { id: "2", customerName: "Jane Smith", lastMessage: "When can you come by?", time: "15m ago", unread: false },
  { id: "3", customerName: "Alice Williams", lastMessage: "Thanks for the quote!", time: "1h ago", unread: false },
];
