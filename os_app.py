from flask import Flask, render_template, request, redirect, url_for
import time

os_app = Flask(__name__)

class Process:
    def __init__(self):
        self.id = 0
        self.at = 0
        self.bt = 0
        self.pt = 0
        self.wt = 0
        self.tat = 0
        self.ct = 0

total_processes = 0
processes = []
gantt_chart = []

@os_app.route("/")
def home():
    return render_template("home.html")

@os_app.route('/process_no')
def process_no():
    return render_template("processno.html")

@os_app.route('/atbtctinput', methods=['POST'])
def atbtctinput():
    global total_processes
    global processes
    if request.method == 'POST':
        total_processes = int(request.form['total_processes'])
        processes = [Process() for _ in range(total_processes)]
        return render_template("atbtctinput.html", total_processes=total_processes)
    else:
        return redirect(url_for('home'))

@os_app.route('/calculate', methods=['POST'])
def calculate():
    global processes
    global gantt_chart

    if request.method == 'POST':
        gantt_chart = []  

    if request.method == 'POST':
        for i in range(total_processes):
            processes[i].at = int(request.form[f'at_{i}'])
            processes[i].bt = int(request.form[f'bt_{i}'])
            processes[i].pt = int(request.form[f'pt_{i}'])
            processes[i].id = i + 1

        processes.sort(key=lambda x: x.at)

        t = 0
        wt = 0
        tat = 0
        remainingtime = [{"id": p.id, "time": p.bt} for p in processes]
        completed = 0
        output_processes = []

        while completed != total_processes:
            highestpriority = float('inf')   #here we are defining infinity as highest priority
            processno = -1
            for i in range(total_processes):
                if processes[i].at <= t and remainingtime[i]["time"] > 0:
                    if processes[i].pt < highestpriority:  # what we do here is compare highest priority with process priority 
                        highestpriority = processes[i].pt # example if 5<inf hp is 5 then priority 4 comes and 4<5 4 becomes hp
                        processno = i

            if processno == -1:    # this is for if no process is started (eg if arrival times are 3,8,4 or if there is any interval in between)
                gantt_chart.append(0)  # Store process as 0
                t += 1
                continue

            remainingtime[processno]["time"] -= 1

            gantt_chart.append(processes[processno].id) #adding process id in ganttchart

            if remainingtime[processno]["time"] == 0:
                completed += 1
                processes[processno].ct = t + 1
                processes[processno].tat = t + 1 - processes[processno].at
                processes[processno].wt = t + 1 - processes[processno].at - processes[processno].bt
                wt += processes[processno].wt
                tat += processes[processno].tat

                output_processes.append(processes[processno])

            t += 1

        output_processes.sort(key=lambda x: x.id)

        return render_template("output.html", processes=output_processes)
    
@os_app.route("/redirect", methods=['POST'])
def redirect_page():
    redirect_button = request.form['redirect_button']
    if redirect_button == 'ganttchart':
        return redirect(url_for('ganttchart'))
    elif redirect_button == 'os_apphomepage':
        return redirect(url_for('home'))

@os_app.route("/ganttchart")
def ganttchart():
    return render_template("ganttchart.html", gan_chart=gantt_chart)



@os_app.route("/team")
def team():
    return render_template("team.html")

# ---------------------------------------------------------semaphore--------------------------------------------------#
class Operation:
    def __init__(self, type, duration, status):
        self.type = type
        self.duration = duration
        self.status = status
#class no instance
class Semaphore:
    def __init__(self, value=1):
        self.value = value
        self.queue = []

    def down(self):
        if self.value > 0:
            self.value -= 1
        else:
            time.sleep(0.1)

    def up(self):
        if len(self.queue) > 0:
            resolve = self.queue.pop(0)
            resolve()
        else:
            self.value += 1

mutex1 = Semaphore(1)
mutex2 = Semaphore(1)
rc = 0
writer_active = False
operations = []
@os_app.route('/semaphore')
def semaphore():
    return render_template('semaphore.html')

