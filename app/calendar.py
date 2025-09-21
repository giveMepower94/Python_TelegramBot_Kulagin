class Calendar:

    def __init__(self):
        self.events = {}

    # Создать метод create_event
    def create_event(self, event_name, event_date, event_time, event_details):
        event_id = len(self.events) + 1
        event = {
            "id": event_id,
            "name": event_name,
            "date": event_date,
            "time": event_time,
            "details": event_details
            }
        self.events[event_id] = event
        return event_id

    # Создать метод read_event
    def read_event(self, event_id):
        event = self.events.get(event_id)

        if not event:
            None

        return (f"ID: {event['id']}\n"
            f"Название: {event['name']}\n"
            f"Дата: {event['date']}\n"
            f"Время: {event['time']}\n"
            f"Детали: {event['details']}")

    # Создать метод edit_event
    def edit_event(self, event_id, name=None, date=None, time=None, details=None):
        if event_id not in self.events:
            return False
        if name:
            self.events[event_id]['name'] = name
        if date:
            self.events[event_id]['date'] = date
        if time:
            self.events[event_id]['time'] = time
        if details:
            self.events[event_id]['details'] = details

        return True

    # Создать метод delete_event
    def delete_event(self, event_id):
        return self.events.pop(event_id, None)

    def get_list_event(self, event_date):
        return [e for e in self.events.values() if e['date'] == event_date]
