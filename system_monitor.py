#!/usr/bin/env python3
import psutil
import time
import os
from collections import deque
try:
    import GPUtil
except ImportError:
    GPUtil = None

# Configurações
HISTORY_LENGTH = 10
REFRESH_INTERVAL = 2

# Cores ANSI
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'reset': '\033[0m'
}

def clear_screen():
    os.system('clear')

def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            return temps['coretemp'][0].current
        return "N/A"
    except:
        return "N/A"

def get_gpu_info():
    if GPUtil:
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0]
        except:
            pass
    return None

def create_ascii_bar(value, max_value=100, color='green'):
    bar_length = 50
    filled = int(round(bar_length * value / max_value))
    return f"{COLORS[color]}{'█' * filled}{COLORS['reset']}{'░' * (bar_length - filled)}"

def display_system_info(history):
    # Uso da CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq().current
    cpu_temp = get_cpu_temperature()
    
    # Uso de memória
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Uso de disco
    disk = psutil.disk_usage('/')
    
    # Uso de rede
    net_io = psutil.net_io_counters()
    
    # Processos ativos
    processes = len(psutil.pids())
    
    # Top 5 processos por uso de CPU
    top_processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']), 
                          key=lambda p: p.info['cpu_percent'], reverse=True)[:5]

    # Informações da GPU
    gpu = get_gpu_info()

    clear_screen()
    print(f"{COLORS['blue']}=== Monitor de Sistema ==={COLORS['reset']}")
    
    # Gráfico de CPU
    print(f"\n{COLORS['green']}Uso da CPU:{COLORS['reset']} {cpu_usage}% ({cpu_count} cores, {cpu_freq} MHz)")
    print(create_ascii_bar(cpu_usage, color='green'))
    
    # Gráfico de Memória
    print(f"\n{COLORS['yellow']}Uso de Memória:{COLORS['reset']} {mem.percent}% ({mem.used//1024//1024}MB / {mem.total//1024//1024}MB)")
    print(create_ascii_bar(mem.percent, color='yellow'))
    
    # Gráfico de Swap
    print(f"\n{COLORS['yellow']}Uso de Swap:{COLORS['reset']} {swap.percent}% ({swap.used//1024//1024}MB / {swap.total//1024//1024}MB)")
    print(create_ascii_bar(swap.percent, color='yellow'))
    
    # Gráfico de Disco
    print(f"\n{COLORS['red']}Espaço em Disco Usado:{COLORS['reset']} {disk.percent}% ({disk.used//1024//1024}MB / {disk.total//1024//1024}MB)")
    print(create_ascii_bar(disk.percent, color='red'))
    
    # Informações da GPU
    if gpu:
        print(f"\n{COLORS['blue']}Uso da GPU:{COLORS['reset']} {gpu.load*100:.1f}%")
        print(f"Memória GPU: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB")
        print(f"Temperatura GPU: {gpu.temperature}°C")
    
    # Outras informações
    print(f"\n{COLORS['blue']}Temperatura da CPU:{COLORS['reset']} {cpu_temp}°C")
    print(f"{COLORS['blue']}Rede:{COLORS['reset']} Enviado {net_io.bytes_sent//1024}KB, Recebido {net_io.bytes_recv//1024}KB")
    print(f"{COLORS['blue']}Processos Ativos:{COLORS['reset']} {processes}")
    
    # Histórico de uso
    history.append((cpu_usage, mem.percent, disk.percent))
    if len(history) > HISTORY_LENGTH:
        history.popleft()
    
    print(f"\n{COLORS['blue']}Histórico de Uso:{COLORS['reset']}")
    for cpu, mem, disk in history:
        print(f"CPU: {cpu:3.0f}% | Mem: {mem:3.0f}% | Disk: {disk:3.0f}%")
    
    print(f"\n{COLORS['blue']}Top 5 Processos por Uso de CPU:{COLORS['reset']}")
    for proc in top_processes:
        mem_usage = proc.info['memory_info'].rss // 1024 // 1024
        print(f"  {proc.info['pid']} {proc.info['name']}: {proc.info['cpu_percent']}% ({mem_usage}MB)")
    
    print(f"{COLORS['blue']}========================={COLORS['reset']}")

def export_data(history, filename='system_monitor.log'):
    with open(filename, 'w') as f:
        f.write("Histórico de Uso do Sistema\n")
        f.write("CPU% | Mem% | Disk%\n")
        for cpu, mem, disk in history:
            f.write(f"{cpu:3.0f} | {mem:3.0f} | {disk:3.0f}\n")

def main():
    history = deque(maxlen=HISTORY_LENGTH)
    try:
        while True:
            display_system_info(history)
            time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        export = input("\nDeseja exportar os dados? (s/n): ").lower()
        if export == 's':
            export_data(history)
            print("Dados exportados para system_monitor.log")
        print("\nMonitor encerrado.")

if __name__ == "__main__":
    main() 