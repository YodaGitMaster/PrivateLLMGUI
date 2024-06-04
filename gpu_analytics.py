

# def get_gpu_stats():
#     try:
#         result = subprocess.run(['nvidia-smi', '--query-gpu=index,name,utilization.gpu,memory.total,memory.used,memory.free', '--format=csv,noheader,nounits'], capture_output=True, text=True, check=True)
#         gpu_stats = result.stdout.strip().split('\n')
#         for stat in gpu_stats:
#             print(stat)
#     except subprocess.CalledProcessError as e:
#         print(f"Error: {e}")
import psutil
import time
from threading import Thread
import GPUtil
import streamlit as st
import pandas as pd
import warnings
import altair as alt
import matplotlib.pyplot as plt
# Suppress import warnings
warnings.filterwarnings("ignore")


def create_usage_chart(cpu_data, memory_data, gpu_data):
    # Create a chart with the latest data
    plt.figure(figsize=(10, 6))

    # Set the background color to black
    plt.gca().set_facecolor('black')

    # Plot CPU Usage
    plt.plot(cpu_data, label='CPU Usage (%)', color='green')

    # Plot Memory Usage
    plt.plot(memory_data, label='Memory Usage (%)', color='blue')

    # Plot GPU Usage
    plt.plot(gpu_data, label='GPU Usage (%)', color='orange')

    # Set y-axis range between 0 and 100
    plt.ylim(0, 100)

    # Set labels and title
    plt.xlabel('Time')
    plt.ylabel('Percentage')
    plt.title('CPU, Memory, and GPU Usage')

    # Get the legend frame and set face color for the legend
    legend = plt.legend()
    legend.get_frame().set_facecolor('black')


    # Get the legend texts and set color
    for text in legend.get_texts():
        text.set_color('white')

    # Set the background color of the entire plot
    plt.gca().set_facecolor('black')

    return plt




def check_system_conditions():
    # Get CPU usage for each core
    cpu_percent = psutil.cpu_percent()
    cpu_percent_per_core = psutil.cpu_percent(percpu=True)
    used_cores = sum(1 for percent in cpu_percent_per_core if percent > 0)

    # Get memory information
    memory_info = psutil.virtual_memory()
    memory_used_gb = memory_info.used / (1024 ** 3)  # Convert bytes to GB
    memory_percent = memory_info.percent

    # Get GPU information
    gpu_info = GPUtil.getGPUs()[0]
    gpu_percent = gpu_info.load * 100  # GPU usage in percentage
    gpu_memory_used_gb = (gpu_info.memoryTotal * (gpu_percent /100))/1000  # GPU memory used in GB  # GPU memory in use in GB

    # Collect data in a dictionary
    result = {
        'CPU Usage (%)': cpu_percent,
        'Used Cores': used_cores,
        'Memory Usage (GB)': memory_used_gb,
        'Memory Usage (%)': memory_percent,
        'GPU Usage (GB)': float(gpu_memory_used_gb),
        'GPU Usage (%)': gpu_percent
    }

    # Print the information
    print(f"System Conditions:\n"
      f"  CPU Usage (%): {result['CPU Usage (%)']} |"
      f"  Used Cores: {result['Used Cores']} |"
      f"  Memory Usage (GB): {result['Memory Usage (GB)']:.2f} GB |"
      f"  Memory Usage (%): {result['Memory Usage (%)']}% |"
      f"  GPU Usage (GB): {result['GPU Usage (GB)']:.2f} GB |"
      f"  GPU Usage (%): {result['GPU Usage (%)']}%")

    return result

# Streamlit app
st.title("Real-time System Monitor")
st.write("Updated every 2 seconds")
# Initial placeholder dictionaries for each variable
cpu_usage_dict = {'CPU Usage (%)': 0}
used_cores_dict = {'Used Cores': 0}
memory_usage_gb_dict = {'Memory Usage (GB)': 0}
memory_usage_percent_dict = {'Memory Usage (%)': 0}
gpu_usage_gb_dict = {'GPU Usage (GB)': 0}
gpu_usage_percent_dict = {'GPU Usage (%)': 0}

# Create empty elements for each variable
cpu_usage_element = st.empty()
used_cores_element = st.empty()
memory_usage_gb_element = st.empty()
memory_usage_percent_element = st.empty()
gpu_usage_gb_element = st.empty()
gpu_usage_percent_element = st.empty()

chart_element = st.empty()

memory_usage_gb_data = []
gpu_usage_gb_data = []
cpu_usage_data = []

while True:
    # Get system conditions
    current_conditions = check_system_conditions()

    # Update the placeholders with new values
    cpu_usage_dict['CPU Usage (%)'] = current_conditions['CPU Usage (%)']
    used_cores_dict['Used Cores'] = current_conditions['Used Cores']
    memory_usage_gb_dict['Memory Usage (GB)'] = current_conditions['Memory Usage (GB)']
    memory_usage_percent_dict['Memory Usage (%)'] = current_conditions['Memory Usage (%)']
    gpu_usage_gb_dict['GPU Usage (GB)'] = current_conditions['GPU Usage (GB)']
    gpu_usage_percent_dict['GPU Usage (%)'] = current_conditions['GPU Usage (%)']

    # Display the updated system conditions within the same div for each variable
    cpu_usage_element.write(f"CPU Usage (%): {cpu_usage_dict['CPU Usage (%)']}")
    used_cores_element.write(f"Used Cores: {used_cores_dict['Used Cores']}")
    memory_usage_gb_element.write(f"Memory Usage (GB): {memory_usage_gb_dict['Memory Usage (GB)']:.2f} GB")
    memory_usage_percent_element.write(f"Memory Usage (%): {memory_usage_percent_dict['Memory Usage (%)']}%")
    gpu_usage_gb_element.write(f"GPU Usage (GB): {gpu_usage_gb_dict['GPU Usage (GB)']:.2f} GB")
    gpu_usage_percent_element.write(f"GPU Usage (%): {gpu_usage_percent_dict['GPU Usage (%)']}%")
    
     # Update the chart with the latest data
     
    memory_usage_gb_data.append(memory_usage_percent_dict['Memory Usage (%)'])
    gpu_usage_gb_data.append(gpu_usage_percent_dict['GPU Usage (%)'])
    cpu_usage_data.append(cpu_usage_dict['CPU Usage (%)'])

    memory_usage_gb_data = memory_usage_gb_data[-100:]
    gpu_usage_gb_data = gpu_usage_gb_data[-100:]
    cpu_usage_data = cpu_usage_data[-100:]
    
    chart_data = pd.DataFrame({
        'Memory Usage %': memory_usage_gb_data,
        'GPU Usage %': gpu_usage_gb_data,
        'CPU Usage %': cpu_usage_data
    })
    

    cpu_usage_data.append(current_conditions['CPU Usage (%)'])
    memory_usage_gb_data.append(current_conditions['Memory Usage (%)'])
    gpu_usage_gb_data.append(current_conditions['GPU Usage (%)'])

    # Keep only the last 100 data points
    cpu_usage_data = cpu_usage_data[-100:]
    memory_usage_gb_data = memory_usage_gb_data[-100:]
    gpu_usage_gb_data = gpu_usage_gb_data[-100:]

     # Create the chart
    chart = create_usage_chart(cpu_usage_data, memory_usage_gb_data, gpu_usage_gb_data)

    # Display the chart with fixed y-axis range
    chart_element.pyplot(chart)

    
    # Add a short sleep to prevent excessive updates
    time.sleep(2)
