#! /usr/bin/env python
import argparse, subprocess, time, tempfile, math
from string import Template

def template(templateFileName, values):
    fp = tempfile.NamedTemporaryFile()

    template = Template(open(templateFileName).read())
    result = template.substitute(values)

    fp.write(result)

    fp.seek(0)
    return fp

def run_simulation(args):
    processes = []
    # Start Gazebo
    # processes.append(subprocess.Popen("/entrypoint.sh roslaunch marcus_gazebo basic.launch gui:={}".format("{}".format(args.gui).lower()), shell=True))
    processes.append(subprocess.Popen("/entrypoint.sh roslaunch dragonfly_sim run_sim.launch gui:={}".format("{}".format(args.gui).lower()), shell=True))


    time.sleep(3)

    tempfiles = []

    columnsize = math.sqrt(args.drones)
    spacing = 2
    # Start pursuers (dragonfly/kopterworx)
    for i in range(0, args.drones):
        parameters = {'target': (i + 1),
                      'name': "dragonfly{}".format(i + 1),
                      'fdm_port_in': (9002 + (i * 10)),
                      'fdm_port_out': (9003 + (i * 10))
                      }
        juav_param = template('/workspace/templates/kopter.param.template', parameters)
        tempfiles.append(juav_param)

        row = spacing * int(i / columnsize)
        column = spacing * (i % columnsize)

        processes.append(subprocess.Popen('/entrypoint.sh roslaunch dragonfly_sim spawn_kopterworx.launch '
                                          "name:=dragonfly{} ".format(i + 1) +
                                          "instance:={} ".format(i) +
                                          "tgt_system:={} ".format(i + 1) +
                                          "spawn_offset_x:={} ".format(row) +
                                          "spawn_offset_y:={} ".format(column) +
                                          "fcu_url:=udp://127.0.0.1:{}@{} ".format(14551 + (i * 10), 14555 + (i * 10)) +
                                          "param_file:={} ".format(juav_param.name) +
                                          "fdm_port_in:={} ".format(9002 + (i * 10)) +
                                          "fdm_port_out:={} ".format(9003 + (i * 10)) +
                                          "location:={} ".format(args.location),
                                          shell=True))

    angle = 360/args.intruders if args.intruders else 0
    r = args.zone_radius

    # Start targets (iris)
    for i in range(0, args.intruders):
        intruder_parameters = {'target': (i + args.drones + 1),
                      'name': "intruder{}".format(i + args.drones + 1),
                      'fdm_port_in': (9002 + ((i + args.drones) * 10)),
                      'fdm_port_out': (9003 + ((i + args.drones) * 10))
                      }
        jintruder_param = template('/workspace/templates/kopter.param.template', intruder_parameters)
        tempfiles.append(jintruder_param)

        x_tmp = r * math.cos(angle * i)
        y_tmp = r * math.sin(angle * i)

        processes.append(subprocess.Popen('/entrypoint.sh roslaunch dragonfly_sim spawn_kopterworx.launch '
                                          "name:=intruder{} ".format(i + args.drones + 1) +
                                          "instance:={} ".format(i + args.drones ) +
                                          "tgt_system:={} ".format(i + args.drones + 1) +
                                          "spawn_offset_x:={} ".format(x_tmp) +
                                          "spawn_offset_y:={} ".format(y_tmp) +
                                          "fcu_url:=udp://127.0.0.1:{}@{} ".format(14551 + ((i + args.drones) * 10), 14555 + ((i + args.drones) * 10)) +
                                          "fdm_port_in:={} ".format(9002 + ((i + args.drones) * 10)) +
                                          "fdm_port_out:={} ".format(9003 + ((i + args.drones) * 10)) +
                                          "param_file:={} ".format(jintruder_param.name) +
                                          "location:={} ".format(args.location),
                                          shell=True))

    for p in processes:
        p.wait()

    for file in tempfiles:
        file.close()

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_args():
    parser = argparse.ArgumentParser(description='ARGoS Fault Tolerant Drone Simulator')

    parser.add_argument(
        '--drones',
        type=int,
        default=1
    )
    parser.add_argument(
        '--intruders',
        type=int,
        default=1
    )
    parser.add_argument(
        '--location',
        type=str,
        default='HUMMINGBIRD'
    )
    parser.add_argument(
        '--gui',
        type=str2bool,
        nargs='?',
        const=True,
        default=True
    )
    parser.add_argument(
        '--zone_radius',
        type=float,
        default=10.0
    )
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    run_simulation(args)


if __name__ == '__main__':
    main()
