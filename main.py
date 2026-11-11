import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import heapq
import math

class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, city):
        if city not in self.graph:
            self.graph[city] = {}

    def remove_vertex(self, city):
        if city not in self.graph:
            return
        del self.graph[city]
        for neighbor in self.graph:
            self.graph[neighbor].pop(city, None)

    def add_edge(self, city1, city2, distance):
        if city1 == city2 or distance <= 0:
            raise ValueError("Некоректна дорога")
        self.add_vertex(city1)
        self.add_vertex(city2)
        self.graph[city1][city2] = distance
        self.graph[city2][city1] = distance

    def remove_edge(self, city1, city2):
        if city1 in self.graph:
            self.graph[city1].pop(city2, None)
        if city2 in self.graph:
            self.graph[city2].pop(city1, None)

    def dijkstra(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None

        distances = {}

        for city in self.graph:
            distances[city] = float('inf')

        distances[start] = 0
        previous = {}
        priority_queue = [(0, start)]
        visited = set()
        steps = []

        while priority_queue:
            current_distance, current_city = heapq.heappop(priority_queue)
            if current_city in visited:
                continue

            visited.add(current_city)
            steps.append(("visit", current_city, distances.copy()))
            if current_city == end:
                break
            for neighbor, weight in self.graph[current_city].items():
                if neighbor in visited:
                    continue

                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_city
                    heapq.heappush(priority_queue,(new_distance, neighbor))
                    steps.append(("update", neighbor, distances.copy()))

        if distances[end] == float('inf'):
            return None, None, steps
        
        path = []
        current = end

        while current != start:
            path.append(current)
            current = previous[current]

        path.append(start)
        path.reverse()
        return path, distances[end], steps

edges = [
    ("Вінниця", "Житомир", 127),
    ("Вінниця", "Київ", 267),
    ("Вінниця", "Кропивницький", 320),
    ("Вінниця", "Миколаїв", 428),
    ("Вінниця", "Одеса", 423),
    ("Вінниця", "Черкаси", 341),
    ("Вінниця", "Чернівці", 276),
    ("Дніпро", "Донецьк", 248),
    ("Дніпро", "Запоріжжя", 85),
    ("Дніпро", "Кропивницький", 244),
    ("Дніпро", "Кривий Ріг", 146),
    ("Дніпро", "Полтава", 160),
    ("Дніпро", "Харків", 218),
    ("Донецьк", "Луганськ", 156),
    ("Донецьк", "Маріуполь", 113),
    ("Донецьк", "Харків", 294),
    ("Запоріжжя", "Мелітополь", 125),
    ("Івано-Франківськ", "Тернопіль", 133),
    ("Івано-Франківськ", "Ужгород", 293),
    ("Київ", "Житомир", 140),
    ("Київ", "Полтава", 340),
    ("Київ", "Суми", 333),
    ("Київ", "Черкаси", 189),
    ("Київ", "Чернігів", 148),
    ("Кропивницький", "Полтава", 246),
    ("Луганськ", "Харків", 325),
    ("Львів", "Івано-Франківськ", 134),
    ("Львів", "Луцьк", 151),
    ("Львів", "Рівне", 211),
    ("Львів", "Тернопіль", 127),
    ("Львів", "Ужгород", 268),
    ("Львів", "Чернівці", 268),
    ("Мелітополь", "Маріуполь", 192),
    ("Мелітополь", "Сімферополь", 250),
    ("Миколаїв", "Херсон", 69),
    ("Рівне", "Житомир", 188),
    ("Рівне", "Луцьк", 73),
    ("Рівне", "Тернопіль", 155),
    ("Харків", "Полтава", 143),
    ("Херсон", "Мелітополь", 231),
    ("Хмельницький", "Вінниця", 119),
    ("Хмельницький", "Житомир", 183),
    ("Хмельницький", "Рівне", 194),
    ("Хмельницький", "Тернопіль", 112),
    ("Хмельницький", "Чернівці", 187),
    ("Суми", "Харків", 184),
    ("Черкаси", "Полтава", 233),
    ("Полтава", "Суми", 175),
    ("Чернігів", "Суми", 306),
    ("Сімферополь", "Севастополь", 81)
]

class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм Дейкстри - Україна")
        self.root.geometry("1100x750")
        self.graph = Graph()
  
        for city1, city2, distance in edges:
            self.graph.add_edge(city1, city2, distance)

        self.positions = {}
        self.current_path = []
        self.visited = set()
        self.current_city = None

        self.create_interface()
        self.draw_graph()

    def create_interface(self):
        controls = ttk.Frame(self.root, padding=10)
        controls.pack(fill="x")
        ttk.Label(controls, text="Початкове місто:").grid(row=0, column=0, padx=5)
        self.start_box = ttk.Combobox(controls, state="readonly", width=20)
        self.start_box.grid(row=0, column=1, padx=5)

        ttk.Label(controls, text="Кінцеве місто:").grid(row=0, column=2, padx=5)
        self.end_box = ttk.Combobox(controls, state="readonly", width=20)
        self.end_box.grid(row=0, column=3, padx=5)

        ttk.Button(controls,text="Знайти шлях",command=self.find_path).grid(row=0, column=4, padx=5)
        edit_frame = ttk.Frame(self.root, padding=10)
        edit_frame.pack(fill="x")
        ttk.Button(edit_frame,text="Додати місто",command=self.add_city).pack(side="left", padx=5)
        ttk.Button(edit_frame,text="Видалити місто",command=self.remove_city).pack(side="left", padx=5)
        ttk.Button(edit_frame,text="Додати дорогу",command=self.add_road).pack(side="left", padx=5)
        ttk.Button(edit_frame,text="Видалити дорогу",command=self.remove_road).pack(side="left", padx=5)
        ttk.Button(edit_frame,text="Змінити відстань",command=self.change_distance).pack(side="left", padx=5)
        self.canvas = tk.Canvas(self.root,bg="white",width=1000,height=550)
        self.canvas.pack(fill="both", expand=True, padx=10)
        self.status = ttk.Label(self.root,text="Оберіть початкове та кінцеве місто",padding=10)
        self.status.pack()

        self.update_city_boxes()

    def update_city_boxes(self):
        cities = sorted(self.graph.graph.keys())
        self.start_box["values"] = cities
        self.end_box["values"] = cities

        if cities:
            if self.start_box.get() not in cities:
                self.start_box.set(cities[0])
            if self.end_box.get() not in cities:
                self.end_box.set(cities[-1])

    def calculate_positions(self):
        cities = list(self.graph.graph.keys())
        self.positions = {}

        width = max(self.canvas.winfo_width(), 1000)
        height = max(self.canvas.winfo_height(), 550)

        center_x = width / 2
        center_y = height / 2

        radius_x = min(width * 0.42, 420)
        radius_y = min(height * 0.40, 220)

        total = len(cities)

        if total == 0:
            return

        for i, city in enumerate(cities):
            angle = 2 * math.pi * i / total
            x = center_x + radius_x * math.cos(angle)
            y = center_y + radius_y * math.sin(angle)
            self.positions[city] = (x, y)

    def draw_graph(self):
        self.canvas.delete("all")
        self.calculate_positions()
        for city in self.graph.graph:
            x1, y1 = self.positions[city]
            for neighbor, distance in self.graph.graph[city].items():
                if city >= neighbor:
                    continue

                x2, y2 = self.positions[neighbor]
                color = "gray"

                if (city in self.current_path and neighbor in self.current_path and abs(self.current_path.index(city)
                    - self.current_path.index(neighbor)) == 1): color = "green"
                self.canvas.create_line(x1, y1, x2, y2,fill=color,width=3 if color == "green" else 1)

                middle_x = (x1 + x2) / 2
                middle_y = (y1 + y2) / 2

                self.canvas.create_text(middle_x,middle_y,text=str(distance),fill="blue",font=("Arial", 8))

        for city, (x, y) in self.positions.items():
            color = "lightblue"
            if city in self.visited:
                color = "orange"
            if city == self.current_city:
                color = "yellow"
            if city in self.current_path:
                color = "lightgreen"

            self.canvas.create_oval(x - 18, y - 18,x + 18, y + 18,fill=color,outline="black")
            self.canvas.create_text(x,y - 30,text=city,font=("Arial", 8))

    def find_path(self):
        start = self.start_box.get()
        end = self.end_box.get()

        if not start or not end:
            messagebox.showerror("Помилка", "Оберіть обидва міста")
            return

        result = self.graph.dijkstra(start, end)

        if result[0] is None:
            messagebox.showinfo("Результат", "Маршрут не знайдено")
            return

        path, distance, steps = result

        self.current_path = []
        self.visited = set()
        self.current_city = None

        self.draw_graph()
        self.animate_search(steps, 0, path, distance)

    def animate_search(self, steps, index, path, distance):
        if index >= len(steps):
            self.current_city = None
            self.current_path = path
            self.draw_graph()
            self.show_result(path, distance)
            return

        action, city, distances = steps[index]

        if action == "visit":
            self.visited.add(city)
            self.current_city = city
            self.status.config(text="Перевіряється місто: " + city)

        self.draw_graph()

        self.root.after(400,lambda: self.animate_search(steps, index + 1, path, distance))

    def show_result(self, path, distance):
        window = tk.Toplevel(self.root)
        window.title("Результат пошуку")
        window.geometry("400x300")

        ttk.Label(window,text="Найкоротший маршрут",font=("Arial", 14, "bold")).pack(pady=15)
        ttk.Label(window,text=" → ".join(path),wraplength=350,justify="center").pack(pady=10)
        ttk.Label(window,text=f"Загальна відстань: {distance} км",font=("Arial", 12, "bold")).pack(pady=15)
        ttk.Label(window,text=f"Кількість міст: {len(path)}").pack()

    def add_city(self):
        city = simpledialog.askstring("Нове місто", "Введіть назву міста:")

        if city and city.strip():
            self.graph.add_vertex(city.strip())
            self.update_city_boxes()
            self.draw_graph()

    def remove_city(self):
        city = self.start_box.get()
        if not city:
            return
        if messagebox.askyesno("Підтвердження",f"Видалити місто {city}?"):
            self.graph.remove_vertex(city)
            self.current_path = []
            self.visited = set()
            self.update_city_boxes()
            self.draw_graph()

    def add_road(self):
        city1 = simpledialog.askstring("Дорога", "Перше місто:")
        if not city1:
            return
        city2 = simpledialog.askstring("Дорога", "Друге місто:")
        if not city2:
            return
        distance = simpledialog.askinteger("Відстань", "Відстань у кілометрах:",minvalue=1)
        if distance is None:
            return
        try:
            self.graph.add_edge(city1.strip(),city2.strip(),distance)
            self.update_city_boxes()
            self.draw_graph()

        except ValueError as error:
            messagebox.showerror("Помилка", str(error))

    def remove_road(self):
        city1 = simpledialog.askstring("Видалення дороги", "Перше місто:")
        if not city1:
            return
        city2 = simpledialog.askstring("Видалення дороги", "Друге місто:")
        if not city2:
            return
        self.graph.remove_edge(city1.strip(), city2.strip())

        self.current_path = []
        self.draw_graph()

    def change_distance(self):
        city1 = simpledialog.askstring("Зміна відстані", "Перше місто:")
        if not city1:
            return
        city2 = simpledialog.askstring("Зміна відстані", "Друге місто:")
        if not city2:
            return
        if (city1 not in self.graph.graph or city2 not in self.graph.graph[city1]):
            messagebox.showerror("Помилка", "Такої дороги не існує")
            return

        distance = simpledialog.askinteger("Нова відстань", "Введіть нову відстань:",minvalue=1)

        if distance is not None:
            self.graph.add_edge(city1, city2, distance)
            self.current_path = []
            self.draw_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()