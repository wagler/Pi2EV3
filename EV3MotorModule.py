import paramiko

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

Motor = enum('A', 'B', 'C', 'AB', 'BC', 'ABC')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(192.168.2.100,username='root',password='r00tme')

def moveMotor(motors, speed):
    if(motors = Motor.A):
        stdin, stdout, stderr = ssh.exec_command("cd /sys/class/tacho-motor/tacho-motor0/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run", speed)
    if(motors = Motor.B):
        stdin, stdout, stderr = ssh.exec_command("cd /sys/class/tacho-motor/tacho-motor1/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run", speed)
    if(motors = Motor.C):
        stdin, stdout, stderr = ssh.exec_command("cd /sys/class/tacho-motor/tacho-motor2/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run", speed)
    if(motors = Motor.AB):
        stdin, stdout, stderr = ssh.exec_command("cd /sys/class/tacho-motor/tacho-motor0/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run; cd /sys/class/tacho-motor/tacho-motor1/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run", speed, speed)
    if(motors = Motor.BC):
        stdin, stdout, stderr = ssh.exec_command("cd /sys/class/tacho-motor/tacho-motor1/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run; cd /sys/class/tacho-motor/tacho-motor2/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run", speed, speed)
    if(motors = Motor.ABC):
        stdin, stdout, stderr = ssh.exec_command("cd /sys/class/tacho-motor/tacho-motor0/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run; cd /sys/class/tacho-motor/tacho-motor1/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run; cd /sys/class/tacho-motor/tacho-motor2/duty_cycle_sp; echo %d > duty_cycle_sp; echo 1 > run", speed, speed, speed)


    
