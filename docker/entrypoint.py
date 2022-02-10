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
    processes.append(subprocess.Popen("roslaunch dragonfly_sim run_sim.launch gui:={}".format("{}".format(args.gui).lower()), shell=True))

    time.sleep(3)

    tempfiles = []

    columnsize = math.sqrt(args.drones)
    spacing = 2
    # Start drones
    for i in range(0, args.drones):
        parameters = {'target': (i + 1),
                      'name': "dragonfly{}".format(i + 1),
                      'fdm_port_in': (9002 + (i * 10)),
                      'fdm_port_out': (9003 + (i * 10))
                      }
        juav_param = template('/workspace/templates/juav.param.template', parameters)
        model_sdf = template('/workspace/templates/model.sdf.template', parameters)
        tempfiles.append(juav_param)
        tempfiles.append(model_sdf)

        row = spacing * int(i / columnsize)
        column = spacing * (i % columnsize)

        processes.append(subprocess.Popen('roslaunch dragonfly_sim juav.launch '
                                          "name:=dragonfly{} ".format(i + 1) +
                                          "instance:={} ".format(i) +
                                          "tgt_system:={} ".format(i + 1) +
                                          "spawn_offset_x:={} ".format(row) +
                                          "spawn_offset_y:={} ".format(column) +
                                          "fcu_url:=udp://127.0.0.1:{}@{} ".format(14551 + (i * 10), 14555 + (i * 10)) +
                                          "param_file:={} ".format(juav_param.name) +
                                          "model_file:={} ".format(model_sdf.name) +
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
        default=1)
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
        default=True)
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    run_simulation(args)


if __name__ == '__main__':
    main()
