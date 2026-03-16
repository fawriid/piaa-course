import matplotlib.pyplot as plt

# Read CSV file
data = []
with open("research.csv", "r") as file:
    header = file.readline().strip()  
    line = file.readline().strip()
    while(line):
        data.append(line)
        line = file.readline().strip()

print(f"data loaded: {len(data)} rows")

# Parse your data
n_values = []
calls_values = []
attempts_values = []
time_values = []

for line in data:
    parts = line.split(',')
    n_values.append(int(parts[0]))
    calls_values.append(int(parts[2]))      # recursive calls
    attempts_values.append(int(parts[3]))    # placement attempts
    time_values.append(float(parts[4]))

even_n = [n for i, n in enumerate(n_values) if n % 2 == 0]
even_calls = [calls for i, calls in enumerate(calls_values) if n_values[i] % 2 == 0]
odd_n = [n for i, n in enumerate(n_values) if n % 2 != 0]
odd_calls = [calls for i, calls in enumerate(calls_values) if n_values[i] % 2 != 0]

# Create graph
fig, ax = plt.subplots(figsize=(12, 8))

# Plot odd numbers only 
ax.plot(odd_n, odd_calls, 'bo-', linewidth=2, markersize=8, label='recursive calls')
ax.set_xlabel('square size n (odd numbers only)', fontsize=12)
ax.set_ylabel('number of operations', fontsize=12)
ax.set_title('recursive calls for odd n', fontsize=14)
ax.grid(True, alpha=0.3)
ax.set_yscale('log')

# Add labels on points
for i, n in enumerate(odd_n):
    ax.annotate(f'{odd_calls[i]}', (n, odd_calls[i]), 
                textcoords="offset points", xytext=(0, 10), 
                ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('my_research_graph.png', dpi=150)
plt.show()

print("graph saved as my_research_graph.png")