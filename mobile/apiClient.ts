export interface Task {
  id: number;
  title: string;
  description?: string;
  due_datetime?: string | null;
  priority: 'low' | 'medium' | 'high';
  status: string;
  calendar_event_id?: string | null;
}

export interface CalendarEvent {
  id: string;
  title: string;
  start: string;
  end: string;
}

export async function fetchTasks(): Promise<Task[]> {
  const r = await fetch('/api/v1/tasks');
  if (!r.ok) {
    throw new Error('Failed to fetch tasks');
  }
  return r.json();
}

export async function syncGoogleEvents(): Promise<CalendarEvent[]> {
  const r = await fetch('/api/v1/google/sync');
  if (!r.ok) {
    throw new Error('Failed to fetch calendar events');
  }
  return r.json();
}
