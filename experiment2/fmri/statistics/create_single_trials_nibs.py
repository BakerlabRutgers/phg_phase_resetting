import os
from subprocess import Popen, PIPE, STDOUT

data_dir = 'file_directory'
out_dir = os.path.join(data_dir, "tmaze", "derivatives", "lss")
work_dir = os.path.join(out_dir, "work")

# Loop over all subjects and run the BIDS app NIBS for each subject to create single trial BOLD estimates
cmd = """\
for s in ({001..30});
do nibs -c WhiteMatter CSF \
--participant-label $s \
--estimator lss \
--hrf-model glover \
-w {work_dir} \
{bids_dir} \
fmriprep \
{out_dir} \
participant;
done
""".format(bids_dir=os.path.join(data_dir, "tmaze"),
           out_dir=out_dir,
           work_dir=work_dir)

# Call the nibs command
p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

while True:
    line = p.stdout.readline()
    if not line:
        break
    print(line)
