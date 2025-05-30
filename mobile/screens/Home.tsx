import React, { useEffect, useState } from 'react';
import { View, ScrollView, Text, ActivityIndicator, StyleSheet } from 'react-native';
import { Card } from '../ui/components';
import BigCalendar, { Event as CalendarEvent } from 'react-native-big-calendar';
import { fetchTasks, syncGoogleEvents, Task } from '../apiClient';

const priorityColors: Record<Task['priority'], string> = {
  low: '#4caf50',
  medium: '#ff9800',
  high: '#f44336',
};

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [taskData, eventData] = await Promise.all([
          fetchTasks(),
          syncGoogleEvents(),
        ]);
        setTasks(taskData);
        const taskEvents: CalendarEvent[] = taskData.map(t => ({
          title: t.title,
          start: t.due_datetime ? new Date(t.due_datetime) : new Date(),
          end: t.due_datetime ? new Date(t.due_datetime) : new Date(),
          color: priorityColors[t.priority],
        }));
        const googleEvents: CalendarEvent[] = eventData.map(e => ({
          title: e.title,
          start: new Date(e.start),
          end: new Date(e.end),
        }));
        setEvents([...taskEvents, ...googleEvents]);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <View style={styles.loader}>
        <ActivityIndicator />
      </View>
    );
  }

  return (
    <View style={{ flex: 1 }}>
      <BigCalendar events={events} height={400} />
      <ScrollView style={styles.list}>
        {tasks.map(task => (
          <Card key={task.id}>
            <Text style={{ color: priorityColors[task.priority] }}>
              {task.title}
            </Text>
          </Card>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  loader: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  list: {
    padding: 16,
  },
});