@os_app.route('/start_operation', methods=['POST'])
def start_operation():
    operation_type = request.form['operationType']
    duration = int(request.form['duration'])

    operation_status = ""

    global rc, writer_active

    if operation_type == "reader":
        mutex1.down()
        rc += 1

        if rc == 1:
            mutex2.down()

        mutex1.up()

        operation_status = "Success: Reader entered"

        time.sleep(duration)

        mutex1.down()
        rc -= 1

        if rc == 0:
            mutex2.up()
        mutex1.up()

        operation_status = "Success: Reader completed"
    elif operation_type == "writer":
        mutex2.down()
        
        writer_active = True

        operation_status = "Success: Writer entered"
        time.sleep(duration)
        writer_active = False

        operation_status = "Success: Writer completed"
        mutex2.up()

    operations.append(Operation(operation_type, duration, operation_status))

    return render_template('ot.html',operations=operations)


#------------------------------------------------------fcfs------------------------------------------------#


def fcfs_disk_scheduling(start_pos_appition, sequence):
    total_head_movement = 0
    head_movement_diff = []
    current_pos_appition = start_pos_appition
    for request in sequence:
        diff = abs(request - current_pos_appition)
        head_movement_diff.append(diff)
        total_head_movement += diff
        current_pos_appition = request
    return total_head_movement, head_movement_diff

@os_app.route('/FCFSD')
def FCFSD():
    return render_template('FCFSD.html')

@os_app.route('/fcfs', methods=['POST'])
def fcfs():
    start_pos_appition = int(request.form['start_pos_appition'])
    num_requests = int(request.form['num_requests'])
    sequence = [int(request.form[f'request_{i}']) for i in range(num_requests)]
    
    zipped_data = zip(sequence, fcfs_disk_scheduling(start_pos_appition, sequence)[1])
    
    total_head_movement = fcfs_disk_scheduling(start_pos_appition, sequence)[0]
    return render_template('fc.html', start_pos_appition=start_pos_appition, zipped_data=zipped_data, total_head_movement=total_head_movement)

#------------------------------------------------------LRU-----------------------------------------------------------------#


@os_app.route('/LRU')
def LRU():
    return render_template('LRU.html')

@os_app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    ref_string = request.form['inputString']
    num_frames = int(request.form['inputFrames'])
    pages = ref_string.split()
    num_pages = len(pages)
    frames = [-1] * num_frames
    faults = 0
    hits = 0
    last_used = [0] * num_frames  # Initialize with 0 instead of float('inf')
    table_data = "<tr><th>Reference</th>"
    for i in range(num_frames):
        table_data += "<th>Frame " + str(i) + "</th>"
    table_data += "<th>Page Status</th></tr>"
    for i in range(num_pages):
        found = False
        for j in range(num_frames):
            if frames[j] == pages[i]:
                hits += 1
                found = True
                last_used[j] = i + 1  # Update last used index
                break
        if not found:
            index = last_used.index(min(last_used))
            frames[index] = pages[i]
            last_used[index] = i + 1
            faults += 1
        table_data += "<tr><td>" + pages[i] + "</td>"
        for j in range(num_frames):
            if frames[j] == -1:
                table_data += "<td></td>"
            else:
                table_data += "<td>" + frames[j] + "</td>"
        if not found:
            table_data += "<td>FAULT</td></tr>"
        else:
            table_data += "<td>HIT</td></tr>"
        table_data+="<br>"
    hit_ratio = ((hits / num_pages) * 100)
    fault_ratio = ((faults / num_pages) * 100)
    table_data2 = "<h2>Page Faults: " + str(faults) + "</h2><br>"
    table_data2 += "<h2>Page Hits: " + str(hits) + "</h2></br>"
    table_data2 += "<h2>Fault Ratio : {:.2f}% </h2><br>".format(fault_ratio)
    table_data2 += "<h2>Hit Ratio : {:.2f}% </h2><br>".format(hit_ratio)
    return render_template('LRUresult.html', table_data=table_data, table_data2=table_data2)

@os_app.route('/result')
def result():
    table_data = """
        <tr>
            <td>1</td>
            <td>1</td>
            <td></td>
            <td>FAULT</td>
        </tr>
        <!-- Add more rows for each reference/frame -->
    """
    table_data2 = """
        <h2>Page Faults: 7</h2>
        <h2>Page Hits: 1</h2>
        <h2>Fault Ratio: 87.50%</h2>
        <h2>Hit Ratio: 12.50%</h2>
    """
    return render_template('result.html', table_data=table_data, table_data2=table_data2)

if __name__ == "__main__":
    os_app.run(debug=True)