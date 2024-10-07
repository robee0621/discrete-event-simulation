import simpy
import random
import matplotlib.pyplot as plt

RANDOM_SEED = 42
TELLERS = 3  # Number of tellers
SIM_TIME = 100  # Simulation time in units (e.g., minutes)

# Metrics for analysis
wait_times = []  # To track customer wait times
queue_lengths = []  # To track queue length over time
utilization_times = []  # To track teller utilization over time

# Customer process
def customer(env, name, bank, wait_times):
    arrival_time = env.now
    print(f'{name} arrives at the bank at {arrival_time:.2f}')
    
    with bank.request() as req:
        yield req  # Wait for a teller
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        print(f'{name} starts being served at {env.now:.2f} after waiting {wait_time:.2f}')
        
        # Random service time (e.g., between 5 and 10 minutes)
        service_time = random.uniform(5, 10)
        yield env.timeout(service_time)
        print(f'{name} leaves the bank at {env.now:.2f}')

# Bank process
def setup(env, num_tellers, wait_times):
    bank = simpy.Resource(env, num_tellers)

    i = 0
    while True:
        # Customers arrive at random intervals (e.g., every 1-10 minutes)
        yield env.timeout(random.uniform(1, 10))
        i += 1
        env.process(customer(env, f'Customer {i}', bank, wait_times))

        # Track the queue length at each time step
        queue_lengths.append(len(bank.queue))
        # Track teller utilization (i.e., number of busy tellers)
        utilization_times.append(bank.count)

# Running the simulation
random.seed(RANDOM_SEED)
env = simpy.Environment()
env.process(setup(env, TELLERS, wait_times))
env.run(until=SIM_TIME)

# Output Analysis
avg_wait_time = sum(wait_times) / len(wait_times) if wait_times else 0
print(f'\nAverage wait time: {avg_wait_time:.2f} minutes')

# Plotting the results
time_points = range(len(queue_lengths))

plt.figure(figsize=(12, 5))

# Plot queue lengths over time
plt.subplot(1, 2, 1)
plt.plot(time_points, queue_lengths)
plt.title('Queue Length Over Time')
plt.xlabel('Time (units)')
plt.ylabel('Queue Length')

# Plot teller utilization over time
plt.subplot(1, 2, 2)
plt.plot(time_points, utilization_times)
plt.title('Teller Utilization Over Time')
plt.xlabel('Time (units)')
plt.ylabel('Number of Busy Tellers')

plt.tight_layout()
plt.show()
