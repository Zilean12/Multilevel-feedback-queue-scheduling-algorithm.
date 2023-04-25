import csv
from prettytable import PrettyTable


def reader(inputFile):
    with open(inputFile, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data


def scheduling(dataset):
    time = 0
    proc = []
    for data in dataset:
        proc.append({
            'name': data['Process'],
            'arrivaltime': int(data['ArrivalTime']),
            'bursttime': int(data['BurstTime']),
            'remaining_time': int(data['BurstTime']),
            'queue': 1,
            'resptime': -1,
            'completion_time': 0
        })
    R8 = []
    R16 = []
    FCFS = []
    compprocesses = []


    while len(compprocesses) < len(proc):

        for process in proc:
            if process['arrivaltime'] <= time and process['queue'] == 1 and process not in R8 and process not in compprocesses:
                R8.append(process)


        if len(R8) > 0:
            k = R8.pop(0)
            if k['resptime'] == -1:
                k['resptime'] = time - \
                    k['arrivaltime']
            if k['remaining_time'] > 8:
                k['remaining_time'] -= 8
                time += 8
                k['queue'] = 2
                R16.append(k)
            else:
                time += k['remaining_time']
                k['remaining_time'] = 0
                k['compTIme'] = time
                compprocesses.append(k)
        else:

            for process in proc:
                if process['arrivaltime'] <= time and process['queue'] == 2 and process not in R16 and process not in compprocesses:
                    R16.append(process)


            if len(R16) > 0:
                k = R16.pop(0)
                if k['resptime'] == -1:
                    k['resptime'] = time - \
                        k['arrivaltime']
                if k['remaining_time'] > 16:
                    k['remaining_time'] -= 16
                    time += 16
                    k['queue'] = 3
                    FCFS.append(k)
                else:
                    time += k['remaining_time']
                    k['remaining_time'] = 0
                    k['compTIme'] = time
                    compprocesses.append(k)
            else:

                for process in proc:
                    if process['arrivaltime'] <= time and process['queue'] == 3 and process not in FCFS and process not in compprocesses:
                        FCFS.append(process)


                if len(FCFS) > 0:
                    k = FCFS.pop(0)
                    if k['resptime'] == -1:
                        k['resptime'] = time - \
                            k['arrivaltime']
                    time += k['remaining_time']
                    k['remaining_time'] = 0
                    k['compTIme'] = time
                    compprocesses.append(k)
                else:
                    time += 1
    for process in compprocesses:
        process['turnaround'] = process['compTIme'] - \
            process['arrivaltime']
        process['waittime'] = process['turnaround'] - \
            int(process['bursttime'])
        process['reldelay'] = round(
            process['waittime']/int(process['bursttime']), 2)

    return compprocesses


def output(dataset):
    Ta = PrettyTable()
    Ta.field_names = ["Process ID", "TurnARoundTime","Wait Time", "Response Time", "Relative Delay"]
    dataset.sort(key=lambda x: x["name"])
    for row in dataset:
        Ta.add_row([row["name"], row["turnaround"],
                      row["waittime"], row["resptime"], row["reldelay"]])
    print(Ta)

    AVGTAT = sum([data["turnaround"]
                for data in dataset]) / len(dataset)
    AVGWT = sum([data["waittime"] for data in dataset]) / len(dataset)
    AVGRT = sum([data["resptime"] for data in dataset]) / len(dataset)
    AVGRD = sum([data["reldelay"] for data in dataset]) / len(dataset)

    print(f"\nAvG TAT: {AVGTAT:.1f}")
    print(f"AvG WT: {AVGWT:.1f}")
    print(f"AvG RT: {AVGRT:.1f}")
    print(f"AvG RD: {AVGRD:.1f}")


data = reader('input.txt')
result = scheduling(data)
output(result)
