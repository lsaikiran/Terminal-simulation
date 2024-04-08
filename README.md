# Container Terminal Simulation

**Description:**
This Python script simulates the operations of a container terminal, where vessels arrive for unloading containers, which are then transferred to trucks for transportation to the yard. The simulation models the concurrent processes of vessel berthing, container unloading using cranes, and truck movement within the terminal.

**Features:**
- Simulates the arrival of vessels at the terminal according to an exponential distribution.
- Utilizes SimPy, a process-based discrete-event simulation framework.
- Tracks the movement of containers from vessels to trucks, considering resource constraints such as berth availability, crane capacity, and truck availability.
- Provides real-time logging of events during the simulation for monitoring and analysis.

**Key Components:**
1. **ContainerTerminal Class**: Represents the terminal entity, managing resources such as berths, cranes, and trucks. It handles the processes of vessel berthing, container unloading, and truck movement.
   
2. **vessel_generator Function**: Generates vessels at random intervals based on an exponential distribution, simulating their arrival at the terminal.

3. **run_simulation Function**: Initializes the simulation environment, prompts the user to input the simulation time, and runs the simulation until the specified time.

**Dependencies:**
- Python 3.x
- SimPy library

**How to Use:**
1. Ensure Python and SimPy library are installed on your system.
2. Run the script using a Python interpreter.
3. Input the desired simulation time in minutes when prompted.
4. Monitor the simulation output in the console, which provides real-time updates on events occurring at the container terminal.

**Contributors:**
- This simulation script was developed by Sai Kiran for educational and demonstrative purposes.

**Disclaimer:**
This simulation is a simplified model for educational use and may not accurately reflect real-world container terminal operations. Adjustments and enhancements may be necessary for specific use cases or detailed analysis.
