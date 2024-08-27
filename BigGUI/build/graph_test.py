import csv
import matplotlib.pyplot as plt

def read_csv(filename):
    times = []
    angles_paka = []
    angles_kolo = []

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            times.append(float(row["Time"]))
            angles_paka.append(float(row["Angle_paka"]))
            angles_kolo.append(float(row["Angle_kolo"]))

    return times, angles_paka, angles_kolo

def plot_data(times, angles_paka, angles_kolo):
    plt.figure(figsize=(10, 5))
    plt.plot(times, angles_paka, label='Angle_paka')
    plt.plot(times, angles_kolo, label='Angle_kolo')
    plt.xlabel('Čas [s]')
    plt.ylabel('Úhel (°)')
    plt.title('Grafík')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    filename = 'Test_oba_1.csv'  # Změňte na název vašeho CSV souboru
    times, angles_paka, angles_kolo = read_csv(filename)
    plot_data(times, angles_paka, angles_kolo)