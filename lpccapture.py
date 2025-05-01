#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os

SECONDS = 10
HZ = 24_000_000  # 24 MHz para LPC
CHANNELS = "0-5"  # LAD0-3, LFRAME#, CLK (6 líneas digitales)
DRIVER = "fx2lafw"  # Cambia si usas otro driver
OUTPUT_FILE = "capture.csv"

class LPCCaptureSigrok:
    def __init__(self, output_file="capture.csv"):
        self.output_file = output_file

    def run(self):
        # Ejecutar sigrok-cli para capturar
        cmd = [
            "sigrok-cli",
            "--driver", DRIVER,
            "--channels", CHANNELS,
            "--samples", str(HZ * SECONDS),
            "--output-format", "csv",
            "--output-file", self.output_file
        ]
        print(f"[*] Ejecutando: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] Error durante la captura con sigrok-cli: {e}")
            return

        if not os.path.exists(self.output_file):
            print(f"[!] Archivo no generado: {self.output_file}")
            return

        try:
            subprocess.run(['python3', 'lpc_decoder.py', self.output_file])
        except Exception as e:
            print(f"[!] Error al ejecutar lpc_decoder.py: {e}")

def banner():
    print(f"Uso: {sys.argv[0]} <archivo_salida.csv>")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        banner()

    recorder = LPCCaptureSigrok(sys.argv[1])
    recorder.run()
    print(f"[*] Capturando datos LPC desde {recorder.output_file}...")
    print(f"[*] Captura finalizada. Datos guardados en {recorder.output_file}.")
    print(f"[*] Procesa los datos con lpc_decoder.py <recorded.csv>...")
    print(f"[*] Proceso finalizado.")