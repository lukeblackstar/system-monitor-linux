# System Monitor

Um monitor de sistema em tempo real escrito em Python que exibe informações sobre CPU, memória, disco, rede e GPU (se disponível).

## Funcionalidades

- Monitoramento em tempo real de:
  - Uso da CPU (porcentagem e frequência)
  - Uso de memória RAM e Swap
  - Uso de espaço em disco
  - Tráfego de rede
  - Temperatura da CPU
  - Uso da GPU (se disponível)
  - Processos ativos
- Exibição gráfica usando barras ASCII
- Histórico dos últimos 10 ciclos de monitoramento
- Lista dos 5 processos que mais consomem CPU
- Exportação dos dados para um arquivo de log

## Requisitos

- Python 3.x
- Pacotes necessários:
  - `psutil`
  - `GPUtil` (opcional, para monitoramento de GPU)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/lukeblackstar/system-monitor-linux.git
   cd system-monitor
   ```
## Uso

Execute o script:
```bash
python system_monitor.py
```

O monitor será exibido no terminal e atualizado a cada 2 segundos. Para sair, pressione `Ctrl+C`.

Ao encerrar, você terá a opção de exportar os dados para um arquivo `system_monitor.log`.

## Personalização

Você pode ajustar as configurações no início do arquivo `system_monitor.py`:

- `HISTORY_LENGTH`: Número de ciclos a serem armazenados no histórico
- `REFRESH_INTERVAL`: Intervalo de atualização em segundos

![Image](https://github.com/user-attachments/assets/189ae55a-4b61-4535-b140-1747820e7fa6)

 
